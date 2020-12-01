import numpy as np
import random as rd
import matplotlib.pyplot as mp

class Station:
    def __init__(self,station_ID=999,basic_delay=5,Line_List = [],Time_List = []):
        self.ID=station_ID
        self.Line_Dic=dict(zip(Line_List,Time_List))
        self.basic_delay=basic_delay
         #站点存储线路号，以及对应线路的到达时间,其中初始值为线路默认的间隔(为负值)
         #字典的key是线路的序列号,Time_List是上一次到达的时间(初始值为负值)
         #不同时间到达站点的基本等待时间相同 站点ID为001-999

    def addline(self,Line,Time_init):
        self.Line_Dic[Line]=Time_init
        #每条线路在站点均有固定等待时间，时间初始为负值
    
class Crossing:
    def __init__(self,crossing_ID,passing,offset_time,period_time):
        self.ID=crossing_ID #路口序列号 ID为 1000-9999
        self.passtime=passing #通过时间占比
        self.offset=offset_time #路口偏置时间(防止重复)
        self.period=period_time #路口周期时间
        
    def lastpass(self,time):
        time_basic=(time-self.offset)%(self.period)
        if time_basic<0:
            time_basic=time_basic+self.period
        
        return time_basic #用于描述到达时路口的状态，距离上一次pass的时间

class Line:
    def __init__(self,number,first_Station_ID):
        self.Line_ID=number
        self.Start_ID=first_Station_ID
        self.walking=[] # 路由列表 仅支持一个个添加
        self.Length=0 #线路总长度
        self.up_tuple=() 
        self.down_tuple=()

    def add_Station(self,Station_ID,distance): # 严禁distance=1！要求路口和站点实际上只到达，不暂停(否则容易出问题)
        self.walking.append((Station_ID,distance))
        self.Length=self.Length + distance

    def add_Crossing(self,Crossing_ID,distance):
        self.walking.append((Crossing_ID,distance))
        self.Length=self.Length + distance

    def Stantion_number(self,ID): #输入ID 返回这是第几站 从0开始数
        if ID == self.Start_ID:
            return 0
        else:
            i=1
            temp=-1 #返回 -1 说明没有找到 该函数从0开始数~
            for item in self.walking:
                if item[0] == ID:
                    temp=i
                elif item[0] < 1000:
                    i=i+1
            return temp
    
    def number_station(self):
        number=0
        for item in self.walking:
            if item[0]<1000:
                number=number+1

        number=number+1
        return number
    
    def Locate(self,Location): #未验证 返回一个list
        Distant=0
        ID=[10001,10002]
        if Location == 0:
            ID=[self.Start_ID,self.Start_ID]
        else:
            for item in self.walking:
                Distant=Distant+item[1] #遍历法返回当前路口和车站,应该有更聪明的办法，直接打个表就完事了
                if Location == Distant:
                    ID=[item[0],item[0]] #直接返回两次序号,最后一个是站序号
                    break  
                if Distant > Location:
                    ID=[10001,item[0]] #返回下一个stint的序号 路口或者车站
                    break
        return ID

    def passenger_initial(self,up=(),down=()):
        if (len(up) == (self.number_station()-1)) & (len(down) == (self.number_station()-1)) :
            self.up_tuple=tuple(up)
            self.down_tuple=tuple(down)
        else:
            self.up_tuple=tuple(np.ones(self.number_station()-1))
            self.down_tuple=tuple(np.ones(self.number_station()-1))


class Bus: #声明具体运行的一辆公交车
    def __init__(self,Line,start_time,Bus_ID=43477,location=-1): #注意，这里需要传一个 Line 类进来
        self.Matrix=np.zeros((Line.number_station(),Line.number_station())) 
        #没错，我懒，所以开了一整个矩阵，其实只需要下半边,用于存储车上乘客目的地
        self.start_time=start_time #出场时间
        self.ID=Bus_ID #到达时间
        self.location=location # 初始距离=-1 不出现在图中
        self.delay=0 #初始没有delay

    def move(self):
        if self.delay == 0:
            self.location=self.location+1
        else:
            self.delay=self.delay-1

