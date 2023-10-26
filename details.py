"""
Elastic Search / vCons

"""
import streamlit as st
from vcon import Vcon
from datetime import datetime

st.set_page_config(
     page_title='Strolid vCon Details',
     )

def main():
    # Show the timestamp of this run
    now = datetime.now()
    st.text(f"Last run: {now}")

    #Upload a vCon file
    uploaded_file = st.file_uploader("Choose a vCon file", type="json")

    # If a file is uploaded
    # Read the file
    # Convert to a Vcon object
    # Display the vCon object
    if uploaded_file is not None:
        vcon_json = uploaded_file.read()
        vcon = Vcon().from_json(vcon_json)
        created_at_str = datetime.fromisoformat(vcon.created_at).strftime('%Y-%m-%d %H:%M:%S')

        # Show the overall summary of the vCon
        # include the vCon UUID, created_at, updated_at
        # a summary if available and the list of the parties
        st.header("vCon Summary")
        st.write(f"UUID: {vcon.uuid}")
        st.write(f"Created: {created_at_str}")
        st.write(f"Updated: {vcon.updated_at}")
        st.write(f"Summary: {vcon.summary()}")
        st.write(f"Parties: {vcon.get_party_names()}")

        # If there's recorded dialog, show it
        if vcon.dialog:
            st.header("Recorded Dialog")
            for dialog in vcon.dialog:
                # Show a link to the audio file
                st.audio(dialog.get("url"))

        # If there's a transcript, show it
        transcript = vcon.get_transcript()
        if transcript:
            st.header("Transcript")
            st.write(transcript)
        
        # Show the vCon object if the user clicks the checkbox
        if st.checkbox("Show vCon object"):
            st.write(vcon)


# Run main()

if __name__ == '__main__':
    main()