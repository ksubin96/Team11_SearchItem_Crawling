import data_management as dm
import data_analysis as da
from tkinter import *
from tkinter import ttk
from tkinter.simpledialog import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# 전역변수 선언
#con = None
con = dm.ConnectmainDB('11whzlqhem', '127.0.0.1')
SltObjects = []
SltMethod = None
ListObject = []


class AnlsObject :
    name = ''
    url = ''
    select = False
    label = None
    type = 0
    def __init__(self,name = '',url = '') :
        self.name=name
        self.url=url
        if 'user/' in url or 'channel/' in url:
            self.type = 0
        else:
            self.type = 1
    def NewLabel(self, place, color='black') :
        label = Label(place, text=self.name, bg='Yellow', fg=color)
        label.pack(side=TOP, anchor='w')
        label.bind('<Button-1>', self.click)
        return label
    def click(self, event):
        global SltObjects
        if self.select == False :
            if len(SltObjects)==3:
                return
            if SltObjects == [] :
                Info3.pack_forget()
            SltObjects += [self]
            self.label = self.NewLabel(SltObjectList,'Indigo')
            self.select = True
        else :
            SltObjects.remove(self)
            self.label.destroy()
            if SltObjects == [] :
                Info3.pack(side=TOP)
            self.select = False
        # 조건에 맞으면 분석방법을 활성화 시킨다.
        try : Result.destroy()
        except : None
        if len(SltObjects) == 1 and SltObjects[0].type == 0:
            for i in Method :
                if i.name == '영상 별 상관관계' or i.name == '영상 제목 정렬' or i.name == '영상 제목 시각화':
                    i.active()
                    if i.check == True:
                        CreatResult()
                else : i.disable()
        elif len(SltObjects) == 1 and SltObjects[0].type == 1:
            for i in Method:
                if i.name == '댓글 시각화':
                    i.active()
                    if i.check == True:
                        CreatResult()
                else: i.disable()
        else:
            for i in Method:
                i.disable()

class AnlsMethod :
    name=''
    button = None
    act = False
    check = False
    def __init__(self,name) :
        self.name=name
        self.act = False
        self.check = False
    def NewButton(self, place) :
        self.button = Button(place, text=self.name, bg='Yellow', fg='red')
        self.button.pack(side=LEFT, anchor='n')
        self.button.bind('<Button-1>', self.click)
    def click(self, event):
        global SltMethod
        try : Result.destroy()
        except : None
        if self.check == False:
            for i in Method:
                i.button.configure(text=i.name)
                i.check = False
            self.button.configure(text='✓ ' + self.name)
            self.check = True
            SltMethod = self
            if self.act==True:
                CreatResult()
        else:
            self.button.configure(text=self.name)
            self.check = False
            SltMethod = None
    def active(self) :
        self.button.configure(fg='green')
        self.act = True
    def disable(self):
        self.button.configure(fg='red')
        self.act = False
    def anls(self,url):
        global Result
        Result = Frame(frame_Result, width=0, height=0, bg='Orange')
        Result.pack()
        if self.name == '영상 별 상관관계':
            da.videos_corr(dm.GetData(url, con))

            Label(Result, text='영상 별 상관관계', width=0, height=0, bg='Yellow').pack() # 임시 결과물
        elif self.name == '영상 제목 정렬':
            da.title_sort(dm.GetData(url, con))

            Label(Result, text='영상 제목 정렬', width=0, height=0, bg='Yellow').pack() # 임시 결과물
        elif self.name == '댓글 시각화':
            da.comment_freq(dm.GetData(url, con))

            Label(Result, text='댓글 시각화', width=0, height=0, bg='Yellow').pack() # 임시 결과물
        elif self.name == '영상 제목 시각화':
            da.title_freq(dm.GetData(url, con))

            Label(Result, text='영상 제목 시각화', width=0, height=0, bg='Yellow').pack() # 임시 결과물

def InputPwIp(event):
    global con
    con = dm.ConnectmainDB(str_pw.get(), str_ip.get())
    if con == None :
        Info2.pack_forget()
        Info1.pack(side=LEFT)
    else :
        Info1.pack_forget()
        Info2.pack(side=LEFT)

# 검색버튼을 누르면 발동
def Search(event) :
    if con == None : return
    url = dm.GetYoutuberUrl(str_search.get(), con)
    list_scroll.pack_forget()
    Info4.pack_forget()
    Info5.pack_forget()
    if url != None:
        youtuber_name = dm.GetYoutuberName(url, con)
        if youtuber_name != None : # 해당하는 url에 대응하는 유튜버가 있는 지 확인
            list_scroll.pack()
            global ObjectList, ListObject
            try : ObjectList.destroy()
            except : None
            ListObject.clear()
            ObjectList = Frame(canvas_ObjectList, bg='Yellow')
            temp=AnlsObject('[Y] '+youtuber_name, url)
            temp.NewLabel(ObjectList)
            ListObject+=[temp]
            data = dm.GetData(url, con)
            i=0
            while True:
                try :
                    temp=AnlsObject(data[i][1], data[i][0])
                    temp.NewLabel(ObjectList)
                    ListObject+=[temp]
                except : break
                i+=1
            canvas_ObjectList.create_window(0, 0, anchor='nw', window=ObjectList)
            canvas_ObjectList.update_idletasks()
            canvas_ObjectList.configure(scrollregion=canvas_ObjectList.bbox('all'), yscrollcommand=scrollbar_ObjectList)
            scrollbar_ObjectList.pack(fill=Y, side='right')
            canvas_ObjectList.pack(fill='both', expand=True, side='left')
            Info3.pack(side=TOP)
        else:
            Info5.pack()
            Info3.pack_forget()
    else:
        Info4.pack()
        Info3.pack_forget()


# 조건에 맞으면 분석결과를 생성한다.
def CreatResult() :
    SltMethod.anls(SltObjects[0].url)


# 메인 코드 시작!
Method=[AnlsMethod('영상 별 상관관계'), AnlsMethod('영상 제목 정렬'), AnlsMethod('댓글 시각화'), AnlsMethod('영상 제목 시각화')]


# 윈도우 창
window=Tk()
window.title('유튜버 정보 분석')
window.geometry('900x500')
window.resizable(width = FALSE, height = FALSE)

# DB ip, password 입력란
frame_PwIp = Frame(window, height=2, bg='gray') # DB ip, password 입력란이 생성될 자리
frame_PwIp.pack(side=TOP, fill=X)
str_pw= StringVar()
str_ip= StringVar()
Label(frame_PwIp, text =' DB ip :', width=7, bg='gray', fg='white').pack(side=LEFT)
ttk.Entry(frame_PwIp, width=19, textvariable=str_ip).pack(side=LEFT)
Label(frame_PwIp, text=' DB password :', width=12, bg='gray', fg='white').pack(side=LEFT)
ttk.Entry(frame_PwIp, width=19, textvariable=str_pw).pack(side=LEFT)
Label(frame_PwIp, width=0, bg='gray').pack(side=LEFT)
save = Button(frame_PwIp, text='저장', width=5, bg='gray', fg='white')
save.pack(side=LEFT)
Info1 = Label(frame_PwIp, text='  No connection', width=12, bg='gray', fg='#FF5555')
Info1.pack(side=LEFT)
Info2 = Label(frame_PwIp, text='  Connected!   ', width=12, bg='gray', fg='#00FF00')
save.bind('<Button-1>',InputPwIp) # 저장 버튼 누르면 InputPwIp발동

# DB ip, password 입력란을 제외한 나머지 위젯들의 자리배치 설정
frame_main = Frame(window, bg='Orange')
frame_main.pack(expand=True, fill='both')
frame=[]
for i in range(5) :
    frame += [Frame(frame_main, width=8, bg='Orange')]
    frame[i].pack(side=LEFT, fill=Y)

# 검색어 입력란
frame_search = Frame(frame[1], bg='Orange') # 검색어 입력란이 생성될 자리
frame_search.pack(side=TOP)
str_search= StringVar()
ttk.Entry(frame_search, width=40, textvariable=str_search).pack(side=LEFT)
search = Button(frame_search, text='검색', width=5, bg='Orange')
search.pack(side=LEFT)
search.bind('<Button-1>',Search)

# 선택된 분석대상 목록
Frame(frame[1], height=3, bg='Orange').pack(side=TOP) # 여백
frame_SltObjectList = Frame(frame[1], bg='Orange') # 선택된 분석대상 목록이 생성될 자리
frame_SltObjectList.pack(side=TOP)
SltObjectList = Frame(frame_SltObjectList, width=0, height=0, bg='Yellow')
SltObjectList.pack()
Info3=Label(SltObjectList, text='분석대상을 선택해주세요.', bg='Yellow',fg='blue')

# 분석대상 목록
Frame(frame[1], height=8, bg='Orange').pack(side=TOP) # 여백
frame_ObjectList = Frame(frame[1], width=390, bg='Orange') # 분석대상 목록이 생성될 자리
frame_ObjectList.pack(side=TOP)
list_scroll = Frame(frame_ObjectList, bg='Orange')
canvas_ObjectList = Canvas(list_scroll, width=370, height=364)
scrollbar_ObjectList = Scrollbar(list_scroll, orient='vertical',command=canvas_ObjectList.yview)
Info4 = Label(frame_ObjectList, width=43, text='해당 유튜버가 존재하지 않습니다.', bg='Yellow',font=('맑은 고딕',12),fg='blue')
Info5 = Label(frame_ObjectList, width=43, text='찾으시는 정보가 없습니다.', bg='Yellow',font=('맑은 고딕',12),fg='blue')

# 분석방법 목록
frame_MethodList = Frame(frame[3], bg='Orange') # 분석방법 목록이 생성될 자리
frame_MethodList.pack(side=TOP)
MethodList = Frame(frame_MethodList, width=0, height=0, bg='Orange')
MethodList.pack()
for i in Method:
    i.NewButton(MethodList)
    Frame(MethodList, width=5, bg='Orange').pack(side=LEFT, anchor='n')  # 여백


# 분석결과
Frame(frame[3], height=8, bg='Orange').pack(side=TOP) # 여백
frame_Result = Frame(frame[3], bg='Orange') # 분석결과가 생성될 자리
frame_Result.pack(side=TOP)

window.mainloop()








