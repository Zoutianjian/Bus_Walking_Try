from project import *
from Function import *


def main(): #you can try by using a file to read in

    Station_Dic={
        1:Station(1,5,[498],[-200]),
        2:Station(2,5,[498],[-200]),
        3:Station(3,5,[498],[-200]),
        4:Station(4,5,[498],[-200])
    }

    Crossing_Dic={
        1001:Crossing(1001,15,25,70),
        1002:Crossing(1002,10,15,60),
        1003:Crossing(1003,10,5,70),
    }

    Line_498=Line(498,1)
    Line_498.add_Crossing(1001,100)
    Line_498.add_Station(2,200)
    Line_498.add_Crossing(1002,150)
    Line_498.add_Station(3,200)
    Line_498.add_Crossing(1003,150)
    Line_498.add_Station(4,210)


    Bus_List_498=[Bus(Line_498,2,20015,-1),Bus(Line_498,400,20016,-1)] 
    #一般只针对一条线路打开一个List 现在还不考虑多线路的情形
    #一般情况下，start_time小的车辆会先进站(如果同时进入)

    t=0

    while len(Bus_List_498)!=0:
        Bus_List_498=sorted(Bus_List_498,key=lambda x:x.location,reverse=True) #将数组按照Location由小到大排列
        while Bus_List_498[0].location > Line_498.Length+1 :  
                                        #注意这里出链表的要求和最终到达的细节有关系
                                        #真正结束时，最后一站停站时间并不会被计算在内 有+1则会
            Bus_List_498.pop(0)
            if len(Bus_List_498) ==0:
                break

        for item in Bus_List_498:
            if item.start_time < t:
                item = move_bus(item,Station_Dic,Crossing_Dic,Line_498,t)
        
        t=t+1

if __name__ == "__main__":
    main()