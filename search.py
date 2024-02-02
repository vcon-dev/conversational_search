"""
Elastic Search / vCons

"""
import streamlit as st
from elasticsearch import Elasticsearch
from vcon import Vcon
from datetime import datetime
import uuid

ELASTIC_SEARCH_CLOUD_ID = st.secrets["ELASTIC_SEARCH_CLOUD_ID"]
ELASTIC_SEARCH_API_KEY = st.secrets["ELASTIC_SEARCH_API_KEY"]
CONV_DETAIL_URL = st.secrets["CONV_DETAIL_URL"]

st.set_page_config(
     page_title='Strolid Conversational Search'
     )

def main():
    st.title("Strolid Conversational Search")
    st.caption("Searches vCons for a given term, powered by Elastic Search. Search for nearly anything, including customer names, dealer names, agent names, phone numbers, and more. Open sidebar on left for advanced options")
    terms, sort = st.columns(2)
    with terms:
        q = st.text_input(label="Search terms")
    with sort:
        sort_option = st.selectbox(
            'Sort by', ('Newest', 'Oldest', 'Most Relevant'))
        if sort_option == 'Newest':
            sort_by = [
                {
                    "created_at": {
                        "order": "desc"  # Sorting by 'created_at' in descending order
                    }
                }]
        elif sort_option == 'Oldest':
            sort_by = [
                {
                    "created_at": {
                        "order": "desc"  # Sorting by 'created_at' in descending order
                    }
                }]
        else:
            sort_by = [
                {
                    "_score": {
                        "order": "desc"
                    }
                },
                {
                    "created_at": {
                        "order": "desc"  # Sorting by 'created_at' in descending order
                    }
                }]


    # Show the advanced search options in the sidebar
    sidebar = st.sidebar
    sidebar.header("Advanced Search Options")
    with sidebar:
        show_only_summary = False
        num_hits = 10
        show_only_summary = st.checkbox("Only show results with a summary", value=False)
        num_hits = st.slider("Number results", 10, 100, 10)

    if not q:
        st.stop()

    with st.spinner(text='searching...'):
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
            },
            "size": num_hits,
            "sort": sort_by
            }
        )

    # Process the response
    for hit in resp['hits']['hits']:
        print(hit['_source'])  # Prints out the document source
        # Show the timestamp of this run
        now = datetime.now().strftime('%m/%d/%y %H:%M')
        st.subheader("Results")
        st.caption(f"Found {resp['hits']['total']['value']} possible matches, showing {num_hits} matches, completed at {now}.")

    
        # Show a checkbox to only show hits with a summary
        # If the checkbox is checked, only show hits with a summary
        # If the checkbox is not checked, show all hits
        for hit in resp['hits']['hits']:
            # Create a vCon object from the hit
            vcon_dict = hit['_source']
            v = Vcon().from_dict(vcon_dict)
            uuid = hit['_source']['uuid']

            # Make a new UUID
            new_uuid = str(uuid.uuid4())

            details_url = f"{CONV_DETAIL_URL}\"{uuid}\""
            created_at_str  = hit['_source']['created_at']
            created_at = datetime.fromisoformat(created_at_str).strftime('%m/%d/%y %H:%M')
            duration = v.duration()
            dialog_urls = v.get_dialog_urls()
            summary = v.summary()
            dealer_name = v.get_dealer_name()
            customer_name = v.get_customer_name()
            team_name = v.get_team_name()
            agent_email = v.get_agent_mailto()

            if not summary and show_only_summary:
                continue        

            st.divider()
            st.markdown(f"**{created_at}, {duration} sec**")


            # Three columns with different widths
            col1, col2 = st.columns([2,1])
            with col1:
                if summary:
                    st.markdown(
                        f"**Summary** {summary} [Full Details]({details_url})", 
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f"**No summary available**\n\nFor full details, [click here]({details_url})", 
                        unsafe_allow_html=True
                    )
                for url in dialog_urls:
                    st.markdown(
                        f"[Listen]({url}) to the conversation.",
                        unsafe_allow_html=True
                        )
            with col2:
                st.markdown(
                    f"**Dealer**: {dealer_name}",
                    unsafe_allow_html=True
                )
                st.markdown(
                    f"**Team**: {team_name}",
                    unsafe_allow_html=True
                )
                st.markdown(
                    f"**Customer**: {customer_name}",
                    unsafe_allow_html=True
                )

                st.markdown(
                    f"**Agent**: {agent_email}",
                    unsafe_allow_html=True
                )

                st.markdown(
                    f"**Search Score**: {hit['_score']}",
                    unsafe_allow_html=True
                )
                st.download_button("Download", v.to_json(), f"{uuid}.vcon", "application/json", key="download:"+str(new_uuid))


            # Show the highlighted fields controlled by a checkbox
            st.caption(f"vCon: {uuid}, {created_at_str}, {duration} sec")
            if st.checkbox("Show why this result matched", key="result_reason:"+str(new_uuid)):
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