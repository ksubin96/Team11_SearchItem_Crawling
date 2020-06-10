# 프로그램명 : 유튜버 분석
# 작성자 : 박민우   조(팀명) : 11조 키보드

#하단의 주석문에서 시키는 대로 해야 프로그램이 동작합니다.

# mysql다운 받기
# ! ecampus 강의자료 - 9주차 - 데이터베이스pdf파일 에서 맨 밑에 보시면 mysql다운 받는 방법이 있음
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
def GetYoutuberNameUrl(youtube_search) :# 검색어를 인자로 받아 유튜버 이름과 유튜버url을 반환
    browser = Chrome('./chromedriver')
    browser.implicitly_wait(10)  # 브라우저에서 파싱이 완료될 때까지 기다려줌.
    browser.get('http://www.youtube.com')  # youtube로 이동
    browser.find_elements_by_name("search_query")[0].send_keys(youtube_search + '\n')  # 검색창 영역에 검색어+엔터
    time.sleep(1)
    Search_html = BeautifulSoup(browser.page_source, 'html.parser')
    try : return Search_html.find('yt-formatted-string', {'class':'style-scope ytd-channel-name'}).text, Search_html.find('a', {'class': 'yt-simple-endpoint style-scope yt-formatted-string'})['href'][1:]
    except : return None

# 사용 가능
# url에 해당하는 table의 값들을 csv파일의 형태으로 반환
def GetData(url, pw, ip='127.0.0.1') : # ip 입력안하면 본인 컴퓨터를 가리키는 ip로 지정
    con = pymysql.connect(ip, user='root', password=pw, database='youtuberDB', charset='utf8')
    cur = con.cursor()
    try:
        if 'user/' in url or 'channel/' in url :
            cur.execute('SELECT * FROM videos:' + re.sub(r'[^\w_]',r'',url))
        else:
            cur.execute('SELECT * FROM comments:' + re.sub(r'[^\w_]',r'',url))
        return cur.fetchall()
    except : return None

# 사용가능
# 순전히 test용 함수
def PrintData(x) :
    print(df(x))

# 사용 가능
def CrawlAndSave(youtuber_name, youtuber_url, pw, ip='127.0.0.1') : # ip 입력안하면 본인 컴퓨터를 가리키는 ip로 지정
    # 유튜버 이름과 유튜버 url 수집
    con = pymysql.connect(ip, user='root', password=pw, database='youtuberDB', charset='utf8')
    cur = con.cursor()
    cur.execute("INSERT INTO youtubers VALUES('"+youtuber_url+"','"+youtuber_name+"')")
    try : cur.execute(
            'CREATE TABLE videos_' + re.sub(r'[^\w_]',r'',youtuber_name) + ' (url VARCHAR(12),name VARCHAR(180),view VARCHAR(11),likes_num VARCHAR(6),unlikes_num VARCHAR(6),length VARCHAR(9),comment_num VARCHAR(8),previous_time VARCHAR(6))')
    except : None

    # 검색한 유튜버의 영상 목록 page로 이동
    browser = Chrome('./chromedriver')
    browser.implicitly_wait(10)  # 브라우저에서 파싱이 완료될 때까지 기다려줌.
    browser.get('https://www.youtube.com/'+youtuber_url+'/videos')  # youtuber의 동영상 카테고리으로 이동

    # 스크롤을 내림. youtube는 스크롤을 내려야 page의 요소들이 업로드됨
    VideoList_pagedown = 0  # 일정 횟수만큼 pagedown. 적은 시간으로 적은 정보를 수집할려면 해당 값을 작게 설정 * 필요한 만큼만 pagedown하도록 코드를 개선할 필요가 있음
    time.sleep(1)  # VideoList_pagedown = 0이라서 필요. 원래는 없어도 됨
    for i in range(VideoList_pagedown):
        browser.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN) #pagedown 입력

    # 영상 목록 page source 추출 + 필요한 정보(VideoList_element1)만 따로 추출
    VideoList_html = BeautifulSoup(browser.page_source, 'html.parser')
    VideoList_element0 = VideoList_html.find('div', {'id': 'items', 'class': 'style-scope ytd-grid-renderer'})
    list_videoList_element = VideoList_element0.find_all('ytd-grid-video-renderer', {
        'class': 'style-scope ytd-grid-renderer'})  # 각각의 영상의 정보가 담긴 element들의 리스트 (영상 1개당 value 1개)

    for each_VideoList_element in list_videoList_element:
        # 영상으로 이동
        video_url = each_VideoList_element.find('a', {'id': 'thumbnail'})[
            'href'][9:]
        browser.get('https://www.youtube.com/watch?v=' + video_url)

        # 영상 pause
        # * 아직 안 만듬. 해당 부분은 없어도 상관없음

        # 스크롤을 내림 + 댓글 인기순 정렬. youtube는 스크롤을 내려야 page의 요소들이 업로드됨
        Video_pagedown = 7  # 일정 횟수만큼 pagedown. 적은 시간으로 적은 정보를 수집할려면 해당 값을 작게 설정 * 필요한 만큼만 pagedown하도록 코드를 개선할 필요가 있음
        t = True
        for i in range(Video_pagedown):
            browser.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
            if t==True :
                try:
                    browser.find_element_by_xpath(
                        '//paper-button[@class="dropdown-trigger style-scope yt-dropdown-menu"]').click()  # 인기순/작성순 선택할 수 있는 영역 클릭
                    browser.find_element_by_xpath(
                        '//paper-listbox[@class="dropdown-content style-scope yt-dropdown-menu"]/a[1]').click()  # 인기순 카테고리 클릭
                    t = False
                except:
                    None




        # 영상 page source 추출 + 필요한 정보(comment_element) 추가로 추출
        video_html = BeautifulSoup(browser.page_source, 'html.parser')
        list_comment_element = video_html.find_all('ytd-comment-renderer', {
            'class': 'style-scope ytd-comment-thread-renderer'})  # 각각의 댓글의 정보가 담긴 element들의 리스트 (댓글 1개당 value 1개)

        # 하나의 영상에 대해 필요한 정보(each_VideoList_element, video_html, list_comment_element)가 추출되었다. 이제 본격적으로 데이터를 수집하기 시작한다.
        video_name = each_VideoList_element.find('a', {'id': 'video-title'}).text.replace('\'', '').replace('\"', '')
        video_length = each_VideoList_element.find('span', {'class': 'style-scope ytd-thumbnail-overlay-time-status-renderer'}).text.replace(' ', '').replace('\n', '')
        meta = each_VideoList_element.find('div', {'id': 'metadata-line'})
        video_view = meta.find_all('span', {'class': 'style-scope ytd-grid-video-renderer'})[0].text.replace('조회수 ', '').replace('회', '')
        video_previous_time = meta.find_all('span', {'class': 'style-scope ytd-grid-video-renderer'})[1].text.replace(' 전', '')
        video_comment_num = video_html.find('h2', {'id': 'count'}).find('yt-formatted-string').text.replace('댓글 ', '').replace('개', '').replace(',', '')
        video_likes_num = video_html.find('yt-formatted-string', {'id': 'text','class': 'style-scope ytd-toggle-button-renderer style-text','aria-label': re.compile('좋아요')}).text
        video_unlikes_num = video_html.find('yt-formatted-string', {'id': 'text','class': 'style-scope ytd-toggle-button-renderer style-text','aria-label': re.compile('싫어요')}).text
        cur.execute("INSERT INTO videos_" + re.sub(r'[^\w_]',r'',youtuber_name) + " VALUES('" + video_url + "','" + video_name + "','" + video_view + "','" + video_likes_num + "','" + video_unlikes_num + "','" + video_length + "','" + video_comment_num + "','" + video_previous_time + "')")
        try :
            cur.execute('CREATE TABLE comments_' + re.sub(r'[^\w_]', r'',
                                                          video_url) + ' (youtube_id VARCHAR(80),like_num VARCHAR(6),comment TEXT)')
        except : None
        for each_comment_element in list_comment_element:
            comment_youtube_id = "".join( re.findall('[가-힣0-9a-zA-Z]', each_comment_element.find('a', {'id': 'author-text'}).find('span').text)).replace('\'', '').replace('\"', '')
            comment_comment = each_comment_element.find('yt-formatted-string', {'id': 'content-text', 'class': 'style-scope ytd-comment-renderer'}).text.replace('\'', '').replace('\"', '')
            try: comment_like_num = "".join(re.findall('[0-9]', each_comment_element.find('span', {'id': 'vote-count-left'}).text))
            except: comment_like_num = '0'
            cur.execute("INSERT INTO comments_" + re.sub(r'[^\w_]',r'',video_url) + " VALUES('" + comment_youtube_id + "','" + comment_like_num + "','" + comment_comment + "')")
    con.commit()
    con.close()

# 사용가능
# 이 함수를 작동시키면 : 본인 컴퓨터에 원래 있던(있다면) youtuberDB를 제거 + 새로 youtuberDB생성
def newDB(pw):
    con = pymysql.connect(host='127.0.0.1', user='root', password=pw)
    cur = con.cursor()
    try : cur.execute("DROP DATABASE youtuberDB")
    except : None
    cur.execute("CREATE DATABASE youtuberDB")
    con = pymysql.connect(host='127.0.0.1', user='root', password='11whzlqhem', database='youtuberDB', charset='utf8')
    cur = con.cursor()
    cur.execute("CREATE TABLE youtubers (url VARCHAR(33), name VARCHAR(80))")

# 사용 불가
# 이 함수의 용도 : 서버 관리자가 서버 호스트 db의 데이터를 업데이트해주는 데에 사용
# 이 함수는 없어도 딱히 상관없다.
def GetUpdateData() :
    return None


# 이하 내용은 신경안써도 됨

# '11whzlqhem'

videos_data = {'name':[], 'view':[], 'previous_time':[], 'url':[], 'start_date':[],'comment_num':[], 'likes_num':[], 'unlikes_num':[], 'length':[], 'comments':[]}
comments_data = {'youtube_id':[], 'comment':[], 'like_num':[]}

def testprint(s) :
    print('name : '+videos_data['name'][0])
    print('length : '+videos_data['length'][0])
    print('url : '+videos_data['url'][0])
    print('view : '+videos_data['view'][0])
    print('previous_time : '+videos_data['previous_time'][0])
    print('comment_num : '+videos_data['comment_num'][0])
    print('likes_num : '+videos_data['likes_num'][0])
    print('unlikes_num : '+videos_data['unlikes_num'][0])
    print('')
    print('youtube_id : '+comments_data['youtube_id'][0])
    print('like_num : '+comments_data['like_num'][0])
    print('comment : '+comments_data['comment'][0])


def test1() :
    browser = Chrome('C:/Users/박민우/Desktop/오픈소스/파일/chromedriver_win32/chromedriver')  # 본인의 chromdriver 파일의 위치로 바꿔넣을 것
    browser.implicitly_wait(10)  # 브라우저에서 파싱이 완료될 때까지 기다려줌. 10초를 기다려도 완료되지 않으면 에러를 떨구고 종료
    browser.get('https://www.youtube.com/channel/UC4m8f3vD6AgN07EBYBLX-ZA/videos')
    time.sleep(1)
    VideoList_html = BeautifulSoup(browser.page_source, 'html.parser')
    VideoList_element0 = VideoList_html.find('div', {'id': 'items', 'class': 'style-scope ytd-grid-renderer'})
    each_VideoList_element= VideoList_element0.find_all('ytd-grid-video-renderer', {
        'class': 'style-scope ytd-grid-renderer'})[0]

def testDB1() :
    con = pymysql.connect(host='127.0.0.1', user='root', password='11whzlqhem')
    cur = con.cursor()
    try : cur.execute('DROP DATABASE test')
    except : None
    cur.execute("CREATE DATABASE test")
    con = pymysql.connect(host='127.0.0.1', user='root', password='11whzlqhem', database='test',charset='utf8')
    cur=con.cursor()
    cur.execute("CREATE TABLE tt (id char(1),pw char(3),pw2 TEXT)")
    cur.execute("INSERT INTO tt VALUES('가','111','aaa')")
    cur.execute("INSERT INTO tt VALUES('나','222','bbb')")
    cur.execute("INSERT INTO tt VALUES('다','333','ccc')")
    con.commit()
    cur.execute("SELECT * FROM tt")
    row = None
    while(1) :
        row = cur.fetchone()
        if row == None :
            break;
        print(row[0]+" "+row[1]+" "+row[2])
    cur.execute("SELECT * FROM tt")
    print(df(cur.fetchall()))
    print()
    cur.execute("SELECT * FROM tt")
    print(cur.fetchall()[1][0])
    cur.execute('DROP DATABASE test')
    con.close()
#testDB1()
# CHARSET utf8mb4