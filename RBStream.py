import streamlit as st
import pandas as pd
import mysql.connector

# Database connection
connection = mysql.connector.connect(
    host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
    port=4000,
    user="2XYVe2q7YJj2Bap.root",
    password="80xE8BbcMzFYrLl7",
    database="RB",
)

# Create a cursor object
mycursor = connection.cursor(buffered=True)
# Query to fetch the data
mycursor.execute("SELECT * FROM RB.RedBus")

out = mycursor.fetchall()

# Convert the result to a pandas DataFrame
if mycursor.description is not None:
    columns = [desc[0] for desc in mycursor.description]
else:
    st.error("No data available in the database")

df = pd.DataFrame(out, columns=columns)

# Streamlit application
st.set_page_config(page_title="RedBus Data Filtering", page_icon="🚌", layout="wide")

# Add a background image
st.markdown(
    """
    <style>
    .stApp {
        background-image: url('https://miro.medium.com/v2/resize:fit:828/format:webp/1*S-95TWd9jgxT87cKkZWnFg.jpeg');
        background-size: cover;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title('🚌 RedBus Data Filtering Application')

# Sidebar filters
st.sidebar.title("Filters")

# State filter
if 'state' in df.columns:
    state_options = df["state"].unique()
    selected_state = st.sidebar.selectbox("Select State", state_options)
else:
    st.error("The column 'State' is not in the DataFrame")

# Dynamic "From Station" and "To Station" based on selected State
if selected_state:
    state_filtered_df = df[df["state"] == selected_state]

    st.subheader("Search for Buses by Station")
    col1, col2 = st.columns(2)

    with col1:
        if 'fromstation' in state_filtered_df.columns:
            from_station_options = state_filtered_df["fromstation"].unique()
            selected_from_station = st.selectbox("From_Station", from_station_options)
        else:
            st.error("The column 'From_Station' is not in the DataFrame")

    with col2:
        if 'tostation' in state_filtered_df.columns:
            to_station_options = state_filtered_df["tostation"].unique()
            selected_to_station = st.selectbox("To_Station", to_station_options)
        else:
            st.error("The column 'To_Station' is not in the DataFrame")
else:
    st.write("Please select a state to view stations.")


# Price filter
if 'price' in df.columns:
    # price_min = df["price"].min()
    # price_max = df["price"].max()
    selected_price = st.sidebar.slider("Select Price Range", 100, 2000, (100, 2000))
else:
    st.error("The column 'price' is not in the DataFrame")

# Rating filter
if 'rating' in df.columns:
    rating_min = float(df["rating"].min())
    rating_max = float(df["rating"].max())
    selected_rating = st.sidebar.slider("Select Rating Range", rating_min, rating_max, (rating_min, rating_max))
else:
    st.error("The column 'rating' is not in the DataFrame")

# Bus Type filter
if 'bustype' in df.columns:
    bus_type_options = df["bustype"].unique()
    selected_bus_type = st.sidebar.multiselect("Select Bus Type", bus_type_options)
else:
    st.error("The column 'bustype' is not in the DataFrame")

# Filter button
if st.sidebar.button("Apply Filters"):
    filtered_df = df.copy()

    if 'state' in df.columns:
        filtered_df = filtered_df[filtered_df["state"] == selected_state]
    
    if 'price' in df.columns:
        filtered_df = filtered_df[
            (filtered_df["price"] >= selected_price[0]) &
            (filtered_df["price"] <= selected_price[1])
        ]
    
    if 'rating' in df.columns:
        filtered_df = filtered_df[
            (filtered_df["rating"] >= selected_rating[0]) &
            (filtered_df["rating"] <= selected_rating[1])
        ]
    
    if 'bustype' in df.columns and selected_bus_type:
        filtered_df = filtered_df[filtered_df["bustype"].isin(selected_bus_type)]
    
    
    if 'fromstation' in df.columns:
        filtered_df = filtered_df[filtered_df["fromstation"] == selected_from_station]
    
    if 'tostation' in df.columns:
        filtered_df = filtered_df[filtered_df["tostation"] == selected_to_station]

    # Display the filtered data
    st.write(filtered_df)
else:
    st.write("Apply filters to see the data.")
