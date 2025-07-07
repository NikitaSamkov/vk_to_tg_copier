# -*- coding: utf-8 -*-
__author__ = "Самков Н.А. https://github.com/NikitaSamkov"
__maintainer__ = "Самков Н.А. https://github.com/NikitaSamkov"
__doc__ = "Основная логика и точка входа"

from datetime import datetime
from settings import get_settings
from vk_api import VkApi
from tg_api import TgApi


DATE_FORMAT = '%d.%m.%Y'


def main():
    settings = get_settings()
    start_date = input('Введите начальную дату для копирования постов (в формате День.Месяц.Год): ')
    start_date = '01.05.2025'
    start_date = datetime.strptime(start_date, DATE_FORMAT)
    end_date = input('Введите конечную дату для копирования постов (в формате День.Месяц.Год): ')
    end_date = '05.07.2025'
    end_date = datetime.strptime(end_date, DATE_FORMAT)

    vk = VkApi(settings.get('VK', 'VK_ACCESS_TOKEN'), settings.get('VK', 'VK_GROUP_ID'))
    posts = vk.get_posts(start_date, end_date)

    tg = TgApi(settings.get('TG', 'TG_API_ID'), 
               settings.get('TG', 'TG_API_HASH'),
               settings.get('TG', 'TG_CHANNEL'))
    
    with tg.client:
        tg.client.loop.run_until_complete(tg.schedule_posts(posts, settings.get('POSTING', 'POSTING_TIME').split(', ')))
    tg.close()


if __name__ == '__main__':
    main()
