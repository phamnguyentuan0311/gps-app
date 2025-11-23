import streamlit as st
import requests
import datetime
import random
from folium import Map, Marker
from streamlit_folium import st_folium
import streamlit.components.v1 as components

# ============================
#  PAGE CONFIG
# ============================
st.set_page_config(page_title="Ứng dụng thu thập GPS", page_icon="🛰️", layout="wide")
st.title("🛰️ ỨNG DỤNG THU THẬP DỮ LIỆU GPS")
st.write("Ứng dụng lấy vị trí GPS thật từ thiết bị của bạn bằng HTML5 Geolocation API.")

# ============================
# 3.1 — MODULE ĐỌC DỮ LIỆU GPS
# ============================
st.subheader("📡 Đang lấy vị trí thực từ thiết bị...")

# JavaScript lấy vị trí thật
components.html(
    """
    <script>
        navigator.geolocation.getCurrentPosition(
            (pos) => {
                const lat = pos.coords.latitude;
                const lon = pos.coords.longitude;
                const url = new URL(window.location.href);

                url.searchParams.set("lat", lat);
                url.searchParams.set("lon", lon);

                window.location.href = url.toString();
            },
            (err) => {
                console.log("GPS error:", err);
            }
        );
    </script>
    """,
    height=0
)

# Nhận dữ liệu GPS từ query params
params = st.query_params

if "lat" in params and "lon" in params:
    latitude = float(params["lat"][0])
    longitude = float(params["lon"][0])
    st.success("✅ Đã lấy được vị trí thực của thiết bị!")
else:
    st.warning("⚠ Không thể lấy vị trí – hiển thị vị trí mặc định (Hà Nội).")
    latitude = 21.0285
    longitude = 105.8542

# ============================
# HIỂN THỊ BẢN ĐỒ
# ============================
st.subheader("📍 Bản đồ vị trí hiện tại")

m = Map(location=[latitude, longitude], zoom_start=17)
Marker([latitude, longitude], tooltip="Vị trí hiện tại").add_to(m)

st_folium(m, width=700, height=450)

# ============================
# HIỂN THỊ THÔNG TIN GPS
# ============================
timestamp = datetime.datetime.now().isoformat()
st.subheader("🧭 Thông tin GPS hiện tại")

col1, col2, col3 = st.columns(3)
col1.metric("Vĩ độ", f"{latitude:.6f}")
col2.metric("Kinh độ", f"{longitude:.6f}")
col3.metric("Thời gian", timestamp[:19])

# ============================
# GỬI DỮ LIỆU GPS VỀ SERVER
# ============================
st.subheader("📤 Gửi dữ liệu GPS đến server")
server_url = st.text_input("Nhập URL API:", "http://localhost:8000/gps")

gps_data = {
    "device_id": "TUAN001",
    "timestamp": timestamp,
    "latitude": latitude,
    "longitude": longitude,
    "speed": random.uniform(0, 12),
    "traffic_light_id": "TL005",
    "day_type": "weekday"
}

st.json(gps_data)

if st.button("🚀 Gửi dữ liệu"):
    try:
        response = requests.post(server_url, json=gps_data)
        if response.status_code == 200:
            st.success("🎉 Gửi dữ liệu thành công!")
            st.write("Phản hồi server:", response.json())
        else:
            st.error(f"⚠ Lỗi server: {response.status_code}")
    except Exception as e:
        st.error(f"Lỗi kết nối: {e}")

st.caption("Ứng dụng phục vụ đề tài NCKH — Thu thập dữ liệu GPS thực từ thiết bị.")
