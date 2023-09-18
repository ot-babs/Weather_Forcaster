import streamlit as st
import plotly.express as px
from backend import get_data

# Add title, text input, slider, selectbox, and subheader
st.title("Weather Forecast for the Coming Days")
place = st.text_input("Place: ")
days = st.slider("Forecast Days", min_value=1, max_value=5,
                 help="Select the number of forecasted days")
options = st.selectbox("Select data to view",
                        ("Temperature", "Sky"))

st.subheader(f"{options} for the next {days} days in {place}.")
try:
    if place:

        # Get the temperature/sky data
        filtered_data = get_data(place, days)

        if options == "Temperature":
            # Create a temperature plot
            temperatures = [dict["main"]["temp"] / 10 for dict in filtered_data]
            date = [dict["dt_txt"] for dict in filtered_data]
            figure = px.line(x=date, y=temperatures, labels={"x":"Date", "y":"Temperature (C)"})
            st.plotly_chart(figure)

        if options == "Sky":
            images = {"Clear": "images/clear.png", "Clouds": "images/cloud.png",
                      "Rain": "images/rain.png", "Snow": "images/snow.png"}
            sky_conditions = [dict["weather"][0]["main"] for dict in filtered_data]
            image_paths = [images[condition] for condition in sky_conditions]
            st.image(image_paths, width=115)

except KeyError:
    st.text("Please input a valid city.")
