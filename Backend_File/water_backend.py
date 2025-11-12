import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

water_train = pd.read_csv(
    r"D:\Projects\AI_Water_Well_Predictor\Ground_Water_Level-2015-2022.csv",
    encoding="latin1"
)

water_train = water_train.drop(columns=[
    "Sr. No.", "State_Name_With_LGD_Code", "District_Name_With_LGD_Code",
    "Block_Name_With_LGD_Code", "GP_Name_With_LGD_Code",
    "Village", "Site_Name", "Well_ID"
], errors="ignore")

categorical_cols = ["TYPE", "SOURCE", "Aquifer"]
for col in categorical_cols:
    water_train[col] = water_train[col].fillna("Unknown")

le = LabelEncoder()
for col in categorical_cols:
    water_train[col] = le.fit_transform(water_train[col])

numerical_cols = water_train.select_dtypes(include=[np.number]).columns
year_cols = [col for col in water_train.columns if "monsoon" in col.lower()]

for col in year_cols:
    water_train[col] = pd.to_numeric(water_train[col], errors="coerce")

water_train[year_cols] = water_train[year_cols].interpolate(axis=1, limit_direction="both")
for col in year_cols:
    water_train[col] = water_train[col].fillna(water_train[col].median())


target = "Pre-monsoon_2022 (meters below ground level)"
X = water_train.drop(columns=[target, "Post-monsoon_2022 (meters below ground level)"], errors="ignore")
y = water_train[target]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

rf = RandomForestRegressor(n_estimators=200, random_state=42)
rf.fit(X_train, y_train)

def predict_depth(lat, lon, selected_aquifer="Unconfined", threshold=20):
    """
    Predict groundwater depth for given coordinates.
    Returns (predicted_depth, suitability)
    """

    try:
        aquifer_encoded = le.transform([selected_aquifer])[0]
    except:
        aquifer_encoded = 0

    feature_cols = X.columns
    new_row = water_train[feature_cols].median().to_dict()

    if "Latitude" in new_row: new_row["Latitude"] = lat
    if "Longitude" in new_row: new_row["Longitude"] = lon
    if "Aquifer" in new_row: new_row["Aquifer"] = aquifer_encoded

    new_data = pd.DataFrame([new_row], columns=feature_cols)

    new_data_scaled = scaler.transform(new_data)
    predicted_depth = rf.predict(new_data_scaled)[0]

    suitability = "Yes" if predicted_depth < threshold else "No"
    return predicted_depth, suitability
