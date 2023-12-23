from .config import CONFIG
from .peralog import logdir
from typing import Optional
import requests


def send_report(info: Optional[str] = ""):
    with open(logdir.joinpath("peracotta.log"), "rb") as fs:
        files = {"file": (fs.name, fs, "peracotta/error-log")}
        response = requests.put(CONFIG["REPORT_URL"], files=files)
