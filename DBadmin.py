#  조(팀명) : 11조 키보드
# 작성자 : 박민우
# 범위 : 해당 파일 전체

import data_management as dm

con=None
num = 0
while True :
    id = input('id : ')
    pw = input('password : ')  # 본인의 root 비밀번호
    con = dm.ConnectmainDB('127.0.0.1', pw, id)
    if con != None :
        break
    else :
        con = dm.ConnectDB(pw, id)
        if con != None :
            try:
                num = int(input('\nCreat newDB? (yes:1) : '))
                if num == 1 :
                    dm.newDB(pw)
                    con = dm.ConnectmainDB('127.0.0.1', pw, id)
                    break
            except:
                None
        else :
            print('\nwrong password\n')

while True:
    print('\n===== 메뉴 =====')
    print('1. 데이터 수집')
    print('2. 유튜버 체크')
    print('3. 종료')
    print('4. DB 제거 후 종료')
    try :num=int(input('수행할 항목 번호 입력 :'))
    except :
        print('\n잘못된 입력')
        continue
    if num == 1 :
        youtube_search = input('\n유튜브 검색어 : ')
        url = dm.GetYoutuberUrl(youtube_search, con)
        dm.CrawlAndSave(url, con)
    elif num == 2 :
        youtube_search = input('\n유튜브 검색어 : ')
        url = dm.GetYoutuberUrl(youtube_search, con)
        check = dm.GetYoutuberName(url, con)  # 해당하는 url에 대응하는 유튜버가 있는 지 확인
        if check == None:
            print('\n데이터 없음')
        else:
            print('\n"'+check+'" 데이터 있음')
    elif num == 3 :
        break
    elif num == 4 :
        try :
            num = int(input('Delete DB? (yes:1234) : '))
            if num == 1234:
                dm.delDB(pw)
                break
        except: None
    else :
        print('\n잘못된 입력')
