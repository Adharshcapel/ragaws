import streamlit as st
import requests

API_URL ="http://54.152.78.189:8000/query"


st.set_page_config(page_title="Diet RAG Chatbot", layout="wide")

st.title("🥗 Diet RAG Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msgs in st.session_state.messages:
    with st.chat_message(msgs['role']):
        st.write(msgs['content'])
        
## user input
user_input = st.chat_input('Ask your diet')

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        with st.spinner('Thinking'):
            try:
                response=requests.post(
                    API_URL,
                    params={"question":user_input},
                    timeout=100
                )
                data= response.json()
                answer = data.get("answer", "No answer received")
                sources = data.get("sources", [])
                st.write(answer)
                with st.expander("source chunks"):
                    for i,src in enumerate(sources):
                        st.markdown(f"** chunk {i+1}")
                        st.write(src)
                        st.markdown("---")

            except Exception as e:
                st.error(f'Error:{str(e)}')
                answer = "something went wrong"

        st.session_state.messages.append({"role": "assistant", "content": answer})