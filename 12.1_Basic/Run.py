from project import *
from Function import *


def main(): #you can try by using a file to read in

    Station_Dic={
        1:Station(1,3,[498],[-400]), #注意这里要求是列表形式
        2:Station(2,3,[498],[-400]),
        3:Station(3,3,[498],[-400]),
        4:Station(4,3,[498],[-400]), #注意这里的ID号是唯一标识，必须相同
        5:Station(5,3,[498],[-400]),
        6:Station(6,3,[498],[-400]),
        7:Station(7,3,[498],[-400]),
        8:Station(8,3,[498],[-400]),
        9:Station(9,3,[498],[-400]),
        10:Station(10,3,[498],[-400])
    }

    Crossing_Dic={
        1001:Crossing(1001,20,23,50),
        1002:Crossing(1002,20,52,60),
        1003:Crossing(1003,8,4,40),
        1004:Crossing(1004,15,33,40),
        1005:Crossing(1005,15,42,50),
        1006:Crossing(1006,20,15,80),
        1007:Crossing(1007,5,14,20),
        1008:Crossing(1008,10,12,30),
    }

    Line_498=Line(498,1) #有个问题，Station等候时间需要去Line里查询
    Line_498.add_Crossing(1001,70)
    Line_498.add_Station(2,140)
    Line_498.add_Crossing(1002,150)
    Line_498.add_Station(3,140)
    Line_498.add_Crossing(1003,150)
    Line_498.add_Station(4,150) #线路初始化只有一次机会，后面再改则必出问题！！
    Line_498.add_Crossing(1004,120)
    Line_498.add_Station(5,80)
    Line_498.add_Station(6,280)
    Line_498.add_Crossing(1005,110)
    Line_498.add_Station(7,80)
    Line_498.add_Crossing(1006,180)
    Line_498.add_Station(8,100)
    Line_498.add_Crossing(1007,120)
    Line_498.add_Station(9,100)
    Line_498.add_Crossing(1008,110)
    Line_498.add_Station(10,80)
    Line_498.passenger_initial()
    # please don't modified Line after this 

    Bus_List_498=[
        Bus(Line_498,2,43461,-1),
        Bus(Line_498,402,43462,-1),
        Bus(Line_498,802,43463,-1),
        Bus(Line_498,1202,43464,-1),
        Bus(Line_498,1602,43465,-1),
        Bus(Line_498,2002,43466,-1),
        Bus(Line_498,2402,43467,-1),
        Bus(Line_498,2802,43468,-1),
        Bus(Line_498,3202,43469,-1),
        Bus(Line_498,3602,43470,-1)
    ] 

    bus_amount=len(Bus_List_498)
    ans_Matrix=np.zeros((bus_amount,Line_498.number_station(),Line_498.number_station()),int)
    Line_498.number_station()
    #一般只针对一条线路打开一个List 现在还不考虑多线路的情形
    #一般情况下，start_time小的车辆会先进站(如果同时进入)

    t=0

    while len(Bus_List_498)!=0:
        Bus_List_498=sorted(Bus_List_498,key=lambda x:x.location,reverse=True) #将数组按照Location由小到大排列
        while Bus_List_498[0].location > Line_498.Length+1 :  
                                        #注意这里出链表的要求和最终到达的细节有关系
                                        #真正结束时，最后一站停站时间并不会被计算在内 有+1则会

            ans_Matrix[bus_amount-len(Bus_List_498):bus_amount-len(Bus_List_498)+1,:,:]=Bus_List_498[0].Matrix
            ans_Matrix[bus_amount-len(Bus_List_498)][0][0]=Bus_List_498[0].ID
            Bus_List_498.pop(0)
            if len(Bus_List_498) ==0:
                break

        for item in Bus_List_498:
            if item.start_time < t:
                item = move_bus(item,Station_Dic,Crossing_Dic,Line_498,t) #注意，这里传列表时传递的是实参
        
        t=t+1
    
    np.save('test.npy',ans_Matrix)
    return 0

if __name__ == "__main__":
    main()