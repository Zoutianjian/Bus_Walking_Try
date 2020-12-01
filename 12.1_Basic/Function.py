from project import *

# Line用于填充候车人数矩阵 Time 用于计算等车人数和时间
def move_bus(bus,Station_information,Crossing_information,Line,Time):
    ID_list=Line.Locate(bus.location)
    if ID_list[0]==ID_list[1]:
        bus.location=bus.location+1
        if ID_list[0]>1000:
            temp_cross = Crossing_information[ID_list[0]].period - Crossing_information[ID_list[0]].lastpass(Time)
            if temp_cross > Crossing_information[ID_list[0]].period - Crossing_information[ID_list[0]].passtime:
                temp_cross=0
            bus.delay = temp_cross #Crossing 使得系统更加鲁棒！不容易出大间隔
        else: #到站进行Delay
            if Station_information[ID_list[0]].Line_Dic[Line.Line_ID] < 0: #更新和计算时间差T 注意，时间差的简单计算只在单线路中有效，多线路应该是一个时间差向量
                Time_temp=-Station_information[ID_list[0]].Line_Dic[Line.Line_ID]
                Station_information[ID_list[0]].Line_Dic[Line.Line_ID]=Time
            else:
                Time_temp=Time-Station_information[ID_list[0]].Line_Dic[Line.Line_ID]
                Station_information[ID_list[0]].Line_Dic[Line.Line_ID]=Time

            # Time_temp=400 #均匀产生
            Time_temp=Time_temp/40   #具体参数可以后续再设计
            number_temp=Line.Stantion_number(ID_list[0]) #首先计算出这是第几站
            bus.Matrix[-1:,number_temp:number_temp+1]=Time #把时间放进矩阵里

            if number_temp == Line.number_station() - 1 : #判断会不会是最后一站,无需等待
                bus.delay=sum(bus.Matrix[0:-1,-1:]) #抽取矩阵最后一列(除最后一个元素，作加和)
            else: #判断是不是最后一站
                u=list(poisson_station([Line.up_tuple[number_temp]],tuple(Line.down_tuple[number_temp:]),Time_temp)) 
                #上一行代码或许有坑，运行时绝对要注意
                bus.Matrix[number_temp:number_temp+1,number_temp+1:]=u
                u_temp=np.sum(bus.Matrix[0:number_temp,number_temp:number_temp+1])
                bus.delay=Station_information[ID_list[0]].basic_delay+max(u_temp,sum(u))
                # bus.delay=Station_information[ID_list[0]].basic_delay+np.sum(bus.Matrix[number_temp:numbertemp+1,number_temp+1:])
                #这里直接进行运算的都是numpy类型
    bus.move()
    return bus
      #首先判断停顿，之后再进行运算

def poisson_crossing(u):
    u=np.array(u)
    u_poisson=np.random.poisson(u)
    return u_poisson

def poisson_station(u,v,t):
    u=np.array(u)
    if len(u)!=1:
        u=np.array(0.2)
    v=np.array(v)
    t=np.array(t)
    u_poisson=np.random.poisson(t*(u*v))
    return u_poisson