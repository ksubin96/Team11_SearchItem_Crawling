def anls() : #미완성
    import pd as pd
import requests
from bs4 import BeautifulSoup
import time
import urllib.request #
from selenium.webdriver import Chrome
import re
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import datetime as dt

##isabe = pd.DataFrame({'name':[],
                     ##'thumbnail':[],
                     ##'view':[],
                     ##'previous_time':[],
                     ##'video_url':[],
                     ##'start_date':[],
                     ##'comment':[],
                     ##'likes_num':[],
                     ##'unlikes_num':[]})

start_url = 'http://www.youtube.com'
delay=3
browser = Chrome()
browser.implicitly_wait(delay)

browser.get(start_url)
browser.maximize_window()

#[0].send_keys('테스터훈')


#URL 추출
html0 = browser.page_source
html = BeautifulSoup(html0,'html.parser')
video_ls = html.find_all('ytd-grid-video-renderer',{'class':'style-scope ytd-grid-renderer'})
b = html.find('div',{'id':'items','class':'style-scope ytd-grid-renderer'})
len(b.find_all('ytd-grid-video-renderer',{'class':'style-scope ytd-grid-renderer'}))


tester_url = []
for i in range(len(video_ls)):
    url = start_url+video_ls[i].find('a',{'id':'thumbnail'})['href']
    tester_url.append(url)

# 영상정보 추출


video_info = pd.DataFrame({'title': [], 'view:':[], 'like':[], 'unlike':[],'video_time':[]}) #영상 제목, 조회수 좋아요, 싫어요 , 영상길이

browser.get(tester_url[2])
body = browser.find_element_by_tag_name('body') # 스크롤 위해 소스 추출

num_of_pagedowns =2
#10번 밑으로 내림
while num_of_pagedowns:
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(2)
    num_of_pagedowns -= 1

time.sleep(2)

soup0 = browser.page_source
time.sleep(1.5)
soup = BeautifulSoup(soup0,'html.parser')

info1 = soup.find('div',{'id':'info-contnets'})

title = info1.find('h1', {'class': 'title style-scope ytd-video-primary-info-renderer'}).text
view = info1.find('yt-view-count-renderer', {'class': 'style-scope ytd-video-primary-info-renderer'}).find_all('span')[
    0].text
like = info1.find('div', {'id': 'top-level-buttons'}).find_all('yt-formatted-string')[0].text
unlike = info1.find('div', {'id': 'top-level-buttons'}).find_all('yt-formatted-string')[1].text
video_time = info1.find('span', {'class': 'video_time style-scope ytd-thumbnail-overlay-time-status-renderer'}).text

video_info = pd.DataFrame({'title': [],
                           'view': [],
                           'like': [],
                           'unlike': [],
                           'video_time': []})

for i in range(95,len(tester_url)):
    browser.get(tester_url[i])
    time.sleep(1.5)

    body = browser.find_element_by_tag_name('body')  # 스크롤하기 위해 소스 추출

    num_of_pagedowns = 2
    # 10번 밑으로 내리는 것
    while num_of_pagedowns:
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(2)
        num_of_pagedowns -= 1

    time.sleep(2)

    soup0 = browser.page_source
    time.sleep(1.5)
    soup = BeautifulSoup(soup0, 'html.parser')

    info1 = soup.find('div', {'id': 'info-contents'})

    title = info1.find('h1', {'class': 'title style-scope ytd-video-primary-info-renderer'}).text
    view = \
    info1.find('yt-view-count-renderer', {'class': 'style-scope ytd-video-primary-info-renderer'}).find_all('span')[
        0].text
    like = info1.find('div', {'id': 'top-level-buttons'}).find_all('yt-formatted-string')[0].text
    unlike = info1.find('div', {'id': 'top-level-buttons'}).find_all('yt-formatted-string')[1].text
    video_time = info1.find('span', {'class': 'video_time style-scope ytd-thumbnail-overlay-time-status-renderer'}).text

    insert_data = pd.DataFrame({'title': [title], #영상 제목
                                'view': [view], # 조회수
                                'like': [like], # 좋아요 수
                                'unlike': [unlike], #싫어요 수
                                'video_time': [video_time]}) #영상 길이

    video_info = video_info.append(insert_data)

    video_info = range(len(video_info))

    return None
