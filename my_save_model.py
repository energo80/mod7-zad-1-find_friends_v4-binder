import streamlit as st
from pycaret.clustering import setup, create_model, assign_model, plot_model, save_model, load_model, predict_model
import pandas as pd  # type: ignore
from pathlib import Path


def my_save_model(DATA,MODEL_NAME):
    print(f"save_model from {DATA} to {MODEL_NAME}")
    df = pd.read_csv('welcome_survey_simple_v1.csv', sep=';')
    s = setup(df, session_id=123)
    st.dataframe(s.dataset_transformed.head())
    kmeans = create_model('kmeans', num_clusters=8)
    df_with_clusters = assign_model(kmeans)
    st.dataframe(df_with_clusters)
    plot_model(kmeans, plot='cluster', display_format='streamlit')
    save_model(kmeans, MODEL_NAME.stem, verbose=False)
    st.success(" Zapisano model ")
    if st.button(" OK - Potwierdz"):
        st.rerun()
