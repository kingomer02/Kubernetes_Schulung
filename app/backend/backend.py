from flask import Flask
import socket
import os
from datetime import datetime

hostname = os.uname()[1]
ips = socket.gethostbyname_ex(hostname)[2]
app_version = os.getenv("APP_VERSION", "dev")


app = Flask(__name__)


@app.route('/health')
def health():
    return {"status": "ok", "version": app_version, "hostname": hostname}


@app.route('/')
def index():
    os.makedirs("/data", exist_ok=True)
    with open("/data/access.log", "a+") as f:
        f.write(f"{datetime.now()}: IP: {ips} \n")

    return {
        "ip": str(ips),
        "hostname": hostname,
        "version": app_version,
        "username": "root",
        "now": datetime.now().isoformat(),
    }


app.run(host="0.0.0.0", port=80, debug=False)
