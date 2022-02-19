a=[[11,11,11,12,12,12,13,13,13,14,14,14,15,15]]
#첫번째는 울지 않은 부분, 뒤에 3칸씩은 운 부분 
FList=[11,12,13,14,15,16,17,18,19,21,22,23,24,25,26,27,28,29,31,32,33,34,35,36,37,38,39,41,42,44,45,47,48,50]#만패 통패 삭패 자패 
풍=41 #41,42,44,45가 동남서북
자풍=42 
#전체 카드 리스트
YList=[11,19,21,29,31,39,41,42,44,45,47,48,50]
#요구패 리스트


def bodycheck(a):#BC는 [머리,나머지]
    H=[]
    b=a[0].copy()
    b.sort()
    for i in range(len(b)-1):
        if b[i]==b[i+1]:
            if b[i] not in H:
                H.append(b[i])
    BC=[]
    for i in H:
        b=a[0].copy()
        b.sort()
        b.remove(i)
        b.remove(i)
        c=[]
        c.append([i,i])
        c.append(b)
        for j in a:
            c.append(j)
        c.remove(a[0])
        if [] in c:
            c.remove([])
        BC.append(c)
    return BC

def checkS(a): #슌쯔 체크 
    b=[a[0],a[0]+1,a[0]+2]
    try:
        for i in b:
            a.remove(i)
        return b
    except:
        return False

def checkK(a):#커쯔체크 
    b=[a[0]]*3
    try:
        for i in b:
            a.remove(i)
        return b
    except:
        return False        

def makecases(n):#-> 0은 커쯔, 1은 슌쯔 
    B=[]
    for i in range(2**n):
        A=[]
        for j in range(n):
            a=int(i%2)
            i=(i-a)/2
            A.append(a)
        B.append(A)
    return B




def 화료확인(a):
    C=[]
    try:#치또이츠 확인 
        B=[]
        b=a[0].copy()
        for i in range(7):
            c=b[0]
            if [c,c] in B:
                "가"+1
                break
            b.remove(c)
            b.remove(c)
            B.append([c,c])
        
        C.append(B)
    except:
        pass
    try:#국사무쌍 확인 
        B=[]
        b=a[0].copy()
        for i in YList:
            b.remove(i)
        if b[0] in YList:
            C.append(a)
    except:
        pass
    for i in bodycheck(a):#바디체크는 손패에서 머리만 뗀다 (여러가지 경우의수 )
        for j in makecases(len(i[1])//3):#i는 후보집합, j는 각/순 경우의수
            b=i[1].copy() #checkK/S가 성공하면 b는 원소가 3개줄고 아니면 그대로 
            B=[]
            for k in range(len(i[1])//3): #0000~1111에 대해서 0이면 각자, 1이면 순자 체크 
                if j[k]==0:
                    B.append(checkK(b))
                elif j[k]==1:
                    B.append(checkS(b))
                if False in B:
                    break
            if len(b)==0:
                B.insert(0,i[0])#맨 앞에 머리 삽입
                for k in a:  #운 부분 삽입 
                    B.append(k)
                B.remove(a[0])
                C.append(B)#C에 화료모양 삽입 
    return C
            
def 텐파이확인(a,멘젠,론,장풍,자풍,남은덱,영상):
    대기패=[]
    for i in FList:
        b=[]## 2중리스트에는 copy가 잘 먹히지 않는다. 
        for j in a:
            b.append(j.copy())
        b[0].append(i)
        b[0].sort()
        if bool(화료확인(b)):
            대기패.append([i,역확인(b,멘젠,론,장풍,자풍,남은덱,영상)])
    return(대기패)

def replace(a):#숫자로 나타난 패를 이름으로 변경 
    A=[41,42,44,45,47,48,50]
    B=["동","남","서","북","백","발","중"]
    C=["만","통","삭"]
    if a<40:
        return str(a%10)+str(C[a//10])
    elif a>40:
        for i in range(7):
            if a==A[i]:
                return B[i]
                break

def 버림패추천(a,멘젠,론,장풍,자풍,남은덱,영상):
    B=[]
    C=[]
    for j in range(len(a[0])):
        b=[]
        for i in a:
            b.append(i.copy())
        b[0].remove(b[0][j])
        if 텐파이확인(b,멘젠,론,장풍,자풍,10,0):
            B.append(j)
            #C.append(텐파이확인(b))
    return(B)


def 역확인(a,멘젠,론,장풍,자풍,남은덱,영상): #멘젠은 0은 멘젠아님, 1은 멘젠, 2는 리치
    #론은 1이면 론, 0이면 쯔모 
    #a는 완성패 모양을 넣음 화료확인함수에서 출력되는 값
    #멘젠은 a의 len으로 알 수 있음
    #len이 1이면 멘젠, 2이상이면 아님
    #대신 리치를 나타내는 값이 필요
    #not bool(len(a)-1)
    #으로 할려고 했으나, 안깡의 경우 len만으로 멘젠을 못따지므로
    #멘젠 값이 결국 별도로 필요할듯 
    Yman=0 #최고 역만수
    Pan=0 #최고 판수
    B=[] #최고점 모양
    Y=[] #최고점이 가진 역 목록
    for b in 화료확인(a): #즉 역확인은 완성된 패를 전제로한다.
        y=[] #역 목록 
        pan=0 #판 
        yman=0 #역만
        kz=0 #커츠 각자 
        Kz=0 #깡쯔 공자
        ak=0 #안커 
        for i in b:
            if len(i)==3:
                if i[0]==i[1]:# and i[0]==i[2]
                #3개짜리파츠에서 2개가 같으면 이미 커쯔임
                    kz+=1
                    if (i not in a) and (론==0 or i[0]!=a[0][-1] or a[0].count(i[0])==4):
                        ak+=1
        for i in b:
            if len(i)==4:
                Kz+=1
                if i[0]==0:
                    ak+=1
#---------------------------------------------멘젠쯔모  테스트 미완료
        if 멘젠!=0 and 론==0:
            pan+=1
            y.append("멘젠쯔모")

#---------------------------------------------
        if 영상==1:
            pan+=1
            y.append("영상개화")

        if 남은덱==0 and 론==0:
            pan+=1
            y.append("해저로월")
        elif 남은덱==0 and 론==1:
            pan+=1
            y.append("하저로어")

#---------------------------------------------공자계열 테스트 미완료
        if Kz==4:
            yman+=1
            y.append("사공자")
        elif Kz==3:
            pan+=2
            y.append("삼공자")
        

#---------------------------------------------테스트 미완료
        if (([11,12,13] in b and [14,15,16] in b and [17,18,19] in b)
            or ([21,22,23] in b and [24,25,26] in b and [27,28,29] in b)
            or ([31,32,33] in b and [34,35,36] in b and [37,38,39] in b)):
            pan+=1+bool(멘젠)
            y.append("일기통관")
            
#---------------------------------------------테스트 미완료
        cnt=[]
        for i in b:
            cnt+=i
        cnt2=cnt.copy()
        cnt2.remove(a[0][-1])
        cnt2.sort()
        if (cnt2==[11,11,11,12,13,14,15,16,17,18,19,19,19]
            or cnt2==[21,21,21,22,23,24,25,26,27,28,29,29,29]
            or cnt2==[31,31,31,32,33,34,35,36,37,38,39,39,39]):
            yman+=2
            y.append("순정 구련보등")
        else:
            try:
                for i in [11,11,11,12,13,14,15,16,17,18,19,19,19]:
                    cnt.remove(i)
                yman+=1
                y.append("구련보등")
            except:
                pass
            try:
                for i in [21,21,21,22,23,24,25,26,27,28,29,29,29]:
                    cnt.remove(i)
                yman+=1
                y.append("구련보등")
            except:
                pass
            try:
                for i in [31,31,31,32,33,34,35,36,37,38,39,39,39]:
                    cnt.remove(i)
                yman+=1
                y.append("구련보등")
            except:
                pass
        
#---------------------------------------------테스트 미완료
        cnt=0
        try:
            for i in range(1,len(b)):
                if ([b[i][0]+10,b[i][1]+10,b[i][2]+10] in b
                    and [b[i][0]+20,b[i][1]+20,b[i][2]+20] in b):
                    if b[i][0]==b[i][1] and b[i][0]<20:
                        pan+=2
                        y.append("삼색동각")
                    elif b[i][0]+1==b[i][1]:
                        pan+=1+bool(멘젠)
                        y.append("삼색동순")
        except:
            pass

        
#---------------------------------------------테스트 미완료
        cnt=True
        for i in a:
            for j in i:
                cnt*=(j not in YList)
        if cnt==True:
            pan+=1
            y.append("탕야오")
#---------------------------------------------각자계열    테스트 미완료    
        if kz+Kz==4: #또이또이, 사암각 
            pan+=2
            y.append("또이또이")
        if ak==4:
            if a[0][-1]==b[0][0]: #손에 마지막으로 들어온 패가 머리의 패라면
                yman+=2
                y.append("사암각 단기")
            else:
                yman+=1
                y.append("사암각")
        elif ak==3:
            pan+=2
            y.append("삼암각")
#---------------------------------------------배구  테스트 미완료
        cnt=0
        for i in range(len(b)-1):
            for j in range(i+1,len(b)):
                if b[i]==b[j]:
                    cnt+=1
        if cnt==1 or cnt==3 and 멘젠>0:
            pan+=1
            y.append("일배구")
        elif (cnt==6 or cnt==2) and 멘젠>0:
            pan+=3
            y.append("이배구")
#---------------------------------------------일색  테스트 미완료
        cnt=[]
        for i in b:
            if (i[0]-1)//10 not in cnt:
                cnt.append((i[0]-1)//10)
        if cnt==[1] or cnt==[2] or cnt==[3]:
            pan+=5+bool(멘젠)
            y.append("청일색")
        elif cnt==[1,4] or cnt==[2,4] or cnt==[3,4]:
            pan+=2+bool(멘젠)
            y.append("혼일색")
        elif cnt==[4]:
            yman+=1
            y.append("자일색")

        cnt=1
        for i in b:
            for j in i:
                cnt*=(j in [32,33,34,36,38,48])
        if cnt==1:
            yman+=1
            y.append("녹일색")
#---------------------------------------------테스트 미완료
        if 멘젠==2: #리치 
            pan+=1
            y.append("리치")
        if len(b)==7: #치또이츠 
            pan+=2
            y.append("칠대자")
        elif len(b)==1: #국사무쌍
            yman+=1
            y.append("국사무쌍")

#---------------------------------------------테스트 미완료 
        cnt=0
        for i in [47,48,50]: #역패, 대삼원 
            if [i,i,i] in b or [i,i,i,i] in b:
                cnt+=1
        if cnt==3:
            yman+=1
            y.append("대삼원")
        elif cnt>0:
            pan+=cnt
            y.append("역패")
        if cnt==2 and ([47,47] in b or [48,48] in b or [50,50] in b):
            pan+=2
            y.append("소삼원")
#---------------------------------------------테스트 미완료 
        cnt=0
        for i in [41,42,44,45]: #대사희 소사희
            if [i,i,i] in b or [i,i,i,i] in b:
                cnt+=1
        if cnt==4:
            yman+=2
            y.append("대사희")
        elif cnt==3 and b[0][0] in [41,42,44,45]:
            yman+=1
            y.append("소사희")

        if [자풍,자풍,자풍] in b:
            pan+=1
            y.append("자풍패")
        if [장풍,장풍,장풍] in b:
            pan+=1
            y.append("장풍패")
#---------------------------------------------테스트 미완료
            
        cnt=1
        for i in a:
            for j in i:
                cnt*=(j in [11,19,21,29,31,39])
        if cnt==1:
            yman+=1
            y.append("청로두")

        cnt=1
        for i in a:
            for j in i:
                cnt*=(j in YList)
        if cnt==1 and "국사무쌍" not in y and "자일색" not in y and "청로두" not in y:
            pan+=2
            y.append("혼로두")

#---------------------------------------------테스트 미완료
        cnt=1
        for i in b:
            cnt*=(i[0] in [11,19,21,29,31,39] or i[-1] in [11,19,21,29,31,39])
        if cnt==1:
            pan+=2+bool(멘젠)
            y.append("쥰찬타")

        cnt=1
        for i in b:
            cnt*=(i[0] in YList or i[-1] in YList)
        if (cnt==1 and "혼로두" not in y and "쥰찬타" not in y
            and "국사무쌍" not in y and "자일색" not in y
            and "청로두" not in y):
            pan+=1+bool(멘젠)
            y.append("찬타")


#---------------------------------------------테스트 미완료
        try:
            if 멘젠!=0 and kz==0 and Kz==0:
                cnt=0
                cnt2=[자풍,장풍,47,48,50]
                for i in range(1,5):
                    cnt+=(a[0][-1]==b[i][0] or a[0][-1]==b[i][2]) #마지막에 먹은패가 양면이 맞는지(커쯔는 없으므로)
                for i in a[0]:
                    if i in cnt2:
                        cnt=0
                        break  ##########220116 수정 (장풍패가 머리인 경우 핑후인정이 되는 버그때문)
                if cnt!=0:
                    pan+=1
                    y.append("핑후")
        except:
            pass





#---------------------------------------------역 판정 끝

#---------------------------------------------이후 점수계산 


        if yman>Yman:
            Yman=yman
            Pan=yman*13
            B=b
            Y=y
         #return yman
        if pan>Pan:
           Pan=pan
           B=b
           Y=y
           #return pan
    
    if Yman>0:
       # print(str(Y)+"\n"+str(B)+"\n"+str(Yman)+"역만")
        return [str(Yman)+"역만",Y]
    elif Yman==0 and Pan==0:
        return False
    else:
       # print(str(Y)+"\n"+str(B)+"\n"+str(Pan)+"판")
        return [str(Pan)+"판",Y]












    
    
