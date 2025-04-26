import streamlit as st
import pandas as pd  # type: ignore
from pycaret.clustering import setup, create_model, assign_model, plot_model, save_model, load_model, predict_model
import plotly.express as px  # type: ignore
import json
from dotenv import dotenv_values
from openai import OpenAI
import time
from pathlib import Path
import my_save_model
import os

#import my_env as my
import my_openai_api_key 
my_openai_api_key.my_openai_api_key()
import my_clusters_descr 
#st.title('Find friends v1')


MODEL_NAME = Path('welcome_survey_clustering_pipeline_v1.pkl')
DATA = Path('welcome_survey_simple_v2.csv')
CLUSTER_NAMES_AND_DESCRIPTIONS = Path('welcome_survey_cluster_names_and_descriptions_v1.json')

env = dotenv_values(".envvv")


#my.my_env()

@st.cache_data
def get_model():
    return load_model(MODEL_NAME.stem)

@st.cache_data
def get_cluster_names_and_descriptions():
    with open(CLUSTER_NAMES_AND_DESCRIPTIONS,"r") as f:
        return json.loads(f.read())

@st.cache_data
def get_all_participants():
    model = get_model()
    all_df = pd.read_csv(DATA , sep=';')
    df_with_clusters = predict_model(model, data=all_df)
    return df_with_clusters


if not st.session_state.get("my_openai_api_key"):
    st.session_state["my_openai_api_key"] = ""


if not "OPENAI_API_KEY" in env:
    env["OPENAI_API_KEY"]=""
        


with st.sidebar:
    st.header("Powiedz nam coś o sobie")
    st.markdown("Pomozemy Ci znalezc osoby ktore maja podobne zainteresowania")
    age = st.selectbox("Wiek", ['<18', '25-34', '45-54', '35-44', '18-24', '>=65', '55-64', 'unknown'])
    edu_level = st.selectbox("Wykształcenie", ['Podstawowe', 'Średnie', 'Wyższe'])
    fav_animals = st.selectbox("Ulubione zwierzęta", ['Brak ulubionych', 'Psy', 'Koty', 'Inne', 'Koty i Psy'])
    fav_place = st.selectbox("Ulubione miejsce", ['Nad wodą', 'W lesie', 'W górach', 'Inne'])
    gender = st.radio("Płeć", ['Mężczyzna', 'Kobieta'])

    person_df = pd.DataFrame([
        {
            'age' : age,
            'edu_level' : edu_level,
            'fav_animals' : fav_animals,
            'fav_place': fav_place,
            'gender' : gender,
        }
    ])

#st.write("Wybrane dane:")
#st.dataframe(person_df, hide_index=True)

if MODEL_NAME.is_file() and CLUSTER_NAMES_AND_DESCRIPTIONS.is_file():
    model = get_model()
    all_df = get_all_participants()
    cluster_names_and_descriptions = get_cluster_names_and_descriptions()


    predicted_cluster_id = predict_model(model, data=person_df)["Cluster"].values[0]
    predicted_cluster_data = cluster_names_and_descriptions[predicted_cluster_id]

    st.header(f"Najblizej ci do klastra {predicted_cluster_data['name']}")
    same_cluster_df = all_df[all_df["Cluster"] == predicted_cluster_id]
    st.metric("Liczba twoich znajomych", len(same_cluster_df))

    st.header("Osoby z grupy")
    fig = px.histogram(same_cluster_df.sort_values("age"), x="age")
    fig.update_layout(
        title="Rozklad wieku w grupie",
        xaxis_title="Wiek",
        yaxis_title="Liczba osób",
    )
    st.plotly_chart(fig)

    fig = px.histogram(same_cluster_df, x="edu_level")
    fig.update_layout(
        title="Rozklad edu_level w grupie",
        xaxis_title="edu_level",
        yaxis_title="Liczba osób",
    )
    st.plotly_chart(fig)

    fig = px.histogram(same_cluster_df, x="fav_animals")
    fig.update_layout(
        title="Rozklad fav_animals w grupie",
        xaxis_title="fav_animals",
        yaxis_title="Liczba osób",
    )
    st.plotly_chart(fig)


    fig = px.histogram(same_cluster_df, x="fav_place")
    fig.update_layout(
        title="Rozklad fav_place w grupie",
        xaxis_title="fav_place",
        yaxis_title="Liczba osób",
    )
    st.plotly_chart(fig)

elif not MODEL_NAME.is_file() :
    if st.button(f"Wykonaj brakującą do analizę {DATA} -> {MODEL_NAME}"):
        my_save_model.my_save_model(DATA, MODEL_NAME)
       
elif not CLUSTER_NAMES_AND_DESCRIPTIONS.is_file() :
    if st.session_state["my_openai_api_key"] and  st.button(f"Wykonaj brakującą analizę {MODEL_NAME} -> {CLUSTER_NAMES_AND_DESCRIPTIONS}"):
        my_clusters_descr.my_clusters_descr(DATA, MODEL_NAME, CLUSTER_NAMES_AND_DESCRIPTIONS)
        #print(" openai_api_key: ",st.session_state["openai_api_key"])
        print(" my_openai_api_key: ",st.session_state["my_openai_api_key"], 'ENV: ', env["OPENAI_API_KEY"])


if CLUSTER_NAMES_AND_DESCRIPTIONS.is_file() :
    if st.button(f"Usuń analizę {CLUSTER_NAMES_AND_DESCRIPTIONS}"):
        os.remove(CLUSTER_NAMES_AND_DESCRIPTIONS)
if MODEL_NAME.is_file() :
    if st.button(f"Usuń analizę {MODEL_NAME}"):
        os.remove(MODEL_NAME)
        
#print("2 my_openai_api_key: ",st.session_state.my_openai_api_key)