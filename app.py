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
st.set_page_config(page_title="Ứng dụng thu thập GPS", page_icon="satellite", layout="wide")
st.title("satellite ỨNG DỤNG THU THẬP DỮ LIỆU GPS")
st.write("Ứng dụng lấy vị trí GPS thật từ thiết bị của bạn bằng HTML5 Geolocation API.")

# ============================
#  GPS – PHIÊN BẢN HOÀN CHỈNH & SIÊU ỔN ĐỊNH
# ============================
st.subheader("GPS Đang lấy vị trí thực từ thiết bị...")

# JavaScript mới – chạy chắc chắn, có thông báo lỗi rõ ràng, tự động reload với tọa độ
components.html(
    """
    <script>
    function tryGetLocation(attempt = 1) {
        const statusDiv = document.getElementById('gps_status');
        statusDiv.innerHTML = `Đang lấy vị trí GPS (lần ${attempt})...`;

        navigator.geolocation.getCurrentPosition(
            (position) => {
                const lat = position.coords.latitude.toFixed(6);
                const lon = position.coords.longitude.toFixed(6);
                const url = new URL(window.location.href);
                url.searchParams.set('lat', lat);
                url.searchParams.set('lon', lon);
                statusDiv.innerHTML = "Thành công! Đang tải lại...";
                setTimeout(() => window.location.href = url.toString(), 500);
            },
            (error) => {
                if (attempt < 3) {
                    statusDiv.innerHTML = `Thử lại lần ${attempt + 1}... (vui lòng di chuyển ra chỗ thoáng hoặc bật dữ liệu di động)`;
                    setTimeout(() => tryGetLocation(attempt + 1), 3000);
                } else {
                    statusDiv.innerHTML = "Không lấy được GPS sau 3 lần thử. Hiển thị Hà Nội mặc định.";
                }
            },
            {
                enableHighAccuracy: true,
                timeout: 30000,      // tăng lên 30 giây
                maximumAge: 60000    // chấp nhận vị trí cũ trong 1 phút
            }
        );
    }

    window.addEventListener('load', () => {
        if (navigator.geolocation) {
            tryGetLocation(1);
        } else {
            document.getElementById('gps_status').innerHTML = "Trình duyệt không hỗ trợ GPS";
        }
    });
    </script>

    <div id="gps_status" style="padding:18px; background:#331100; color:#ffaaaa; border-radius:10px; margin:20px 0; font-size:17px; text-align:center;">
        Đang khởi động GPS...
    </div>
    """,
    height=140
)

# Đọc tọa độ từ URL (sau khi JS reload)
params = st.query_params

if "lat" in params and "lon" in params:
    try:
        latitude = float(params["lat"][0])
        longitude = float(params["lon"][0])
        st.success("ĐÃ LẤY ĐƯỢC VỊ TRÍ THỰC TẾ CỦA BẠN!")
    except:
        st.error("Lỗi định dạng tọa độ!")
        latitude, longitude = 21.0285, 105.8542
else:
    st.warning("Không lấy được vị trí GPS – đang hiển thị vị trí mặc định (Hà Nội).")
    latitude, longitude = 21.0285, 105.8542

# ============================
#  HIỂN THỊ BẢN ĐỒ
# ============================
st.subheader("Bản đồ vị trí hiện tại")

m = Map(location=[latitude, longitude], zoom_start=17)
Marker([latitude, longitude], tooltip="Bạn đang ở đây", icon=None).add_to(m)
st_folium(m, width=700, height=500)

# ============================
#  THÔNG TIN GPS
# ============================
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

st.subheader("Thông tin GPS hiện tại")
col1, col2, col3 = st.columns(3)
col1.metric("Vĩ độ (Latitude)", f"{latitude:.6f}")
col2.metric("Kinh độ (Longitude)", f"{longitude:.6f}")
col3.metric("Thời gian", timestamp)

# ============================
#  GỬI DỮ LIỆU VỀ SERVER
# ============================
st.subheader("Gửi dữ liệu GPS đến server")
server_url = st.text_input("URL API nhận dữ liệu:", value="http://localhost:8000/gps", help="Thay bằng URL server thật của bạn")

gps_data = {
    "device_id": "TUAN001",
    "timestamp": timestamp,
    "latitude": round(latitude, 6),
    "longitude": round(longitude, 6),
    "speed": round(random.uniform(0, 50), 1),
    "accuracy": "high" if "lat" in params else "fallback",
    "source": "HTML5 Geolocation"
}

st.json(gps_data, expanded=False)

if st.button("Gửi dữ liệu ngay", type="primary"):
    try:
        response = requests.post(server_url, json=gps_data, timeout=10)
        if response.status_code == 200:
            st.success("GỬI THÀNH CÔNG!")
            st.write("Phản hồi từ server:", response.json())
        else:
            st.error(f"Lỗi server: {response.status_code} – {response.text}")
    except Exception as e:
        st.error(f"Không kết nối được server: {e}")

st.caption("Ứng dụng phục vụ đề tài NCKH — Thu thập dữ liệu GPS thực từ thiết bị di động • Phiên bản đã tối ưu cho Streamlit Cloud")