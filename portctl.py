import subprocess


def process_sockets(user_port):
    ss_result = subprocess.run(["ss", "-lntpH"], capture_output=True, text=True)

    socket_rows = ss_result.stdout.splitlines()

    is_used = False
    for row in socket_rows:
        fields = row.split()
        local_address_port = fields[3]
        local_port = local_address_port.rsplit(":", 1)[1]
        if str(user_port) == local_port:
            print(f"Port {local_port} is used")
            is_used = True
            break
    if not (is_used):
        print(f"Port {user_port} is free")
