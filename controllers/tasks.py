import asyncio
import logging
from abc import ABC, abstractmethod
from collections import deque
from contextlib import suppress
from datetime import datetime, timedelta
from inspect import isawaitable
from typing import List

from pony.orm import db_session

import config
from controllers import actions
from models import Port, SSH

logger = logging.getLogger('Tasks')


class ConcurrentTask(ABC):
    def __init__(self):
        self.tasks: List[asyncio.Task] = []
        self.is_running = False
        self._lock = asyncio.Lock()

    @property
    def task_name(self):
        return type(self).__name__

    @property
    @abstractmethod
    def tasks_limit(self):
        """
        Get maximum tasks allowed for the Task.

        :return: Maximum tasks allowed
        """
        raise NotImplementedError

    @abstractmethod
    def get_new_task(self) -> asyncio.Task:
        """
        Get a task to add to the Task.

        :return: New task
        """
        raise NotImplementedError

    async def log(self):
        sleep_duration = 60  # Seconds
        sleep_interval = 0.5  # Seconds

        while self.is_running:
            logger.debug(f"{self.task_name} is running "
                         f"(currently has {len(self.tasks)} tasks)")

            # Use small sleeping intervals to stop sooner when the Task is
            # stopped (e.g. self.running = False)
            for _ in range(int(sleep_duration / sleep_interval)):
                if self.is_running:
                    await asyncio.sleep(sleep_interval)

    async def run(self):
        """
        Run the task's loop (getting new tasks and execute them).
        """
        self.is_running = True
        asyncio.ensure_future(self.log())

        while self.is_running:
            new_task = self.get_new_task()
            if new_task:
                self.tasks.append(new_task)

            while len(self.tasks) >= self.tasks_limit:
                for task in self.tasks[:]:
                    if task.done():
                        await task
                        self.tasks.remove(task)
                await asyncio.sleep(0)

            await asyncio.sleep(0)

        # Cancel running tasks
        for task in self.tasks:
            with suppress(asyncio.CancelledError):
                task.cancel()
                await task

    async def stop(self):
        self.is_running = False


class SyncTask(ABC):
    @abstractmethod
    def run(self) -> asyncio.Task:
        """
        Run task sequentially (in same "thread" with other tasks).
        """
        pass


class SSHCheckTask(ConcurrentTask):
    @property
    def tasks_limit(self):
        conf = config.get_config()
        return conf.getint('SSH', 'tasks_count')

    def get_new_task(self):
        with db_session(retry=3):
            ssh: SSH = SSH.get_need_checking()
            if ssh is not None:
                return asyncio.ensure_future(actions.check_ssh_status(ssh))
            else:
                return None


class PortCheckTask(ConcurrentTask):
    @property
    def tasks_limit(self):
        conf = config.get_config()
        return conf.getint('PORT', 'tasks_count')

    def get_new_task(self):
        with db_session:
            port: Port = Port.get_need_checking()
            if port is not None:
                asyncio.ensure_future(actions.check_port_ip(port))
            else:
                return None


class ConnectSSHToPortTask(SyncTask):
    def run(self):
        port: Port = Port.get_need_ssh()
        ssh: SSH = SSH.select()
        port.connect_to_ssh(ssh)
        logger.info(f"Connecting SSH {ssh.ip} to Port {port.port_number}")
        return asyncio.ensure_future(actions.connect_ssh_to_port(ssh, port))


class ReconnectNewSSHTask(SyncTask):
    def run(self):
        conf = config.get_config()
        if not conf.getboolean('PORT', 'auto_reset_ports'):
            return

        reset_interval = conf.getint('PORT', 'reset_interval')
        time_expired = datetime.now() - timedelta(seconds=reset_interval)
        ports = Port.get_need_reset(time_expired)
        if ports:
            port_numbers = [str(port.port_number) for port in ports]
            logger.info(f"Resetting ports [{','.join(port_numbers)}]")
            return asyncio.ensure_future(actions.reset_ports(ports, ))


class AllTasksRunner(ConcurrentTask):
    def __init__(self):
        super().__init__()
        self.concurrent_tasks = [
            SSHCheckTask(),
            PortCheckTask()
        ]
        self.sync_tasks = deque([
            ConnectSSHToPortTask(),
            ReconnectNewSSHTask()
        ])
        self.tasks = [
            asyncio.ensure_future(task.run()) for task in self.concurrent_tasks
        ]

    @property
    def tasks_limit(self):
        return 50

    def get_new_task(self) -> asyncio.Task:
        for task in self.sync_tasks:
            result = task.run()
            if isawaitable(result):
                self.sync_tasks.rotate(-1)
                return result
