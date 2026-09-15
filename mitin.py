import streamlit as st
st.title(' Welcome to :rainbow[MITin] ')
st.write(':blue[Your talent finding platform]')
st.write('# Choose your type of access')
col1, col2, col3, col4 = st.columns(4)
with col1:
  b1=st.button('Login as :blue[recruiter]')

with col2:
  b2=st.button('Login as :green[student]')

with col3:
  b3=st.button('Signup as :violet[recruiter]')

with col4:
  b4=st.button('Signup as :red[student]')
