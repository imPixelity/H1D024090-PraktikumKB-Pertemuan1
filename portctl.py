import os
import re
import subprocess
import signal
import time
import argparse


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
        try:
            opts = input("Do you want to terminate the port? [y/N]: ").strip().lower()
        except KeyboardInterrupt:
            exit(0)

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
                    return
                time.sleep(interval)

            while True:
                try:
                    force = (
                        input("Process still running. Force kill ? [y/N]: ")
                        .strip()
                        .lower()
                    )
                except KeyboardInterrupt:
                    exit(0)

                if force == "y":
                    os.kill(pid, signal.SIGKILL)
                    print("Process terminated")
                    return
                elif force == "n" or force == "":
                    print("Process left running")
                    return
                else:
                    print("Please enter 'y' or 'n'")
        elif opts == "n" or opts == "":
            print("Process left running")
            break
        else:
            print("Please enter 'y' or 'n'")


def main():
    parser = argparse.ArgumentParser(
        description="Portctl is a tool for checking and terminating port in Python."
    )

    parser.add_argument("-p", "--port", type=int, required=True, help="Port to inspect")
    parser.add_argument("-k", "--kill", action="store_true", help="Port to terminate")

    args = parser.parse_args()
    pid = check_port_usage(args.port)

    if pid is not None and args.kill:
        terminate_socket_listener(int(pid))


main()
