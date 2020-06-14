import data_management as dm
import re
import pandas as pd
from konlpy.tag import Hannanum
from collections import Counter
from wordcloud import WordCloud
import matplotlib as mpl
import matplotlib.pylab as plt
import numpy as np
import random

#단어 빈도수 wordcloud 출력
def comment_freq(url, password) :
    youtuber_csv_data = dm.GetData(url, password)
    if youtuber_csv_data == None:
        print("데이터 없음")
        return None
    video_num = int(input("몇 번 동영상을 분석할까요 ? "))
    youtube_data = dm.GetData(youtuber_csv_data[video_num][0], password)
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
def title_freq(url, password) :
    youtuber_csv_data = dm.GetData(url, password)
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