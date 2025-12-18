from flask import Flask
import socket
import os
import requests
from datetime import datetime


hostname = os.uname()[1]
ips = socket.gethostbyname_ex(hostname)[2]

# port = os.getenv("FRONTEND_PORT")
# port = 5000
backend_url = os.getenv("BACKEND_URL", "http://backend:80")
bg_color = os.getenv("BG_COLOR", "green")
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

    backend_response = requests.get(backend_url).text

    try:
        backend_response = requests.get(backend_url, timeout=2).text
    except Exception as e:
        backend_response = f"ERROR calling backend ({backend_url}): {e}"
    # backend_response = "Backend is coming later!"
    # backend_response = "Not yet!"
    return (
        f"<html style='background:{bg_color}; font-family: sans-serif;'>"
        f"<h2>Sushi‑Bar Frontend Hallo ({app_version})</h2>"
        f"<p><b>Pod:</b> {hostname} | <b>IP:</b> {ips}</p>"
        f"<p><b>Backend URL:</b> {backend_url}</p>"
        f"<pre style='background:#fff; padding:12px; border-radius:8px;'>"
        f"{backend_response}"
        f"</pre>"
        f"</html>"
    )


app.run(host="0.0.0.0", port=80, debug=False)
