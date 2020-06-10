def anls() : #미완성
import pandas as pd
import re
import seaborn as sns #데이터 시각화 위한 seaaborn
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
import matplotlib

#한글 형태소 분석기인 konlpy사용
#이때 konlpy에는 hannanum, kommoran, kkma, twitter이 있는데 해당 분석에서는 kkma사용
from konlpy.tag import Kkma
from konlpy.tag import Mecab
from konlpy.tag import Twitter
#apply lambda사용
from konlpy.tag import Komoran

youtuber_data = pd.read_cs('xxx.csv',encoding = 'utf-8') # 임의로 xxx로 정해둠
youtuber_data.head() # 상위5개의 데이터만 출력된다

view_ls = []
like_ls = []
unlike_ls = []
comment_ls = []
date_ls = []
videotime_ls = []

# a는 첫번째 자리 like
for i in range(len(youtuber_data)):# iloc은 loc 처럼 index 이름, 열 이름을 사용하는 것이 아니라 몇 번째 행인지, 몇 번째 열인지 지정을 하여 숫자로 나타내주어야함. 기존의 파이썬 범위 지정과 마찬가지로 마지막 숫자의 행과 열은 추출 X
    if '천' in youtuber_data['like'].iloc[i]: #데이터프레임명.iloc[시작 행:끝 행,시작 열: 끝 열]
        a = ''.join(re.findall('[0-9]', youtuber_data['like'].iloc[i])) #한자리 수 이상을 찾아라 0~9
        if len(a) == 2:
            b = a + '00'
        else:
            b = a + '000'
    elif '만' in youtuber_data['like'].iloc[i]:
        b = ''.join(re.findall('[0-9]', youtuber_data['like'].iloc[i])) + '000' # 한자리 수 이상을 찾아라
    else:
        b = youtuber_data['like'].iloc[i]
    like_ls.append(b)

## aa는 첫번째 자리 unlike
    if '천' in youtuber_data['unlike'].iloc[i]:
        aa = ''.join(re.findall('[0-9]', youtuber_data['unlike'].iloc[i])) #한자리 수 이상을 찾아라
        if len(a) == 2:
            bb = aa + '00'
        else:
            bb = aa + '000'
    elif '만' in youtuber_data['unlike'].iloc[i]:
        bb = ''.join(re.findall('[0-9]', youtuber_data['unlike'].iloc[i])) + '000' #한자리 수 이상을 찾아라
    else:
        bb = youtuber_data['unlike'].iloc[i]
    unlike_ls.append(bb)

    view0 = ''.join(re.findall('[0-9]', youtuber_data['view'].iloc[i]))
    view_ls.append(view0)

    comment0 = ''.join(re.findall('[0-9]', youtuber_data['comment'].iloc[i]))
    comment_ls.append(comment0)

    date0 = ''.join(re.findall('[.0-9]', youtuber_data['date'].iloc[i]))
    date_ls.append(date0[:-1])

    videotime0 = ''.join(re.findall('[.0-9]', youtuber_data['videotime'].iloc[i]))
    videotime_ls.append(videotime0[:-1])

youtuber_data['like'] = like_ls
youtuber_data['unlike'] = unlike_ls
youtuber_data['view'] = view_ls
youtuber_data['comment'] = comment_ls
youtuber_data['date'] = date_ls
youtuber_data['videotime'] = videotime_ls

#조회수 평균 구하고, 평균 조회수 까지 걸리는 시간 구함 그리고 그것을 걸린 날짜로 나누면 일자별 조회수 증가량 알 수 있음

youtuber_data['view'] = youtuber_data['view'].astype('float64') #실수형으로 형변환
youtuber_data['view'].mean() # 평균을 구함    xxx.xxxxxx 이런식으로 나올것

#상관분석
youtuber_data2 = youtuber_data[youtuber_data['like'] != '좋아요']
youtuber_data2 = youtuber_data2[youtuber_data2['comment']!='']

youtuber_data2['view'] = youtuber_data2['view'].astype('float64')
youtuber_data2['like'] = youtuber_data2['like'].astype('float64')
youtuber_data2['unlike'] = youtuber_data2['unlike'].astype('float64')
youtuber_data2['comment'] = youtuber_data2['comment'].astype('float64')

#corr() 상관분석
youtuber_data2[['view','like','comment']].corr()    #	     view	      like	    comment
                                                    #view	1.000000	0.813429	0.341466
                                                    #like	0.813429	1.000000	0.615822
                                                    #comment	0.341466	0.615822	1.000000

#sns.heatmap(heat,annot=True) heat install이 안됨  나중에 다시.
#이모티콘 제거
emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)

#분석에 어긋나는 불용어구 제외 (특수문자, 의성어)
han = re.compile(r'[ㄱ-ㅎㅏ-ㅣ!?~,".\n\r#\ufeff\u200d]')

#제목
title_ls = []
for i in range(len(youtuber_data)):
    a = re.sub(emoji_pattern, '', youtuber_data['title'].iloc[i])

    b = re.sub(han, '', a)

    title_ls.append(b)

youtuber_data['title'] = title_ls

twitter = Twitter()
kkma = Kkma()

#영상제목 토큰화 하는 과정
noun_final = []
for text in range(len(youtuber_data)):
    noun0=kkma.pos(youtuber_data['title'].iloc[text])
    noun=[]
    for i,j in noun0:
        if j=='NNG': #NNG는 일반 명사. VA는 형용사
           # if i == '테스터' or i == '훈': #이 부분 수정
                pass
            else:
                noun.append(i)
    noun_final.append(noun)
youtuber_data['token'] = noun_final

#토큰화 작업을 거친 뒤에 단어가 하나인 것은 제외하기
noun_ls = []
for i in range(len(youtuber_data)):
    noun_ls0=[]
    for j in range(len(youtuber_data['token'].iloc[i])):
        if len(youtuber_data['token'].iloc[i][j]) == 1:
            pass
        else:
            noun_ls0.append(youtuber_data['token'].iloc[i][j])
    noun_ls.append(list(set(noun_ls0))) #중복제거

youtuber_data['token2'] = noun_ls

youtuber_data


# 각 키워드를 기준으로 조회수 정렬하기
token_df = pd.DataFrame({'token': []})
for i in range(len(youtuber_data)):
    insert_data = pd.DataFrame({'token': youtuber_data['token2'].iloc[i]})
    insert_data['view'] = youtuber_data['view'].iloc[i]

    token_df = token_df.append(insert_data)

token_df2 = token_df.groupby('token')['view'].sum().reset_index()  # 키워드별 조회수 합
token_df2['count'] = token_df.groupby(['token']).count().reset_index()['view'].tolist()  # 각 키워드의 갯수
# 키워드별 조회수의합 / 갯수 - 동등하게 만들어야 하기 때문에
view_count = []
for i in range(len(token_df2)):
    a = token_df2['view'].iloc[i] / token_df2['count'].iloc[i]
    view_count.append(a)
token_df2['view_count'] = view_count

#단어별 조회수
token_df = pd.DataFrame({'token': []})
for i in range(len(youtuber_data)):
    insert_data = pd.DataFrame({'token': youtuber_data['token2'].iloc[i]})
    insert_data['view'] = youtuber_data['view'].iloc[i]

    token_df = token_df.append(insert_data)

token_df['view'] = token_df['view'].astype('float64')
token_df2 = token_df.groupby('token')['view'].sum().reset_index()
token_df2['count'] = token_df.groupby(['token']).count().reset_index()['view'].tolist()
view_count = []
for i in range(len(token_df2)):
    a = token_df2['view'].iloc[i]/token_df2['count'].iloc[i]
    view_count.append(a)
token_df2['view_count'] = view_count
token_df2.sort_values(by='count',ascending=False).head(15)
token_df2.sort_values(by='view',ascending=False).head(20)
token_df2.sort_values(by='view').head(20)
token_df2.sort_values(by='view_count',ascending=False).head(15)
token_df2.sort_values(by='view_count').head(15)

#키워드별 좋아요
token_df = pd.DataFrame({'token': []})
for i in range(len(youtuber_data)):
    insert_data = pd.DataFrame({'token': youtuber_data['token2'].iloc[i]})
    insert_data['like'] = youtuber_data['like'].iloc[i]

    token_df = token_df.append(insert_data)

token_df = token_df[token_df['like']!='좋아요']
token_df['like'] = token_df['like'].astype('float64')
token_df2 = token_df.groupby('token')['like'].sum().reset_index()
token_df2['count'] = token_df.groupby(['token']).count().reset_index()['like'].tolist()
view_count = []
for i in range(len(token_df2)):
    a = token_df2['like'].iloc[i]/token_df2['count'].iloc[i]
    view_count.append(a)
token_df2['like_count'] = view_count

token_df2.sort_values(by='like_count',ascending=False).head(15)
token_df2.sort_values(by='like_count').head(15)
