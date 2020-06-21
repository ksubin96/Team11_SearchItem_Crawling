#하단의 주석문에서 시키는 대로 해야 프로그램이 동작합니다.

# 관리자 명령프롬프트에 다음 명령어를 전부 입력
# curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
# python get-pip.py
# pip install seaborn
# pip install konlpy
# pip install matplotlib
# pip install wordcloud

import re
import pandas as pd
import seaborn as sns
from konlpy.tag import Kkma
from konlpy.tag import Mecab
from konlpy.tag import Twitter

from konlpy.tag import Hannanum
from collections import Counter
from wordcloud import WordCloud
import matplotlib as mpl
import matplotlib.pylab as plt
import numpy as np
import random

from tkinter import *

def videos_corr(youtuber_csv_data):
    # youtuber_csv_data = dm.GetData(url, con) << main.py에서 구현
    youtuber_data = list(youtuber_csv_data)
    title = []
    view = []
    like = []
    unlike = []
    videolength = []
    comment = []
    date = []

    for i in range(len(youtuber_data)):
        title.append(youtuber_data[i][1])
        view.append(youtuber_data[i][2])
        like.append(youtuber_data[i][3])
        unlike.append(youtuber_data[i][4])
        videolength.append(youtuber_data[i][5])
        comment.append(youtuber_data[i][6])
        date.append(youtuber_data[i][7])

    #print(youtuber_data[0])  # 0행 출력

    video_info = pd.DataFrame({'title': [],
                               'view': [],
                               'like': [],
                               'unlike': [],
                               'comment': [],
                               'date': []})

    insert_data = pd.DataFrame({'title': title,
                                'view': view,
                                'like': like,
                                'unlike': unlike,
                                'comment': comment,
                                'date': date})

    video_info = video_info.append(insert_data)
    video_info.index = range(len(video_info))

    like_ls = []
    view_ls = []
    unlike_ls = []
    comment_ls = []
    date_ls = []

    for i in range(len(video_info)):
        if '천' in video_info['like'].iloc[i]:
            a = ''.join(re.findall('[0-9]', video_info['like'].iloc[i]))
            if len(a) == 2:
                b = a + '00'
            else:
                b = a + '000'
        elif '만' in video_info['like'].iloc[i]:
            b = ''.join(re.findall('[0-9]', video_info['like'].iloc[i])) + '000'
        else:
            b = video_info['like'].iloc[i]
        like_ls.append(b)

        if '천' in video_info['unlike'].iloc[i]:
            aa = ''.join(re.findall('[0-9]', video_info['unlike'].iloc[i]))
            if len(a) == 2:
                bb = aa + '00'
            else:
                bb = aa + '000'
        elif '만' in video_info['unlike'].iloc[i]:
            bb = ''.join(re.findall('[0-9]', video_info['unlike'].iloc[i])) + '000'
        else:
            bb = video_info['unlike'].iloc[i]
        unlike_ls.append(bb)

        view0 = ''.join(re.findall('[0-9]', video_info['view'].iloc[i]))
        view_ls.append(view0)

        comment0 = ''.join(re.findall('[0-9]', video_info['comment'].iloc[i]))
        comment_ls.append(comment0)

        date0 = ''.join(re.findall('[.0-9]', video_info['date'].iloc[i]))
        date_ls.append(date0[:-1])

    video_info['like'] = like_ls
    video_info['view'] = view_ls
    video_info['comment'] = comment_ls
    video_info['date'] = date_ls
    video_info['unlike'] = unlike_ls

    video_info2 = video_info[video_info['like'] != '좋아요']
    video_info2 = video_info2[video_info2['comment'] != '']
    video_info2['view'] = video_info2['view'].astype('float64')
    video_info2['like'] = video_info2['like'].astype('float64')
    video_info2['unlike'] = video_info2['unlike'].astype('float64')
    video_info2['comment'] = video_info2['comment'].astype('float64')

    video_info2[['view', 'like', 'comment']].corr()
    print(video_info2[['view', 'like', 'comment']].corr())  # 상관분석 표... 조회수 좋아요 댓글의 상관관계를 보여준다
    # 영상 길이는 실수 형태로 변경이 되지 않아 4x4로 표현 불가 13:24 이런 식이라서..
    heat = video_info2[['view', 'like', 'comment']].corr()
    sns.heatmap(heat, annot=True)  # 파이참으로는 안보입니다

def title_sort(youtuber_csv_data):
    # youtuber_csv_data = dm.GetData(url, con) << main.py에서 구현
    youtuber_data = list(youtuber_csv_data)
    title = []
    view = []
    like = []
    unlike = []
    videolength = []
    comment = []
    date = []

    for i in range(len(youtuber_data)):
        title.append(youtuber_data[i][1])
        view.append(youtuber_data[i][2])
        like.append(youtuber_data[i][3])
        unlike.append(youtuber_data[i][4])
        videolength.append(youtuber_data[i][5])
        comment.append(youtuber_data[i][6])
        date.append(youtuber_data[i][7])

    video_info = pd.DataFrame({'title': [],
                               'view': [],
                               'like': [],
                               'unlike': [],
                               'comment': [],
                               'date': []})

    insert_data = pd.DataFrame({'title': title,
                                'view': view,
                                'like': like,
                                'unlike': unlike,
                                'comment': comment,
                                'date': date})

    video_info = video_info.append(insert_data)
    video_info.index = range(len(video_info))

    like_ls = []
    view_ls = []
    unlike_ls = []
    comment_ls = []
    date_ls = []

    video_info['like'] = like_ls
    video_info['view'] = view_ls
    video_info['comment'] = comment_ls
    video_info['date'] = date_ls
    video_info['unlike'] = unlike_ls


    # 이모티콘 제거
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               "]+", flags=re.UNICODE)

    # 분석에 어긋나는 불용어구 제외 (특수문자, 의성어)
    han = re.compile(r'[ㄱ-ㅎㅏ-ㅣ!?~,".\n\r#\ufeff\u200d]')

    title_ls = []
    for i in range(len(video_info)):
        a = re.sub(emoji_pattern, '', video_info['title'].iloc[i])

        b = re.sub(han, '', a)

        title_ls.append(b)

    video_info['title'] = title_ls

    twitter = Twitter()
    #kkma = Kkma()

    # 영상제목 토큰화 하는 과정
    noun_final = []
    for text in range(len(video_info)):
        noun0 = twitter.pos(video_info['title'].iloc[text])
        noun = []
        for i, j in noun0:
            if j == 'NNG':
                if i == '뽀' or i == '블리':
                    pass
                else:
                    noun.append(i)
        noun_final.append(noun)
    video_info['token'] = noun_final

    token_df = pd.DataFrame({'token': []})
    for i in range(len(video_info)):
        insert_data = pd.DataFrame({'token': video_info['token2'].iloc[i]})
        insert_data['view'] = video_info['view'].iloc[i]

        token_df = token_df.append(insert_data)

    token_df['view'] = token_df['view'].astype('float64')
    token_df2 = token_df.groupby('token')['view'].sum().reset_index()
    token_df2['count'] = token_df.groupby(['token']).count().reset_index()['view'].tolist()

    view_count = []
    for i in range(len(token_df2)):
        a = token_df2['view'].iloc[i] / token_df2['count'].iloc[i]
        view_count.append(a)
    token_df2['view_count'] = view_count

    token_df2.sort_values(by='count', ascending=False).head(15)
    token_df2.sort_values(by='view', ascending=False).head(20)
    token_df2.sort_values(by='view').head(20)
    token_df2.sort_values(by='view_count', ascending=False).head(15)
    token_df2.sort_values(by='view_count').head(15)




#단어 빈도수 wordcloud 출력
def comment_freq(youtube_data) :
    # youtuber_csv_data = dm.GetData(url, con)
    # if youtuber_csv_data == None:
    #     print("데이터 없음")
    #     return None
    # video_num = int(input("몇 번 동영상을 분석할까요 ? "))
    # youtube_data = dm.GetData(youtuber_csv_data[video_num][0], password) >> main.py에서 구현
    if youtube_data == None:
        print("데이터 없음")
        return None
    comment = []
    for i in range(len(youtube_data)):
        comment.append(youtube_data[i][2])

    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               "]+", flags=re.UNICODE)
    han = re.compile(r'[ㄱ-ㅎㅏ-ㅣ!?~,".\n\r#\ufeff\u200d]')

    comment_noemot = []
    for i in comment:
        tokens = re.sub(emoji_pattern, "", i)
        tokens = re.sub(han, "", tokens)
        comment_noemot.append(tokens)


    nouns = []
    h = Hannanum()

    for i in comment_noemot:
        n = h.nouns(i)
        nouns.append(n)

    noun_list = []
    for i in range(len(nouns)):
        for j in range(len(nouns[i])):
            noun_list.append(nouns[i][j])

    counts = Counter(noun_list)
    tags = counts.most_common(30)

    wc = WordCloud(font_path='C:\\Windows\\Fonts\\gulim.ttc', background_color='black', width=800,
                   height=600)

    cloud = wc.generate_from_frequencies(dict(tags))
    plt.figure(figsize=(10, 8))
    plt.axis('off')
    plt.imshow(cloud)
    plt.show()

#제목 빈도수 wordcloud 출력
def title_freq(youtuber_csv_data) :
    # youtuber_csv_data = dm.GetData(url, con) << main.py에서 구현
    if youtuber_csv_data == None:
        print("데이터 없음")
        return None
    title = []
    for i in range(len(youtuber_csv_data)):
        title.append(youtuber_csv_data[i][1])

    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               "]+", flags=re.UNICODE)
    han = re.compile(r'[ㄱ-ㅎㅏ-ㅣ!?~,".\n\r#\ufeff\u200d]')
    title_noemot = []
    for i in title:
        tokens = re.sub(emoji_pattern, "", i)
        tokens = re.sub(han, "", tokens)
        title_noemot.append(tokens)

    nouns = []
    h = Hannanum()

    for i in title_noemot:
        n = h.nouns(i)
        nouns.append(n)

    noun_list = []
    for i in range(len(nouns)):
        for j in range(len(nouns[i])):
            noun_list.append(nouns[i][j])

    counts = Counter(noun_list)
    tags = counts.most_common(30)

    wc = WordCloud(font_path='C:\\Windows\\Fonts\\gulim.ttc', background_color='white', width=800,
                   height=600)

    cloud = wc.generate_from_frequencies(dict(tags))
    plt.figure(figsize=(10, 8))
    plt.axis('off')
    plt.imshow(cloud)
    plt.show()