import streamlit as st
import google.generativeai as genai
from PIL import Image
import datetime as dt
import os

# configure the model

gemini_api_key = os.getenv('Gemini_API_Key')
genai.configure(api_key = gemini_api_key)
model = genai.GenerativeModel('gemini-2.5-flash-lite')


# lets create sidebar for image upload
st.sidebar.title(':red[upload the image here]')
uploaded_image = st.sidebar.file_uploader('Image',type=['jpeg','png','jfif'],
                                          accept_multiple_files=True)

uploaded_image =[Image.open(img) for img in uploaded_image]
if uploaded_image:
    uploaded_image = Image.open(uploaded_image)
    st.sidebar.success('Image has been uploaded Successfully')
    st.sidebar.subheader(':blue[Upload Image]')
    st.sidebar.image(uploaded_image)
    


# lets create the main page
st.title(':orange[Structutal Anomaly Detection:-] :blue[AI assisted structural anamoly detection system]')
st.markdown('#### :green[This application takes the image and describe the stuctural defect]')
title=st.text_input('Enter the Title of the report:')
name=st.text_input('Enter the Name of the person who has prepared input:')
desig=st.text_input('Enter the designation of person who have prepared the report:')
org=st.text_input('Enter the name of the organisation:')

if st.button('Submit'):
    with st.spinner('Processing...'):
        prompt = f'''
        <Role> You are an expert strucural engineer with 20 plus years of experiance
        <Goal> You need to provide a detailed report on the structural defects in the image provided by the user.
              <Context> The images shared by user has been attached.
        <Format> Follow the steps to prepare the report:
        * Add title at the top of the report. The title provided by the user is {title}.
        * next add name, designationa and organization of the person who prepare the report
        also include the date. Followings are the detailed provided by the user:
        name: {name}
        designation: {desig} 
        organization: {org}
        date: {dt.datetime.now().date()}
        * Indentify and classify the defect for eg: crack,spalling, corossion, honeycombing,etc.
        * There could be more than one defects in images.Identify all defects seperatly.
        * For each defect identified provide a short description of the defect and its potential impact on the structure.
        * For each defect measure the severity as low , medium or high .Also mentioning if the defect is inevitable or not.
        * Provide the short term and the long term solution for the repair along with an estimated cost in INR and estimated time.
        * What precautionary measures can be taken to avoid these defects in future.
        
        <Istruction>
        * the report generated should be in word format.
        * the report should not exceed more than 3 pages.
        * use points and tables wherever required.'''
        
        response = model.generate_content([prompt,*uploaded_image],
                                          generation_config={'temperature':0.7})
        
        st.write(response.text)
        
        if st.download_button(
            label='Click to download',
            data = response.text,
            file_name = 'structural_defect_report.txt',
            mime='text/plain'
        ):
            st.success('Your file is downloaded')