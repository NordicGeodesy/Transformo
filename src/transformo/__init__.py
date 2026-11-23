"""
Transformo - The general purpose tool for determining geodetic transformations
"""

from __future__ import annotations

import asyncio
import logging

__version__ = "0.2.0"

# Logging
console_handler = logging.StreamHandler()
logger = logging.getLogger(__name__)
logger.addHandler(console_handler)
logger.setLevel(logging.WARNING)


# The functions below are all related to running shell commands. It may
# seem overly complicated but there does not seem to be a simpler way to
# capture the STDOUT and STDERR seperately.

async def _log_stdout_to_file(stream, filename):
    with open(filename, "w") as f:
        while not stream.at_eof():
            data = await stream.readline()
            line = data.decode("ascii")
            f.write(line)


async def _log_warning(stream):
    while not stream.at_eof():
        data = await stream.readline()
        line = data.decode("ascii").rstrip()
        logger.warning(line)


async def _log_error(stream):
    while not stream.at_eof():
        data = await stream.readline()
        line = data.decode("ascii").rstrip()
        logger.error(line)


async def _execute(command, *argument):
    proc = await asyncio.create_subprocess_exec(
        command,
        *argument,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    tasks = [
        asyncio.create_task(_log_warning(proc.stdout)),
        asyncio.create_task(_log_error(proc.stderr)),
        asyncio.create_task(proc.wait()),
    ]
    await asyncio.wait(tasks)

    return proc.returncode


def run_command(command: str):
    """Run a command.

    Stdout and stderr utput of command is logged at WARNING and ERROR
    levels respectively.
    """
    cmd = command.split()
    asyncio.run(_execute(cmd[0], *cmd[1:]))


async def _execute_with_input(command, *argument, input_text: str = None):
    proc = await asyncio.create_subprocess_exec(
        command,
        *argument,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        stdin=asyncio.subprocess.PIPE,
    )
    tasks = [
        asyncio.create_task(_log_warning(proc.stdout)),
        asyncio.create_task(_log_error(proc.stderr)),
        asyncio.create_task(proc.wait()),
    ]

    if input_text is not None:
        proc.stdin.write(input_text.encode())
        await proc.stdin.drain()
        proc.stdin.close()  # luk stdin for at signalere EOF til processen

    await asyncio.wait(tasks)

    return proc.returncode


def run_command_with_input(command: str, input_text: str):
    """Run a command.

    Stdout and stderr output of command is logged at WARNING and ERROR
    levels respectively.
    """
    cmd = command.split()
    asyncio.run(_execute_with_input(cmd[0], *cmd[1:], input_text=input_text,))


async def _execute_with_output(command, *argument, output_file: str = None):
    proc = await asyncio.create_subprocess_exec(
        command,
        *argument,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        stdin=asyncio.subprocess.PIPE,
    )
    tasks = [
        asyncio.create_task(_log_stdout_to_file(proc.stdout, output_file)) if output_file is not None else asyncio.create_task(_log_warning(proc.stdout)),
        asyncio.create_task(_log_error(proc.stderr)),
        asyncio.create_task(proc.wait()),
    ]

    await asyncio.wait(tasks)

    return proc.returncode

def run_command_with_output(command: str, output_file: str):
    """Run a command.

    Stdout and stderr output of command is logged at WARNING and ERROR
    levels respectively.
    """
    cmd = command.split()
    asyncio.run(_execute_with_output(cmd[0], *cmd[1:], output_file=output_file,))
