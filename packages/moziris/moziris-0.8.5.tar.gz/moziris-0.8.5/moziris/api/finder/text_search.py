# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


import difflib
import logging

import pytesseract
from PIL import ImageEnhance

from moziris.api.rectangle import Rectangle
from moziris.api.save_debug_image.save_image import save_debug_ocr_image
from moziris.api.screen.display import DisplayCollection
from moziris.api.screen.screenshot_image import ScreenshotImage

TRY_RESIZE_IMAGES = 2
OCR_RESULT_COLUMNS_COUNT = 12
WORD_PROXIMITY = 5

logger = logging.getLogger(__name__)

cutoffs = {
    "string": {"min_cutoff": 0.7, "max_cutoff": 0.9, "step": 0.1},
    "digit": {"min_cutoff": 0.75, "max_cutoff": 0.9, "step": 0.05},
}

digit_chars = [".", "%", ","]


def _is_similar_result(result_list, x: int, y: int, pixels: int):
    """Checks if current result is similar to previous results based on pixel proximity."""
    if len(result_list) == 0:
        return False

    for result in result_list:
        if (x - pixels <= result.x <= x + pixels) and (
            y - pixels <= result.y <= y + pixels
        ):
            return True
    return False


def _is_next_word(prev_word, x, y):
    """Checks if previous - current word are located correctly."""
    if (prev_word.x + prev_word.width + 10 >= x) and (y - 5 <= prev_word.y <= y + 5):
        return True
    return False


def _replace_multiple(main_string, replace_string, replace_with_string):
    """Replace a string with a list of substrings."""
    for elem in replace_string:
        if elem in main_string:
            main_string = main_string.replace(elem, replace_with_string)

    return main_string


def _create_rectangle_from_ocr_data(data, scale):
    """Generates a Rectangle object based on OCR processed data and image scale."""
    x = int(int(data[6]) / (scale * (1 if scale - 1 == 0 else scale - 1)))
    y = int(int(data[7]) / (scale * (1 if scale - 1 == 0 else scale - 1)))
    width = int(int(data[8]) / (scale * (1 if scale - 1 == 0 else scale - 1)))
    height = int(int(data[9]) / (scale * (1 if scale - 1 == 0 else scale - 1)))
    return Rectangle(x, y, width, height)


def _assemble_results(result_list):
    """Merge all Rectangle objects into one that contains them all."""
    from operator import attrgetter

    x = min(result_list, key=attrgetter("x")).x
    y = min(result_list, key=attrgetter("y")).y

    x_max = max(result_list, key=attrgetter("x")).x
    width = max([x.width for x in result_list if x.x == x_max]) + x_max - x

    y_max = max(result_list, key=attrgetter("y")).y
    height = max([x.height for x in result_list if x.y == y_max]) + y_max - y
    return Rectangle(x, y, width, height)


def _get_processed_data(image_list):
    """Get all OCR data from images."""
    data = []
    for index_image, stack_image in enumerate(image_list):
        for index_scale, scale in enumerate(range(1, TRY_RESIZE_IMAGES + 1)):
            stack_image = stack_image.resize(
                [stack_image.width * scale, stack_image.height * scale]
            )
            processed_data = pytesseract.image_to_data(stack_image)
            for index_data, line in enumerate(processed_data.split("\n")[1:]):
                d = line.split()
                if len(d) == OCR_RESULT_COLUMNS_COUNT:
                    d.append(scale)
                    data.append(d)
    return data


def _get_first_word(word, data_list):
    """Finds all occurrences of the first searched word."""
    words_found = []
    cutoff_type = (
        "digit" if _replace_multiple(word, digit_chars, "").isdigit() else "string"
    )
    for data in data_list:
        cutoff = cutoffs[cutoff_type]["max_cutoff"]
        while cutoff >= cutoffs[cutoff_type]["min_cutoff"]:
            if difflib.get_close_matches(word, [data[11]], cutoff=cutoff):
                try:
                    vd = _create_rectangle_from_ocr_data(data, data[12])
                    if not _is_similar_result(words_found, vd.x, vd.y, WORD_PROXIMITY):
                        words_found.append(vd)
                except ValueError:
                    continue
            cutoff -= cutoffs[cutoff_type]["step"]
    return words_found


def _text_search(text, region: Rectangle = None, multiple_search=False):
    """Search text in region or screen."""
    if region is None:
        region = DisplayCollection[0].bounds

    logger.debug("Text find: '{}'".format(text))
    img = ScreenshotImage(region=region)
    raw_gray_image = img.get_gray_image()
    enhanced_image = ImageEnhance.Contrast(img.get_gray_image()).enhance(10.0)
    data_list = _get_processed_data([raw_gray_image, enhanced_image])
    first_word_occurrences = _get_first_word(text.split()[0], data_list)
    word_count = len(text.split())

    if not multiple_search:
        if len(first_word_occurrences) == 0:
            first_word = []
        else:
            if word_count == 1:
                first_word = [first_word_occurrences[0]]
            else:
                first_word = first_word_occurrences
    else:
        first_word = first_word_occurrences

    if word_count == 1:
        for result in first_word:
            result.x += region.x
            result.y += region.y
        return first_word

    sentence = []
    for data in first_word:
        sentence.append([data])

    for index, word in enumerate(first_word):
        for index_word, word_to_search in enumerate(text.split()[1:]):
            found = False
            cutoff_type = (
                "digit"
                if _replace_multiple(word_to_search, digit_chars, "").isdigit()
                else "string"
            )
            for d in data_list:
                if not found:
                    cutoff = cutoffs[cutoff_type]["max_cutoff"]
                    while cutoff >= cutoffs[cutoff_type]["min_cutoff"]:
                        if difflib.get_close_matches(
                            word_to_search, [d[11]], cutoff=cutoff
                        ):
                            try:
                                vd = _create_rectangle_from_ocr_data(d, d[12])
                                if _is_next_word(
                                    sentence[index][-1], vd.x, vd.y
                                ) and not _is_similar_result(
                                    sentence[index], vd.x, vd.y, WORD_PROXIMITY
                                ):
                                    sentence[index].append(vd)
                                    found = True
                            except ValueError:
                                continue
                        cutoff -= cutoffs[cutoff_type]["step"]
    final_result = []
    for words in sentence:
        if len(words) == word_count:
            final_result.append(_assemble_results(words))

    save_debug_ocr_image(text, img, final_result)

    for result in final_result:
        result.x += region.x
        result.y += region.y

    return final_result


def text_find(text, region):
    return _text_search(text, region, False)


def text_find_all(text, region):
    return _text_search(text, region, True)
