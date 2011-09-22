
from threading import Thread, Lock

class RoboException(Exception):
    """ Exception which gets raised when there is a need to stop executing the
        RoboThread.
    """

class RoboThread(Thread):
    func = None
    args = ()
    kwargs = {}
    
    def __init__(self, target, args = (), kwargs = {}, cleaner = None):
        Thread.__init__(self)

        self.func = target
        self.args = args
        self.kwargs = kwargs
        self.cleaner = cleaner

    def run(self):
        
        try:
            self.func(*self.args, **self.kwargs)
            
        except RoboException:
            pass

        if self.cleaner is not None:
            self.cleaner()
