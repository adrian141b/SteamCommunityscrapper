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
# print("--- %s seconds ---" % (time.time() - start_time))
# #
# #
# # from selenium import webdriver
# from bs4 import BeautifulSoup
# from webdriver_manager.chrome import ChromeDriverManager
# import time
# from selenium.webdriver.common.action_chains import ActionChains
# import datetime
# import base64
# import re
# start_time = time.time()
#
# def gog(game, date_range):
#     chromeOptions = webdriver.ChromeOptions()
#     chromeOptions.add_argument("--no-sandbox")
#     chromeOptions.add_argument("--disable-setuid-sandbox")
#     # chromeOptions.add_argument("--remote-debugging-port=9222")
#     chromeOptions.add_argument("--disable-dev-shm-using")
#     chromeOptions.add_argument("--disable-extensions")
#     chromeOptions.add_argument("--disable-gpu")
#     # chromeOptions.add_argument("--headless")
#     chromeOptions.add_argument("start-maximized")
#     chromeOptions.add_argument("disable-infobars")
#     chromeOptions.add_argument("--disable-dev-shm-usage")
#     driver = webdriver.Chrome(
#         executable_path=ChromeDriverManager().install(),
#         options=chromeOptions
#     )
#
#     driver.get(game)
#     time.sleep(3)
#     age_gate = BeautifulSoup(driver.page_source, 'html.parser').find(class_="button button--big age-gate__button")
#     if age_gate is not None:
#         driver.find_element_by_css_selector("button.button.button--big.age-gate__button").click()
#
#     lenofpage = driver.execute_script(
#         "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
#     match = False
#     while (match == False):
#         lastcount = lenofpage
#         time.sleep(2)
#         lenofpage = driver.execute_script(
#             "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
#         if lastcount == lenofpage:
#             match = True
#     # cookie popup
#     try:
#         driver.find_element_by_css_selector("#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll").click()
#         time.sleep(3)
#
#     except:
#         time.sleep(3)
#
#     languages = driver.find_elements_by_css_selector(
#         'span.option__text')
#
#     for elem in languages[1:7]:
#         if elem.is_displayed():
#             actions_language = ActionChains(driver)
#             actions_language.move_to_element(elem).click().perform()
#     time.sleep(4)
#     show_on_page = driver.find_element_by_css_selector(
#         "div.dropdown.dropdown--bottom.reviews-sorting__trigger-container.ng-scope")
#
#     actions = ActionChains(driver)
#     actions.move_to_element(show_on_page).click().perform()
#     time.sleep(4)
#     reviews_number = driver.find_elements_by_css_selector(
#         "label.sort-dropdown__item")[2]
#     actions = ActionChains(driver)
#     actions.move_to_element(reviews_number).click().perform()
#
#     recent = driver.find_elements_by_css_selector(
#         "div.dropdown.dropdown--bottom.reviews-sorting__trigger-container.ng-scope")[1]
#
#     actions.move_to_element(recent).click().perform()
#     time.sleep(2)
#     recent_option = driver.find_elements_by_css_selector(
#         "label.sort-dropdown__item")[7]
#
#     actions = ActionChains(driver)
#     actions.move_to_element(recent_option).click().perform()
#
#     reviews_data = []
#
#     page = "page"
#     date_timestamp = date_range
#     while page is not None and date_timestamp >= date_range:
#         time.sleep(5)
#
#         soup2 = BeautifulSoup(driver.page_source, 'html.parser')
#         for reviews in BeautifulSoup(driver.page_source, 'html.parser').find_all(class_="review__item"):
#
#             read_more = reviews.find('button', class_="review__read-more ng-binding ng-scope")
#             if read_more is not None:
#                 read_more_button = driver.find_element_by_css_selector(
#                     "button.review__read-more.ng-binding.ng-scope")
#                 actions_read_more = ActionChains(driver)
#                 time.sleep(1)
#                 actions_read_more.move_to_element(read_more_button).click().perform()
#
#         for reviews in BeautifulSoup(driver.page_source, 'html.parser').find_all(class_="review__item")[1:]:
#             review = reviews.find(class_="review__text ng-binding").get_text()
#             from_name = reviews.find(class_="ng-binding").get_text()
#             if from_name == "OVERALL MOST HELPFUL REVIEW":
#                 from_name = reviews.find_all(class_="ng-binding")[1].get_text()
#
#             games = "0"
#             if reviews.find(
#                     class_="review__profile-stats-line review__profile-stats-line--with-separator ng-binding") is not None:
#                 games = reviews.find(
#                     class_="review__profile-stats-line review__profile-stats-line--with-separator ng-binding").get_text().strip()
#             num_reviews = reviews.find(
#                 class_="review__profile-stats-line ng-binding").get_text().strip()
#
#             date = reviews.find(class_="review__extra-item ng-binding ng-scope").get_text()
#             month = date.split()[0]
#             day = date.split()[1]
#             year = date.split()[2]
#             if month == "stycznia" or month == "January" or month == "Januar":
#                 month = "1"
#             elif month == "lutego" or month == "February" or month == "Februar":
#                 month = "2"
#             elif month == "marca" or month == "March" or month == "März":
#                 month = "3"
#             elif month == "kwietnia" or month == "April" or month == "April":
#                 month = "4"
#             elif month == "maja" or month == "May" or month == "Mai":
#                 month = "5"
#             elif month == "czerwca" or month == "June" or month == "Juni":
#                 month = "6"
#             elif month == "lipca" or month == "July" or month == "Juli":
#                 month = "7"
#             elif month == "sierpnia" or month == "August" or month == "August":
#                 month = "8"
#             elif month == "września" or month == "September" or month == "September":
#                 month = "9"
#             elif month == "października" or month == "October" or month == "Oktober":
#                 month = "10"
#             elif month == "listopada" or month == "November" or month == "November":
#                 month = "11"
#             elif month == "grudnia" or month == "December" or month == "Dezember":
#                 month = "12"
#
#             day = (str(day[:-1]) + "/" + str(month) + '/' + str(year))
#             date_timestamp = time.mktime(datetime.datetime.strptime(day, "%d/%m/%Y").timetuple())
#             link = (driver.current_url[25:] + str(date_timestamp) + from_name)
#             msgid_string_bytes = link.encode("UTF-8")
#             msgid_bytes = base64.b64encode(msgid_string_bytes)
#             msgid = msgid_bytes.decode("UTF-8")
#             app_rating = int()
#             for link in reviews.find_all(class_="star-rating star-rating--full"):
#                 app_rating = app_rating + 1
#             subject = str()
#             for subjects_info in reviews.find_all(class_="review__title"):
#                 subject = subjects_info.find(class_="ng-binding").get_text()
#
#             review = {
#                 'msgid': msgid,
#                 'review': review,
#                 'subject': subject,
#                 'from_name': from_name,
#                 'games': int(re.search(r'\d+', games).group()),
#                 'num_reviews': int(re.search(r'\d+', num_reviews).group()),
#                 'app_rating': str(app_rating),
#                 'date': date_timestamp
#             }
#             if date_timestamp >= date_range:
#                 reviews_data.append(review)
#
#         page = soup2.find(class_="arrow-wrapper arrow-wrapper--right")
#
#         if page is not None:
#             driver.find_element_by_css_selector('div.arrow-wrapper.arrow-wrapper--right').click()
#     driver.quit()
#     print(reviews_data)
#     print("--- %s seconds ---" % (time.time() - start_time))
#     return reviews_data