import os
import streamlit as st
import requests


from app.config.settings import Settings
from app.common.logger import get_logger
from app.common.custom_exception import CustomException
from dotenv import load_dotenv

load_dotenv()

URI = os.getenv('URI') 

logger = get_logger(__name__)

st.set_page_config(page_title = "Multi AI Agent", layout= 'centered')
st.title("Multi AI Agent using Groq and Tavily")

system_prompt = st.text_area('Define your AI Agent', height= 70)
selected_model = st.selectbox("Select your AI Model", Settings.ALLOWED_MODEL_NAMES)
allow_web_search = st.checkbox("Allow Web Search")
user_query = st.text_area('Enter your Query', height= 150)

API_URL = URI+"/chat"

if st.button('Ask Agent') and user_query.strip():
    messages = []
    if system_prompt:
        messages.append({'role': 'system', 'content': system_prompt})
    messages.append({'role': 'user', 'content': user_query})
    
    payload = {
        'model_name': selected_model,
        'messages': messages,
        'allow_search': allow_web_search,
        'system_prompt': system_prompt
        }

    try:
        logger.info(f"Sending request to {API_URL} with payload: {payload}")
        response = requests.post(API_URL, json=payload)
        # print(f'response: {response}')

        if response:
            response_data = response.json().get('response', '')
            logger.info(f"Recieved response from backend: {response_data}")
            
            st.subheader("Response from AI Agent")
            st.markdown(response_data.replace('\n', '<br>'), unsafe_allow_html=True)
        
        else:
            logger.error(f"Backend error")
            st.error("Error with backend")

    except CustomException as e:
        logger.error(f"Error occured while requesting backend")
        st.error(CustomException("Failed communicate to backend"))
            


