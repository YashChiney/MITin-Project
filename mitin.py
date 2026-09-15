import streamlit as st
st.markdown("""
<style>
.stApp {
    background-image: url("https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/background.png");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}
</style>
""", unsafe_allow_html=True)

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
st.title('What is :rainbow[MITin]?')
st.write('MITin is an exclusive digital platform designed for MIT-WPU students and recruiters to connect through student projects, skills, achievements, and academic profiles. It provides students with a single place to showcase their projects, certifications, technical skills, CGPA, coding languages, and other achievements, while allowing recruiters to discover suitable candidates without having to manually search through multiple sources.') 
st.title('Why use :rainbow[MITin]?')
st.markdown(
  """
  Student projects and achievements are often scattered across different platforms, making it difficult for recruiters to identify the right students. MITin solves this by bringing everything together in one college-specific platform.

Recruiters can use multiple filters such as branch, CGPA, skills, programming languages, project type, and project level to quickly find students matching their requirements. Students can build and maintain their profiles throughout college, creating a digital portfolio that represents their growth and capabilities.
"""
)

