# -*- coding: utf-8 -*-

# Copyright (c) 2017

# Author(s):

#   Panu Lahtinen <panu.lahtinen@fmi.fi>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from six.moves.queue import Empty as queue_empty
import os
import os.path
from six.moves.configparser import (RawConfigParser, NoOptionError,
                                    NoSectionError)
import logging
import logging.config
import datetime as dt
import glob
from six.moves.urllib.parse import urlparse

import xarray as xr
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import gc

from posttroll.listener import ListenerContainer
from pycoast import ContourWriter
from trollsift import parse, compose
from trollsift.parser import get_convert_dict
from satpy.resample import get_area_def
from satpy import Scene
from trollimage.xrimage import XRImage


try:
    GSHHS_DATA_ROOT = os.environ['GSHHS_DATA_ROOT']
except KeyError:
    logging.warning("GSHHS_DATA_ROOT is not set, unable to add coastlines")
    GSHHS_DATA_ROOT = None

# Default values for each section
DEFAULT_SECTION_VALUES = {'update_existing': False,
                          'only_backup': False,
                          'crops': [],
                          'sizes': [],
                          'tags': [],
                          'timeliness': 10,
                          'static_image_fname_pattern': None,
                          'tidy_platform_name': False,
                          'text_pattern': None,
                          'area_def': None,
                          'overlay_config_fname': None,
                          'out_dir': '',
                          'fill_value': None,
                          'force_gc': False
                          }

# Default text settings
DEFAULT_TEXT_SETTINGS = {'text_location': 'SW',
                         'font_fname': '',
                         'font_size': '12',
                         'text_color': '0,0,0',
                         'text_bg_color': '255,255,255',
                         'x_marginal': '10',
                         'y_marginal': '3',
                         'bg_extra_width': '0',
                         }

# Default save settings for TIFF images
DEFAULT_SAVE_OPTIONS = {'save_tags': None,
                        'compress': 'deflate',
                        'zlevel': 6,
                        'tile': True,
                        'blockxsize': 512,
                        'blockysize': 512,
                        'overviews': None}

# Merge the two default dictionaries to one master dict
DEFAULT_CONFIG_VALUES = DEFAULT_SECTION_VALUES.copy()
DEFAULT_CONFIG_VALUES.update(DEFAULT_TEXT_SETTINGS)
DEFAULT_CONFIG_VALUES.update(DEFAULT_SAVE_OPTIONS)

BANDS = {1: ['L'], 2: ['L', 'A'], 3: ['R', 'G', 'B'], 4: ['R', 'G', 'B', 'A']}


class ImageScaler(object):

    '''Class for scaling images to defined sizes.'''

    # Config options for the current received message
    out_dir = ''
    update_existing = False
    is_backup = False
    subject = None
    crops = []
    sizes = []
    tags = []
    timeliness = 10
    static_image_fname = None
    areaname = None
    in_pattern = None
    fileparts = {}
    out_pattern = None
    text_pattern = None
    text_settings = None
    area_def = None
    overlay_config = None
    filepath = None
    existing_fname_parts = {}
    time_name = 'time'
    time_slot = None
    fill_value = None

    def __init__(self, config):
        self.config = config
        topics = config.sections()
        self.listener = ListenerContainer(topics=topics)
        self._loop = True

        if GSHHS_DATA_ROOT:
            self._cw = ContourWriter(GSHHS_DATA_ROOT)
        else:
            self._cw = None
        self._force_gc = False

    def stop(self):
        '''Stop scaler before shutting down.'''
        if self._loop:
            self._loop = False
            if self.listener is not None:
                self.listener.stop()

    def run(self):
        '''Start waiting for messages.

        On message arrival, read the image, scale down to the defined
        sizes and add coastlines.
        '''

        while self._loop:
            # Wait for new messages
            try:
                msg = self.listener.output_queue.get(True, 5)
            except KeyboardInterrupt:
                self.stop()
                raise
            except queue_empty:
                continue

            logging.info("New message with topic %s", msg.subject)

            self.subject = msg.subject
            self.filepath = urlparse(msg.data["uri"]).path

            try:
                self._update_current_config()
            except (NoOptionError, NoSectionError):
                logging.warning("Skip processing for this message.")
                continue

            self.time_name = self._get_time_name(msg.data)
            # Adjust in_pattern and out_pattern to match this time_name
            self.in_pattern = adjust_pattern_time_name(self.in_pattern,
                                                       self.time_name)
            self.out_pattern = adjust_pattern_time_name(self.out_pattern,
                                                        self.time_name)

            # parse filename parts from the incoming file
            try:
                self.fileparts = parse(self.in_pattern,
                                       os.path.basename(self.filepath))
            except ValueError:
                logging.info("Filepattern doesn't match, skipping.")
                logging.debug("in_pattern: %s", self.in_pattern)
                logging.debug("fname: %s", os.path.basename(self.filepath))
                continue
            self.fileparts['areaname'] = self.areaname
            self._tidy_platform_name()

            self.time_slot = msg.data[self.time_name]
            existing_fname_parts = \
                self._check_existing(msg.data[self.time_name])

            # There is already a matching image which isn't going to
            # be updated
            if existing_fname_parts is None:
                continue
            self.existing_fname_parts = existing_fname_parts

            # Read the image
            img = read_image(self.filepath)

            if img is None:
                logging.error("Could not read image %s", self.filepath)
                continue

            # Add overlays, if any
            img = self.add_overlays(img)

            # Save image(s)
            self.save_images(img)

            # Delete obsolete image object
            del img

            # Run garbage collection if configured
            self._gc()

    def _gc(self):
        """Run garbage collection if it is configured."""
        if self._force_gc:
            num = gc.collect()
            logging.debug("Garbage collection cleaned %s objects", num)

    def _get_time_name(self, info):
        """"Try to find the name for 'nominal' time"""
        for key in info:
            if "time" in key and "end" not in key and "proc" not in key:
                return key
        return None

    def add_overlays(self, img):
        """Add overlays to image.  Add to cache, if not already there."""
        if self.overlay_config is None:
            return img

        if self._cw is None:
            logging.warning("GSHHS_DATA_ROOT is not set, "
                            "unable to add coastlines")
            return img

        if self.area_def is None:
            logging.warning("Area definition not available, "
                            "can't add overlays!")
        else:
            return add_overlay_from_config(img, self._cw,
                                           self.overlay_config,
                                           self.area_def)

    def save_images(self, img):
        """Save image(s)"""

        # Loop through different image sizes
        num = np.max([len(self.sizes), len(self.crops), len(self.tags)])
        for i in range(num):
            img_out = img.copy()
            # Crop the image
            try:
                img_out = crop_image(img_out, self.crops[i])
                logging.debug("Applied crop: %s", str(self.crops[i]))
            except IndexError:
                logging.debug("No valid crops configured")

            # Resize the image
            try:
                img_out = resize_image(img_out, self.sizes[i])
            except IndexError:
                logging.debug("No valid sizes configured")

            # Update existing image if configured to do so
            if self.update_existing and len(self.existing_fname_parts) > 0:
                try:
                    self.existing_fname_parts['tag'] = self.tags[i]
                except IndexError:
                    pass
                fname = compose(os.path.join(self.out_dir, self.out_pattern),
                                self.existing_fname_parts)
                img_out = self._update_existing_img(img_out, fname)

                # Add text
                img_out = self._add_text(img_out, update_img=True)
            # In other case, save as a new image
            else:
                # Add text
                img_out = self._add_text(img_out, update_img=False)
                # Compose filename
                try:
                    self.fileparts['tag'] = self.tags[i]
                except IndexError:
                    pass
                fname = compose(os.path.join(self.out_dir, self.out_pattern),
                                self.fileparts)

            # Save image
            save_image(img_out, fname, adef=self.area_def,
                       fill_value=self.fill_value,
                       save_options=self.save_options)

            # Update static image, if given in config
            try:
                self.fileparts['tag'] = self.tags[i]
            except IndexError:
                pass
            self._update_static_img(img_out)

    def _get_save_options(self):
        """Get save options from config"""
        save_tags = self._get_conf_with_default('save_tags')
        if save_tags is not None:
            save_tags = save_tags.split()
        compress = self._get_conf_with_default('compress')
        zlevel = int(self._get_conf_with_default('zlevel'))
        tile = self._get_conf_with_default('tile') in ('1', 1, 'True', True)
        blockxsize = int(self._get_conf_with_default('blockxsize'))
        blockysize = int(self._get_conf_with_default('blockysize'))
        overviews = self._get_conf_with_default('overviews')
        if overviews is not None:
            overviews = [int(i) for i in overviews.split()]
        save_options = {'tags': save_tags,
                        'compress': compress,
                        'zlevel': zlevel,
                        'tile': tile,
                        'blocxksize': blockxsize,
                        'blockysize': blockysize,
                        'overviews': overviews}
        return save_options

    def _update_current_config(self):
        """Update the current config to class attributes."""

        # These are mandatory config items, so handle them first
        self._get_mandatory_config_items()

        self._parse_crops()
        self._parse_sizes()
        self._parse_tags()
        self._get_text_settings()

        # Get image save options
        self.save_options = self._get_save_options()

        self.out_dir = self._get_conf_with_default('out_dir')

        self.update_existing = self._get_bool('update_existing')

        self.is_backup = self._get_bool('only_backup')

        self.timeliness = int(self._get_conf_with_default('timeliness'))

        self.fill_value = self._get_fill_value()

        self.static_image_fname_pattern = \
            self._get_conf_with_default("static_image_fname_pattern")

        self.overlay_config = \
            self._get_conf_with_default('overlay_config_fname')
        self._force_gc = self._get_bool('force_gc')

    def _get_conf_with_default(self, item):
        """Get a config item and use a default if no value is available"""
        return _get_conf_with_default(self.config, self.subject, item)

    def _get_bool(self, key):
        """Get *key* from config and interpret it as boolean"""
        val = self._get_conf_with_default(key)
        if isinstance(val, bool):
            return val
        return val.lower() in ['yes', '1', 'true']

    def _get_fill_value(self):
        """Parse fill value"""
        fill_value = self._get_conf_with_default('fill_value')
        if not isinstance(fill_value, (int, type(None))):
            fill_value = int(fill_value)
        return fill_value

    def _get_text_settings(self):
        """Parse text overlay pattern and text settings"""
        self.text_pattern = self._get_conf_with_default('text_pattern')
        self.text_settings = _get_text_settings(self.config, self.subject)

    def _get_mandatory_config_items(self):
        """Get mandatory config items and log possible errors"""
        try:
            self.areaname = self.config.get(self.subject, 'areaname')
            try:
                self.area_def = get_area_def(self.areaname)
            except (IOError, NoOptionError):
                self.area_def = None
                logging.warning("Area definition not available")
            self.in_pattern = self.config.get(self.subject, 'in_pattern')
            self.out_pattern = self.config.get(self.subject, 'out_pattern')
        except NoOptionError:
            logging.error("Required option missing!")
            logging.error("Check that 'areaname', 'in_pattern' and "
                          "'out_pattern' are all defined under section %s",
                          self.subject)
            raise KeyError("Required config item missing")
        except NoSectionError:
            logging.error("No config section for message subject %s",
                          self.subject)
            raise KeyError("Missing config section")

    def _tidy_platform_name(self):
        """Remove "-" from platform names"""
        tidy = self._get_bool('tidy_platform_name')
        if tidy:
            self.fileparts['platform_name'] = self.fileparts[
                'platform_name'].replace('-', '')

    def _parse_crops(self):
        """Parse crop settings from the raw crop config"""
        crop_conf = self._get_conf_with_default('crops')
        if isinstance(crop_conf, list):
            self.crops = crop_conf
            return

        self.crops = []
        for crop in crop_conf.split(','):
            if 'x' in crop and '+' in crop:
                # Crop strings are formated like this:
                # <x_size>x<y_size>+<x_start>+<y_start>
                # eg. 1000x300+103+200
                # Origin (0, 0) is at top-left
                parts = crop.split('+')
                left, up = map(int, parts[1:])
                x_size, y_size = map(int, parts[0].split('x'))
                right, bottom = left + x_size, up + y_size
                crop = (left, up, right, bottom)

                self.crops.append(crop)
            else:
                self.crops.append(None)

    def _parse_sizes(self):
        """Parse crop settings from crop config"""
        size_conf = self._get_conf_with_default('sizes')
        if isinstance(size_conf, list):
            self.sizes = size_conf
            return

        self.sizes = []
        for size in size_conf.split(','):
            self.sizes.append([int(val) for val in size.split('x')])

    def _parse_tags(self):
        """Parse tags from tag config"""
        tag_conf = self._get_conf_with_default('tags')

        if isinstance(tag_conf, list):
            self.tags = tag_conf
            return
        self.tags = [tag for tag in tag_conf.split(',')]

    def _check_existing(self, start_time):
        """Check if there's an existing image that should be updated"""

        # check if something silmiar has already been made:
        # checks for: platform_name, areaname and
        # start_time +- timeliness minutes
        check_start_time = start_time - \
            dt.timedelta(minutes=self.timeliness)
        check_dict = self.fileparts.copy()
        try:
            check_dict["tag"] = self.tags[0]
        except IndexError:
            pass
        if self.is_backup:
            check_dict["platform_name"] = '*'
            check_dict["sat_loc"] = '*'
        # check_dict["composite"] = '*'

        first_overpass = True
        update_fname_parts = {}
        for i in range(2 * self.timeliness + 1):
            check_dict[self.time_name] = \
                check_start_time + dt.timedelta(minutes=i)
            glob_pattern = compose(os.path.join(self.out_dir,
                                                self.out_pattern),
                                   check_dict)
            logging.debug("Check pattern: %s", glob_pattern)
            glob_fnames = glob.glob(glob_pattern)
            if len(glob_fnames) > 0:
                fname = os.path.basename(glob_fnames[0])
                first_overpass = False
                logging.debug("Found files: %s", str(glob_fnames))
                try:
                    update_fname_parts = parse(self.out_pattern,
                                               fname)
                    update_fname_parts["composite"] = \
                        self.fileparts["composite"]
                    if not self.is_backup:
                        try:
                            update_fname_parts["platform_name"] = \
                                self.fileparts["platform_name"]
                            return update_fname_parts
                        except KeyError:
                            pass
                except ValueError:
                    logging.debug("Parsing failed for update_fname_parts.")
                    logging.debug("out_pattern: %s, basename: %s",
                                  self.out_pattern, fname)
                    update_fname_parts = {}

        # Only backup, so save only if there were no matches
        if self.is_backup and not first_overpass:
            logging.info("File already exists, no backuping needed.")
            return None
        # No existing image
        else:
            return {}

    def _update_static_img(self, img):
        """Update image with static filename"""
        if self.static_image_fname_pattern is None:
            return

        fname = compose(os.path.join(self.out_dir,
                                     self.static_image_fname_pattern),
                        self.fileparts)
        img = self._update_existing_img(img, fname)
        img = self._add_text(img, update_img=False)

        save_image(img, fname, adef=self.area_def,
                   fill_value=self.fill_value,
                   save_options=self.save_options)

        logging.info("Updated image with static filename: %s", fname)

    def _add_text(self, img, update_img=False):
        """Add text to the given image"""
        if self.text_pattern is None:
            return img

        if update_img:
            text = compose(self.text_pattern, self.existing_fname_parts)
        else:
            text = compose(self.text_pattern, self.fileparts)

        return add_text(img, text, self.text_settings)

    def _update_existing_img(self, img, fname):
        """Update existing image"""
        logging.info("Updating image %s with image %s",
                     fname, self.filepath)
        img_out = update_existing_image(fname, img, fill_value=self.fill_value)

        return img_out


def resize_image(img, size):
    """Resize given image to size (x_size, y_size)"""
    x_res, y_res = size

    if img.size[0] == x_res and img.size[1] == y_res:
        img_out = img
    else:
        img_out = img.resize((x_res, y_res))

    return img_out


def crop_image(img, crop):
    """Crop the given image"""
    try:
        # Adjust limits so that they don't exceed image dimensions
        # crop = (left, up, right, bottom)
        if crop is not None:
            crop = list(crop)
            # Left edge
            if crop[0] < 0:
                crop[0] = 0
            # Upper edge
            if crop[1] < 0:
                crop[1] = 0
            # Right edge. Wrap around if exceedes image width
            if crop[2] > img.size[0]:
                # Create a new image
                img_new = Image.new(img.mode, (crop[2], img.size[1]))
                # Paste original image to top-left corner of the new image
                img_new.paste(img)
                # Paste a crop from the left edge to the right edge of the
                # new image
                img_new.paste(img.crop((0, 0,
                                       crop[2] - img.size[0], img.size[1])),
                              (img.size[0], 0))
                # Replace original image with the extended image
                img = img_new.copy()
                del img_new
            # Bottom edge
            if crop[3] > img.size[1]:
                crop[3] = img.size[1]
            img_wrk = img.crop(crop)
        else:
            img_wrk = img
    except IndexError:
        img_wrk = img

    return img_wrk


def save_image(img, fname, adef=None, fill_value=None, save_options=None):
    """Save image.  In case of area definition and start time are given,
    and the image type is tif, convert first to Geoimage to save geotiff
    """
    if save_options is None:
        save_options = {}
    save_options.update({'fill_value': fill_value})
    img = _pil_to_xrimage(img, adef=adef, fill_value=fill_value)
    logging.info("Saving image to %s", fname)
    img.save(fname, **save_options)
    overviews = save_options.get('overviews', None)
    if overviews is not None:
        from trollflow_sat.utils import add_overviews
        add_overviews([fname], overviews, logger=logging)


def _pil_to_xrimage(img, adef, fill_value=None):
    """Convert PIL image to trollimage.xrimage.XRImage"""
    # Get image mode, width and height
    mode = img.mode
    width = img.width
    height = img.height

    # Convert to Numpy array
    img = np.array(img)

    # Get the minimum and maximum values of the input datatype
    min_val = np.iinfo(img.dtype).min
    max_val = np.iinfo(img.dtype).max

    img = img.reshape((height, width, len(mode)))

    # Reorder for XRImage
    img = np.rollaxis(img, 2, -3)
    # Remove alpha channel if fill_value is set
    if fill_value is not None:
        if 'A' in mode:
            mask = img[-1, :, :] == min_val
            # Remove alpha channel
            img = img[:-1, :, :]
            if np.any(mask):
                # Set fill_value for each channel
                for i in range(img.shape[0]):
                    chan = img[i, :, :]
                    chan[mask] = fill_value
    bands = BANDS[img.shape[0]]

    # Add image data to scene as xarray.DataArray
    img = xr.DataArray(img, dims=['bands', 'y', 'x'])
    img['bands'] = bands
    # Add area definition
    img.attrs['area'] = adef

    # Convert to XRImage
    img = XRImage(img)
    # Static stretch
    img.crude_stretch(min_val, max_val)

    return img


def _get_crange(num):
    """Get crange for interval (0, 1) for *num* image channels."""
    tupl = (0., 1.)
    return num * (tupl, )


def _get_text_settings(config, subject):
    """Parse text settings from the config."""
    settings = {}
    settings['loc'] = _get_conf_with_default(config, subject, 'text_location')
    font_fname = _get_conf_with_default(config, subject, 'font_fname')
    if font_fname == '':
        settings['font_fname'] = None
    else:
        settings['font_fname'] = font_fname
    settings['font_size'] = int(_get_conf_with_default(config, subject,
                                                       'font_size'))
    text_color = _get_conf_with_default(config, subject, 'text_color')
    settings['text_color'] = tuple([int(x) for x in text_color.split(',')])

    bg_color = _get_conf_with_default(config, subject, 'text_bg_color')
    settings['bg_color'] = tuple([int(x) for x in bg_color.split(',')])
    settings['x_marginal'] = int(_get_conf_with_default(config, subject,
                                                        'x_marginal'))
    settings['y_marginal'] = int(_get_conf_with_default(config, subject,
                                                        'y_marginal'))
    settings['bg_extra_width'] = int(_get_conf_with_default(config, subject,
                                                            'bg_extra_width'))

    return settings


def add_text(img, text, settings):
    """Add text to the image"""
    # TODO: replace with pydecorate?
    img = _adjust_img_mode_for_text(img, (settings['text_color'],
                                          settings['bg_color']))
    # Use 3-tuples only for RGB and RGBA, for others use integers
    if len(img.mode) < 3:
        text_color = settings['text_color'][0]
        bg_color = settings['bg_color'][0]
    else:
        text_color = settings['text_color']
        bg_color = settings['bg_color']

    draw = ImageDraw.Draw(img)
    font = _get_font(settings['font_fname'], settings['font_size'])
    textsize = draw.textsize(text, font)

    marginals = (settings['x_marginal'], settings['y_marginal'])
    loc = settings['loc']
    bg_extra_width = settings['bg_extra_width']
    text_loc, box_loc = _get_text_and_box_locations(img.size, loc,
                                                    textsize, marginals,
                                                    bg_extra_width)

    draw.rectangle(box_loc, fill=bg_color)
    draw.text(text_loc, text, fill=text_color, font=font)

    return img


def _get_text_and_box_locations(img_shape, loc, textsize, marginals,
                                bg_extra_width):
    """Get text and text box locations in the image based on the config"""

    if 'S' in loc:
        text_loc, box_loc = _text_in_south(img_shape, loc,
                                           textsize, marginals,
                                           bg_extra_width)
    else:
        text_loc, box_loc = _text_in_north(img_shape, loc, textsize,
                                           marginals, bg_extra_width)

    return text_loc, box_loc


def _text_in_north(img_shape, loc, textsize, marginals,
                   bg_extra_width):
    width, height = img_shape
    x_marginal, y_marginal = marginals

    if 'W' in loc:
        text_loc = (x_marginal, y_marginal)
        box_loc = [text_loc[0] - bg_extra_width,
                   0,
                   text_loc[0] + textsize[0] + bg_extra_width,
                   textsize[1] + 2 * y_marginal]
    elif 'E' in loc:
        text_loc = (width - textsize[0] - x_marginal, 0)  # y_marginal)
        box_loc = [text_loc[0] - bg_extra_width,
                   0,
                   text_loc[0] + textsize[0] + bg_extra_width,
                   textsize[1] + 2 * y_marginal]
    # Center
    else:
        text_loc = ((width - textsize[0]) / 2, 0)  # y_marginal)
        box_loc = [text_loc[0] - bg_extra_width,
                   0,
                   text_loc[0] + textsize[0] + bg_extra_width,
                   textsize[1] + 2 * y_marginal]

    return text_loc, box_loc


def _text_in_south(img_shape, loc, textsize, marginals,
                   bg_extra_width):
    width, height = img_shape
    x_marginal, y_marginal = marginals
    if 'W' in loc:
        text_loc = (x_marginal, height - textsize[1] - 2 * y_marginal)
        box_loc = [text_loc[0] - bg_extra_width,
                   height - textsize[1] - 2 * y_marginal,
                   text_loc[0] + textsize[0] + bg_extra_width,
                   height]
    elif 'E' in loc:
        text_loc = (width - textsize[0] - x_marginal,
                    height - textsize[1] - 2 * y_marginal)
        box_loc = [text_loc[0] - bg_extra_width,
                   height - textsize[1] - 2 * y_marginal,
                   text_loc[0] + textsize[0] + bg_extra_width,
                   height]
    # Center
    else:
        text_loc = ((width - textsize[0]) / 2,
                    height - textsize[1] - 2 * y_marginal)
        box_loc = [text_loc[0] - bg_extra_width,
                   height - textsize[1] - 2 * y_marginal,
                   text_loc[0] + textsize[0] + bg_extra_width,
                   height]

    return text_loc, box_loc


def _adjust_img_mode_for_text(img, colors):
    """Adjust image mode to mach the text settings"""
    if 'L' in img.mode:
        if _is_rgb_color(colors):
            mode = 'RGB'
            if 'A' in img.mode:
                mode += 'A'
            logging.info("Converting to %s", mode)
            img = img.convert(mode)
    return img


def _is_rgb_color(colors):
    """Return True if RGB colors are needed to represent *colors*, or
    False if grayscale is enough."""
    for col in colors:
        if np.unique(col).size > 1:
            return True
    return False


def _get_font(font_fname, font_size):
    """Load a font from the given file, or if that fails, load the default
    font from PIL"""
    try:
        font = ImageFont.truetype(font_fname, font_size)
        logging.debug('Font read from %s', font_fname)
    except (AttributeError, IOError, TypeError):
        try:
            font = ImageFont.load(font_fname)
            logging.debug('Font read from %s', font_fname)
        except (AttributeError, IOError, TypeError):
            logging.warning('Falling back to default font')
            font = ImageFont.load_default()

    return font


def update_existing_image(fname, new_img,
                          fill_value=DEFAULT_SECTION_VALUES['fill_value']):
    '''Read image from fname, if present, and update valid data (= not
    fill_value or masked by alpha channel) from img_in.  Return updated image
    as PIL image.
    '''

    try:
        # Read existing image, use .copy() to ensure the image is readable
        old_img = Image.open(fname).copy()
    except IOError:
        return new_img

    old_img_mode = old_img.mode
    new_img_mode = new_img.mode
    if (old_img.height != new_img.height or
        old_img.width != new_img.height or
        old_img_mode != new_img_mode):
        logging.warning("Images have different shape/mode, using new image")
        return new_img

    old_img = np.array(old_img)
    new_img = np.array(new_img)

    logging.debug("Image dimensions: old_img: %s, new_img: %s",
                  str(old_img.shape), str(new_img.shape))

    # Get mask for merging
    mask = _get_fill_mask(new_img, fill_value, new_img_mode)

    old_img = _prepare_old_img(old_img, old_img_mode, new_img.shape,
                               new_img_mode, fill_value)
    old_img = _update_img(old_img, new_img, mask)
    old_img = _remove_extra_channels(old_img, new_img.shape, new_img_mode)

    return Image.fromarray(old_img, mode=new_img_mode)


def read_image(filepath):
    """Read the image from *filepath* and return it as PIL Image object."""
    scn = Scene(reader='generic_image', filenames=[filepath, ])
    scn.load(['image'])
    y_size = scn['image']['y'].size
    x_size = scn['image']['x'].size
    arr = np.array(scn['image'])
    alpha = np.isnan(arr[0, :, :])
    arr = arr.astype(np.uint8)
    if np.any(alpha):
        alpha = 255 * np.invert(alpha).astype(np.uint8)
        alpha = alpha.reshape(1, y_size, x_size)
        arr = np.vstack((arr, alpha))
    arr = np.squeeze(np.rollaxis(arr, 0, 3))
    img = Image.fromarray(arr)

    return img


def add_image_as_overlay(img, overlay):
    """Add PIL image as overlay to another image"""
    logging.info("Adding overlays")
    if len(img.mode) > len(overlay.mode) or 'A' not in overlay.mode:
        logging.info("Overlay needs to have same channels as the "
                     "image, AND an alpha channel")
        raise ValueError
    img.paste(overlay, mask=overlay)

    return img


def add_overlay_from_config(img, cw_, overlay_config, area_def):
    """Add overlay from confit to the given image"""
    logging.info("Adding overlays")
    overlay = cw_.add_overlay_from_config(overlay_config, area_def)
    if len(overlay.mode) > len(img.mode):
        img = img.convert(overlay.mode)
    img.paste(overlay, mask=overlay)

    return img


def _get_conf_with_default(config, subject, item):
    """Get a config item and use a default if no value is available"""
    try:
        val = config.get(subject, item)
    except NoOptionError:
        val = DEFAULT_CONFIG_VALUES[item]
    return val


def adjust_pattern_time_name(pattern, time_name):
    """Adjust filename pattern so that time_name is present."""
    # Get parse definitions and try to figure out if there's
    # an item for time
    convert_dict = get_convert_dict(pattern)
    for key, val in convert_dict.items():
        # Need to exclude 'end_time' and 'proc_time' / 'processing_time'
        if ("time" in key or "%" in val) and \
           "end" not in key and key != time_name:
            logging.debug("Updating pattern from '%s' ...", pattern)

            while '{' + key in pattern:
                pattern = pattern.replace('{' + key,
                                          '{' + time_name)
            logging.debug("... to '%s'", pattern)
    return pattern


def _get_fill_mask(img, fill_value, mode):
    """Get mask where channels equal the fill value for that channel"""
    if fill_value is None:
        fill_value = np.nan
    shape = img.shape
    if len(shape) == 2:
        mask = img == fill_value
    # Use alpha channel if available
    elif 'A' in mode:
        mask = img[:, :, -1] > 0
    else:
        mask = img[:, :, 0] == fill_value
        if 'A' not in mode:
            num = min(2, shape[-1])
            for i in range(1, num):
                mask &= (img[:, :, i] == fill_value)

    # Remove extra dimensions from the mask
    mask = np.squeeze(mask)

    return mask


def _add_channels(img, mode):
    if len(img.shape) == 2:
        img = np.expand_dims(img, -1)
    for i in range(len(mode) - img.shape[-1]):
        img = np.dstack((img, img[:, :, 0]))
    return img


def _prepare_old_img(old_img, old_img_mode, new_img_shape, new_img_mode,
                     fill_value):
    """Prepare old image: expand dimensions, duplicate channels, add mask"""
    if old_img.ndim == 2:
        # Add "channel" dimension to output image
        old_img = np.expand_dims(old_img, -1)
    if old_img.shape[-1] < new_img_shape[-1]:
        # Copy the existing data to each channel
        old_img = _add_channels(old_img, new_img_mode)
    if 'A' in new_img_mode and 'A' not in old_img_mode:
        logging.debug("Set alpha channel to output image")
        old_img[:, :, -1] = 255
        # Set fill_value areas in the alpha channel as transparent
        old_img[_get_fill_mask(old_img, fill_value, old_img_mode), -1] = 0

    return old_img


def _update_img(old_img, new_img, mask):
    """Update image where mask is true"""
    if len(new_img.shape) > 2:
        # Update the image
        for i in range(new_img.shape[-1]):
            old_img[mask, i] = new_img[mask, i]
    else:
        old_img[mask] = new_img[mask]

    return old_img


def _remove_extra_channels(old_img, new_img_shape, new_img_mode):
    """Remove extra channels from the image"""
    if old_img.ndim > 2:
        while old_img.shape[-1] > new_img_shape[-1]:
            logging.debug("Removing extra channel from output image")
            old_img = old_img[:, :, :-1]
    # Remove empty dimensions
    if len(new_img_mode) == 1:
        old_img = np.squeeze(old_img)

    return old_img
