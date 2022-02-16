import asyncio
import os.path
import re
import socket

import psutil


def get_ipv4_address():
    """
    Get this machine's local IPv4 address
    :return: IP address in LAN
    """
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)


def get_free_port():
    """
    Get a free port in local machine
    :return: Port number
    """
    sock = socket.socket()
    sock.bind(('', 0))
    return sock.getsockname()[1]


async def wait_for_db_update(last_updated=0):
    """
    Wait until there is a database query that is not SELECT
    """
    while True:
        modified_time = os.path.getmtime('db.sqlite')
        if last_updated < modified_time:
            return modified_time
        await asyncio.sleep(1)


async def kill_process_on_port(port_number: int):
    """
    Kill all child processes running on given port.

    :param port_number: Target port number
    :return: Whether any child process running on `port_number` is found
    """

    async def run_shell_command(command):
        completed = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE)
        return (await completed.stdout.read()).decode()

    netstat = await run_shell_command("netstat -ano")
    pids = []

    # Get all process pids
    for line in netstat.splitlines():
        try:
            _, local_address, *_, pid = line.split()
        except ValueError:
            continue
        if local_address.endswith(f":{port_number}"):
            pids.append(int(pid))

    child_pids = [p.pid for p in psutil.Process().children(recursive=True)]

    if pids:
        # Kill the processes
        loop = asyncio.get_running_loop()
        for pid in pids:
            if pid in child_pids:
                try:
                    await loop.run_in_executor(
                        None, lambda i: psutil.Process(i).kill(), pid
                    )
                except psutil.NoSuchProcess:
                    pass
        return True
    else:
        return False


def parse_ssh_file(file_content):
    """
    Parse SSH from file content. Expects IP, username, password, delimiting by
    some delimiter.

    :param file_content: Parsing file content
    :return: List of {ip: "...", username: "...", password: "..."}
    """
    results = []
    for line in file_content.splitlines():
        match = re.search(
            r'((?:[0-9]{1,3}\.){3}(?:[0-9]{1,3}))[;,|]([^;,|]*)[;,|]([^;,|]*)',
            line
        )
        if match:
            ip, username, password = match.groups()
            results.append({
                'ip': ip,
                'username': username,
                'password': password
            })
    return results
