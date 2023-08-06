# BOTD - python3 IRC channel daemon.
#
# clock module providing timers and repeaters 

import threading
import time
import typing

from botd.dbs import Db
from botd.hdl import Event
from botd.obj import Cfg, Object
from botd.thr import launch
from botd.utl import get_name

# defines

def __dir__():
    return ("Repeater", "Timer", "Timers")

# classes

class Cfg(Cfg):

    def __init__(self):
        super().__init__()
        self.latest =  0
        self.starttime =  0

class Timers(Object):

    def __init__(self, *args, **kwargs):
        super().__init__()
        self._stopped = False
        self.cfg = Cfg()
        self.timers = Object()

    def loop(self):
        while not self._stopped:
            time.sleep(1.0)
            remove = []
            for t in self.timers:
                event = self.timers[t]
                if time.time() > t:
                    self.cfg.latest = time.time()
                    save(self.cfg)
                    event.raw(event.txt)
                    remove.append(t)
            for r in remove:
                del self.timers[r]

    def start(self):
        db = Db()
        for evt in db.all("botd.clk.Timers"):
            e = Event()
            e.update(evt)
            if "done" in e and e.done:
                continue
            if "time" not in e:
                continue
            if time.time() < int(e.time):
                self.timers[e.time] = e
        return launch(self.loop)

    def stop(self):
        self._stopped = True

class Timer(Object):

    def __init__(self, sleep, func, *args, **kwargs):
        super().__init__()
        self.func = func
        self.sleep = sleep
        self.args = args
        self.name = kwargs.get("name", "")
        self.kwargs = kwargs
        self.state = Object()
        self.timer = None

    def start(self):
        if not self.name:
            self.name = get_name(self.func)
        timer = threading.Timer(self.sleep, self.run, self.args, self.kwargs)
        timer.setName(self.name)
        timer.sleep = self.sleep
        timer.state = self.state
        timer.state.starttime = time.time()
        timer.state.latest = time.time()
        timer.func = self.func
        timer.start()
        self.timer = timer
        return timer

    def run(self, *args, **kwargs):
        self.state.latest = time.time()
        launch(self.func, *self.args, **self.kwargs)

    def exit(self):
        if self.timer:
            self.timer.cancel()

class Repeater(Timer):

    def run(self, *args, **kwargs):
        self.func(*args, **kwargs)
        return launch(self.start)
