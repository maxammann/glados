from threading import Condition, Lock
from io import BytesIO


class ByteBufferQueue:
    def __init__(self):
        lock = Lock()
        self.condition = Condition(lock)
        self.buffer = BytesIO()
        self.destroyed = False
        pass

    def destroy(self):
        self.condition.acquire()
        self.destroyed = True
        self.condition.notify()
        self.condition.release()

    def append(self, bytes):
        self.condition.acquire()

        self.buffer.write(bytes)

        self.condition.notify()
        self.condition.release()
        pass

    def pop(self):
        buf = None
        self.condition.acquire()
        while True:
            if self.destroyed:
                buf = None
                break

            buf = self.buffer.getvalue()

            if buf:
                # clear our buffer
                self.buffer = BytesIO()
                break
            self.condition.wait()

        self.condition.release()
        return buf
