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
st.set_page_config(page_title="Thu thập GPS - NCKH", page_icon="satellite", layout="wide")
st.title("ỨNG DỤNG THU THẬP DỮ LIỆU GPS")
st.write("Lấy vị trí GPS thực từ điện thoại/máy tính bằng HTML5 Geolocation API")

# ============================
#  GPS – PHIÊN BẢN CUỐI CÙNG (chỉ chạy 1 lần duy nhất)
# ============================
st.subheader("GPS Đang lấy vị trí thực từ thiết bị...")

params = st.query_params

# Chỉ hiển thị JavaScript khi URL chưa có ?lat= và ?lon=
if "lat" not in params or "lon" not in params:
    components.html(
        """
        <script>
        if (!window.location.search.includes('lat=')) {
            const status = document.getElementById('gps_status');
            status.innerHTML = "Đang lấy vị trí GPS (có thể mất 5–45 giây)...";

            navigator.geolocation.getCurrentPosition(
                (pos) => {
                    const lat = pos.coords.latitude.toFixed(6);
                    const lon = pos.coords.longitude.toFixed(6);
                    status.innerHTML = "Thành công! Đang tải lại trang...";
                    const newUrl = `${window.location.pathname}?lat=${lat}&lon=${lon}`;
                    window.location.replace(newUrl);
                },
                (err) => {
                    status.innerHTML = "Không lấy được GPS (tín hiệu yếu hoặc bị chặn). Dùng vị trí gần đúng.";
                },
                {
                    enableHighAccuracy: true,
                    timeout: 45000,
                    maximumAge: 60000
                }
            );
        }
        </script>

        <div id="gps_status" style="padding:18px; background:#331100; color:#ffaaaa; border-radius:10px; margin:20px 0; font-size:17px; text-align:center;">
            Đang khởi động GPS...
        </div>
        """,
        height=130
    )
else:
    # Đã có tọa độ → không hiện gì cả, chỉ để trống
    st.empty()

# ============================
#  ĐỌC TỌA ĐỘ (ưu tiên từ URL → nếu lỗi thì dùng tọa độ nhà bạn)
# ============================
if "lat" in params and "lon" in params:
    try:
        latitude = float(params["lat"][0])
        longitude = float(params["lon"][0])
        st.success("ĐÃ LẤY ĐƯỢC VỊ TRÍ THỰC TẾ TỪ THIẾT BỊ CỦA BẠN!")
    except:
        st.warning("Lỗi định dạng tọa độ → dùng vị trí nhà bạn")
        latitude, longitude = 21.046798, 105.797929  # 167 Hoàng Tăng Bí, Bắc Từ Liêm
else:
    st.warning("Chưa lấy được GPS → hiển thị vị trí gần đúng nhà bạn")
    latitude, longitude = 21.046798, 105.797929  # 167 Hoàng Tăng Bí

# ============================
#  HIỂN THỊ BẢN ĐỒ
# ============================
st.subheader("Bản đồ vị trí hiện tại")
m = Map(location=[latitude, longitude], zoom_start=18)
Marker([latitude, longitude], tooltip="Vị trí của bạn", popup="167 Hoàng Tăng Bí (hoặc GPS thật)").add_to(m)
st_folium(m, width=700, height=550)

# ============================
#  THÔNG TIN GPS
# ============================
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
st.subheader("Thông tin chi tiết")
col1, col2, col3 = st.columns(3)
col1.metric("Vĩ độ", f"{latitude:.6f}")
col2.metric("Kinh độ", f"{longitude:.6f}")
col3.metric("Thời gian", timestamp)

# ============================
#  GỬI DỮ LIỆU
# ============================
st.subheader("Gửi dữ liệu lên server")
server_url = st.text_input("URL API:", "http://localhost:8000/gps")

gps_data = {
    "device_id": "TUAN001",
    "timestamp": timestamp,
    "latitude": round(latitude, 6),
    "longitude": round(longitude, 6),
    "speed": round(random.uniform(0, 50), 1),
    "accuracy": "real_gps" if "lat" in params else "fallback_home",
    "source": "HTML5 Geolocation API"
}

st.json(gps_data)

if st.button("Gửi dữ liệu", type="primary"):
    try:
        r = requests.post(server_url, json=gps_data, timeout=10)
        if r.status_code == 200:
            st.success("GỬI THÀNH CÔNG!")
            st.write(r.json())
        else:
            st.error(f"Lỗi {r.status_code}")
    except Exception as e:
        st.error(f"Không kết nối được: {e}")

st.caption("Đề tài NCKH 2025 – Phạm Nguyễn Tuân – GPS hoạt động trên điện thoại & máy tính")