pip install streamlit
import streamlit as st
import pandas as pd
st.write("Hello Guys!")
st.markdown("# This is a basic streamlit exercise")
num=st.slider("Enter ur age",min_value=1, max_value=100)
st.write('You are {num} years old')
if num>=18:
    check=st.checkbox("Pls agree to terms")
    if check:
        st.write("Yay , you agreed")
