from collections import deque
from random import randint
from time import sleep


def prime(func):
    def wrapper(*args, **kwargs):
        v = func(*args, **kwargs)
        v.send(None)
        return v

    return wrapper


class FSM:
    def __init__(self):
        self.start = self.__create_start()
        self.s1 = self.__eating_state()
        self.s2 = self.__study_state()
        self.s22 = self.__study_state_two()
        self.s3 = self.__chill_state()
        self.s4 = self.__coffee_state()

        self.current_state = self.start

    def send(self, event):
        self.current_state.send(event)

    @prime
    def __create_start(self):
        while True:
            event = yield
            if 6 < event[0] < 22:
                print(event[0], "time to grab some food")
                self.current_state = self.s2
            else:
                print(event[0], "Sleeping...")
                self.current_state = self.start

    @prime
    def __eating_state(self):
        while True:
            event = yield
            if event[1] == "not much work":
                print(event[0], "Not much to do, gotta take a nap")
                self.current_state = self.start
            else:
                print(event[0], "Time to study")
                self.current_state = self.s2

    @prime
    def __study_state(self):
        while True:
            event = yield
            print(event[0], "One hour of studying passed")
            self.current_state = self.s22

    @prime
    def __study_state_two(self):
        while True:
            event = yield
            if 20 < event[0] or event[0] < 7:
                print(event[0], "Time to sleep")
                self.current_state = self.start
            elif event[0] in (7, 13, 18):
                print(event[0], "Time to eat")
                self.current_state = self.s1
            elif event[2] == "feeling good":
                print(event[0], "I love studying so much, one more hour")
                self.current_state = self.s22
            elif event[3] == "sleepy":
                print(event[0], "I am too sleepy, wanna get some coffee")
                self.current_state = self.s4
            else:
                print(
                    event[0],
                    "Nice session, time to refresh my mind and chill a little bit",
                )
                self.current_state = self.s3

    @prime
    def __chill_state(self):
        while True:
            event = yield
            if 20 < event[0] or event[0] < 7:
                print(event[0], "Time to sleep")
                self.current_state = self.start
            elif event[0] in (7, 13, 18):
                print(event[0], "Time to eat")
                self.current_state = self.s1
            else:
                print(event[0], "Time to study")
                self.current_state = self.s2

    @prime
    def __coffee_state(self):
        while True:
            event = yield
            if 20 < event[0] or event[0] < 7:
                print(event[0], "Time to sleep")
                self.current_state = self.start
            elif event[0] in (7, 13, 18):
                print(event[0], "Time to eat")
                self.current_state = self.s1
            elif event[4] == "no use of coffee":
                print(event[0], "Even coffee can't wake me up, I am so tired")
                self.current_state = self.start
            else:
                print(event[0], "Coffee refreshed me, guess I will take a walk")
                self.current_state = self.s3


if __name__ == "__main__":
    my_life = FSM()
    queue = deque([(0, "much work", "feeling good", "", "")])
    curr_hour = 0
    while True:
        my_life.send(queue.popleft())
        curr_hour += 1
        curr_hour %= 24
        next_hour = [curr_hour, "", "", "", ""]
        if randint(1, 10) == 1:
            next_hour[1] = "not much work"
        if randint(1, 10) <= 5:
            next_hour[2] = "feeling good"
        if randint(1, 10) <= 6:
            next_hour[3] = "sleepy"
        if randint(1, 10) <= 2:
            next_hour[4] = "no use of coffee"

        queue.append(tuple(next_hour))
        sleep(1)
