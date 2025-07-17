import streamlit as st
import joblib
import base64
import pandas as pd

model = joblib.load("model.pkl")

def set_background(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def style_predict_button():
    st.markdown("""
        <style>
        div.stButton > button {
            background-color: #1f77b4;
            color: white;
            font-weight: bold;
            border: none;
            border-radius: 8px;
            padding: 0.75em 1.5em;
            transition: background-color 0.3s ease;
        }
        div.stButton > button:hover {
            background-color: #0056b3;
        }
        </style>
    """, unsafe_allow_html=True)

def gif_image():
    gif_url = "https://tenor.com/view/squid-game-front-man-squid-game-2-happy-celebration-gif-12369111202088932661.gif"
    st.markdown(f'<img src="{gif_url}" alt="Loading..." width="100%">', unsafe_allow_html=True)

town_mapping = {
    "ANG MO KIO": 0, "BEDOK": 1, "BISHAN": 2, "BUKIT BATOK": 3,
    "BUKIT MERAH": 4, "BUKIT PANJANG": 5, "BUKIT TIMAH": 6,
    "CENTRAL AREA": 7, "CHANGI": 8, "CHOA CHU KANG": 9,
    "CLEMENTI": 10, "GEYLANG": 11, "HOUGANG": 12, "JURONG EAST": 13,
    "JURONG WEST": 14, "KALLANG/WHAMPOA": 15, "MARINE PARADE": 16,
    "PASIR RIS": 17, "PUNGGOL": 18, "QUEENSTOWN": 19, "SEMBAWANG": 20,
    "SENGKANG": 21, "SINGAPORE RIVER": 22, "TAMPINES": 23,
    "TOA PAYOH": 24, "WOODLANDS": 25, "YISHUN": 26
}

storey_mapping = {
    "01 TO 04": 0, "05 TO 10": 1, "11 TO 20": 2, "21 TO 30": 3, "31 TO 40": 4, "41 TO 50": 5
}

flatmodel_mapping = {
    "1 ROOM": 0, "2 ROOM": 1, "3 ROOM": 2, "4 ROOM": 3,
    "5 ROOM": 4, "EXECUTIVE": 5, "MULTI-GENERATION": 6
}

flattype_mapping = {
    "Improved": 0, "New Generation": 1, "Maisonette": 2, "Apartment": 3, "Multi-Generation": 4
}

def main():
    st.markdown('<h1 style="color:black;">HDB Resale Price Prediction</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:white;">This app predicts the resale price of HDB flats based on various features.</p>', unsafe_allow_html=True)

    st.markdown(
        "<style>label, .stSelectbox label, .stSlider label, .stSlider .css-1cpxqw2, .stSlider .css-14xtw13 { color: white !important; }</style>",
        unsafe_allow_html=True
    )

    selected_town = st.selectbox("Select Town", list(town_mapping.keys()))
    selected_storeyrange = st.selectbox("Select Storey Range", list(storey_mapping.keys()))
    selected_flatmodel = st.selectbox("Select Flat Model", list(flatmodel_mapping.keys()))
    selected_flattype = st.selectbox("Select Flat Type", list(flattype_mapping.keys()))
    selected_floorarea = st.slider("Enter Floor Area (sqm)", min_value=30.0, max_value=200.0)
    selected_leasecommenceyr = st.slider("Enter Lease Commence Year", min_value=1960, max_value=2000)

    if st.button("Predict Resale Price"):
        input_df = pd.DataFrame({
            'town': [selected_town],
            'flat_type': [selected_flatmodel],
            'storey_range': [selected_storeyrange], 
            'floor_area_sqm': [selected_floorarea],
            'lease_commence_date': [selected_leasecommenceyr]
        })

        ohe_df = pd.get_dummies(input_df, columns=['town', 'flat_type', 'storey_range'])
        ohe_df = ohe_df.reindex(columns=model.feature_names_in_, fill_value=0)

        prediction = model.predict(ohe_df)

        st.markdown(f'<span style="color:white;">The predicted resale price is: ${prediction[0]:,.2f}</span>', unsafe_allow_html=True)
        gif_image()

if __name__ == "__main__":
    set_background("hdb.jpg")
    style_predict_button()
    main()