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
st.title('# What is MITin')
st.write('MITin is an exclusive digital platform designed for MIT-WPU students and recruiters to connect through student projects, skills, achievements, and academic profiles. It provides students with a single place to showcase their projects, certifications, technical skills, CGPA, coding languages, and other achievements, while allowing recruiters to discover suitable candidates without having to manually search through multiple sources.') 
st.title('# Why use MITin')
st.markdown(
  """
  Student projects and achievements are often scattered across different platforms, making it difficult for recruiters to identify the right students. MITin solves this by bringing everything together in one college-specific platform.

Recruiters can use multiple filters such as branch, CGPA, skills, programming languages, project type, and project level to quickly find students matching their requirements. Students can build and maintain their profiles throughout college, creating a digital portfolio that represents their growth and capabilities.
"""
)
