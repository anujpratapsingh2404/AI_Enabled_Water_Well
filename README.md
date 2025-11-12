💧 AI-Enabled Ground Water Level Prediction Web App

This project is an AI-powered web application that predicts groundwater depth and determines whether a particular location is suitable for well drilling. Users can interact with a live map, copy coordinates, or enter latitude and longitude manually in the sidebar, choose aquifer properties, and get predictions instantly.

🚀 Features

✅ Interactive Google Satellite Map
✅ Copy latitude and longitude by clicking on the map
✅ Enter latitude & longitude in the sidebar to make predictions
✅ Predict groundwater depth using AI/ML model
✅ Display suitability for drilling (✅ Yes / ❌ No)
✅ Modular architecture with frontend and backend separated
✅ Ready for deployment and GitHub hosting
✅ Optional district search feature (coming soon)

🧠 Technologies Used
Component	Technology
Frontend	Streamlit + Folium Map
Backend	Python (Custom ML Model)
Data	CSV Dataset (Ground Water Levels)
Map Layer	Google Maps Tile
Deployment	Localhost / GitHub Ready

water_app/
│
├─ app.py               # Main Streamlit application
├─ frontend.py          # Handles UI and map rendering
├─ water_backend.py     # Prediction logic and ML model
├─ GroundWaterData.csv  # Dataset (optional)
├─ requirements.txt     # List of dependencies
└─ README.md            # Project documentation

📊 Prediction Logic

The prediction model uses:

Latitude & Longitude

Aquifer Type

Historical Water Level Patterns

Regional Training Dataset

It returns:

Depth (meters below ground level)

Suitability based on user-defined threshold
