
# Conversational Search
by @howethomas (https://github.com/howethomas)

This Streamlit app searches an ElasticSearch server for simple text based search
of anything that would appear in a vCon: names of agents, customers, phone numbers,
stores - anything contained within the parties, dialogs, attachments and analysis.

The upper left has a sidebar for advanced options, currently to restrict viewed results
to those containing summaries, and the number of results to return. 

## Features

- Search the vCon index by passing any search terms
- Retrieve matching vCons sorted by relevance 
- Display key metadata like date, duration, dealer name, etc.
- Show highlighted matches in the conversation
- Listen to audio recordings of the conversations
- Download the full vCon JSON
- Configure advanced options like number of results and summary filter

## Usage

The script is meant to be run in Streamlit. Simply enter your search terms in the input box.

Advanced configuration options are available in the left sidebar:

- Only show results with a summary 
- Number of results to display

## Implementation

The script uses the official Elasticsearch Python client to query the index.

It connects to a hosted Elasticsearch instance defined in the Streamlit secrets.

The index contains vCon documents - the open conversation standard.

Results are parsed into Vcon objects to extract key fields and build the UI.

## Deployment

This script is designed to run on Streamlit Cloud.

The Elasticsearch credentials need to be configured in the Streamlit secrets:

- `ELASTIC_SEARCH_CLOUD_ID` 
- `ELASTIC_SEARCH_API_KEY`

Other secrets:

- `CONV_DETAIL_URL` - Base URL for the vCon detail pages

## Future Work

Some ideas for enhancing the search:

- Suggest search terms as the user types
- Support more advanced query syntax and operators
- Add filters for metadata fields like date, team, etc
- Page through results
- Build an analytics dashboard for search usage

Let me know if you have any other questions!