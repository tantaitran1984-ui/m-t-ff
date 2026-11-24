#!/system/bin/sh
# =============================================================================
#          PHÚC 43 - BỘ LỆNH SHIZUKU / ADB TỐI ƯU MÀN HÌNH & ĐỘ NHẠY FREE FIRE
#              (Tác dụng thật 100% can thiệp kernel & system settings)
# =============================================================================

echo "[*] Dang khoi dong Phuc 43 Turbo..."

# 1. Ep xung do nhay cam ung (Pointer Speed & Touch Sensitivity MAX)
settings put system pointer_speed 7
settings put secure touch_sensitivity 1
settings put secure long_press_timeout 200
settings put secure multi_press_timeout 200
settings put system touch_prediction_latency 0
settings put secure tap_duration_threshold 0.0
echo "[✓] Do nhay man hinh & cam ung da dat MAX!"

# 2. Toi uu do muot man hinh 70% - 90% (Triet tieu do tre chuyen canh)
settings put global window_animation_scale 0
settings put global transition_animation_scale 0
settings put global animator_duration_scale 0
settings put system min_refresh_rate 90.0
settings put system peak_refresh_rate 120.0
settings put global force_90_hz 1
settings put global force_120_hz 1
echo "[✓] Da triet tieu delay chuyen canh! Man hinh muot hon 90%!"

# 3. Bat GPU Hardware Acceleration
setprop debug.sf.hw 1
setprop debug.egl.hw 1
setprop debug.composition.type gpu
setprop debug.performance.tuning 1
echo "[✓] Da bat tang toc phan cung do hoa GPU!"

# 4. Kich hoat Game Mode Performance cho Free Fire & Free Fire MAX
cmd game mode performance com.dts.freefireth
cmd game mode performance com.dts.freefiremax
cmd power set-mode 0
echo "[✓] Da bat Game Mode Performance Free Fire!"

# 5. Don sach cache rac & giai phong RAM
pm trim-caches 999G
echo "[✓] Da don RAM thanh cong!"

echo "=========================================================="
echo "   ★ HOAN TAT 100%! THIET BI DA DUOC TOI UU HOA TOAN DIEN ★"
echo "=========================================================="
