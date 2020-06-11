import data_management as dm
import anls1
import anls2
import anls3
import anls4


def test() :
    password = input('password:')  # 본인의 root 비밀번호
    youtube_search = input('youtube_search:')
    choice = input('새로 데이터를 수집(예 : 1, 아니요 : 0):') # 1을 선택하면 시간이 좀 걸린다...
    url = dm.GetYoutuberUrl(youtube_search)
    if choice == '1' :
        dm.delDB(password)
        dm.newDB(password)
        dm.CrawlAndSave(url, password)
    dm.PrintTable(password) # db에 있는 table들을 보여줌
    if dm.YoutuberCheck(url, password) : # 해당하는 url에 대응하는 유튜버가 있는 지 확인
        print('데이터 존재')
    else :
        print('데이터 없음') # 혹시 데이터 없다고 뜨면 test()를 다시 실행시키고, 새로 데이터 수집에 0 입력해본다.
    youtuber_csv_data = dm.GetData(url, password)
    dm.PrintData(youtuber_csv_data) #유튜버의 데이터 출력
    video_csv_data = dm.GetData(youtuber_csv_data[0][0], password)
    dm.PrintData(video_csv_data) # 유튜버의 첫번째에 있던 동영상의 출력
    video_csv_data = dm.GetData(youtuber_csv_data[1][0], password)
    dm.PrintData(video_csv_data) # 유튜버의 두번째에 있던 동영상의 출력
    # 원하는 데이터를 db로부터 뽑아오는 법!! >>
    # 원하는 데이터의 의 n행 m열 의 원소 = dm.GetData(원하는 데이터의 url, db의 비밀번호, db의 ip)[n-1][m-1]
    # 참고 >> 유튜버의 데이터의 1열 : url, 2열 : 이름, 3열 : 조회수, 4열 : 좋아요 수, 5열 : 싫어요 수, 6열 : 영상길이, 7열 : 댓글 수, 8열 : 영상이 얼마 전에 올라왔는지(시간)
    # 참고 >> 영상의 데이터의 1열 : 댓글 쓴 사람의 id, 2열 : 댓글에 달린 좋아요 수, 3열 : 댓글(text)

test()