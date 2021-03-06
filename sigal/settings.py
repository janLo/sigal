# -*- coding:utf-8 -*-

# Copyright (c) 2009-2013 - Simon Conseil
# Copyright (c) 2013      - Christophe-Marie Duquesne

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

import logging
import os
from pprint import pformat

_DEFAULT_CONFIG = {
    'adjust_options': {'color': 1.0, 'brightness': 1.0,
                       'contrast': 1.0, 'sharpness': 1.0},
    'copy_exif_data': True,
    'copyright': '',
    'destination': '_build',
    'google_analytics': '',
    'img_ext_list': ['.jpg', '.jpeg', '.JPG', '.JPEG', '.png'],
    'img_processor': 'ResizeToFit',
    'img_size': (640, 480),
    'index_in_url': False,
    'jpg_options': {'quality': 85, 'optimize': True, 'progressive': True},
    'keep_orig': False,
    'links': '',
    'locale': '',
    'make_thumbs': True,
    'orig_dir': 'original',
    'orig_link': False,
    'source': '',
    'theme': 'colorbox',
    'thumb_dir': 'thumbnails',
    'thumb_fit': True,
    'thumb_prefix': '',
    'thumb_size': (200, 150),
    'thumb_suffix': '',
    'vid_ext_list': ['.MOV', '.mov', '.avi', '.mp4', '.webm', '.ogv'],
    'video_size': (480, 360),
    'webm_options': ['-crf', '10', '-b:v', '1.6M',
                     '-qmin', '4', '-qmax', '63'],
    'write_html': True,
    'zip_gallery': False,
}


def get_thumb(settings, filename):
    """Return the path to the thumb.

    examples:
    >>> default_settings = create_settings()
    >>> get_thumb(default_settings, "bar/foo.jpg")
    "bar/thumbnails/foo.jpg"
    >>> get_thumb(default_settings, "bar/foo.png")
    "bar/thumbnails/foo.png"

    for videos, it returns a jpg file:
    >>> get_thumb(default_settings, "bar/foo.webm")
    "bar/thumbnails/foo.jpg"
    """

    path, filen = os.path.split(filename)
    name, ext = os.path.splitext(filen)
    if ext in settings['vid_ext_list']:
        ext = '.jpg'
    return os.path.join(path, settings['thumb_dir'], settings['thumb_prefix'] +
                        name + settings['thumb_suffix'] + ext)


def get_orig(settings, filename):
    """Return the path to the original image."""

    path, filen = os.path.split(filename)
    return os.path.join(path, settings['orig_dir'], filen)


def read_settings(filename=None):
    """Read settings from a config file in the source_dir root."""

    logger = logging.getLogger(__name__)
    logger.info("Reading settings ...")
    settings = _DEFAULT_CONFIG.copy()
    settings_path = os.path.dirname(filename)

    if filename:
        logger.debug("Settings file: %s", filename)
        tempdict = {}

        with open(filename) as f:
            code = compile(f.read(), filename, 'exec')
            exec(code, tempdict)

        settings.update((k, v) for k, v in tempdict.items()
                        if k not in ['__builtins__'])

        # Make the paths relative to the settings file
        paths = ['source', 'destination']

        if os.path.isdir(os.path.join(settings_path, settings['theme'])):
            paths.append('theme')

        for p in paths:
            path = settings[p]
            if path and not os.path.isabs(path):
                settings[p] = os.path.abspath(os.path.normpath(os.path.join(
                    settings_path, path)))
                logger.debug("Rewrite %s : %s -> %s", p, path, settings[p])

    for key in ('img_size', 'thumb_size', 'video_size'):
        w, h = settings[key]
        if h > w:
            settings[key] = (h, w)
            logger.warning("The %s setting should be specified with the "
                           "largest value first.", key)

    if not settings['img_processor']:
        logger.info('No Processor, images will not be resized')

    logger.debug('Settings:\n%s', pformat(settings, width=120))
    return settings


def create_settings(**kwargs):
    """Create a new default setting copy and initialize it with kwargs."""
    settings = _DEFAULT_CONFIG.copy()
    settings.update(kwargs)
    return settings
