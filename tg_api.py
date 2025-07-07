# -*- coding: utf-8 -*-
__author__ = "Самков Н.А. https://github.com/NikitaSamkov"
__maintainer__ = "Самков Н.А. https://github.com/NikitaSamkov"
__doc__ = "Работа с ТГ"

import os
import time
import schedule
import requests
from datetime import datetime, timedelta
from telethon.sync import TelegramClient
from telethon.tl.types import InputMediaPhoto, InputMediaDocument
from telethon import functions
from common import VkPost


TEMP_FOLDER = 'temp'


class TgApi:
    def __init__(self, api_id, api_hash, channel):
        self.client = TelegramClient('tg', api_id, api_hash, system_version="4.16.30-vxCUSTOM")
        self.channel = channel

    def download_file(self, url: str, file_ext: str, idx=0):
        """Загрузить файл в временную директорию и вернуть его название

        Args:
            url (str): URL для скачивания
            file_ext (str): Расширение файла

        Returns:
            Optional[str]: Название загруженного файла (если был загружен)
        """
        try:
            response = requests.get(url)
            if response.status_code == 200:
                filename = f"temp_{int(time.time())}_{idx}.{file_ext}"
                filepath = os.path.join(TEMP_FOLDER, filename)
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                return filepath
            return None
        except Exception as e:
            print(f"Ошибка при загрузке файла: {e}")
            return None
        
    def mk_temp(self):
        """Создание тестовой директории"""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        temp_dir = os.path.join(script_dir, "temp")
        os.makedirs(temp_dir, exist_ok=True)
    
    def remove_temp(self):
        """"Удаление временной директории"""
        os.remove(TEMP_FOLDER)
    
    async def get_last_sheduled_post_time(self, channel) -> datetime:
        """Получение времени последнего запланированного поста в канале

        Returns:
            datetime: Время последнего поста
        """
        scheduled_messages = self.client.iter_messages(channel, scheduled=True, limit=None)
        
        max_date = None
        async for message in scheduled_messages:
            if max_date is None or message.date > max_date:
                max_date = message.date
        
        return max_date
    
    async def schedule_post(self, post: VkPost, publish_time: datetime, channel):
        """Запланировать пост для публикации в Telegram

        Args:
            post (VkPost): Пост
            publish_time (datetime): Дата и время публикации
            channel: Сущность канала
        """
        media_files = []
        
        for i, photo_url in enumerate(post.photos):
            if (photo_path := self.download_file(photo_url, 'jpg', i)) is not None:
                media_files.append(photo_path)
        
        for i, video_url in enumerate(post.videos):
            if (video_path := self.download_file(video_url, 'mp4', i)) is not None:
                media_files.append(video_path)
        
        # Создаем отложенный пост
        if media_files:
            await self.client.send_file(
                channel,
                file=media_files,
                caption=post.text,
                schedule=publish_time,
                supports_streaming=True
            )
        else:
            # Если нет медиа, отправляем только текст
            await self.client.send_message(
                channel,
                message=post.text,
                schedule=publish_time
            )
    
    async def schedule_posts(self, posts: list[VkPost], post_times: list[str]):
        """Планирование постов в ТГ

        Args:
            posts (list[VkPost]): Посты из вк
            post_times (list[str]): Время в которое постить
        """
        print('Публикую посты в отложку тг')
        # Создаём временную директорию для файлов
        self.mk_temp()
        
        post_times = sorted(post_times)
        channel = await self.client.get_entity(self.channel)
        last_post = await self.get_last_sheduled_post_time(channel) or datetime.now()
        last_date = datetime.combine(last_post.date(), datetime.strptime('00:00', '%H:%M').time()) + timedelta(days=1)
        for i, post in enumerate(posts):
            post_time = post_times[i % len(post_times)]
            publish_datetime = datetime.combine(last_date, datetime.strptime(post_time, '%H:%M').time())
            if publish_datetime < last_date:
                publish_datetime += timedelta(days=1)
            await self.schedule_post(post, publish_datetime, channel)
            last_date = publish_datetime
        
        # Удаляем временные файлы
        self.remove_temp()
