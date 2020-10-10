import threading


class SingletonType(type):
    _instance_lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with SingletonType._instance_lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = super(SingletonType, cls).__call__(*args, **kwargs)
        return cls._instance


class MyClass(metaclass=SingletonType):
    def __init__(self):
        self.incr = 0

    def add(self):
        self.incr += 1


if __name__ == '__main__':
    MyClass().a = 2
    print(MyClass().a)
