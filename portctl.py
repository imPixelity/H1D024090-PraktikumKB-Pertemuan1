import os
import re
import subprocess
import signal
import time


def check_port_usage(user_port):
    ss_result = subprocess.run(["ss", "-lntpH"], capture_output=True, text=True)

    socket_rows = ss_result.stdout.splitlines()

    is_used = False
    pid_regex = ""
    for row in socket_rows:
        fields = row.split()
        local_address_port = fields[3]
        local_port = local_address_port.rsplit(":", 1)[1]

        if str(user_port) == local_port:
            # regex for pid in ss
            pid_regex = re.search(r"pid=(\d+)", fields[5])
            print(f"Port {local_port} is being used")
            is_used = True

        if pid_regex:
            local_pid = pid_regex.group(1)
            return local_pid
    if not (is_used):
        print(f"Port {user_port} is free")
        return None


def terminate_socket_listener(pid):
    while True:
        opts = input("Do you want to terminate the port? [y/N]: ").strip().lower()

        if opts == "y":
            print("Sending SIGTERM...")
            os.kill(pid, signal.SIGTERM)

            timeout = 3
            interval = 0.5

            for _ in range(int(timeout / interval)):
                try:
                    # check if pid still alive
                    os.kill(pid, 0)
                except ProcessLookupError:
                    print("Process terminated gracefully")
                    break
                time.sleep(interval)

            # TODO: SIGKILL, force kill
            break
        elif opts == "n" or opts == "":
            print("nossir")
            break
        else:
            print("Please enter 'y' or 'n'")


pid = check_port_usage(5173)
print(pid)
if pid is not None:
    terminate_socket_listener(int(pid))

