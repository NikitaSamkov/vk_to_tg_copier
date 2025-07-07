# -*- coding: utf-8 -*-
__author__ = "Самков Н.А. https://github.com/NikitaSamkov"
__maintainer__ = "Самков Н.А. https://github.com/NikitaSamkov"
__doc__ = "Работа с ВК"

import vk
from datetime import datetime


class VkApi:
    def __init__(self, access_token, group_id):
        self.group = group_id
        self.session = vk.API(access_token=access_token)

    def get_posts(self, start_date: datetime, end_date: datetime):
        """Получение постов за указанный период

        Args:
            start_date (datetime): Начало периода
            end_date (datetime): Конец периода

        Returns:
            list: Список постов
        """
        result = []
        offset = 0
        count = 100

        while True:
            print(f'Получаю посты {offset} - {offset + count - 1}')
            posts = self.session.wall.get(
                owner_id=f'-{self.group}',
                count=count,
                offset=offset,
                extended=1,
                v='5.131'
            )['items']

            if not posts:
                break

            for post in posts:
                post_date = datetime.fromtimestamp(post['date'])
                if post_date < start_date:
                    return result
                if start_date <= post_date <= end_date and 'copy_history' not in post:
                    result.append(post)
            
            offset += count
        
        return result

