import threading
from time import sleep

class Root(object):
    def __init__(self):
        self.value = 0
        if not hasattr(self, 'watch_tread'):
            _thread = threading.Thread(target=self._monitor)
            _thread.setDaemon(True)
            _thread.start()
            self.watch_tread = True
            print "Started BG thread"
            
    def index(self):
        return 'Hello World! '+str(self.value)

    def _monitor(self):
        while 1:
            self.value += 1
            sleep(1)
    
    index.exposed = True
