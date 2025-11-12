import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from water_backend import predict_depth, water_train
import copy

st.set_page_config(page_title="💧 AI Water Well Predictor", layout="wide")
st.title("💧 AI-Enabled Ground Water Level Predictor")
st.markdown("Click on the map to get coordinates, copy them into the sidebar, and predict groundwater depth.")

aquifer_types = ["Unconfined", "Confined", "Semi-confined", "Unknown"]
selected_aquifer = st.sidebar.selectbox("Aquifer Type", aquifer_types)
threshold = st.sidebar.slider("Water Depth Threshold (m)", 0, 100, 20)

st.sidebar.markdown("### Enter Coordinates for Prediction")

if 'predicted_depth' not in st.session_state:
    st.session_state['predicted_depth'] = None
if 'suitability' not in st.session_state:
    st.session_state['suitability'] = None

lat = st.sidebar.number_input("Latitude", value=water_train["Latitude"].mean(), format="%.6f")
lon = st.sidebar.number_input("Longitude", value=water_train["Longitude"].mean(), format="%.6f")

if st.sidebar.button("Predict Groundwater Depth"):
    try:
        predicted_depth, suitability = predict_depth(lat, lon, selected_aquifer, threshold)
    except TypeError:
        predicted_depth = predict_depth(lat, lon, selected_aquifer, threshold)
        suitability = "Yes" if predicted_depth <= threshold else "No"

    st.session_state['predicted_depth'] = predicted_depth
    st.session_state['suitability'] = suitability

if st.session_state['predicted_depth'] is not None:
    st.sidebar.markdown("---")
    st.sidebar.subheader("🌊 Prediction Result")
    st.sidebar.markdown(f"""
    **Latitude:** {lat:.6f}  
    **Longitude:** {lon:.6f}  
    **Predicted Depth:** `{st.session_state['predicted_depth']:.2f}` m  
    **Suitable for Well Drilling:** **{'✅ Yes' if st.session_state['suitability'] == 'Yes' else '❌ No'}**
    """, unsafe_allow_html=True)

if 'map_base' not in st.session_state:
    m_base = folium.Map(
        location=[water_train["Latitude"].mean(), water_train["Longitude"].mean()],
        zoom_start=6,
        tiles="https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}",
        attr="Google Street"
    )
    for _, row in water_train.sample(min(200, len(water_train))).iterrows():
        folium.CircleMarker(
            location=[row["Latitude"], row["Longitude"]],
            radius=3,
            color="blue",
            fill=True,
            fill_opacity=0.5
        ).add_to(m_base)
    m_base.add_child(folium.LatLngPopup())
    st.session_state['map_base'] = m_base


m = copy.deepcopy(st.session_state['map_base'])

if st.session_state['predicted_depth'] is not None:
    folium.Marker(
        location=[lat, lon],
        popup=f"<b>Predicted Depth:</b> {st.session_state['predicted_depth']:.2f} m<br><b>Suitable:</b> {st.session_state['suitability']}",
        icon=folium.Icon(color="green" if st.session_state['suitability'] == "Yes" else "red", icon="tint", prefix="fa")
    ).add_to(m)

st.markdown("### 🗺️ Reference Map: Click to copy coordinates")
st_folium(m, width=750, height=500)
