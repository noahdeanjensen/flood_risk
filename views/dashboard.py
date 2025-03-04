import streamlit as st
import folium
from streamlit_folium import st_folium
import asyncio
import websockets
import json
import threading
import queue

# Create a thread-safe queue for WebSocket data updates
data_queue = queue.Queue()

# 🔹 Cache map creation to prevent slow rendering
@st.cache_data(ttl=60)
def create_map(points):
    """Create a Folium map with all points efficiently."""
    if not points:
        return folium.Map(location=[40, -95], zoom_start=5)

    map_obj = folium.Map(location=[40, -95], zoom_start=5)
    feature_group = folium.FeatureGroup(name="Points").add_to(map_obj)

    # Precomputed colors for scores
    score_colors = {
        1: "#FF0000",  2: "#FF3300",  3: "#FF6600",  4: "#FF9900",
        5: "#FFCC00",  6: "#FFFF00",  7: "#CCFF00",  8: "#99FF00",
        9: "#66FF00", 10: "#00FF00"
    }

    for point in points:
        score = min(max(int(point["Score"]), 1), 10)
        color = score_colors[score]
        folium.CircleMarker(
            location=[point["Latitude"], point["Longitude"]],
            radius=6,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7,
            popup=f"<b>ID:</b> {point['ID']}<br><b>Score:</b> {point['Score']}"
        ).add_to(feature_group)

    return map_obj

def websocket_listener():
    """Runs WebSocket listener and stores updates in a queue."""
    
    async def get_live_data():
        while True:
            try:
                async with websockets.connect("ws://localhost:8472/ws") as websocket:
                    while True:
                        data = await websocket.recv()
                        parsed_data = json.loads(data)

                        # 🔹 Store data in the queue (to be processed in the main thread)
                        data_queue.put(parsed_data)

            except Exception as e:
                print(f"⚠️ WebSocket Error: {e}")
                await asyncio.sleep(5)  # Retry after 5 seconds

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(get_live_data())

# 🔹 Show function (UI-related logic)
def show():
    """Displays the real-time performance dashboard."""
    
    st.title("Optimized Real-Time Performance Dashboard")

    # 🔹 Initialize session state
    if "points" not in st.session_state:
        st.session_state["points"] = []
    if "selected_point" not in st.session_state:
        st.session_state["selected_point"] = None

    # 🔹 Process WebSocket updates in the main thread
    while not data_queue.empty():
        st.session_state["points"] = data_queue.get()
        st.rerun()  # Trigger UI refresh safely

    # 🔹 Start WebSocket listener in the background (only once)
    if "websocket_thread" not in st.session_state:
        ws_thread = threading.Thread(target=websocket_listener, daemon=True)
        ws_thread.start()
        st.session_state["websocket_thread"] = ws_thread

    # 🔹 Render the map efficiently
    map_obj = create_map(st.session_state["points"])
    st_folium(map_obj, width=700, height=500)

    # 🔹 Sidebar UI for selecting a point
    st.sidebar.header("Select a Point")
    selected_id = st.sidebar.selectbox("Choose an ID:", [p["ID"] for p in st.session_state["points"]])

    if selected_id:
        st.session_state["selected_point"] = next((p for p in st.session_state["points"] if p["ID"] == selected_id), None)

    if st.session_state["selected_point"]:
        st.sidebar.write("### Point Details")
        st.sidebar.json(st.session_state["selected_point"])
