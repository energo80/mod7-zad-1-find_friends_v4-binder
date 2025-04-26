import streamlit as st
from pycaret.clustering import setup, create_model, assign_model, plot_model, save_model, load_model, predict_model
import pandas as pd  # type: ignore
from pathlib import Path
import json
from openai import OpenAI
from dotenv import dotenv_values

import my_openai_api_key 


env = dotenv_values(".env")
openai_client = OpenAI(api_key=st.session_state["my_openai_api_key"])

def my_clusters_descr(DATA, MODEL_NAME,CLUSTER_NAMES_AND_DESCRIPTIONS ):
    print(f" Analiza {MODEL_NAME} do {CLUSTER_NAMES_AND_DESCRIPTIONS}")
    df = pd.read_csv(DATA, sep=';')
    st.dataframe(df.head())

    kmeans_pipeline = load_model(MODEL_NAME.stem)
    df_with_clusters = predict_model(model=kmeans_pipeline, data=df)

    st.dataframe(df_with_clusters["Cluster"].value_counts())  


    cluster_descriptions = {}
    for cluster_id in df_with_clusters['Cluster'].unique():
        cluster_df = df_with_clusters[df_with_clusters['Cluster'] == cluster_id]
        summary = ""
        for column in df_with_clusters:
            if column == 'Cluster':
                continue

            value_counts = cluster_df[column].value_counts()
            value_counts_str = ', '.join([f"{idx}: {cnt}" for idx, cnt in value_counts.items()])
            summary += f"{column} - {value_counts_str}\n"

        cluster_descriptions[cluster_id] = summary
    
    st.text_area("40 Sample cluster",cluster_descriptions["Cluster 5"] )
    

    prompt = "Użyliśmy algorytmu klastrowania."
    for cluster_id, description in cluster_descriptions.items():
        prompt += f"\n\nKlaster {cluster_id}:\n{description}"

    prompt += """
    Wygeneruj najlepsze nazwy dla każdego z klasterów oraz ich opisy

    Użyj formatu JSON. Przykładowo:
    {
        "Cluster 0": {
            "name": "Klaster 0",
            "description": "W tym klastrze znajdują się osoby, które..."
        },
        "Cluster 1": {
            "name": "Klaster 1",
            "description": "W tym klastrze znajdują się osoby, które..."
        }
    }
    """
    st.text_area("62 Sample prompt",prompt)



    response = openai_client.chat.completions.create(
        model="gpt-4o",
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": [{"type": "text", "text": prompt}],
            }
        ],
    )
    result = response.choices[0].message.content.replace("```json", "").replace("```", "").strip()
    cluster_names_and_descriptions = json.loads(result)

    with open(CLUSTER_NAMES_AND_DESCRIPTIONS, "w") as f:
        f.write(json.dumps(cluster_names_and_descriptions))

    with open(CLUSTER_NAMES_AND_DESCRIPTIONS, "r") as f:
        st.text_area("Input info", json.loads(f.read()))


    if st.button("Nacisnij OK"):
        st.rerun()
    #my_openai_api_key.my_openai_api_key()
    #print(f'222my_openai_api_key=[{st.session_state["my_openai_api_key"]}] ')
