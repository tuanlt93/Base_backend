import asyncio
from typing import Callable, Awaitable, Dict, Union
from utils.logger import Logger
from .base_tasks import BaseTasks

AsyncFunc = Callable[[], Awaitable]
AsyncInput = Union[AsyncFunc, Awaitable]


class BackgroundTasks(BaseTasks):
    def __init__(self, app):
        self._app = app
        self._tasks: Dict[str, asyncio.Task] = {}

    # =============================================================
    # START MULTIPLE TASKS FROM A DICT
    # =============================================================
    def start_tasks(self, tasks: Dict[str, AsyncInput]):
        for name, func in tasks.items():
            task = self._wrap_and_create(name, func)
            self._tasks[name] = task

        self._sync_to_app()

    # =============================================================
    # START ONE
    # =============================================================
    def start_task(self, name: str, func: AsyncInput):
        task = self._wrap_and_create(name, func)
        self._tasks[name] = task
        self._sync_to_app()

    # =============================================================
    # STOP ONE
    # =============================================================
    def stop_task(self, name: str):
        task = self._tasks.get(name)
        if task:
            task.cancel()
            del self._tasks[name]
            Logger().info(f"[BackgroundTasks] Stopped task: {name}")
        self._sync_to_app()

    # =============================================================
    # STOP ALL
    # =============================================================
    def stop_tasks(self):
        for name, task in list(self._tasks.items()):
            task.cancel()
            Logger().info(f"[BackgroundTasks] Stopped task: {name}")

        self._tasks.clear()
        self._sync_to_app()

    # =============================================================
    # Internal helpers
    # =============================================================
    def _wrap_and_create(self, name: str, func: AsyncInput) -> asyncio.Task:
        """
        Accept either:
        - coroutine
        - async function (callable)
        """
        if asyncio.iscoroutine(func):
            coro = func
        else:
            raise TypeError(
                f"Task '{name}' must be function, got: {type(func)}"
            )

        task = asyncio.create_task(coro)
        Logger().info(f"[BackgroundTasks] Started task: {name}")
        return task

    def _sync_to_app(self):
        self._app.state.sub_tasks = self._tasks
