import streamlit as st
import streamlit.components.v1 as components
from sap_engine import query_sap_assistant

st.set_page_config(page_title="SAP All-in-One AI Assistant", page_icon="⚡", layout="wide")

st.title("⚡ SAP All-in-One AI Assistant")
st.caption("Coverage: SAP Basis • SAP S/4HANA Functionality • SAP ABAP Programming")

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Process User Query
if user_prompt := st.chat_input("Ask any SAP query..."):
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching online forums, Reddit, and SAP docs..."):
            response = query_sap_assistant(user_prompt)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

    # Automatically scroll down to the newest message
    components.html(
        """
        <script>
            window.parent.document.querySelector('section.main').scrollTo({
                top: window.parent.document.querySelector('section.main').scrollHeight,
                behavior: 'smooth'
            });
        </script>
        """,
        height=0
    )