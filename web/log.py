# log management

import sys

def log_error(msg:str ="ERROR") -> None:
    print("[CRITICAL ERROR]", msg)
    sys.exit(1)

def log_warn(msg:str ="WARNING") -> None:
    print("[WARNING]", msg)

def log_info(msg:str ="INFO") -> None:
     print("[info]", msg)

