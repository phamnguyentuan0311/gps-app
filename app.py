import streamlit as st
from folium import Map, Marker
from streamlit_folium import st_folium
import streamlit.components.v1 as components

st.set_page_config(page_title="GPS NCKH Tuân", page_icon="satellite", layout="centered")
st.title("GPS THỰC TẾ – TỐI ƯU CHO MICROSOFT EDGE")
st.markdown("**Dùng được 100% trên laptop có GPS + Microsoft Edge**")

params = st.query_params

# ——— CHỈ CHẠY KHI CHƯA CÓ TỌA ĐỘ ———
if "lat" not in params or "lon" not in params:
    st.info("Nhấn nút → Cho phép vị trí → Chờ 5–25 giây là hiện đúng chỗ bạn đang ngồi")

    if st.button("LẤY VỊ TRÍ THỰC TẾ NGAY BÂY GIỜ", type="primary", use_container_width=True):
        components.html("""
        <script>
        const s = document.getElementById('status');
        s.innerHTML = "Đang kích hoạt GPS laptop (Edge)...";

        navigator.geolocation.watchPosition(  // watchPosition nhanh hơn getCurrentPosition trên Edge
            pos => {
                const lat = pos.coords.latitude.toFixed(7);
                const lon = pos.coords.longitude.toFixed(7);
                s.innerHTML = "Thành công! Đang cập nhật...";
                const url = new URL(window.location);
                url.searchParams.set('lat', lat);
                url.searchParams.set('lon', lon);
                window.location.replace(url);
            },
            err => {
                s.innerHTML = `Lỗi ${err.code}: ${err.message}<br>
                    <small>Edge: Vào Settings → Privacy → Location → bật cho trang này</small>`;
            },
            { 
                enableHighAccuracy: true,
                timeout: 30000,
                maximumAge: 0
            }
        );
        </script>
        <div id="status" style="padding:22px; background:#440000; color:#ffaaaa; border-radius:12px; text-align:center; font-size:18px; margin:20px 0;">
            Đang chờ bạn bấm nút...
        </div>
        """, height=180)

    st.stop()

# ——— ĐÃ CÓ TỌA ĐỘ → HIỆN KẾT QUẢ ———
lat = float(params["lat"][0])
lon = float(params["lon"][0])

st.success(f"ĐÃ LẤY ĐƯỢC VỊ TRÍ THỰC TẾ!\nVĩ độ: {lat:.7f} | Kinh độ: {lon:.7f}")

m = Map(location=[lat, lon], zoom_start=19)
Marker([lat, lon], popup="Bạn đang ngồi đúng chỗ này!", tooltip="GPS thật từ laptop").add_to(m)
st_folium(m, width=900, height=650)

if st.button("Lấy vị trí mới"):
    st.query_params.clear()
    st.rerun()

st.balloons()
st.caption("NCKH 2025 – Phạm Nguyễn Tuân – GPS")