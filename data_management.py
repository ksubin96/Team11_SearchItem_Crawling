# 프로그램명 : 유튜버 분석
# 작성자 : 박민우   조(팀명) : 11조 키보드

# 인터넷속도가 느려서 브라우저의 파싱이 코드의 진행을 따라가지 못하면 오류가 발생합니다.
# 오류가 발생하면 다시 실행해보고, 오류가 반복되면 코드 내의 time.sleep()함수의 인자 값을 증가시키십시오.

# 관리자 명령프롬프트에 다음 명령어를 차례대로 입력
# curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
# python get-pip.py
# pip install bs4
# pip install requests
# pip install selenium
# pip install pandas

# 크롬 브라우저 실행 > 메뉴 > 도움말 > Chrome 정보에서 현재 크롬 버전 확인
# 시작메뉴에서 pc 정보를 검색 > 현재 os 확인
# https://sites.google.com/a/chromium.org/chromedriver/downloads에서 Chromedriver다운로드
# ! 현재 크롬 버전과 os에 맞는 것을 선택할 것
# ! 윈도우64비트도 win32를 다운받을 것
# 다운받은 zip파일을 원하는 위치에 압축해제, chromdriver 파일의 위치를 확인


# * ~내용~ : 추후에 개선하면 좋을 것 같은 내용을 서술함


import requests
from bs4 import BeautifulSoup
import time
import urllib.request
import re
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import datetime as dt
import pandas as pd
from pandas import DataFrame as df # DataFrame은 데이터분석에 특화된 자료구조이다.

# 수집할 데이터의 자료구조
# 설명 : 해당 자료들은 스프레드시트와 유사한 형태로 저장된다. 그리고 스프레드시트(예 : videos_data)안의 항목에 스프레드시트(예 : comments_data)가 포함되는 꼴을 형성한다.
youtubers_data = {'name':[], 'videos':[]}
videos_data = {'name':[], 'thumbnail':[], 'view':[], 'previous_time':[], 'video_url':[], 'start_date':[],
'comment_num':[], 'likes_num':[], 'unlikes_num':[], 'comments':[]} # videos_data는 youtubers_data의 'videos''의 value리스트에 추가된다.
comments_data = {'youtube_id':[], 'comment':[], 'like_num':[]} # comments_data는 'comments'의 value리스트에 추가된다. 아직 대댓글에 대한 정보는 수집 안함

def GetYoutuberName(youtube_search) :#미완성, 검색어를 인자로 받아 유튜버 이름을 반환
    youtube_name = 0
    # if  :
    #    return None 검색어에 해당하는 유튜버 이름이 없다면 None 반환
    return youtube_name

def GetYoutuberData(youtube_name) :#미완성, 유튜버 이름을 인자로 받아 유튜버의 영상 데이터를 반환
    index = 0
    # if  :
    #    return None 유튜버 이름이 DB에 없다면 None 반환
    return youtubers_data['videos'][index]

def test() :
    # 유튜버 검색어 입력
    youtube_search = input('유튜버 검색어 입력 : ')

    # 검색한 유튜버의 영상 목록 page로 이동
    browser = Chrome('C:/Users/박민우/Desktop/오픈소스/파일/chromedriver_win32/chromedriver')  # 본인의 chromdriver 파일의 위치로 바꿔넣을 것
    browser.get('http://www.youtube.com')  # youtube로 이동
    browser.implicitly_wait(4)  # 브라우저에서 파싱이 완료될 때까지 기다려줌. 4초를 기다려도 완료되지 않으면 에러를 떨구고 종료
    search = browser.find_elements_by_name("search_query")[0]  # 검색창영역 (youtube 기준)
    search.send_keys(youtube_search + '\n')  # 검색창 영역에 검색어+엔터
    time.sleep(4)  # 인터넷속도를 고려해서 코드의 진행속도를 제한
    browser.find_elements_by_xpath('//*[@class="style-scope ytd-channel-name"]')[0].click()  # 이동한 화면에서 youtuber 클릭
    browser.find_element_by_xpath(
        '//*[@class="scrollable style-scope paper-tabs"]/paper-tab[2]').click()  # '동영상' 카테고리 클릭

    # 스크롤을 내림. youtube는 스크롤을 내려야 page의 요소들이 업로드됨
    body = browser.find_element_by_tag_name('body')  # 스크롤하기 위해 소스 추출
    VideoList_pagedown = 1  # 일정 횟수만큼 pagedown. 적은 시간으로 적은 정보를 수집할려면 해당 값을 작게 설정 * 필요한 만큼만 pagedown하도록 코드를 개선할 필요가 있음
    for i in range(VideoList_pagedown):
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(3)  # 인터넷속도를 고려해서 코드의 진행속도를 제한

    # 영상 목록 page source 추출 + 필요한 정보(VideoList_element1)만 따로 추출
    VideoList_html = BeautifulSoup(browser.page_source, 'html.parser')
    VideoList_element0 = VideoList_html.find('div', {'id': 'items', 'class': 'style-scope ytd-grid-renderer'})
    list_videoList_element = VideoList_element0.find_all('ytd-grid-video-renderer', {
        'class': 'style-scope ytd-grid-renderer'})  # 각각의 영상의 정보가 담긴 element들의 리스트 (영상 1개당 value 1개)

    for each_VideoList_element in list_videoList_element:
        # 영상으로 이동
        video_url = 'https://www.youtube.com' + each_VideoList_element.find('a', {'id': 'thumbnail'})[
            'href']  # 영상 url이 유튜브 기본 url을 포함하지 않기 때문에 기본 url을 앞에 붙임
        browser.get(video_url)

        # 영상 pause
        # * 아직 안 만듬. 해당 부분은 없어도 딱히 문제가 되진 않음

        # 스크롤을 내림 + 댓글 인기순 정렬. youtube는 스크롤을 내려야 page의 요소들이 업로드됨
        body = browser.find_element_by_tag_name('body')
        Video_pagedown = 4  # 일정 횟수만큼 pagedown. 적은 시간으로 적은 정보를 수집할려면 해당 값을 작게 설정 * 필요한 만큼만 pagedown하도록 코드를 개선할 필요가 있음
        for i in range(4):  # 4번 정도는 pagedown을 입력해야 "인기순/작성순 선택할 수 있는 영역"이 page에 업로드됨
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(3)  # 인터넷속도를 고려해서 코드의 진행속도를 제한
        browser.find_element_by_xpath(
            '//paper-button[@class="dropdown-trigger style-scope yt-dropdown-menu"]').click()  # 인기순/작성순 선택할 수 있는 영역 클릭
        browser.find_element_by_xpath(
            '//paper-listbox[@class="dropdown-content style-scope yt-dropdown-menu"]/a[1]').click()  # 인기순 카테고리 클릭
        for i in range(Video_pagedown - 4):
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(3)  # 인터넷속도를 고려해서 코드의 진행속도를 제한

        # 영상 page source 추출 + 필요한 정보(comment_element) 추가로 추출
        video_html = BeautifulSoup(browser.page_source, 'html.parser')
        list_comment_element = video_html.find_all('ytd-comment-renderer', {
            'class': 'style-scope ytd-comment-thread-renderer'})  # 각각의 댓글의 정보가 담긴 element들의 리스트 (댓글 1개당 value 1개)

        # 하나의 영상에 대해 필요한 정보(each_VideoList_element, video_html, list_comment_element)가 추출되었다. 이제 본격적으로 데이터를 수집하기 시작한다.
        videos_data['name'] += [each_VideoList_element.find('a', {'id': 'video-title'}).text]
        videos_data['thumbnail'] += [each_VideoList_element.find('a', {'id': 'thumbnail'}).find('img')['src']]
        videos_data['video_url'] += [video_url]
        meta = each_VideoList_element.find('div', {'id': 'metadata-line'})
        videos_data['view'] += [
            meta.find_all('span', {'class': 'style-scope ytd-grid-video-renderer'})[0].text.split()[1]]
        videos_data['previous_time'] += [
            meta.find_all('span', {'class': 'style-scope ytd-grid-video-renderer'})[1].text]
        videos_data['start_date'] += [
            video_html.find('span', {'class': 'date style-scope ytd-video-secondary-info-renderer'}).text]
        videos_data['comment_num'] += [video_html.find('h2', {'id': 'count'}).find('yt-formatted-string').text]
        videos_data['likes_num'] += [video_html.find('yt-formatted-string', {'id': 'text',
                                                                             'class': 'style-scope ytd-toggle-button-renderer style-text',
                                                                             'aria-label': re.compile(
                                                                                 '좋아요')}).text + '개']
        videos_data['unlikes_num'] += [video_html.find('yt-formatted-string', {'id': 'text',
                                                                               'class': 'style-scope ytd-toggle-button-renderer style-text',
                                                                               'aria-label': re.compile(
                                                                                   '싫어요')}).text + '개']
        for each_comment_element in list_comment_element:
            comments_data['youtube_id'] += ["".join(
                re.findall('[가-힣0-9a-zA-Z]', each_comment_element.find('a', {'id': 'author-text'}).find('span').text))]
            comments_data['comment'] += [each_comment_element.find('yt-formatted-string', {'id': 'content-text',
                                                                                           'class': 'style-scope ytd-comment-renderer'}).text]
            try:
                comments_data['like_num'] += ["".join(
                    re.findall('[0-9]', each_comment_element.find('span', {'id': 'vote-count-left'}).text)) + '개']
            except:
                comments_data['like_num'] += ['0개']
        videos_data['comments'] += [comments_data]  # comments_data를 'comments'의 value리스트에 추가
        comments_data = {'youtube_id': [], 'comment': [], 'like_num': []}  # 이후의 반복에서 comments_data를 쓰기 위해 미리 초기화

    # videos_data를 출력해서 확인해보기
    print_data = videos_data.copy()
    del (print_data['comments'])
    print(df(print_data))

    # 첫번째 영상의 첫번째 댓글 내용을 출력 해보기
    print(videos_data['comments'][0]['comment'][0])


