"""
Elastic Search / vCons

"""
import streamlit as st
from elasticsearch import Elasticsearch
from vcon import Vcon
from datetime import datetime

ELASTIC_SEARCH_CLOUD_ID = st.secrets["ELASTIC_SEARCH_CLOUD_ID"]
ELASTIC_SEARCH_API_KEY = st.secrets["ELASTIC_SEARCH_API_KEY"]
CONV_DETAIL_URL = st.secrets["CONV_DETAIL_URL"]

st.set_page_config(
     page_title='Strolid Conversational Search'
     )

def main():
    # Show the timestamp of this run
    now = datetime.now()
    st.text(f"Last run: {now}")

    q = st.text_input(label="Search terms")

    if not q:
        st.stop()


    # Create the client instance
    client = Elasticsearch(
        cloud_id=ELASTIC_SEARCH_CLOUD_ID,
        api_key=ELASTIC_SEARCH_API_KEY,
    )
    resp = client.search(
    index="vcon-index", 
    body={ 
        "query": {
            "bool": {
                "must": [{ 
                "query_string": {
                        "query": q
                    }}]
                }
            },
        "highlight": {
            "fields": {
                "agent": {},
                "agent.keyword": {},
                "analysis": {},
                "analysis.body": {},
                "analysis.type": {},
                "analysis.type.keyword": {},
                "analysis.vendor": {},
                "attachments.body": {},
                "attachments.type": {},
                "created_at": {},
                "dealer_id": {},
                "dialog": {},
                "dialog.meta.direction": {},
                "dialog.meta.disposition": {},
                "parties.mailto": {},
                "parties.meta.extension": {},
                "parties.meta.role": {},
                "parties.name": {},
                "parties.tel": {},
                "team_id": {},
                "updated_at": {},
                "uuid": {},
                }
        }
    })
    for hit in resp['hits']['hits']:
        # Create a vCon object from the hit
        vcon_dict = hit['_source']
        v = Vcon().from_dict(vcon_dict)

        uuid = hit['_source']['uuid']
        details_url = f"{CONV_DETAIL_URL}\"{uuid}\""
        created_at  = hit['_source']['created_at']
        duration = v.duration()
        parties = v.get_party_names()
        dialog_urls = v.get_dialog_urls()
        summary = v.summary()
    

        st.divider()
        st.header(f"Conversation at {created_at}, {duration} seconds")
        st.markdown(
            f"**Summary**: {summary}",
            unsafe_allow_html=True
        )
        st.markdown(
            f"**UUID**: {uuid}",
            unsafe_allow_html=True
        )
        st.markdown(
            f"**Parties**: {parties}",
            unsafe_allow_html=True
        )
        for url in dialog_urls:
            st.markdown(
            f"**Recording**: [Listen Here](url)",
            unsafe_allow_html=True
        )
        st.markdown(
            f"**Score**: {hit['_score']}",
            unsafe_allow_html=True
        )
        st.markdown(
            f"**Details**: [Click Me for Details]({details_url})",
            unsafe_allow_html=True
        )
        for hint in hit['highlight']:
            st.markdown(
                f"**{hint}**",
                unsafe_allow_html=True
            )
            st.markdown(
                f"{hit['highlight'][hint]}",
                unsafe_allow_html=True
            )   

# Run main()

if __name__ == '__main__':
    main()