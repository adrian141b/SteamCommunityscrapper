from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from datetime import datetime as d, date
import time
import base64




class SteamCommunity:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-setuid-sandbox")
        options.add_argument("--disable-dev-shm-using")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        #options.add_argument("--headless")
        options.add_argument("start-maximized")
        options.add_argument("disable-infobars")
        service = ChromeService()

        self.driver = webdriver.Chrome(service=service, options=options)

    def forums(self, link_to_community, date_range):
        self.post_data = []
        self.date_range = date_range
        self.link_to_community = link_to_community
        self.driver.get(self.link_to_community)
        time.sleep(4)
        try:
            self.driver.find_element_by_css_selector(
                "div#acceptAllButton.btn_blue_steamui.btn_medium.replyButton").click()
            time.sleep(3)
        except:
            pass

        try:
            self.driver.find_element_by_css_selector(
                "div#age_gate_btn_continue.btn_grey_white_innerfade.btn_medium").click()
            time.sleep(4)
        except:
            pass

        try:
            self.driver.execute_script("javascript:Forum_SetTopicsPerPage( 15 );")
        except:
            pass
        time.sleep(3)
        self.soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        self.name = self.soup.find(class_="apphub_AppName ellipsis").get_text()
        self.forum_id = self.link_to_community.split("/")[4]
        forum_data = {
            'forum_id': self.forum_id,
            'name': self.name,
            'channel': 'steam_community',
        }
        yield forum_data

    def threads(self, link_to_community, date_range):
        self.date_range = date_range
        self.link_to_community = link_to_community
        self.driver.get(self.link_to_community)
        all_threads = self.soup.find_all('div', class_="forum_list_name")[1:]
        self.last_thread = len(all_threads)
        thread_number = 1
        for thread in all_threads:
            thread_name = thread.find(class_="whiteLink").get_text().strip()
            thread_link = thread.find(class_="whiteLink")['href'].strip()
            if thread_name == "exits_thread":
                pass
            else:
                self.driver.get(thread_link)
                href = self.driver.current_url
                msgid_string_bytes = href.encode("UTF-8")
                msgid_bytes = base64.b64encode(msgid_string_bytes)
                self.thread_id = msgid_bytes.decode("UTF-8")
                thread = {
                    'number': thread_number,
                    'href': href,
                    'thread_id': self.thread_id,
                    'forum_id': self.forum_id,
                    'name': thread_name,
                    'channel': 'steam_community',
                    'thread_number': thread_number
                }
                thread_number += 1
                yield thread

    def topics(self, link_to_community, date_range, thread_number, browser_close):
        date_range_topic = date_range
        self.link_to_community = link_to_community
        self.page = 1
        try:
            last_page = BeautifulSoup(self.driver.page_source, 'html.parser')(class_="forum_paging_pagelink")[
                -1].get_text()
        except:
            last_page = 0
        old = 0
        topic_data = []
        while int(last_page) >= (self.page) and old < 5:
            all_topics = BeautifulSoup(self.driver.page_source, 'html.parser')
            for topic in all_topics.find_all(class_="forum_topic unread"):
                if old < 5:
                    self.driver.delete_all_cookies()
                    self.link_to_topic = topic.find(class_="forum_topic_overlay").get('href')
                    self.driver.get(self.link_to_topic)
                    topic_last_update_timestamp = topic.find(class_="forum_topic_lastpost")["data-timestamp"]
                    topic_last_update = d.fromtimestamp(int(topic_last_update_timestamp)).strftime("%Y-%m-%d %H:%M:%S")
                    self.all_thread = BeautifulSoup(self.driver.page_source, 'html.parser')
                    for topic in self.all_thread.find_all(class_="forum_op"):
                        topic_created_at = topic.find(class_="date")["data-timestamp"]
                        if int(topic_created_at) > int(date_range_topic):
                            try:
                                author_name = topic.find(class_="hoverunderline forum_op_author").get_text().strip()
                            except:
                                author_name = "Anonymous"
                            try:
                                author = topic.find(class_="hoverunderline forum_op_author")["data-miniprofile"].strip()
                            except:
                                author = "1111111111"
                            subject = topic.find(class_="topic").get_text().strip()
                            body_text = topic.find('div', class_="content").get_text().strip()
                            created_at = topic_created_at
                            msgid = self.link_to_topic.split("/")[7]
                            if not msgid:
                                msgid = self.link_to_topic.split("/")[6]
                            external_content_check = topic.find(class_="bb_link")
                            if external_content_check is not None:
                                external_content = str(external_content_check['href'])
                            else:
                                external_content = ""
                            message_date = d.fromtimestamp(int(created_at)).strftime("%Y-%m-%d %H:%M:%S")
                            topic_json = {
                                'topic_id': msgid,
                                'thread_id': self.thread_id,
                                'user_id': author,
                                'user_name': author_name,
                                'subject': subject,
                                'original_text': body_text,
                                'topic_date': message_date,
                                'channel': 'steam_community',
                                'last_update': topic_last_update,
                                'link_to_review': self.link_to_topic,
                                'external_content': external_content
                            }
                            print(topic_json)
                            topic_data.append(topic_json)
                            if topic_json:
                                yield topic_json
                        else:
                            old += 1
            print("dane topic:")
            if self.link_to_community.split("/")[3] == "workshop":
                self.driver.get(self.link_to_community + "&fp=" + str(self.page))
            else:
                self.driver.get(self.link_to_community + "/?fp=" + str(self.page))
            time.sleep(1)
            self.page += 1
        if thread_number == self.last_thread and browser_close is True:
            self.driver.quit()

    def posts(self, link_to_topic, last_topic):
        time.sleep(1)
        self.driver.get(link_to_topic)
        posts_source = BeautifulSoup(self.driver.page_source, 'html.parser')
        try:
            last_page2 = posts_source.find_all(class_="commentthread_pagelink")[-1].get_text()
            last_page2 = int(last_page2)
        except:
            last_page2 = 1
        page2 = 1
        topic_url = (self.driver.current_url)


        while last_page2 >= page2:
            comment_type = 0
            all_comments = BeautifulSoup(self.driver.page_source, 'html.parser')
            best_commment = all_comments.find_all(class_="commentthread_comment responsive_body_text commentthread"
                                                         "_answer_comment")
            standard_comments = all_comments.find_all(class_="commentthread_comment responsive_body_text")
            while comment_type < 2:

                if best_commment and comment_type < 1:
                    comments_data = best_commment
                    comment_type += 1
                else:
                    comments_data = standard_comments
                    comment_type += 2
                try:
                    for post in comments_data:
                        post_id = post.find(class_="forum_comment_permlink")
                        topic = topic_url.split("/")[7]
                        if not topic:
                            topic = topic_url.split("/")[6]
                        body_text = post.find(class_="commentthread_comment_text").get_text().strip()
                        try:
                            user = post.find(class_="hoverunderline commentthread_author_link").get_text().strip()
                            user_id = post.find(class_="hoverunderline commentthread_author_link")[
                                'data-miniprofile'].strip()
                        except:
                            try:
                                user = post.find(class_="hoverunderline commentthread_author_link commentthread"
                                                        "_author_globalmoderator").get_text().strip()
                            except:
                                user = post.find(class_="hoverunderline commentthread_author_link commentthread"
                                                        "_author_developer").get_text().strip()
                                user_id = post.find(class_="hoverunderline commentthread_author_link commentthread"
                                                           "_author_developer")['data-miniprofile'].strip()
                        post_created_at = post.find(class_="commentthread_comment_timestamp")["data-timestamp"].strip()
                        post_message_date = d.fromtimestamp(int(post_created_at)).strftime("%Y-%m-%d %H:%M:%S")
                        link_to_post_class = post.find(class_="forum_comment_permlink")
                        external_content_check = post.find(class_="bb_link")
                        if external_content_check is not None:
                            external_content = str(external_content_check['href'])
                        else:
                            external_content = ""
                        for link in link_to_post_class('a', href=True):
                            link_to_post = str(link_to_topic) + str(link['href'])
                        post = {
                            'post_id': str(post_id).split("#")[1][:-2],
                            'topic_id': topic,
                            'user_id': user_id,
                            'user_name': user,
                            'body_text': body_text,
                            'post_date': post_message_date,
                            'channel': 'steam_community',
                            'link_to_post': link_to_post,
                            'external_content': external_content
                        }
                        print(post)
                        self.post_data.append(post)
                        if post:
                            yield post
                except:
                    pass
            page2 += 1
            time.sleep(1)
            if last_page2 >= page2:
                self.driver.get(topic_url + "/?ctp=" + str(page2))

        print("dane post:")
        print(len(self.post_data))
        if last_topic == 1:
            pass