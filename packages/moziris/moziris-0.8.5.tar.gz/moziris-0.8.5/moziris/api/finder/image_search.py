# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


import datetime
import logging

import cv2
import numpy as np


try:
    import Image
except ImportError:
    from PIL import Image

from moziris.api.enums import MatchTemplateType
from moziris.api.errors import ScreenshotError
from moziris.api.finder.pattern import Pattern
from moziris.api.location import Location
from moziris.api.rectangle import Rectangle
from moziris.api.save_debug_image.save_image import save_debug_image
from moziris.api.screen.display import DisplayCollection
from moziris.api.screen.screenshot_image import ScreenshotImage
from moziris.api.settings import Settings


logger = logging.getLogger(__name__)

FIND_METHOD = cv2.TM_CCOEFF_NORMED
last_image_write_time = datetime.datetime.now()


def _is_pattern_size_correct(pattern, region):
    """validates that the pattern is inside the region."""
    if region is None:
        return True

    p_width, p_height = pattern.get_size()
    r_width = region.width
    r_height = region.height
    is_correct = True

    if p_width > r_width:
        logger.warning(
            "Pattern Width (%s) greater than Region/Screenshot Width (%s)"
            % (p_width, r_width)
        )
        is_correct = False
    if p_height > r_height:
        logger.warning(
            "Pattern Height (%s) greater than Region/Screenshot Height (%s)"
            % (p_height, r_height)
        )
        is_correct = False
    return is_correct


def match_template(
    pattern: Pattern,
    region: Rectangle = None,
    match_type: MatchTemplateType = MatchTemplateType.SINGLE,
):
    """Find a pattern in a Region or full screen

    :param Pattern pattern: Image details
    :param Region region: Region object.
    :param MatchTemplateType match_type: Type of match_template (single or multiple)
    :return: Location.
    """
    if region is None:
        region = DisplayCollection[0].bounds

    locations_list = []
    save_img_location_list = []
    if not isinstance(match_type, MatchTemplateType):
        logger.warning(
            "%s should be an instance of `%s`" % (match_type, MatchTemplateType)
        )
        return []
    try:
        stack_image = ScreenshotImage(
            region=region, screen_id=_region_in_display_list(region)
        )
        precision = pattern.similarity
        if precision == 0.99:
            logger.debug("Searching image with similarity %s" % precision)
            res = cv2.matchTemplate(
                stack_image.get_color_array(), pattern.get_color_array(), FIND_METHOD
            )
        else:
            logger.debug("Searching image with similarity %s" % precision)
            res = cv2.matchTemplate(
                stack_image.get_gray_array(), pattern.get_gray_array(), FIND_METHOD
            )

        if match_type is MatchTemplateType.SINGLE:
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            logger.debug("Min location %s and max location %s" % (min_val, max_val))
            if max_val >= precision:
                locations_list.append(
                    Location(max_loc[0] + region.x, max_loc[1] + region.y)
                )
                save_img_location_list.append(Location(max_loc[0], max_loc[1]))
        elif match_type is MatchTemplateType.MULTIPLE:
            loc = np.where(res >= precision)
            for pt in zip(*loc[::-1]):
                save_img_location = Location(pt[0], pt[1])
                location = Location(pt[0] + region.x, pt[1] + region.y)
                save_img_location_list.append(save_img_location)
                locations_list.append(location)

        # Limit debug image creation to one per second to avoid creating unnecessary images.
        global last_image_write_time
        next_write_time = last_image_write_time + datetime.timedelta(seconds=1)
        if datetime.datetime.now() > next_write_time:
            save_debug_image(pattern, stack_image, save_img_location_list)
            last_image_write_time = datetime.datetime.now()

    except ScreenshotError:
        logger.warning("Screenshot failed.")
        return []

    return locations_list


def _region_in_display_list(region=None):
    r_x = region.x
    r_y = region.y
    r_w = region.width
    r_h = region.height

    for index, display in enumerate(DisplayCollection):
        d_x = display.bounds.x
        d_y = display.bounds.y
        d_w = display.bounds.width
        d_h = display.bounds.height

        if (
            r_x >= d_x
            and r_x - d_x + r_w <= d_w
            and r_y >= d_y
            and r_y - d_y + r_h <= d_h
        ):
            return index


def image_find(pattern, timeout=None, region=None):
    """ Search for an image in a Region or full screen.

    :param Pattern pattern: Name of the searched image.
    :param timeout: Number as maximum waiting time in seconds.
    :param Region region: Region object.
    :return: Location.
    """
    if not _is_pattern_size_correct(pattern, region):
        return None

    if timeout is None:
        timeout = Settings.auto_wait_timeout

    start_time = datetime.datetime.now()
    end_time = start_time + datetime.timedelta(seconds=timeout)

    while start_time < end_time:
        time_remaining = end_time - start_time
        logger.debug(
            "Image find: {} - {} seconds remaining".format(
                pattern.get_filename(), time_remaining
            )
        )
        pos = match_template(pattern, region, MatchTemplateType.SINGLE)
        start_time = datetime.datetime.now()

        if len(pos) == 1:
            return pos[0]
    return None


def image_vanish(
    pattern: Pattern, timeout: float = None, region: Rectangle = None
) -> None or bool:
    """ Search if an image is NOT in a Region or full screen.

    :param Pattern pattern: Name of the searched image.
    :param timeout: Number as maximum waiting time in seconds.
    :param Region region: Region object.
    :return: Location.
    """
    if not _is_pattern_size_correct(pattern, region):
        return None

    pattern_found = True

    start_time = datetime.datetime.now()
    end_time = start_time + datetime.timedelta(seconds=timeout)

    while pattern_found and start_time < end_time:
        time_remaining = end_time - start_time
        logger.debug(
            "Image vanish: {} - {} seconds remaining".format(
                pattern.get_filename(), time_remaining
            )
        )
        image_found = match_template(pattern, region, MatchTemplateType.SINGLE)
        if len(image_found) == 0:
            pattern_found = False
        else:
            pattern_found = True
        start_time = datetime.datetime.now()

    return None if pattern_found else True
