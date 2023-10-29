# QReye

a simple script to fix the missing/broken eyes in the QR code



```bash
   ███████    ███████
  ██░░░░░██  ░██░░░░██           ██   ██
 ██     ░░██ ░██   ░██   █████  ░░██ ██   █████
░██      ░██ ░███████   ██░░░██  ░░███   ██░░░██
░██    ██░██ ░██░░░██  ░███████   ░██   ░███████
░░██  ░░ ██  ░██  ░░██ ░██░░░░    ██    ░██░░░░
 ░░███████ ██░██   ░░██░░██████  ██     ░░██████
  ░░░░░░░ ░░ ░░     ░░  ░░░░░░  ░░       ░░░░░░    v0.1

                python QReye.py -h [FOR HELP]

usage: QReye.py [-h] FILE

positional arguments:
  FILE        QR image file to fix

options:
  -h, --help  show this help message and exit
```



## Installation

clone the repository and install the requirment `Pillow`



## Todos

- [ ] better broken eye detection (The current script cannot check if the existing eyes are valid)