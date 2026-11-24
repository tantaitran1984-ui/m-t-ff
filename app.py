"""
=============================================================================
             PHÚC 43 - PROXY FF & SHIZUKU GAMING OPTIMIZER
     Chuẩn Framework Flask & Gunicorn dành cho Render.com & Local PC
=============================================================================
"""

import os
import sys
import json
import time
import subprocess
from flask import Flask, send_from_directory, jsonify, request, Response

app = Flask(__name__, static_folder=".", static_url_path="")

@app.after_request
def add_api_cors_headers(response):
    if request.path.startswith("/api/"):
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ADB_PATH = os.path.join(CURRENT_DIR, "platform-tools", "adb.exe")
if not os.path.exists(ADB_PATH):
    ADB_PATH = "adb"

APK_FILENAME = "Phuc43_Turbo_Shizuku.apk"
APK_PATH = os.path.join(CURRENT_DIR, APK_FILENAME)

SHIZUKU_COMMANDS = []

RAW_SHIZUKU_SCRIPT = "# Không có lệnh tối ưu giả lập; cần Shizuku hoặc thiết bị ADB được kết nối."

def run_adb_command(cmd_args):
    try:
        full_cmd = [ADB_PATH] + cmd_args
        res = subprocess.run(full_cmd, capture_output=True, text=True, timeout=6)
        return res.returncode == 0, res.stdout.strip()
    except Exception as e:
        return False, str(e)

def check_adb_devices():
    success, output = run_adb_command(["devices"])
    if not success or not output:
        return []
    devices = []
    lines = output.split("\n")
    for line in lines[1:]:
        parts = line.strip().split()
        if len(parts) >= 2 and parts[1] == "device":
            devices.append(parts[0])
    return devices

# 1. Trang chủ chính - Phục vụ file index.html
@app.route("/")
def index():
    return send_from_directory(CURRENT_DIR, "index.html")

# 2. Tải APK trực tiếp về điện thoại
@app.route("/download_apk")
@app.route("/Phuc43_Turbo_Shizuku.apk")
@app.route("/phuc43.apk")
def download_apk():
    apk_path = os.path.join(CURRENT_DIR, "Phuc43_Proxy.apk")
    if os.path.exists(apk_path):
        return send_from_directory(
            CURRENT_DIR,
            "Phuc43_Proxy.apk",
            as_attachment=True,
            mimetype="application/vnd.android.package-archive"
        )
    return "APK Phuc43 Proxy chưa được build.", 404

# 3. Lấy script Shizuku
@app.route("/shizuku.sh")
def shizuku_script():
    body = "# Chưa cấu hình thiết bị. Không chạy lệnh tối ưu giả lập.\n"
    return Response(body, mimetype="text/plain; charset=utf-8")

# 4. API Chạy Proxy & Kích hoạt Shizuku
@app.route("/api/run_proxy", methods=["POST", "OPTIONS"])
def api_run_proxy():
    if request.method == "OPTIONS":
        return "", 204
    data = request.get_json(silent=True) or {}
    code = data.get("code", "").strip()

    devices = check_adb_devices()
    if not devices:
        return jsonify({
            "success": False,
            "applied_on_phone": False,
            "device_name": None,
            "msg": "Chưa có điện thoại ADB kết nối. Bật Gỡ lỗi USB hoặc Gỡ lỗi không dây rồi kết nối trong Shizuku."
        })

    return jsonify({
        "success": False,
        "active_code": code,
        "applied_on_phone": False,
        "device_name": devices[0],
        "msg": "Thiết bị đã được ADB nhận diện, nhưng chưa có app Android Shizuku companion. Không thể thay đổi cấu hình hoặc gán proxy tự động."
    })

# 5. API Trạng thái
@app.route("/api/status")
def api_status():
    devices = check_adb_devices()
    return jsonify({
        "status": "online",
        "adb_devices": devices,
        "connected": len(devices) > 0
    })

# Khởi chạy
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8043))
    print(f"[*] Phuc 43 App dang chay tai port {port}")
    app.run(host="0.0.0.0", port=port, debug=False)
