import streamlit as st
import json
import requests
from io import StringIO


st.title("NLP Process Kecil-kecilan")




tab1,tab2,tab3 = st.tabs(["Summarize","Sentiment","Upload Sentiment"])
with tab1:
    sum_text = st.text_area("Summarize your text :",key="text")
    
    col1,col2 = st.columns([1,1])
    with col1:
        summary = {"text":sum_text}
        if st.button('Summarize'):
            res = requests.post(url="http://127.0.0.1:8000/NLP/Summary",data = json.dumps(summary))
            st.subheader("Summarized Text  = " )  
            st.write(f"{res.text}")
            
    def clear_text():
        st.session_state["text"] = ""
    with col2:
        st.button("Clear Text",on_click=clear_text)

with tab2:
    sent_text = st.text_input("Get your sentiment :")

    sentiment = {"text":sent_text}
    if st.button('Sentiment'):
        res = requests.post(url="http://127.0.0.1:8000/NLP/Sentiment",data = json.dumps(sentiment))
        res_json = res.json()
        st.subheader("Sentiment Result  = " )  
        

        if res_json :
            try:
                for item in res_json:
                    st.text("Aspects       = {}".format(item['aspects']))
                    st.text("Description   = {}".format(item['desc']))
                    st.text("Subjectivity  = {}".format(item['subjectivity']))
                    st.text("Polarity      = {}".format(item['polarity']))
                    st.text("Sentiment     = {}".format(item['sentiment']))
                    st.text("\n")
            except:
                st.write("Error not found")

        

with tab3:
    uploaded_file = st.file_uploader("Choose a file") 
    if st.button('Check your sentiment'):
       stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
       data = stringio.read()
       test = uploaded_file.getvalue()
       
       

       res = requests.post(url="http://127.0.0.1:8000/upload",data = uploaded_file)
       res_json = res.json()


       st.subheader("Result : ")
       
        
         
            
            

        
        
