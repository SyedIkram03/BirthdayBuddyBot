import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import streamlit as st

# Initialize Firebase Admin SDK
cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://birthday-buddy-d9daa-default-rtdb.firebaseio.com/"
})

# Get a database reference
ref = db.reference('birthdays')

# Retrieve data from Firebase Realtime Database
data = ref.get()

# Display data using Streamlit
if data:
    st.header("Data from Firebase Realtime Database")
    for key, value in data.items():
        st.subheader(f"Key: {key}")
        st.write(value)
        st.write("---")
else:
    st.write("No data available in the Firebase Realtime Database.")
