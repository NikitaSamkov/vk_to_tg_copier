# -*- coding: utf-8 -*-
__author__ = "Самков Н.А. https://github.com/NikitaSamkov"
__maintainer__ = "Самков Н.А. https://github.com/NikitaSamkov"
__doc__ = "Задание настроек"

import os
from configparser import ConfigParser


SETTINGS_PATH = 'settings.ini'
SETTINGS_TMPL_PATH = 'settings.tmpl'


def init_settings() -> None:
    """Инициализация settings.ini"""
    config = ConfigParser()
    config.read(SETTINGS_TMPL_PATH)
    config.set('VK', 'VK_ACCESS_TOKEN', input('Введите токен доступа от ВК: '))
    config.set('VK', 'VK_GROUP_ID', input('Введите идентификатор группы в ВК: '))

    config.set('TG', 'TG_API_ID', input('Введите идентификатор TG API (Получить можно на my.telegram.org): '))
    config.set('TG', 'TG_API_HASH', input('Введите хэш TG API (Получить можно на my.telegram.org): '))
    config.set('TG', 'TG_CHANNEL', input('Введите идентификатор тг канала (без @): '))

    time = []
    while (new_time := input('Введите время публикации в формате ЧЧ:ММ (оставьте пустую строку, чтобы закончить): ')) != '':
        time.append(new_time)
    
    config.set('POSTING', 'POSTING_TIME', ', '.join(time))
    with open(SETTINGS_PATH, 'w') as f:
        config.write(f)
    print(f'Настройки сохранены в {SETTINGS_PATH}')


def get_settings() -> ConfigParser:
    """Получение настроек

    Returns:
        ConfigParser: настройки
    """
    if not os.path.exists(SETTINGS_PATH):
        init_settings()
    settings = ConfigParser()
    settings.read(SETTINGS_PATH)
    return settings
