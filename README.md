## portctl

A simple command line tool for inspecting and terminating processes listening on TCP ports.

### Requirements

- Python 3
- Linux (uses `ss` from the `iproute2` package)

> [!WARNING]
> This tool has only been tested on Linux and is not intended for production use.

### Installation

```bash
git clone https://github.com/imPixelity/H1D024090-PraktikumKB-Pertemuan1
cd portctl
bash install.sh
```

This copies `portctl` to `~/bin/`. Make sure `~/bin` is in your `PATH`.

### Usage

```bash
# List all open ports
portctl

# Inspect a specific port
portctl -p <port>

# Inspect and kill the process on a port
portctl -p <port> -k
```

Some operations may require root privileges to display PID information.
