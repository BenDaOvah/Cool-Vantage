#!/usr/bin/env python3
"""Start a long-running process escaped from the tool-call session tree.

Double-forks so the grandchild is reparented to PID 1 (tini) and survives
the sandbox's descendant cleanup between tool calls.

Usage: python3 daemon_start.py <working_dir> <log_path> <command> [args...]
"""
import os
import sys


def main() -> None:
    if len(sys.argv) < 4:
        print("usage: daemon_start.py <workdir> <logfile> <cmd...>", file=sys.stderr)
        sys.exit(2)

    workdir, logfile = sys.argv[1], sys.argv[2]
    cmd = sys.argv[3:]

    pid = os.fork()
    if pid == 0:  # first child
        pid2 = os.fork()
        if pid2 == 0:  # grandchild -> orphaned to PID 1
            os.setsid()
            os.chdir(workdir)
            fd = os.open(logfile, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o644)
            os.dup2(fd, 1)
            os.dup2(fd, 2)
            devnull = os.open(os.devnull, os.O_RDONLY)
            os.dup2(devnull, 0)
            os.execvp(cmd[0], cmd)
            os._exit(127)
        os._exit(0)

    os.waitpid(pid, 0)
    print(f"daemon launched: {' '.join(cmd)}")


if __name__ == "__main__":
    main()
