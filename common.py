# -*- coding: utf-8 -*-
__author__ = "Самков Н.А. https://github.com/NikitaSamkov"
__maintainer__ = "Самков Н.А. https://github.com/NikitaSamkov"
__doc__ = "Общая логика"

from dataclasses import dataclass


@dataclass
class VkPost:
    text: str
    photos: list[str]
    videos: list[str]
