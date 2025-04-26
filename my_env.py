from dotenv import dotenv_values
import streamlit as st



@st.cache_data
def my_env():
    env = dotenv_values(".env")
    
    try:
        if len(st.secrets) > 0:
            st.write("st.secrets exists and has values.")
            if 'QDRANT_URL' in st.secrets:
                env['QDRANT_URL'] = st.secrets['QDRANT_URL']

            if 'QDRANT_API_KEY' in st.secrets:
                env['QDRANT_API_KEY'] = st.secrets['QDRANT_API_KEY']

        else:
            st.write("st.secrets exists but is empty.")
    except FileNotFoundError:
        st.write("secrets.toml file not found")
    except KeyError:
        st.write("No such key exists")



    