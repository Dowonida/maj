import random
import mjhr
import time
import tkinter as tk
import threading
###변수 설명
###g.winner : 화료한 사람의 순서 (즉 a.order 등)

Player=[]
ButtonList=[[],[],[],[],[]]


wait=0#wait=0->뽑기->wait=1->버리기->wait2->울기대기
#wait=3 : 승자가 나오고 점수판
#wait=4 : 유국됨 
lock=threading.Lock()
바람=[41,42,44,45]


Image={}
root=tk.Tk()
cvs=tk.Canvas(width=1100,height=800,bg="#00394E")
cvs.pack()
cvs.create_rectangle(410,250,690,530,fill="green",width=0)
cx,cy=0,0

#--------------------------------------------------------------------------------클라 부분---------------------------------------------------
for i in mjhr.FList:
    Image[i]=tk.PhotoImage(file=str(i)+".gif")
    Image[100+i]=tk.PhotoImage(file=str(i)+"하"+".gif")
    Image[200+i]=tk.PhotoImage(file=str(i)+"대"+".gif")
    Image[300+i]=tk.PhotoImage(file=str(i)+"상"+".gif")
Image[0]=tk.PhotoImage(file="뒤.gif")
Image["주모"]=tk.PhotoImage(file="주모.png")
Image["대출"]=tk.PhotoImage(file="대출.png")

def draw():#버림패, 손패, 공개패, 도라표시패, 쯔모버튼, 쯔모시 역,점수 표시
    #버림패,손패는 누군가가 버릴때 변함-wait=2, 공개패,도라표시패는 울 때 변함-wait=1, 쯔모버튼,쯔모시 점수표시는 뽑기시 변함-wait=1
    #이를 단계별로 나누어서 표시해야할듯.. 
    global cx,cy
    cvs.delete("PP")

    try:
        for i in ButtonList:
            i.destroy()
    except:
        pass

    for i in range(len(Player[a.order].패[0])):#손패
        cvs.create_image(40+35*i,750,image=Image[Player[a.order].패[0][i]],tag="PP")
    for i in range(4):  #도라표시패 
        if i<g.도라수:
            cvs.create_image(20+35*i,30,image=Image[g.왕패[9-2*i]],tag="PP")
        else:
            cvs.create_image(20+35*i,30,image=Image[0],tag="PP")
    if a.후리텐:
        cvs.create_text(1000,550,text="후리텐",font=("굴림체",25),fill="red",tag="PP")
        
    if wait==1:
        cvs.delete("wait1")
        for i in range(1,len(Player[a.order].패)):#공개패
            for j in range(len(Player[a.order].패[i])):
                cvs.create_image(1200-35*j-200*i,750,image=Image[Player[a.order].패[i][j]],tag="wait1")
        if a.역확인():#쯔모화료가능시 판 수와 역을 보여줌 
            cvs.create_text(400,680,text=str(a.역확인()[0])+str(a.역확인()[1]),font=("굴림체",20),fill="white",tag="PP")
        for i in a.버림패추천: #버림패추천 
            cvs.create_polygon(40+35*i,720,35+35*i,710,45+35*i,710,fill="yellow",tag="PP")

        if a.order==g.order:
            if a.깡판정():
                for i in range(len(a.깡판정())):
                    btn=tk.Button(text="깡",font=("굴림",15))
                    btn.bind("<Button-1>",lambda event, var=i:a.깡실행(var))
                    ButtonList[i]=btn
                    btn.place(x=1000-150*i,y=680)
                    for j in range(len(a.깡판정()[i])):
                        cvs.create_image(1080-35*j-150*i,650,image=Image[a.깡판정()[i][j]],tag="PP")
    #    try:#버림패에 대한 대기패를 보여줄 때, 쯔모한 패를 버리면 오류가 생긴다.
            #아마도 버리는 순간 패의 개수가 줄어드는데
            #마우스 위치인 cx값은 여전히 같은 곳을 가르키므로 list길이가 안맞아서 생기는 오류인듯하다.
            #수정방법이 생각나면 수정하고 try를 지우자 
        if cx-1 in a.버림패추천 and cy: #화료패 보여주기 
            b=[]
            for i in a.패:
                b.append(i.copy())
            b[0].remove(b[0][cx-1])
            cvs.create_rectangle(-25+cx*35,610,-5+cx*35+30*len(mjhr.텐파이확인(b,a.멘젠,a.론,바람[g.풍],바람[a.order],len(g.deck),g.영상)),700,tag="PP",fill="black")

            L=len(mjhr.텐파이확인(b,a.멘젠,1,바람[g.풍],바람[a.order],len(g.deck),g.영상))
            for j in range(L):
                cvs.create_image(35*cx+30*j,650,image=Image[mjhr.텐파이확인(b,a.멘젠,1,바람[g.풍],바람[a.order],len(g.deck),g.영상)[j][0]],tag="PP")
                
                if mjhr.텐파이확인(b,a.멘젠,1,바람[g.풍],바람[a.order],len(g.deck),g.영상)[j][1]:
                    cvs.create_text(35*cx+30*j,690,text=str(mjhr.텐파이확인(b,a.멘젠,1,바람[g.풍],바람[a.order],len(g.deck),g.영상)[j][1][0]),fill="white",tag="PP")
                else:
                    cvs.create_text(35*cx+30*j,690,text="역 없음",fill="white",tag="PP")


    #------------wait==1
    elif wait==2:
        cvs.delete("wait2")
        for i in range(len(Player[a.order].버림패)):#버림패
            if i==a.리치턴:
                cvs.create_image(425+35*(i%8),560+60*(i//8),image=Image[Player[a.order].버림패[i]+300],tag="wait2")
            else:
                cvs.create_image(425+35*(i%8),560+60*(i//8),image=Image[Player[a.order].버림패[i]],tag="wait2")
 
        if Player[(a.order+1)%4].버림패:
            for i in range(len(Player[(a.order+1)%4].버림패)):#하가버림패
                if i==Player[(a.order+1)%4].리치턴:
                    cvs.create_image(720+60*(i//8),515-35*(i%8),image=Image[Player[(a.order+1)%4].버림패[i]],tag="wait2")
                else:
                    cvs.create_image(720+60*(i//8),515-35*(i%8),image=Image[Player[(a.order+1)%4].버림패[i]+100],tag="wait2")
        if Player[(a.order+2)%4].버림패:
            for i in range(len(Player[(a.order+2)%4].버림패)):#대가버림패
                if i==Player[(a.order+2)%4].리치턴:
                    cvs.create_image(670-35*(i%8),220-60*(i//8),image=Image[Player[(a.order+2)%4].버림패[i]+100],tag="wait2")
                else:
                    cvs.create_image(670-35*(i%8),220-60*(i//8),image=Image[Player[(a.order+2)%4].버림패[i]+200],tag="wait2")
        if Player[(a.order+3)%4].버림패:
            for i in range(len(Player[(a.order+3)%4].버림패)):#상가버림패
                if i==Player[(a.order+3)%4].리치턴:
                    cvs.create_image(380-60*(i//8),265+35*(i%8),image=Image[Player[(a.order+3)%4].버림패[i]+200],tag="wait2")
                else:
                    cvs.create_image(380-60*(i//8),265+35*(i%8),image=Image[Player[(a.order+3)%4].버림패[i]+300],tag="wait2")
        
        if a.order!=g.order:
            if a.울기판정():
                for i in range(len(a.울기판정())):
                    btn=tk.Button(text="선택",font=("굴림",15))
                    btn.bind("<Button-1>",lambda event, var=i:a.울기실행(var))
                    ButtonList[i]=btn
                    btn.place(x=1000-150*i,y=680)
                    if len(a.울기판정()[i])==4:
                        btn["text"]="깡"
                    elif a.울기판정()[i][0]!=a.울기판정()[i][1]:
                        btn["text"]="치"
                    else:
                        btn["text"]="퐁"
                    for j in range(len(a.울기판정()[i])):
                        cvs.create_image(1080-35*j-150*i,650,image=Image[a.울기판정()[i][j]],tag="PP")
                        
    elif wait==3 or wait==4:#3은 화료하여 종료, 4는 유국되어 종료 
        killbtn()
        cvs.delete("wait1")
        cvs.delete("wait2")
        cvs.delete("PP")
        cvs.create_rectangle(100,100,1000,700,fill="black",tag="PP")
        if wait==3:
            for i in range(len(Player[g.winner].패[0])):#손패
                cvs.create_image(150+35*i+(i+1)//(len(Player[g.winner].패[0]))*30,150,image=Image[Player[g.winner].패[0][i]],tag="PP")
                #(i+1)//(len(Player[g.winner].패[0]))*30는 마지막에 쯔모한 패 그림 
            for i in range(1,len(Player[g.winner].패)):#공개패
                for j in range(len(Player[g.winner].패[i])):
                    cvs.create_image(1100-35*j-200*i,150,image=Image[Player[a.order].패[i][j]],tag="PP")
            for i in range(len(g.판정[1])):#역
                cvs.create_text(200,320+50*i,text=str(g.판정[1][i]),font=("궁서",25),fill="white",tag="PP")
            cvs.create_text(800,200,text=str(g.판정[0])+"  "+str(g.score)+"점",font=("궁서",25),fill="white",tag="PP")
            for i in range(len(Player)):#점수현황 
                cvs.create_text(800,250+i*50,text=str(Player[i].name)+str(Player[i].score),font=("궁서",25),fill="white",tag="PP")
            for i in range(4):  #도라표시패 
                if i<g.도라수:
                    cvs.create_image(150+35*i,210,image=Image[g.왕패[9-2*i]],tag="PP")
                else:
                    cvs.create_image(150+35*i,210,image=Image[0],tag="PP")
            if a.멘젠==2:
                for i in range(4):  #도라표시패 
                    if i<g.도라수:
                        cvs.create_image(150+35*i,270,image=Image[g.왕패[10-2*i]],tag="PP")
                    else:
                        cvs.create_image(150+35*i,270,image=Image[0],tag="PP")
            else:
                for i in range(4):  #도라표시패 
                    cvs.create_image(150+35*i,270,image=Image[0],tag="PP")
        elif wait==4:
            for k in Player:
                if k.텐파이확인():
                    for i in range(len(k.패[0])):#손패
                        cvs.create_image(150+35*i,150+k.order*100,image=Image[k.패[0][i]],tag="PP")
                    
                    for i in range(1,len(k.패)):#공개패
                        for j in range(len(k.패[i])):
                            cvs.create_image(7500-35*j-60*i,150+k.order*100,image=Image[k.패[i][j]],tag="PP")
                else:
                    for i in range(13):#손패
                        cvs.create_image(150+35*i,150+k.order*100,image=Image[0],tag="PP")
                  #점수현황 
                cvs.create_text(900,150+k.order*100,text=str(k.name)+str(k.score),font=("궁서",25),fill="white",tag="PP")
                #점수 변동
                cvs.create_text(115,150+k.order*100,text=str(["동","남","서","북"][k.order]),font=("궁서",25),fill="white",tag="PP")
    

    root.after(100,draw)


def makebtn():
    global 화료버튼, 리치버튼
    killbtn()
    if a.쯔모:
        화료버튼=tk.Button(image=Image["주모"],bg="#00394E",border=0,command=a.화료)
        화료버튼.place(x=1000,y=550)
    if g.버림패[0]:
        if a.론판정() and not a.후리텐:
            a.론=1
            화료버튼=tk.Button(image=Image["대출"],bg="#00394E",border=0,command=a.화료)
            화료버튼.place(x=1000,y=550)
    if a.멘젠==1 and a.버림패추천 and a.order==g.order:
        리치버튼=tk.Button(text="리치",font=("굴림",24),fg="white",bg="#00394E",border=0,command=a.리치)
        리치버튼.place(x=1000,y=500)

def killbtn():
    global 화료버튼, 리치버튼
    try:
        화료버튼.destroy()
    except:
        pass
    try:
        리치버튼.destroy()
    except:
        pass
#--------------------------------------------------------------------------------클라 부분---------------------------------------------------

#--------------------------------------------------------------------------------서버 부분---------------------------------------------------
class game:
    def __init__(self):

        random.shuffle(Player)
        
        for i in Player:
            i.score=45000-len(Player)*5000

            print("{}인 마작을 시작합니다.".format(len(Player)))
        self.연장=0
        self.풍=0 #장풍패를 나타냄.
        self.국=0 #player.order를 불변으로 놓는다면, [a,b,c,d]같은식으로 고정이라면 자풍패처리를 어떻게 하지?
        self.리치점수=0

    def start(self):#기본셋팅
        global wait
        self.deck=mjhr.FList*4
        random.shuffle(self.deck)
        if len(Player)==3:
            for i in [12,13,14,15,16,17,18]*4:
                self.deck.remove(i)
        self.왕패=[] #말 그대로 왕패. 도라표시패와 우라도라, 영상패로 이루어짐 
        self.패=[] #버림패와 마찬가지로 패를 분배하기 위함 
        self.버림패=[] #self.버림패는 플레이어별 버림패리스트를 모아둔 리스트임 꼭 필요하다기보다는 버림패를 분배하기 위함
        self.order=0  #self.order 또는 g.order는 현재 턴인 플레이어를 나타냄 
        self.도라수=1 #표시할 도라 수를 나타냄 깡을 치면 1 올라감
        self.영상=0 #깡을 치고나면 일시적으로 활성화 됨. 패를 버리는 등 영상판정상황이 지나가면 0이 됨 
        self.winner=None

        cvs.delete("국정보")
        wait=0

        for i in range(len(Player)):
            self.패.append([[]])
            self.버림패.append([])
            Player[i].패=self.패[i]
            Player[i].버림패=self.버림패[i]
            Player[i].멘젠=1#0이면 울었음, 2면 리치 
            Player[i].론=0
            Player[i].대기패=None
            Player[i].버림패추천=[]
            Player[i].쯔모=0 #쯔모화료 가능 여부를 나타냄. 쯔모화료가능시 쯔모버튼  출력
            Player[i].후리텐=0
            Player[i].리치턴=-1#(리치를 한 턴)
        for i in range(14):
            self.왕패.append(self.deck.pop(0))
        print("도라 표시패는 {}입니다.".format(self.왕패[0]))
            
        for i in range(len(Player)):
            Player[i].order=i
            Player[i].바람=바람[i]
            for j in range(13):
                Player[i].패[0].append(self.deck.pop(0))
                Player[i].패[0].sort()
        cvs.create_text(550,350,text=["동","남","서","북"][self.풍]+"풍",font=("궁서",24),tag="국정보")
        cvs.create_text(550,400,text=str(self.국+1)+"국",font=("궁서",24),tag="국정보")
        cvs.create_text(550,450,text=str(self.연장)+"연장",font=("궁서",24),tag="국정보")
    def 유국(self):#뽑기 할 때 실행 
        #구종구패, 4깡, 패산 없음
        #패산 없는 경우.
        #텐파이한 사람 체크
        #텐파이한 사람 수에 맞춰서 점수분배
        #연장여부 확인    
        #연장여부에 맞춰서 g.연장+1
        #
        global wait
        if len(g.deck)==0:
            cnt=[] #텐파이플레이어 리스트
            for i in Player:
                if i.텐파이확인():
                    cnt.append(i)
            if len(cnt)<4 and len(cnt)>0:
                for i in Player:
                    if i in cnt:
                        i.score+=3000/len(cnt)
                    else:
                        i.score-=3000/(4-len(cnt))
        if Player[0].텐파이확인():
            g.winner=0
        wait=4
        self.다음게임()

    def 다음게임2(self):
        time.sleep(5)
        print(self.국)
        if self.winner==0:#오야화료 
            self.연장+=1
        else:
            Player.append(Player.pop(0))
            if self.국<3:
                self.국=(self.국+1)%len(Player)
            elif self.국==3:
                self.국=0
                self.풍=(self.풍+1)%4
            self.연장=0
        self.start()
        cvs.delete("PP")
        cvs.delete("wait1")
        cvs.delete("wait2")

    def 다음게임(self):
        t=threading.Thread(target=self.다음게임2)
        t.start()
            
"""
장풍패는 바람[self.풍]으로 세팅
시작플레이어가 그대로인 경우는 Player리스트를 그대로 두고
시작플레이어가 다음으로 넘어가는 경우는 Player=Player.append(Player.pop(0))을 하면 됨

g.연장은 화료나 유국에 맞춰서 넘기자 



"""



"""



"""

class player:
    def __init__(self,name):
        self.name=name
        self.score=25000
        if len(Player)<4:
            Player.append(self)
            print("현재 플레이어는 {}명 입니다.".format(len(Player)))
    def 텐파이확인(self):
        return mjhr.텐파이확인(self.패,self.멘젠,self.론,바람[g.풍],바람[self.order],len(g.deck),g.영상)
    def 역확인(self):
        return mjhr.역확인(self.패,self.멘젠,self.론,바람[g.풍],바람[self.order],len(g.deck),g.영상)

    def 뽑기(self):
        global wait
        if self.멘젠<2:
            self.후리텐=0

        if len(self.패[0])+len(self.패)*3-3==13 and g.order==self.order and wait==0:
            killbtn()#화료버튼(론) 삭제
            if not g.deck:
                g.유국()
            else:
                wait=1
                self.패[0].append(g.deck.pop(0))
                if mjhr.역확인(self.패,self.멘젠,self.론,바람[g.풍],바람[self.order],len(g.deck),g.영상):
                    self.쯔모=1
                self.버림패추천=mjhr.버림패추천(self.패,self.멘젠,self.론,바람[g.풍],바람[self.order],len(g.deck),g.영상)
                makebtn()#화료버튼(쯔모) 생성
                if self.멘젠==2 and not self.역확인():
                    self.버리기(0)
             
        

    def 버리기2(self,n):
        global wait
        if len(self.패[0])+len(self.패)*3-3==14 and g.order==self.order and wait==1:
            killbtn()#화료버튼(쯔모)삭제 
            self.버림패.append(self.패[0].pop(n-1))
            g.최근버림패=self.버림패[-1]
            self.패[0].sort()
            self.대기패=self.텐파이확인()
            self.버림패추천=[]
            self.쯔모=0
            g.영상=0
            if self.리치턴>-1:
                self.멘젠=2
            wait=2
            makebtn()#화료버튼(론) 생성
            time.sleep(1)
            if wait==2 and g.order==self.order:
                for i in Player:
                    for j in i.텐파이확인():
                        if j[0]==g.최근버림패:
                            i.후리텐=1
                g.최근버림패=0
                g.order=(self.order+1)%len(Player)
                wait=0
                for i in self.텐파이확인():
                    if i[0] in self.버림패:
                        self.후리텐=1
             
                    

    def 버리기(self,n):
        if self.멘젠<2 or self.리치턴==len(self.버림패):
            t=threading.Thread(target=self.버리기2,args=(n,))
            t.start()
        elif self.멘젠==2 and n==14:
            t=threading.Thread(target=self.버리기2,args=(n,))
            t.start()

    def 퐁판정(self):
        global wait
        if (len(self.패[0])+len(self.패)*3-3==13
            and (self.패[0].count(g.최근버림패)>1
            and g.order!=self.order) and wait==2
            and self.멘젠<2):
            return [[g.최근버림패]*3] #이 리스트를 울기 후보에 추가
        else:
            return [] #그림 그릴 때 사용할 예정 if문의 조건으로 


    def 치판정(self):
        global wait
        cnt=[]
        if (len(self.패[0])+len(self.패)*3-3==13
            and (self.order-g.order)%len(Player)==1
            and wait==2 and len(Player)==4
            and self.멘젠<2):
            if (self.패[0].count(g.최근버림패+1)>0
                and self.패[0].count(g.최근버림패+2)>0):
                cnt.append([g.최근버림패,g.최근버림패+1,g.최근버림패+2])
            if (self.패[0].count(g.최근버림패+1)>0
                and self.패[0].count(g.최근버림패-1)>0):
                cnt.append([g.최근버림패,g.최근버림패-1,g.최근버림패+1])
            if (self.패[0].count(g.최근버림패-1)>0
                and self.패[0].count(g.최근버림패-2)>0):
                cnt.append([g.최근버림패,g.최근버림패-2,g.최근버림패-1])
            return cnt
        else:
            return [] #그림 그릴 때 사용할 예정
    


    def 대명깡판정(self):
        global wait
        cnt=0
        #1) 대명깡 
        if (len(self.패[0])+len(self.패)*3-3==13 #패가 13장 (깡이 있을 경우 3개로 취급)
            and (self.패[0].count(g.최근버림패)==3 #최근버림패가 3장 패에 가지고 있는 경우
            and g.order!=self.order)  #자신의 순서가 아니고 우는 타이밍(wait=2)인 경우
            and wait==2 and g.deck and self.멘젠<2): 
            return [[g.최근버림패]*4]
        else:
            return []
    def 론판정(self):
        if g.order!=self.order:
            if g.최근버림패 in self.버림패:
              #  self.후리텐=1
                return False
            else:
                cnt=[]
                for i in self.패:
                    cnt2=i.copy()
                    cnt.append(cnt2)
                cnt[0].append(g.최근버림패)
                return mjhr.역확인(cnt,self.멘젠,1,바람[g.풍],바람[self.order],len(g.deck),g.영상)

        
    def 울기판정(self):#맨 왼쪽이 우는패 
        cnt=[]
        #cnt.append(self.퐁판정())
        for i in self.치판정()+self.퐁판정()+self.대명깡판정():
            cnt.append(i)
        #cnt.append(self.대명깡판정())
        return cnt
    def 울기실행(self,n):
        global wait
        killbtn()#울었으니까 론버튼 삭제 
        cnt=[self.울기판정()[n][0]]
        for i in self.울기판정()[n][1:]:
            cnt.append(self.패[0].pop(self.패[0].index(i)))
        g.order=self.order
        self.패.append(cnt)
        wait=1
        self.멘젠=0
        
        if len(cnt)==4:
            self.패[0].append(g.왕패.pop(-1))
            g.왕패.insert(10,g.deck.pop(-1))
            g.도라수+=1
            g.영상=1
            if mjhr.역확인(self.패,self.멘젠,self.론,바람[g.풍],바람[self.order],len(g.deck),g.영상):
                self.쯔모=1
            makebtn()#깡쳤으니 쯔모면 쯔모표시 
        self.버림패추천=mjhr.버림패추천(self.패,self.멘젠,self.론,바람[g.풍],바람[self.order],len(g.deck),g.영상)
        g.최근버림패=0
        for i in Player:
            i.리치턴=-1
        
        
    def 깡판정(self):
        global wait
        cnt=[]
        #2)가깡,안깡 
        if (len(self.패[0])+len(self.패)*3-3==14
            and g.order==self.order
            and g.deck): #패가 14장
            for i in self.패[0]:
                if [i,i,i] in self.패:
                    cnt.append([i,i,i,i])

                    """
                    self.패[self.패.index([i,i,i])].append(i)
                    self.패[0].remove(i)
                    cnt+=1
                    """
                if self.패[0].count(i)==4:
                    if [0,i,i,0] not in cnt:
                        cnt.append([0,i,i,0])
            return cnt
        else:
            return False

    def 깡실행(self,n):
        global wait
        cnt=self.깡판정()[n].copy() #선택한 것을 추가하고
        self.패.append(cnt)
        if cnt[0]==0: #선택한 것이 [0,#,#,0] 이라면
            self.패[0].remove(cnt[1]) #손패에서 패를 4장 지운다. i[0]은 0이므로 1에 해당하는 값을 지운다.
            self.패[0].remove(cnt[1])
            self.패[0].remove(cnt[1])
            self.패[0].remove(cnt[1])
        else:
            self.패[0].remove(cnt[1])
            self.패.remove([cnt[1]]*3)
        self.패[0].append(g.왕패.pop(-1))
        g.왕패.insert(10,g.deck.pop(-1))
        g.도라수+=1
        g.영상=1
        self.버림패추천=mjhr.버림패추천(self.패,self.멘젠,0,바람[g.풍],바람[self.order],len(g.deck),0)
        makebtn()
        
    def 화료(self):#점수간편화를 위해 천,2천,4천,8천,12,16,24,32
        global wait
        cnt=0
        cnt2=[]
        for i in range(g.도라수):#도라가 20,30,40,43,46,49,51인 경우 각각 11,21,31,44,41,50,47로 옮겨줘야함
            if g.왕패[9-2*i]+1 in [20,30,40,43,46,49,51]:
                cnt3=[11,21,31,44,41,50,47][[20,30,40,43,46,49,51].index(g.왕패[9-2*i]+1)]
            else:
                cnt3=g.왕패[9-2*i]+1
            cnt2.append(cnt3) #cnt2는 도라집합, cnt3는 도라
        if self.멘젠==2:
            for i in range(g.도라수):#도라가 20,30,40,43,46,49,51인 경우 각각 11,21,31,44,41,50,47로 옮겨줘야함
                if g.왕패[10-2*i]+1 in [20,30,40,43,46,49,51]:
                    cnt3=[11,21,31,44,41,50,47][[20,30,40,43,46,49,51].index(g.왕패[10-2*i]+1)]
                else:
                    cnt3=g.왕패[10-2*i]+1
                cnt2.append(cnt3) #cnt2는 도라집합, cnt3는 도라
        cnt4=0#가지고 있는 도라 수 
        for i in self.패+(len(self.패[0])+len(self.패)*3-3==13)*[[g.최근버림패]]:
            for j in i:
                for k in cnt2:
                    if j==k:
                        cnt4+=1
        일발=0
        if self.리치턴==len(self.버림패):
            일발=1

        if self.역확인():#쯔모화료한 경우
            판정=self.역확인()
        elif self.론판정():
            판정=self.론판정()
        if 판정[0][-1]=="판":#판인 경우 
            pan=int(판정[0][:-1])+cnt4+일발
            판정[0]=str(pan)+"판"
            if pan==1:
                   cnt=1000
            elif pan==2:
                cnt=2000
            elif pan==3:
                cnt=4000
            elif pan in (4,5):
                cnt=8000
            elif pan in (6,7):
                cnt=12000
            elif pan in (8,9,10):
                cnt=16000
            elif pan in (11,12):
                cnt=24000
            elif pan>12:
                cnt=32000
        else:#역만인 경우
            cnt=int(판정[0][:-2])*32000

        if 바람[g.풍]==바람[self.order]:
            cnt*=1.5
        cnt+=g.연장*300 
        if g.order==self.order:#쯔모
            for i in Player:
                if self!=i:
                    if i.바람==바람[g.풍]:
                        i.score-=int(cnt/2)
                    else:
                        i.score-=int(cnt/4)*(1+(바람[g.풍]==바람[self.order])/3)
        else:#론
            Player[g.order].score-=cnt
            self.패[0].append(g.최근버림패)
        g.score=int(cnt+g.리치점수)
        self.score+=cnt+g.리치점수 
        wait=3
        g.판정=판정
        if cnt4>0:
            g.판정[1].append("도라"+str(cnt4)+"판")
        if 일발:
            g.판정[1].append("일발")
        g.winner=self.order
        g.리치점수=0
        g.다음게임()


    def 리치(self):
        if self.리치턴!=-1:
            리치버튼["fg"]="white"
            #self.멘젠=1
            self.리치턴=-1
            self.score+=1000
            g.리치점수-=1000
        elif self.리치턴==-1:
            리치버튼["fg"]="black"
            #self.멘젠=2
            self.리치턴=len(self.버림패)
            self.score-=1000
            g.리치점수+=1000




            

a=player("가")
b=player("나")
c=player("다")
d=player("라")
g=game()
g.start()


#--------------------------------------------------------------------------------서버 부분---------------------------------------------------




#--------------------------------------------------------------------------------클라 부분---------------------------------------------------
draw()

def imsi():
    if g.order!=a.order:
        Player[g.order].뽑기()
        Player[g.order].버리기(0)
        
    elif g.order==a.order:
        a.뽑기()
    root.after(100,imsi)



def move(e):
    global mx,my,cx,cy
    mx=e.x
    my=e.y
    if my>720 and my<780:
        cy=True
        cx=(mx-20)//35+1
    else:
        cy=False


def click(e):
    global cx,cy
    if cx>0 and cx<len(a.패[0])+1 and cy:
        a.버리기(cx)



def Rclick(e):
    print(a.역확인())
    print(mjhr.역확인(a.패,a.멘젠,a.론,바람[g.풍],바람[a.order],len(g.deck),g.영상))
    



root.bind("<Button-1>",click)

root.bind("<Motion>",move)
imsi()

def test():
    cvs.delete("TTT")
    #cvs.create_text(400,300,text=g.order,font=("굴림",25),tag="TTT")
    root.after(100,test)
    
test()
사기패=[[11,11,11,12,12,12,13,13,13,14,14,14,15]]
def cheat(e):
    a.패=[[11,11,11,13,13,13,15,15,15,17,17,17,19]]
 #   b.패=[[11,11,11,12,12,12,13,13,13,14,14,14,16]]
  #  c.패=[[11,11,11,12,12,12,13,13,13,14,14,14,17]]
    g.deck=[11,13,15,17,19]*50
    g.왕패=[19]*15
    #a.멘젠=2

root.bind("<Button-2>",cheat)

root.bind("<Button-3>",cheat)

root.mainloop()
