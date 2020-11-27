from project import *

# Line用于填充候车人数矩阵 Time 用于计算等车人数和时间
def move_bus(bus,Station_information,Crossing_information,Line,Time):
    ID_list=Line.Locate(bus.location)
    if ID_list[0]==ID_list[1]:
        bus.location=bus.location+1
        if ID_list[0]>1000:
            bus.delay=4
        else:
            bus.delay=5+Station_information[ID_list[0]].basic_delay
    bus.move()
    return bus
      #首先判断停顿，之后再进行运算

def poisson(u):
    u_poisson=np.random.poisson(u)
    return u_poisson