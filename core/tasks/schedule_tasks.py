from utils.logger import Logger
from utils.threadpool import Worker
from .base_tasks import BaseTasks
from typing import Callable
import schedule
import time


class ScheduleTasks(BaseTasks):
    def __init__(self):
        self.__is_app_running = False
        self.__funcs: Callable = None

    def start_tasks(self, *funcs: Callable):
        self.__funcs = funcs
        self.__is_app_running = True
        self.__run_schedule()

    def stop_tasks(self):
        self.__is_app_running = False

    @Worker.employ
    def __run_schedule(self):
        Logger().info("SCHEDUAL START")
        schedule.every().minute.at("30").do(self.__funcs())
        while self.__is_app_running:
            schedule.run_pending()
            time.sleep(30) 