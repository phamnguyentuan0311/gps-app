import streamlit as st
import requests
import datetime
from folium import Map, Marker
from streamlit_folium import st_folium
import streamlit.components.v1 as components

st.set_page_config(page_title="GPS NCKH - Tuấn", page_icon="satellite", layout="centered")
st.title("satellite THU THẬP GPS THỰC TẾ TỪ LAPTOP & ĐIỆN THOẠI")
st.markdown("**Luôn lấy đúng vị trí bạn đang ngồi – tối ưu cho laptop có GPS**")

# ============================ CHỈ CHẠY KHI CHƯA CÓ TỌA ĐỘ ============================
params = st.query_params

if "lat" not in params or "lon" not in params:
    st.info("Nhấn nút bên dưới → Cho phép GPS → Chờ 5–40 giây để lấy vị trí")

    if st.button("LẤY VỊ TRÍ THỰC TẾ NGAY", type="primary", use_container_width=True):
        components.html("""
        <script>
        const status = document.getElementById('gps_status');
        status.innerHTML = "Đang kích hoạt GPS của laptop/điện thoại (5–40 giây)...";

        // Thử lấy GPS với độ chính xác cao nhất
        navigator.geolocation.getCurrentPosition(
            pos => {
                const lat = pos.coords.latitude.toFixed(7);
                const lon = pos.coords.longitude.toFixed(7);
                status.innerHTML = "Thành công! Đang cập nhật bản đồ...";
                const url = new URL(window.location);
                url.searchParams.set('lat', lat);
                url.searchParams.set('lon', lon);
                window.location.replace(url);
            },
            err => {
                status.innerHTML = `
                    Không lấy được GPS (lỗi ${err.code}).<br>
                    <small>Nguyên nhân:<br>
                    • Chưa bật GPS trên laptop/điện thoại<br>
                    • Trình duyệt chặn quyền<br>
                    • Tín hiệu yếu (thử ra chỗ thoáng)</small>
                `;
            },
            { 
                enableHighAccuracy: true, 
                timeout: 45000, 
                maximumAge: 0 
            }
        );
        </script>
        <div id="gps_status" style="padding:20px; background:#440000; color:#ff9999; border-radius:12px; text-align:center; font-size:18px; margin:20px 0;">
            Đang chờ bạn bấm nút...
        </div>
        """, height=180)
    
    st.stop()  # Dừng cho đến khi có tọa độ

# ============================ ĐÃ CÓ TỌA ĐỘ → HIỂN THỊ ============================
latitude = float(params["lat"][0])
longitude = float(params["lon"][0])

st.success(f"ĐÃ LẤY ĐƯỢC VỊ TRÍ THỰC TẾ!\nVĩ độ: {latitude:.7f} | Kinh độ: {longitude:.7f}")

# Bản đồ
st.subheader("Bản đồ vị trí bạn đang ngồi")
m = Map(location=[latitude, longitude], zoom_start=19)
Marker([latitude, longitude], popup="Vị trí thực tế của bạn!", tooltip="Đúng chỗ bạn đang ở").add_to(m)
st_folium(m, width=800, height=600)

# Thông tin
st.subheader("Thông tin GPS")
st.metric("Thời gian cập nhật", datetime.datetime.now().strftime("%H:%M:%S - %d/%m/%Y"))

# Nút làm mới
if st.button("Lấy vị trí mới", type="secondary"):
    st.query_params.clear()
    st.rerun()

st.balloons()
st.caption("NCKH 2025 – Phạm Nguyễn Tuấn – GPS chạy 100% từ laptop có GPS")