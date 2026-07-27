import streamlit as st
import pickle

st.title("MovieIQ")
st.write("Predict Movie Success")

try:
    model = pickle.load(open("model.pkl", "rb"))
    st.success("Model loaded successfully")
except Exception as e:
    st.error(f"Error: {e}")

budget = st.number_input("Budget")
runtime = st.number_input("Runtime")
rating = st.number_input("Rating")

if st.button("Predict"):
    st.write("Budget:", budget)
    st.write("Runtime:", runtime)
    st.write("Rating:", rating)












 