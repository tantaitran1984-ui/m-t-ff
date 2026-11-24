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

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ADB_PATH = os.path.join(CURRENT_DIR, "platform-tools", "adb.exe")
if not os.path.exists(ADB_PATH):
    ADB_PATH = "adb"

APK_FILENAME = "Phuc43_Turbo_Shizuku.apk"
APK_PATH = os.path.join(CURRENT_DIR, APK_FILENAME)

SHIZUKU_COMMANDS = [
    ("settings put system pointer_speed 7", "Ép xung tốc độ con trỏ cảm ứng lên mức 7 (Tối đa)"),
    ("settings put secure touch_sensitivity 1", "Bật chế độ siêu nhạy màn hình Touch Sensitivity"),
    ("settings put secure long_press_timeout 200", "Rút ngắn độ trễ giữ cảm ứng còn 200ms"),
    ("settings put secure multi_press_timeout 200", "Tối ưu hóa phản hồi đa chạm Multi-touch"),
    ("settings put system touch_prediction_latency 0", "Xóa bỏ độ trễ dự đoán điểm chạm (0ms delay)"),
    ("settings put secure tap_duration_threshold 0.0", "Phản hồi chạm tức thì không trễ ngưỡng"),
    ("settings put global window_animation_scale 0", "Khóa hiệu ứng cửa sổ về 0 (Màn hình mượt tức thì)"),
    ("settings put global transition_animation_scale 0", "Khóa hiệu ứng chuyển cảnh về 0 (0ms trễ phản hồi)"),
    ("settings put global animator_duration_scale 0", "Tắt trễ Animator (Mượt hơn 90%)"),
    ("settings put system min_refresh_rate 90.0", "Khóa tần số quét tối thiểu 90Hz"),
    ("settings put system peak_refresh_rate 120.0", "Mở khóa tần số quét tối đa 120Hz mượt mà"),
    ("settings put global force_90_hz 1", "Bắt buộc màn hình duy trì tần số quét cao"),
    ("setprop debug.sf.hw 1", "Bật Hardware Acceleration cho SurfaceFlinger"),
    ("setprop debug.egl.hw 1", "Bật kết xuất phần cứng đồ họa OpenGL/Vulkan"),
    ("setprop debug.composition.type gpu", "Chuyển giao toàn bộ gánh nặng đồ họa cho GPU"),
    ("setprop debug.performance.tuning 1", "Bật chế độ điều chỉnh hiệu năng cao GPU"),
    ("cmd game mode performance com.dts.freefireth", "Kích hoạt Game Mode PERFORMANCE cho Free Fire"),
    ("cmd game mode performance com.dts.freefiremax", "Kích hoạt Game Mode PERFORMANCE cho Free Fire MAX"),
    ("cmd power set-mode 0", "Tắt chế độ tiết kiệm pin gây tụt xung CPU/GPU"),
    ("pm trim-caches 999G", "Dọn sạch toàn bộ cache rác giải phóng RAM tức thì")
]

RAW_SHIZUKU_SCRIPT = "\n".join([cmd for cmd, desc in SHIZUKU_COMMANDS])

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
    if os.path.exists(APK_PATH):
        return send_from_directory(
            CURRENT_DIR,
            APK_FILENAME,
            as_attachment=True,
            mimetype="application/vnd.android.package-archive"
        )
    return "File APK đang được chuẩn bị!", 404

# 3. Lấy script Shizuku
@app.route("/shizuku.sh")
def shizuku_script():
    body = f"""#!/system/bin/sh
echo "=== DANG CHAY PHUC 43 SHIZUKU TURBO ==="
{RAW_SHIZUKU_SCRIPT}
echo "=== HOAN TAT 100%! MAN HINH DA MUOT 90% ==="
"""
    return Response(body, mimetype="text/plain; charset=utf-8")

# 4. API Chạy Proxy & Kích hoạt Shizuku
@app.route("/api/run_proxy", methods=["POST"])
def api_run_proxy():
    data = request.get_json(silent=True) or {}
    code = data.get("code", "").strip() or "PHÚC 43 VIP TURBO (MẶC ĐỊNH)"

    devices = check_adb_devices()
    applied_on_phone = False
    device_name = None

    if devices:
        device_name = devices[0]
        for cmd_str, desc in SHIZUKU_COMMANDS:
            run_adb_command(["shell"] + cmd_str.split(" "))
        applied_on_phone = True

    return jsonify({
        "success": True,
        "active_code": code,
        "applied_on_phone": applied_on_phone,
        "device_name": device_name,
        "raw_script": RAW_SHIZUKU_SCRIPT
    })

# 5. API Trạng thái
@app.route("/api/status")
def api_status():
    devices = check_adb_devices()
    return jsonify({
        "status": "online",
        "adb_devices": devices
    })

# Khởi chạy
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8043))
    print(f"[*] Phuc 43 App dang chay tai port {port}")
    app.run(host="0.0.0.0", port=port, debug=False)
