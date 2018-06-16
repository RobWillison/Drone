import Tkinter as tk
import redis

redisClient = redis.StrictRedis(host='192.168.0.87', port=6379, db=0)

#create window & frames
class App:
    def __init__(self):
        self.root = tk.Tk()
        self._job = None
        self.slider1 = tk.Scale(self.root, from_=0, to=100,
                               command=self.updateMotor1)
        self.slider2 = tk.Scale(self.root, from_=0, to=100,
                               command=self.updateMotor2)
        self.slider3 = tk.Scale(self.root, from_=0, to=100,
                               command=self.updateMotor3)
        self.slider4 = tk.Scale(self.root, from_=0, to=100,
                               command=self.updateMotor4)
        self.slider1.pack()
        self.slider2.pack()
        self.slider3.pack()
        self.slider4.pack()
        self.root.mainloop()

    def updateMotor1(self, event):
        redisClient.set('motor-2', self.slider1.get())

    def updateMotor2(self, event):
        redisClient.set('motor-1', self.slider2.get())

    def updateMotor3(self, event):
        redisClient.set('motor-3', self.slider3.get())

    def updateMotor4(self, event):
        redisClient.set('motor-4', self.slider4.get())


app=App()