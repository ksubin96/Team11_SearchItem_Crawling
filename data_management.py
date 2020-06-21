# 프로그램명 : 유튜버 분석
# 작성자 : 박민우   조(팀명) : 11조 키보드
# 범위 : 해당 파일 전체

#하단의 주석문에서 시키는 대로 해야 프로그램이 동작합니다.

# mysql다운 받기
# ! ecampus 강의자료 - 9주차 - 데이터베이스pdf파일 에서 맨 밑에 보면 mysql다운 받는 방법이 있음
# ! 설치할 때 본인이 부여한 비밀번호를 까먹으면 안됨. 적당한 메모장에 비밀번호를 저장해두는 것을 추천

# 관리자 명령프롬프트에 다음 명령어를 전부 입력
# curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
# python get-pip.py
# pip install bs4
# pip install requests
# pip install selenium
# pip install pandas
# pip install pymysql

# 크롬 브라우저 실행 > 메뉴 > 도움말 > Chrome 정보에서 현재 크롬 버전 확인
# 시작메뉴에서 pc 정보를 검색 > 현재 os 확인
# https://sites.google.com/a/chromium.org/chromedriver/downloads에서 Chromedriver다운로드
# ! 현재 크롬 버전과 os에 맞는 것을 선택할 것
# ! 윈도우64비트도 win32를 다운받을 것
# 다운받은 zip파일을 압축해제, 반드시 data_management.py와 chromedriver가 같은 폴더 내에 있도록 할 것.

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
from pandas import DataFrame as df
import pymysql


# 사용 가능
# 검색어를 인자로 받아 해당 검색어와 동일한 이름을 가지는 유튜버가 DB에 있다면 그 유튜버url을 반환. 없다면 해당,,
def GetYoutuberUrl(youtube_search, con) :
    cur = con.cursor()
    cur.execute('SELECT * FROM youtubers')
    list = cur.fetchall()
    i = 0
    while True:
        try:
            if list[i][1] == youtube_search:
                return list[i][0]
        except:
            break
        i += 1
    co=Options()
    co.add_argument('headless')
    browser = Chrome('./chromedriver',chrome_options=co)
    browser.implicitly_wait(10)  # 브라우저에서 파싱이 완료될 때까지 기다려줌.
    browser.get('https://www.youtube.com/results?search_query='+youtube_search)  # youtube로 이동
    Search_html = BeautifulSoup(browser.page_source, 'html.parser')
    browser.close()
    try:
        return Search_html.find('a', {'class': 'yt-simple-endpoint style-scope yt-formatted-string'})['href'][1:]
    except:
        return None

# 사용 가능
# 주어진 ip pw로 youtuberDB에 접속한다.
def ConnectmainDB(pw, ip) :
    try : return pymysql.connect(ip, user='root', password=pw, database='youtuberDB', charset='utf8mb4')
    except : return None

# 사용 가능
# admin 용 : 주어진 pw로 본인의 DB에 접속한다.
def ConnectDB(pw) :
    try : return pymysql.connect(host='127.0.0.1', user='root', password=pw)
    except : return None

# 사용 가능
# url에 해당하는 table의 값들을 csv파일의 형태으로 반환
def GetData(url, con) :
    try:
        cur = con.cursor()
        if 'user/' in url or 'channel/' in url:
            cur.execute('SELECT * FROM videos_' + re.sub(r'[^\w]', r'_', url))
        else:
            cur.execute('SELECT * FROM comments_' + re.sub(r'[^\w]', r'_', url))
        return cur.fetchall()
    except : return None

# 사용 가능
# 주어진 url에 해당하는 유튜버의 이름을 반환 없으면 none 반환
def GetYoutuberName(youtuber_url, con):
    cur = con.cursor()
    cur.execute('SELECT * FROM youtubers')
    list = cur.fetchall()
    i = 0
    while True:
        try:
            if list[i][0] == youtuber_url:
                return list[i][1]
        except:
            return None
        i += 1


# 사용 가능
def CrawlAndSave(youtuber_url, con) :
    VideoList_pagedown = 0
    Video_pagedown = 5

    # 검색한 유튜버의 영상 목록 page로 이동
    browser = Chrome('./chromedriver')
    browser.implicitly_wait(10)  # 브라우저에서 파싱이 완료될 때까지 기다려줌.
    browser.get('https://www.youtube.com/'+youtuber_url+'/videos')  # youtuber의 동영상 카테고리으로 이동

    # 유튜버 이름과 유튜버 url 수집
    cur = con.cursor()
    youtuber_html = BeautifulSoup(browser.page_source, 'html.parser')
    youtuber_name=youtuber_html.find('yt-formatted-string', {'class': 'style-scope ytd-channel-name'}).text.replace('\'', '').replace('\"', '')
    cur.execute("INSERT INTO youtubers VALUES('" + youtuber_url + "','" + youtuber_name + "')")
    try:
        cur.execute('CREATE TABLE videos_' + re.sub(r'[^\w]', r'_',youtuber_url) + ' (url VARCHAR(12),name VARCHAR(180),view VARCHAR(11),likes_num VARCHAR(6),unlikes_num VARCHAR(6),length VARCHAR(9),comment_num VARCHAR(8),previous_time VARCHAR(6))')
    except:
        None

    # 스크롤을 내림. youtube는 스크롤을 내려야 page의 요소들이 업로드됨
    if VideoList_pagedown == 0: time.sleep(1)
    num = 0
    while True:
        if VideoList_pagedown == num: break
        num += 1

    # 영상 목록 page source 추출 + 필요한 정보(VideoList_element1)만 따로 추출
    VideoList_html = BeautifulSoup(browser.page_source, 'html.parser')
    VideoList_element0 = VideoList_html.find('div', {'id': 'items', 'class': 'style-scope ytd-grid-renderer'})
    list_videoList_element = VideoList_element0.find_all('ytd-grid-video-renderer', {
        'class': 'style-scope ytd-grid-renderer'})  # 각각의 영상의 정보가 담긴 element들의 리스트 (영상 1개당 value 1개)

    for each_VideoList_element in list_videoList_element:
        # 영상으로 이동
        video_url = each_VideoList_element.find('a', {'id': 'thumbnail'})['href'][9:]

        delay = 0
        commentexist = True
        while True:
            try:
                browser.get('https://www.youtube.com/watch?v=' + video_url)

                # 영상 pause
                # * 아직 안 만듬. 해당 부분은 없어도 상관없음

                # 스크롤을 내림 + 댓글 인기순 정렬. youtube는 스크롤을 내려야 page의 요소들이 업로드됨
                while True:
                    browser.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
                    try:
                        browser.find_element_by_xpath('//paper-button[@class="dropdown-trigger style-scope yt-dropdown-menu"]').click()  # 인기순/작성순 선택할 수 있는 영역 클릭
                        browser.find_element_by_xpath('//paper-listbox[@class="dropdown-content style-scope yt-dropdown-menu"]/a[1]').click()  # 인기순 카테고리 클릭
                        break
                    except:
                        None
                    try: # 댓글을 달 수 없는 영상인지 확인
                        video_html = BeautifulSoup(browser.page_source, 'html.parser')
                        if video_html.find('ytd-comments', {'id': 'comments'}).find('a', {'class': 'yt-simple-endpoint style-scope yt-formatted-string', 'spellcheck': 'false'}).text == '자세히 알아보기':
                            commentexist = False
                            break
                        break
                    except:
                        None
                if commentexist == True:
                    num = 0
                    while True:
                        if Video_pagedown == num: break
                        num += 1
                        browser.find_element_by_tag_name('body').send_keys(Keys.END)
                else:
                    video_comment_num = '댓글불가'

                # 영상 page source 추출
                video_html = BeautifulSoup(browser.page_source, 'html.parser')

                # 영상 데이터 수집
                video_name = re.sub(r'[\'\"]', r'', each_VideoList_element.find('a', {'id': 'video-title'}).text)
                video_length = re.sub(r'[ \n]', r'', each_VideoList_element.find('span', {'class': 'style-scope ytd-thumbnail-overlay-time-status-renderer'}).text)
                video_previous_time = each_VideoList_element.find('div', {'id': 'metadata-line'}).find_all('span', {'class': 'style-scope ytd-grid-video-renderer'})[1].text.replace(' 전', '')
                if commentexist == True: video_comment_num = re.sub(r'[댓글 개,]', r'', video_html.find('h2', {'id': 'count'}).find('yt-formatted-string').text)
                video_likes_num = video_html.find('yt-formatted-string', {'id': 'text', 'class': 'style-scope ytd-toggle-button-renderer style-text', 'aria-label': re.compile('좋아요')}).text
                video_unlikes_num = video_html.find('yt-formatted-string', {'id': 'text', 'class': 'style-scope ytd-toggle-button-renderer style-text', 'aria-label': re.compile('싫어요')}).text
                video_view = re.sub(r'[조회수 회,]', r'', video_html.find('span', {'class': 'view-count style-scope yt-view-count-renderer'}).text)

                break
            except:
                delay += 1
            if delay == 10:
                break
        if delay == 10:
            print('!')
            continue # 동영상 데이터 한 개 누락됨. 인터넷상태가 안 좋으면 자주 발동된다.

        # 영상 데이터를 DB에 저장
        cur.execute("INSERT INTO videos_" + re.sub(r'[^\w]', r'_', youtuber_url) + " VALUES('" + video_url + "','" + video_name + "','" + video_view + "','" + video_likes_num + "','" + video_unlikes_num + "','" + video_length + "','" + video_comment_num + "','" + video_previous_time + "')")

        if commentexist == True:
            # 댓글 테이블 생성
            try: cur.execute('CREATE TABLE comments_' + re.sub(r'[^\w]', r'_', video_url) + ' (youtube_id VARCHAR(80),like_num VARCHAR(6),comment TEXT)')
            except: None

            # 영상 page source 에서 댓글 source 만 따로 추출
            list_comment_element = video_html.find_all('ytd-comment-renderer', {'class': 'style-scope ytd-comment-thread-renderer'})  # 각각의 댓글의 정보가 담긴 element들의 리스트 (댓글 1개당 value 1개)

            # 댓글 데이터 수집
            for each_comment_element in list_comment_element:
                comment_youtube_id = re.sub(r'[ \n\'\"]', r'', each_comment_element.find('a', {'id': 'author-text'}).find('span').text)
                comment_comment = re.sub(r'[\'\"]', r'', each_comment_element.find('yt-formatted-string', {'id': 'content-text', 'class': 'style-scope ytd-comment-renderer'}).text)
                try: comment_like_num = re.sub(r'[ \n]', r'', each_comment_element.find('span', {'id': 'vote-count-left'}).text)
                except: comment_like_num = '0'

                # 댓글 데이터를 DB에 저장
                cur.execute("INSERT INTO comments_" + re.sub(r'[^\w]', r'_', video_url) + " VALUES('" + comment_youtube_id + "','" + comment_like_num + "','" + comment_comment + "')")
    browser.close()
    con.commit()
    con.close()

# 사용가능
# 본인 컴퓨터에 youtuberDB생성
def newDB(pw):
    con = pymysql.connect(host='127.0.0.1', user='root', password=pw)
    cur = con.cursor()
    try :
        cur.execute("CREATE DATABASE youtuberDB")
        con = pymysql.connect(host='127.0.0.1', user='root', password=pw, database='youtuberDB', charset='utf8mb4')
        cur = con.cursor()
        cur.execute("CREATE TABLE youtubers (url VARCHAR(33), name VARCHAR(80))")
    except : None

# 사용가능
# 본인 컴퓨터에서 youtuberDB제거
def delDB(pw):
    con = pymysql.connect(host='127.0.0.1', user='root', password=pw)
    cur = con.cursor()
    try : cur.execute("DROP DATABASE youtuberDB")
    except : None

# 사용가능
# test용 함수
def PrintData(x) :
    print(df(x))

# 사용가능
# test용 함수
# 왜인지는 모르겠지만 대문자를 소문자로 바꿔서 보여줌
def PrintTable(pw, ip='127.0.0.1') :
    con = pymysql.connect(ip, user='root', password=pw, database='youtuberDB', charset='utf8mb4')
    cur = con.cursor()
    cur.execute("SHOW TABLES")
    print(cur.fetchall())











# 이하 내용은 일종의 더미데이터 (오류 테스트 용)

# '11whzlqhem'


def test1() :
    print(GetYoutuberUrl('보겸'))
    i = input('...')

# test1()

def testone(s) :
    VideoList_pagedown = 0
    Video_pagedown = 1

    # 검색한 유튜버의 영상 목록 page로 이동
    browser = Chrome('./chromedriver')
    browser.implicitly_wait(10)  # 브라우저에서 파싱이 완료될 때까지 기다려줌.
    browser.get(s)  # youtuber의 동영상 카테고리으로 이동


    # 스크롤을 내림. youtube는 스크롤을 내려야 page의 요소들이 업로드됨
    if VideoList_pagedown == 0:time.sleep(1)
    num = 0
    while True:
        if VideoList_pagedown == num: break
        num += 1
        browser.find_element_by_tag_name('body').send_keys(Keys.END)

    # 영상 목록 page source 추출 + 필요한 정보(VideoList_element1)만 따로 추출
    VideoList_html = BeautifulSoup(browser.page_source, 'html.parser')
    VideoList_element0 = VideoList_html.find('div', {'id': 'items', 'class': 'style-scope ytd-grid-renderer'})
    list_videoList_element = VideoList_element0.find_all('ytd-grid-video-renderer', {
        'class': 'style-scope ytd-grid-renderer'})  # 각각의 영상의 정보가 담긴 element들의 리스트 (영상 1개당 value 1개)

    each_VideoList_element=list_videoList_element[14]
    # 영상으로 이동
    video_url = each_VideoList_element.find('a', {'id': 'thumbnail'})[
                    'href'][9:]

    delay = 0
    commentexist=True
    while True:
        try:
            browser.get('https://www.youtube.com/watch?v=' + video_url)

            # 영상 pause
            # * 아직 안 만듬. 해당 부분은 없어도 상관없음

            # 스크롤을 내림 + 댓글 인기순 정렬. youtube는 스크롤을 내려야 page의 요소들이 업로드됨
            while True:
                browser.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
                try:
                    browser.find_element_by_xpath('//paper-button[@class="dropdown-trigger style-scope yt-dropdown-menu"]').click()  # 인기순/작성순 선택할 수 있는 영역 클릭
                    browser.find_element_by_xpath('//paper-listbox[@class="dropdown-content style-scope yt-dropdown-menu"]/a[1]').click()  # 인기순 카테고리 클릭
                    break
                except: None
                try :
                    video_html = BeautifulSoup(browser.page_source, 'html.parser')
                    if video_html.find('ytd-comments', {'id': 'comments'}).find('a', {'class': 'yt-simple-endpoint style-scope yt-formatted-string', 'spellcheck': 'false'}).text == '자세히 알아보기' :
                        commentexist = False
                        break
                except : None
            if commentexist == True:
                num = 0
                while True:
                    if Video_pagedown == num: break
                    num += 1
                    browser.find_element_by_tag_name('body').send_keys(Keys.END)
            else : video_comment_num = '0'

            # 영상 page source 추출 + 필요한 정보(comment_element) 추가로 추출
            video_html = BeautifulSoup(browser.page_source, 'html.parser')
            list_comment_element = video_html.find_all('ytd-comment-renderer', {
                'class': 'style-scope ytd-comment-thread-renderer'})  # 각각의 댓글의 정보가 담긴 element들의 리스트 (댓글 1개당 value 1개)

            # 하나의 영상에 대해 필요한 정보(each_VideoList_element, video_html, list_comment_element)가 추출되었다. 이제 본격적으로 데이터를 수집하기 시작한다.
            video_name = re.sub(r'[\'\"]', r'', each_VideoList_element.find('a', {'id': 'video-title'}).text)
            video_length = re.sub(r'[ \n]', r'', each_VideoList_element.find('span', {'class': 'style-scope ytd-thumbnail-overlay-time-status-renderer'}).text)
            video_previous_time = each_VideoList_element.find('div', {'id': 'metadata-line'}).find_all('span', {'class': 'style-scope ytd-grid-video-renderer'})[1].text.replace(' 전', '')
            if commentexist == True : video_comment_num = re.sub(r'[댓글 개,]', r'', video_html.find('h2', {'id': 'count'}).find('yt-formatted-string').text)
            video_likes_num = video_html.find('yt-formatted-string', {'id': 'text', 'class': 'style-scope ytd-toggle-button-renderer style-text', 'aria-label': re.compile('좋아요')}).text
            video_unlikes_num = video_html.find('yt-formatted-string', {'id': 'text', 'class': 'style-scope ytd-toggle-button-renderer style-text', 'aria-label': re.compile('싫어요')}).text
            video_view = re.sub(r'[조회수 회,]', r'', video_html.find('span', {'class': 'view-count style-scope yt-view-count-renderer'}).text)

            break
        except:
            delay += 1
        if delay == 10:
            break
    if delay == 10:
        print('동영상 데이터 한 개 누락됨')  # 인터넷상태가 안 좋으면 이 문장이 자주 발동된다.
        return None

    print('video_url : ' + video_url)
    print('video_name : ' + video_name)
    print('video_view : ' + video_view)
    print('video_likes_num : ' + video_likes_num)
    print('video_unlikes_num : ' + video_unlikes_num)
    print('video_length : ' + video_length)
    print('video_comment_num : ' + video_comment_num)
    print('video_previous_time : ' + video_previous_time)
    print()

    if commentexist == True :
        #댓글 테이블 생성
        each_comment_element = list_comment_element[3]
        comment_youtube_id = re.sub(r'[ \n\'\"]', r'', each_comment_element.find('a', {'id': 'author-text'}).find('span').text)
        comment_comment = re.sub(r'[\'\"]', r'', each_comment_element.find('yt-formatted-string', {'id': 'content-text', 'class': 'style-scope ytd-comment-renderer'}).text)
        try: comment_like_num = re.sub(r'[ \n]', r'', each_comment_element.find('span', {'id': 'vote-count-left'}).text)
        except: comment_like_num = '0'
        print('comment_youtube_id : ' + comment_youtube_id)
        print('comment_like_num : ' + comment_like_num)
        print('comment_comment : ' + comment_comment)



def heighttest():
    browser = Chrome('./chromedriver')
    browser.implicitly_wait(10)  # 브라우저에서 파싱이 완료될 때까지 기다려줌.
    browser.get('https://www.youtube.com/channel/UC-GDTIsh_jNVM41AIf4C_yw/videos')
    while True:
        pageheight = browser.execute_script("return document.body.scrollHeight")
        print(pageheight)
        if pageheight != 0:break


# heighttest()



def testDB2() :
    con = pymysql.connect(host='127.0.0.1', user='root', password='11whzlqhem')
    cur = con.cursor()
    try:
        cur.execute('DROP DATABASE test')
    except:
        None
    cur.execute("CREATE DATABASE test")
    con = pymysql.connect(host='127.0.0.1', user='root', password='11whzlqhem', database='test', charset='utf8mb4')
    cur = con.cursor()
    comment = 'c'
    cur.execute("CREATE TABLE TT (id char(1),pw char(1),t TEXT)")
    cur.execute("INSERT INTO TT VALUES('가','1','a')")
    cur.execute("INSERT INTO TT VALUES('나','2','b')")
    cur.execute("INSERT INTO TT VALUES('다','3','"+comment+"')")
    con.commit()
    cur.execute("SELECT * FROM tt")
    row = None
    while(1) :
        row = cur.fetchone()
        if row == None :
            break;
        print(row[0]+" "+row[1]+" "+row[2])
    cur.execute("SELECT * FROM TT")
    print(df(cur.fetchall()))
    print()
    cur.execute("SELECT * FROM TT")
    print(cur.fetchall()[2][2])
    cur.execute("SHOW TABLES")
    print(cur.fetchall())
    cur.execute('DROP DATABASE test')
    con.close()
# testDB2()

#browser.find_elements_by_name("search_query")[0].send_keys(youtube_search + '\n')  # 검색창 영역에 검색어 + 엔터