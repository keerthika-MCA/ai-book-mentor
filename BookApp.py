import streamlit as st
from google import genai
from pydantic import BaseModel
import json

class BookAnswer(BaseModel):
    topic_name:str
    explanation:str


st.title("Book Master 📚")
st.write("To know all about books")

topic = st.text_input("what book do you want to explain?(eg:5 AM club,The alchemist)")
ask_btn = st.button("explain")

if ask_btn:
    if topic != "":

        try:
            with st.spinner("Please wait,Master is thinking to give a better most answer....."):
                API_KEY = st.secrets["GEMINI_API_KEY"]
                client = genai.Client(api_key=API_KEY)

                response = client.models.generate_content(
                    model = 'gemini-3.8-flash',
                    contents = topic,
                    config = {
                        "system_instruction":"You are a brillient book master,Explain books interestingly follow the exact json format.STRICT RULE:If the user asks anything beyond the books like(cinema,sports,medicine),you MUST reject It.set query as 'Out of my knowledge'",
                        "response_mime_type":"application/json",
                        "response_schema":BookAnswer,

                    }

            )
                answer_dict = json.loads(response.text)

                if answer_dict ['topic_name'] == 'Out of my knowledge':
                    st.error(answer_dict["explanation"])
                else:
                    st.success(f"Topic:{answer_dict['topic_name']}")
                    st.info(f"Explanation:{answer_dict['explanation']}")

        except Exception as e:
            st.error(f"An error occured:{e}")
    else:
        st.warning("Please enter your topic name")
