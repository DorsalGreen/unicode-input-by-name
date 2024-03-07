from __future__ import absolute_import, with_statement

from unicodedb import UnicodeDatabase
import meta

import wx

from threading import Thread, Lock, Semaphore
import logging as log
import traceback

log.getLogger().setLevel(meta.LOG_LEVEL)



class CountRequest(object):
    """Request for counting matching characters."""
    
    def __init__(self, query):
        self.query = query
        
    def __call__(self, db):
        self.count = db.get_count(self.query)
        
    def notify(self, window):
        window.on_get_count_done(self.query, self.count)

        
        
class CharsRequest(object):
    """Requesting for matching characters."""
    
    def __init__(self, query, start, count):
        self.query = query
        self.start = start
        self.count = count
        self.chars = []

    def __call__(self, db):
        rows = db.get_chars(self.query, self.start, self.count)
        #sqlite objects can't cross threads, so the rows are copied
        self.chars = [dict(id=char['id'], name=char['name']) for char in rows]
            
    def notify(self, window):
        window.on_get_chars_done(self.query, self.chars, self.start)
        
    def __eq__(self, other):
        return (other and isinstance(other, self.__class__)
                and self.start == other.start and self.count == other.count)
    
    def __ne__(self, other):
        return not self == other



class IncrementRequest(object):
    """Request for incrementing the usage count of a char"""
    
    def __init__(self, char):
        self.char = char
        
    def __call__(self, db):
        db.increment_frequency(self.char)
        
    def notify(self, window):
        pass



class WorkerThread(Thread):
    def __init__(self, window):
        self.window = window
        self.queue = []
        self.qlock = Lock()
        self.semaphore = Semaphore(0)
        Thread.__init__(self)
        self.setDaemon(True)
        
    def get_count(self, query):
        req = CountRequest(query)
        self._put_request(req, True)
        
    def get_chars(self, query, start, count):
        req = CharsRequest(query, start, count)
        self._put_request(req, True)
        
    def increment_frequency(self, char):
        req = IncrementRequest(char)
        self._put_request(req)
        
    def _put_request(self, request, flush=False):
        with self.qlock:
            if flush:
                self._flush_same_type(request)
            else:
                self._flush_old(request)
            if request in self.queue:
                return
            self.queue.append(request)
            self.semaphore.release()
            
    def _flush_same_type(self, request):
        queue = []
        for req in self.queue:
            if req.__class__ != request.__class__:
                queue.append(req)
        self.queue = queue
        
    def _flush_old(self, request):
        """Flush older requests of the same type, leaving only the most recent
        
        Prevents the queue from becoming to big.
        """
        queue = []
        i = 0
        MAX = 10
        for req in self.queue:
            if req.__class__ != request.__class__:
                queue.append(req)
            else:
                if i < MAX:
                    queue.append(req)
                i += 1
        self.queue = queue
            
    def on_request_done(self, request):
        request.notify(self.window)
                
    def on_program_closed(self):
        #Flush queue, the put a 'None' request in order to end the thread
        with self.qlock:
            while self.queue:
                self.queue.pop()
            self.queue.insert(0, None)
        self.semaphore.release()
        self.join()
    
    def run(self):
        self.db = UnicodeDatabase()
        while True:
            self.semaphore.acquire()
            while True:
                with self.qlock:
                    if not self.queue:
                        break
                    req = self.queue.pop()
                if req is None:
                    #request to end the thread
                    return
                try:
                    #process request
                    req(self.db)
                    wx.CallAfter(self.on_request_done, req)
                except Exception:
                    tb = traceback.format_exc()
                    log.error(tb)
