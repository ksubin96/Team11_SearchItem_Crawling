import data_management as dm
import anls1
import anls2
import anls3
import anls4

def test() :
    password = input('password:')  # 본인의 root 비밀번호
    youtube_search = input('youtube_search:')
    dm.newDB(password)
    name, url = dm.GetYoutuberNameUrl(youtube_search)
    dm.CrawlAndSave(name, url, password)
    youtuber_csv_data = dm.GetData(url, password)  # 유튜버의 데이터
    dm.PrintData(youtuber_csv_data)
    firstvideo_csv_data = dm.GetData(youtuber_csv_data[0][0], password)  # 유튜버의 첫번째에 있던 동영상의 데이터
    dm.PrintData(firstvideo_csv_data)
    dm.newDB(password)

def mytest() :
    dm.newDB('11whzlqhem')
    name, url = dm.GetYoutuberNameUrl('어펄슨')
    dm.CrawlAndSave(name, url, '11whzlqhem')
    youtuber_csv_data = dm.GetData(url, '11whzlqhem') #유튜버의 데이터
    dm.PrintData(youtuber_csv_data)
    firstvideo_csv_data = dm.GetData(youtuber_csv_data[0][0], '11whzlqhem') #유튜버의 첫번째에 있던 동영상의 데이터
    dm.PrintData(firstvideo_csv_data)
    dm.newDB('11whzlqhem')

test()

