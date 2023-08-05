# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import mozinfo

from enum import Enum


class Alignment(Enum):
    CENTER = "center"
    TOP_LEFT = "top_left"
    TOP_RIGHT = "top_right"
    BOTTOM_LEFT = "bottom_left"
    BOTTOM_RIGHT = "bottom_right"


def _button_value(base_name, mouse_button):
    """Generates the value tuple for a :class:`Button` value.

    :param str base_name: The base name for the button. This shuld be a string
        like ``'kCGEventLeftMouse'``.

    :param int mouse_button: The mouse button ID.

    :return: a value tuple
    """
    if mozinfo.os == "mac":
        import Quartz

        return (
            tuple(
                getattr(Quartz, "%sMouse%s" % (base_name, name))
                for name in ("Down", "Up", "Dragged")
            ),
            mouse_button,
        )


class Button(Enum):
    """The various buttons.
    """

    unknown = None
    left = _button_value("kCGEventLeft", 0)
    middle = _button_value("kCGEventOther", 2)
    right = _button_value("kCGEventRight", 1)


class Color(Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"
    BLACK = "black"
    WHITE = "white"


class LanguageCode(Enum):
    AFRIKAANS = "afr"
    AMHARIC = "amh"
    ARABIC = "ara"
    ASSAMESE = "asm"
    AZERBAIJANI = "aze"
    AZERBAIJANI_CYRILIC = "aze-cyrl"
    BELARUSIAN = "bel"
    BENGALI = "ben"
    TIBETAN = "bod"
    BOSNIAN = "bos"
    BULGARIAN = "bul"
    CATALAN = "cat"
    CEBUANO = "ceb"
    CZECH = "ces"
    CHINESE_SIMPLIFIED = "chi-sim"
    CHINESE_TRADITIONAL = "chi-tra"
    CHEROKEE = "chr"
    WELSH = "cym"
    DANISH = "dan"
    DANISH_FRAKTUR = "dan-frak"
    GERMAN = "deu"
    GERMAN_FRAKTUR = "deu-frak"
    DZONGKHA = "dzo"
    MODERNGREEK = "ell"
    ENGLISH = "eng"
    MIDDLE_ENGLISH = "enm"
    ESPERANTO = "epo"
    ESTONIAN = "est"
    BASQUE = "eus"
    PERSIAN = "fas"
    FINNISH = "fin"
    FRENCH = "fra"
    FRANKISH = "frk"
    MIDDLE_FRENCH = "frm"
    IRISH = "gle"
    IRISHUNCIAL = "gle-uncial"
    GALICIAN = "glg"
    ANCIENT_GREEK = "grc"
    GUJARATI = "guj"
    HAITIAN = "hat"
    HEBREW = "heb"
    HINDI = "hin"
    CROATIAN = "hrv"
    HUNGARIAN = "hun"
    INUKTITUT = "iku"
    INDONESIAN = "ind"
    ICELANDIC = "isl"
    ITALIAN = "ita"
    JAVANESE = "jav"
    JAPANESE = "jpn"
    KANNADA = "kan"
    GEORGIAN = "kat"
    KAZAKH = "kaz"
    KHMER = "khm"
    KYRGYZ = "kir"
    KOREAN = "kor"
    KURDISH = "kur"
    LAO = "lao"
    LATIN = "lat"
    LATVIAN = "lav"
    LITHUANIAN = "lit"
    MALAYALAM = "mal"
    MARATHI = "mar"
    MACEDONIAN = "mkd"
    MALTESE = "mlt"
    MALAY = "msa"
    BURMESE = "mya"
    NEPALI = "nep"
    DUTCH = "nld"
    NORWEGIAN = "nor"
    ORIYA = "ori"
    PUNJABI = "pan"
    POLISH = "pol"
    PORTUGUESE = "por"
    PASHTO = "pus"
    ROMANIAN = "ron"
    RUSSIAN = "rus"
    SANSKRIT = "san"
    SINHALA = "sin"
    SLOVAK = "slk"
    SLOVAK_FRACTUR = "slk-frak"
    SLOVENIAN = "slv"
    SPANISH = "spa"
    ALBANIAN = "sqi"
    SERBIAN = "srp"
    SERBIAN_LATIN = "srp-latn"
    SWAHILI = "swa"
    SWEDISH = "swe"
    SYRIAC = "syr"
    TAMIL = "tam"
    TELUGU = "tel"
    TAJIK = "tgk"
    TAGALOG = "tgl"
    THAI = "tha"
    TIGRINYA = "tir"
    TURKISH = "tur"
    UYGHUR = "uig"
    UKRANIAN = "ukr"
    URDU = "urd"
    UZBEK = "uzb"
    UZBEK_CYRILLIC = "uzb-cyrl"
    VIETNAMESE = "vie"
    YIDDISH = "yid"


class Locales(str, Enum):
    ARABIC = "ar"
    CHINESE = "zh-CN"
    ENGLISH = "en-US"
    FRENCH = "fr"
    GERMAN = "de"
    JAPANESE = "ja"
    KOREAN = "ko"
    POLISH = "pl"
    PORTUGUESE = "pt-PT"
    ROMANIAN = "ro"
    RUSSIAN = "ru"
    SPANISH = "es-ES"
    TURKISH = "tr"
    VIETNAMESE = "vi"

    ALL = [
        ARABIC,
        CHINESE,
        ENGLISH,
        FRENCH,
        GERMAN,
        JAPANESE,
        KOREAN,
        POLISH,
        PORTUGUESE,
        ROMANIAN,
        RUSSIAN,
        SPANISH,
        TURKISH,
        VIETNAMESE,
    ]


class MatchTemplateType(Enum):
    SINGLE = 0
    MULTIPLE = 1


class OSPlatform(str, Enum):
    WINDOWS = "win"
    LINUX = "linux"
    MAC = "osx"

    ALL = [WINDOWS, LINUX, MAC]
