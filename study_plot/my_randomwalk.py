from random import choice
class RandomWalk():

    def __init__(self,num=1000):
        self.num=num
        self.x=[0]
        self.y=[0]

    def fill_walk(self):
        while len(self.x)<self.num:
            x_direction=choice([1,-1])
            x_distance=choice([0,1,2,3,4])
            x_step=x_distance*x_direction

            y_direction=choice([1,-1])
            y_distance=choice([0,1,2,3,4])
            y_step=y_distance*y_direction

            if x_step==0 and y_step==0:
                continue
            next_x=self.x[-1]+x_step
            next_y=self.y[-1]+y_step

            self.x.append(next_x)
            self.y.append(next_y)