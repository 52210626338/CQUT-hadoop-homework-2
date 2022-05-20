

# 对coj上的测试提交数据进行探索分析。主要内容包括：
import datetime

import numpy as np
import pandas as pd

path = r'D:\Study\学习资料\Hadoop\contest.xlsx'
sheet =pd.read_excel(path,header=2)
df=pd.DataFrame(sheet)

#准备:
#替换空值,未完成或者没有时间的一律为0（0）
df1 = df.replace(to_replace=np.nan,value="0(0)")

df2 = df1.iloc[:-1,:]

name_df = df2['Nick'].tolist()

solved = df2['Solved'].tolist()

user = df2['User'].tolist()

rank = df2['Rank'].tolist()

mark = df2['Mark'].tolist()

Penalty = []
A = []
B = []
C = []
D = []
E = []
F = []
G = []
H = []
#创建错误次数列表
Penalty1 = []
A1 = []
B1 = []
C1 = []
D1 = []
E1 = []
F1 = []
G1 = []
H1 = []

def get(col,time,err):

    a = df2[col].tolist()
    for i in a:

        if type(i) == datetime.time:
            i = i.strftime('%H:%M:%S')
            x = float(i.split(":",2)[0])
            y = float(i.split(":",2)[1]) / 60
            z = float(i.split(":",2)[2]) / 3600
            i=round(x+y+z,2)
            time.append(i)
            err.append(0)
        elif type(i) == datetime.datetime:
            i = i.strftime('%y-%m-%d %H:%M:%S')
            a = i.split(" ")[0]
            b = i.split(" ")[1]

            k = int((a.split("-", 2)[2]))

            x = int((b.split(":", 2)[0]))

            y = float((b.split(":", 2)[1])) / 60

            z = float((b.split(":", 2)[2])) / 3600
            i = round((24 * k + x + y + z), 2)
            time.append(i)
            err.append(0)
        elif type(i) == str:
            a = i.split("(")[0]
            b = int(i.split("(")[1].split(")")[0])
            err.append(b)
            if len(a) == 0 or len(a) == 1:
                    a = 0
                    time.append(a)
            else:
                x = float(a.split(":")[0])
                y = float(a.split(":")[1]) / 60
                z = float(a.split(":")[2]) / 3600
                i = round(x + y + z,2)
                time.append(i)


get('A',A,A1)
get('B',B,B1)
get('C',C,C1)
get('D',D,D1)
get('E',E,E1)
get('F',F,F1)
get('G',G,G1)
get('H',H,H1)
get('Penalty',Penalty,Penalty1)


time_df ={'排名':rank,'学号':user,"姓名":name_df,'解决题目数量':solved,'分数':mark,
          '总时间':Penalty,'问题A':A,'问题B':B,'问题C':C,'问题D':D,
            '问题E':E,'问题F':F,'问题G':G,'问题H':H}
n_time_df=pd.DataFrame(time_df,index=name_df)

err_df= {'排名':rank,'学号':  user,"姓名":  name_df,'解决题目数量':solved,'分数':mark,
         '总时间':Penalty1,'问题A':A1,'问题B':B1,'问题C':C1,'问题D':D1,
        '问题E':E1,'问题F':F1,'问题G':G1,'问题H':H1}
n_err_df=pd.DataFrame(err_df,index=name_df)

with pd.ExcelWriter(r'D:\Study\学习资料\Hadoop\提取信息.xlsx',mode='w+') as writer:
    n_time_df.to_excel(writer, sheet_name='完成时间', index=False)
    n_err_df.to_excel(writer, sheet_name='错误次数', index=False)

print(n_time_df.iloc[:,6:14].mean())

print(n_time_df.iloc[:,6:14].mean(axis=1))


print(n_err_df.iloc[:,6:14].mean().sort_values(ascending=True).head(5))

print(n_err_df.iloc[:,6:14].sum(axis=1).sort_values(ascending=True).head(5))

com ={"姓名":name_df,'解决题目数量':solved,'分数':mark,
      '问题A':A,'问题B':B,'问题D':D,
      '问题E':E,'问题F':F,'问题G':G,'问题H':H,
      'A1':A1,'B1':B1,'D1':D1,
      'E1':E1,'F1':F1,'G1':G1,'H1':H1}
com_df=pd.DataFrame(com,index=name_df)
avt_df = com_df.iloc[:,3:10].mean(axis=1)

ect_df = com_df.iloc[:,10:17].sum(axis=1)
n_com={"姓名":name_df,'解决题目数量':solved,'分数':mark,}
n_com_df=pd.DataFrame(n_com,index=name_df)
c_df = pd.concat([n_com_df,avt_df,ect_df],axis=1)

print(c_df.columns)
print(c_df.sort_values(by=['解决题目数量',1,0,'分数'],ascending=[False,False,True,False]).head(5))

print(c_df.sort_values(by=[1,0],ascending=[True,False]).tail(5))
