import streamlit as st
from dotenv import dotenv_values

#env = dotenv_values(".envvv")


def my_openai_api_key() :
    if 'my_openai_api_key' not in st.session_state:
        st.session_state.my_openai_api_key = ""
    print(f'READ my_openai_api_key=[{st.session_state["my_openai_api_key"]}]  ')

    if st.session_state.my_openai_api_key == "":
        test_key = st.text_input("Wprowadz klucz openai api", type="password", )
        #if not st.session_state.get("my_openai_api_key"):
        if test_key:
            st.session_state.my_openai_api_key = test_key
            #env["OPENAI_API_KEY"] = test_key
            print(f'SET my_openai_api_key=[{st.session_state.my_openai_api_key}] test_key[{test_key}] ')
            
        #if st.session_state["my_openai_api_key"]:
            st.rerun()