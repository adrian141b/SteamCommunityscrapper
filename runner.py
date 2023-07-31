from example.steam_community import SteamCommunity
import time
import datetime
from datetime import date

steam_community = SteamCommunity()
steam_link_to_community ="link to community page"       # example("https://steamcommunity.com/app/1578390/discussions/")
day_range = "numbers of days" # how many days back you want to download posts example (60)

today = date.today()
date_range = today - datetime.timedelta(days=int(day_range))
date_range_timestamp = time.mktime(datetime.datetime.strptime(str(date_range), "%Y-%m-%d").timetuple())

forums = steam_community.forums(link_to_community=str(steam_link_to_community),
                                date_range=date_range_timestamp)

threads = steam_community.threads(link_to_community=str(steam_link_to_community),
                                  date_range=date_range_timestamp)

class Producer:
    def serialize_steam_community(self):
        i = 1
        last_topic = 1
        topics_data = []
        post_data = []
        for forum in forums:
            pass

        for thread in threads:
            link_to_thread = thread['href']
            thread_number = thread['thread_number']
            browser_close = False
            if not topics_data:
                browser_close = True
            topics = steam_community.topics(link_to_community=str(link_to_thread),
                                            date_range=date_range_timestamp, thread_number=thread_number,
                                            browser_close=browser_close)

            for topic in topics:
                topics_data.append(topic)

            serialized_topics = [
                self._serialize_single_topic(comm)
                for comm in topics_data
            ]

            for topic in topics_data:
                if i == len(topics_data):
                    last_topic = 1
                link_to_topic = topic['link_to_review']
                topic_posts = steam_community.posts(link_to_topic=link_to_topic, last_topic=last_topic)
                i += 1
                for post in topic_posts:
                    post_data.append(post)

            serialized_posts = [
                self._serialize_single_post(post)
                for post in post_data
            ]

            return serialized_topics, serialized_posts

        for topic in topics_data:
            if i == len(topics_data):
                last_topic = 1
            link_to_topic = topic['link_to_review']
            topic_posts = steam_community.posts(link_to_topic=link_to_topic, last_topic=last_topic)
            i += 1
            for post in topic_posts:
                post_data.append(post)

    def _serialize_single_topic(self, comment):
        if comment:
            topic_data = {
                'topic_id': comment['topic_id'],
                'thread_id': comment['thread_id'],
                'user_id': comment['user_id'],
                'user_name': comment['user_name'],
                'subject': comment['subject'],
                'original_text': comment['original_text'],
                'topic_date': comment['topic_date'],
                'channel': 'steam_community',
                'last_update': comment['last_update'],
                'link_to_review': comment['link_to_review'],
                'external_content': comment['external_content']
            }
            return topic_data

    def _serialize_single_post(self, post):
        if post:
            post_data = {
                'post_id': post['post_id'],
                'user_id': post['user_id'],
                'topic_id': post['topic_id'],
                'user_name': post['user_name'],
                'original_text': post['body_text'],
                'post_date': post['post_date'],
                'channel': 'steam_community',
                'link_to_post': post['link_to_post'],
                'external_content': post['external_content']
            }
            print(post_data)
            return post_data

start = Producer()
start.serialize_steam_community()
