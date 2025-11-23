import streamlit as st
import streamlit.components.v1 as components

st.title("📡 Module đọc dữ liệu GPS (Phần 3.1)")

# ------------------ BƯỚC 1: LẤY VỊ TRÍ BẰNG JAVASCRIPT ------------------
components.html(
    """
    <script>
        navigator.geolocation.getCurrentPosition(
            (pos) => {
                const data = {
                    type: "gps_success",
                    lat: pos.coords.latitude,
                    lon: pos.coords.longitude,
                    acc: pos.coords.accuracy
                };
                window.parent.postMessage(data, "*");
            },
            (err) => {
                window.parent.postMessage(
                    {type: "gps_error", msg: err.message},
                    "*"
                );
            }
        );
    </script>
    """,
    height=0
)

# ------------------ BƯỚC 2: NHẬN TÍN HIỆU TỪ JAVASCRIPT ------------------
params = st.query_params

if "gps_status" not in st.session_state:
    st.session_state.gps_status = "waiting"

if "lat" not in st.session_state:
    st.session_state.lat = None
if "lon" not in st.session_state:
    st.session_state.lon = None
if "acc" not in st.session_state:
    st.session_state.acc = None

if "lat" in params and "lon" in params:
    st.session_state.lat = float(params["lat"])
    st.session_state.lon = float(params["lon"])
    st.session_state.acc = float(params.get("acc", 0))
    st.session_state.gps_status = "success"

elif "gps_error" in params:
    st.session_state.gps_status = "error"
    st.session_state.error_msg = params["gps_error"]

# ------------------ BƯỚC 3: HIỂN THỊ KẾT QUẢ ------------------

if st.session_state.gps_status == "waiting":
    st.info("⏳ Đang chờ cấp quyền vị trí…")

elif st.session_state.gps_status == "error":
    st.error("❌ Không thể lấy vị trí GPS: " + st.session_state.error_msg)

elif st.session_state.gps_status == "success":
    st.success("🎉 Đã lấy được tọa độ GPS!")

    col1, col2, col3 = st.columns(3)
    col1.metric("Latitude", st.session_state.lat)
    col2.metric("Longitude", st.session_state.lon)
    col3.metric("Độ chính xác (m)", st.session_state.acc)
