from threading import Lock

class Singleton(type):
    """
    Create a class which only init once
    Instruction:
        class foo(metaclass=Singleton)
    """
    __instance = {}
    __lock = Lock()
    def __call__(cls, *args, **kwds):
        if cls not in cls.__instance:
            with cls.__lock:
                if cls not in cls.__instance:
                    instance = super().__call__(*args, **kwds)
                    cls.__instance[cls] = instance
        return cls.__instance[cls]
    