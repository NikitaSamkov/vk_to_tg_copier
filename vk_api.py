# -*- coding: utf-8 -*-
__author__ = "Самков Н.А. https://github.com/NikitaSamkov"
__maintainer__ = "Самков Н.А. https://github.com/NikitaSamkov"
__doc__ = "Работа с ВК"

import vk
import re
from datetime import datetime
from common import VkPost


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
            print(f'Получаю посты из вк {offset} - {offset + count - 1}')
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
                    result.append(self.process_post(post))
            
            offset += count
        
        return result
    
    def process_post(self, post: dict) -> VkPost:
        """Обработка поста

        Args:
            post (dict): Пост, полученный через API ВК

        Returns:
            VkPost: Обработанный пост
        """
        text = post.get('text', '')
        # Меняем хэтеги вида #hashtag@group на просто #hashtag
        text = re.sub(r"#(\w+)@\w+", lambda matchobj: "#" + matchobj.group(1), text)
        photos = []
        videos = []

        for attachment in post.get('attachments', []):
            if attachment['type'] == 'photo':
                # Берем фото максимального размера
                photo_url = sorted(
                    attachment['photo']['sizes'],
                    key=lambda x: x['width'] * x['height'],
                    reverse=True
                )[0]['url']
                photos.append(photo_url)
            elif attachment['type'] == 'video':
                # Для видео получаем ссылку на файл (может потребоваться дополнительная обработка)
                video_url = f"https://vk.com/video{attachment['video']['owner_id']}_{attachment['video']['id']}"
                videos.append(video_url)
        
        # Т.к. видео никак не скачать, прикладываем ссылки в текст
        if videos:
            text += '\n\n' + '\n'.join(videos)
        
        return VkPost(text, photos, videos)
