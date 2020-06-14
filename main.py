import data_management as dm
import anls1
import anls2
from tkinter import *
from tkinter import ttk
from tkinter.simpledialog import *

# 전역변수 선언
pw = '11whzlqhem'
ip = '127.0.0.1'


class Objectdata :
    None


# DB ip, password 입력란에서 입력받은 문자열을 전역변수 pw, ip에 대입
def InputPwIp(event):
    global pw, ip
    pw = str_pw.get()
    ip = str_ip.get()

# 검색버튼을 누르면 발동 # 테스트할 목적으로 수정해놓음(중간에 뜬끔없는 1)
def Search(event) :
    try :url = '1'#dm.GetYoutuberUrl(str_search.get())
    except:return
    list_scroll.pack_forget()
    objects = []
    Info4.pack_forget()
    Info5.pack_forget()
    if url != None:
        if 1:#dm.YoutuberCheck(url, pw, ip):  # 해당하는 url에 대응하는 유튜버가 있는 지 확인
            list_scroll.pack()
            for i in range(40):
                objects += [Label(ObjectList, text='영상제목' + str(i))]
                objects[i].pack(side=TOP)
                objects[i].bind('<Button-1>', ClickObject)
            canvas_ObjectList.create_window(0, 0, anchor='nw', window=ObjectList)
            canvas_ObjectList.update_idletasks()
            canvas_ObjectList.configure(scrollregion=canvas_ObjectList.bbox('all'), yscrollcommand=scrollbar_ObjectList)
            scrollbar_ObjectList.pack(fill='y', side='right')
            canvas_ObjectList.pack(fill='both', expand=True, side='left')

        else:
            Info5.pack() # 여기에 추가적인 코드가 있어야 함. 그러나 이 부분은 없어도 프로그램은 돌아감.
    else:
        Info4.pack()


# 클릭된 분석방법 목록의 요소를
def ClickMethod(event) :
    return None

# 클릭된 분석대상 목록의 요소를
def ClickObject(event) :
    print('ClickObject')


# 클릭된 선택된 분석대상 목록의
def ClickSltObject(event) :
    return None

# 조건에 맞으면 분석방법을 활성화 시킨다.
def MethodAct() :
    return None

# 조건에 맞으면 분선결과를 생성한다.
def CreatResult() :
    return None


# 메인 코드 시작!
window=Tk()
window.title('유튜버 정보 분석')
window.geometry('900x450')
window.resizable(width = FALSE, height = FALSE)

# DB ip, password 입력란
frame_PwIp = Frame(window, height=2, bg='gray') # DB ip, password 입력란이 생성될 자리
frame_PwIp.pack(side=TOP, fill=X)
frame_main = Frame(window, bg='Cyan') # DB ip, password 입력란이 생성될 자리를 제외한 나머지 공간
frame_main.pack(expand=True, fill='both')
Frame(frame_main, bg='Cyan', height=3).grid(row=2, column=0)
str_pw= StringVar()
str_ip= StringVar()
Label(frame_PwIp, text =' DB ip :', width=7, bg='gray', fg='white').pack(side=LEFT)
ttk.Entry(frame_PwIp, width=19, textvariable=str_ip).pack(side=LEFT)
Label(frame_PwIp, text=' DB password :', width=12, bg='gray', fg='white').pack(side=LEFT)
ttk.Entry(frame_PwIp, width=19, textvariable=str_pw).pack(side=LEFT)
Label(frame_PwIp, width=0, bg='gray').pack(side=LEFT)
save = Button(frame_PwIp, text='저장', width=5, bg='gray', fg='white')
save.pack(side=LEFT)
save.bind('<Button-1>',InputPwIp) # 저장 버튼 누르면 InputPwIp발동동

# 검색어 입력란
frame_search = Frame(frame_main, bg='Cyan') # 검색어 입력란이 생성될 자리
frame_search.grid(row=1,column=0)
str_search= StringVar()
ttk.Entry(frame_search, width=30, textvariable=str_search).pack(side=LEFT)
search = Button(frame_search, text='검색', width=5, bg='Cyan')
search.pack(side=LEFT)
search.bind('<Button-1>',Search)

# 분석방법 목록
frame_MethodList = Frame(frame_main, bg='Cyan') # 분석방법 목록이 생성될 자리
frame_MethodList.grid(row=3, column=1)

# 분석대상 목록
frame_ObjectList = Frame(frame_main, bg='Cyan') # 분석대상 목록이 생성될 자리
frame_ObjectList.grid(row=3, column=0)
list_scroll = Frame(frame_ObjectList, bg='Cyan')
canvas_ObjectList = Canvas(list_scroll, width=240, height=380)
scrollbar_ObjectList = Scrollbar(list_scroll, orient='vertical',command=canvas_ObjectList.yview)
ObjectList = Frame(canvas_ObjectList)
# https://riptutorial.com/ko/tkinter/example/30942/
# %EC%9C%84%EC%A0%AF-%EA%B7%B8%EB%A3%B9-%EC%8A%A4%ED%81%AC%EB%A1%A4%ED%95%98%EA%B8%B0
Info4 = Label(frame_ObjectList, text='해당 유튜버가 존재하지 않습니다.', bg='Cyan',font=('맑은 고딕',12),fg='blue')
Info5 = Label(frame_ObjectList, text='정보를 준비 중입니다.', bg='Cyan',font=('맑은 고딕',12),fg='blue')
# 선택된 분석대상 목록
frame_SltObjectList = Label(frame_main, bg='Cyan') # 선택된 분석대상 목록이 생성될 자리
frame_SltObjectList.grid(row=1, column=1)

# 분석결과
frame_result = Label(frame_main, bg='Cyan') # 분석결과가 생성될 자리
frame_result.grid(row=1,column=2)

window.mainloop()








