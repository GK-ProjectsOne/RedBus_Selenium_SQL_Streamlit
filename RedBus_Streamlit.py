import streamlit as st
import pandas as pd
import mysql.connector

# Database connection
connection = mysql.connector.connect(
    host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
    port=4000,
    user="EymsToMmCKG1868.root",
    password="Hh15Cev73dkxuTLJ",
    database="test",
)
# Create a cursor object
mycursor = connection.cursor(buffered=True)
# Query to fetch the data
mycursor.execute("SELECT * FROM RedBus.BusDetails")

out = mycursor.fetchall()

# Convert the result to a pandas DataFrame
# Ensure to get column names
columns = [desc[0] for desc in mycursor.description]
df = pd.DataFrame(out, columns=columns)

# Debugging: Print out the DataFrame columns and the first few rows
print("DataFrame columns:", df.columns)
print("DataFrame preview:", df.head())

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

st.title('RedBus Data Filtering Application')

# Sidebar filters
st.sidebar.title("Filters")

# Debugging: Check if 'State' is in the DataFrame columns
if 'State' in df.columns:
    state_options = df["State"].unique()
    selected_state = st.sidebar.selectbox("Select State", state_options)
else:
    st.error("The column 'State' is not in the DataFrame")

# Ensure that the DataFrame has the 'Price' column before using it
if 'Price' in df.columns:
    price_min = int(df["Price"].min())
    price_max = int(df["Price"].max())
    selected_price = st.sidebar.slider("Select Price Range", price_min, price_max, (price_min, price_max))
else:
    st.error("The column 'Price' is not in the DataFrame")

# Ensure that the DataFrame has the 'Rating' column before using it
if 'Rating' in df.columns:
    rating_min = float(df["Rating"].min())
    rating_max = float(df["Rating"].max())
    selected_rating = st.sidebar.slider("Select Rating Range", rating_min, rating_max, (rating_min, rating_max))
else:
    st.error("The column 'Rating' is not in the DataFrame")

# Filter button
if st.sidebar.button("Filter Data"):
    if 'State' in df.columns and 'Price' in df.columns and 'Rating' in df.columns:
        filtered_df = df[
            (df["State"] == selected_state) &
            (df["Price"] >= selected_price[0]) &
            (df["Price"] <= selected_price[1]) &
            (df["Rating"] >= selected_rating[0]) &
            (df["Rating"] <= selected_rating[1])
        ]
        st.write(filtered_df)
else:
    st.write("Apply filters to see the data.")
