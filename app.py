import boto3
import streamlit as st
import boto3
from dotenv import load_dotenv
import os
load_dotenv()

# Read from env
KNOWLEDGE_BASE_ID = os.getenv("KNOWLEDGE_BASE_ID")
MODEL_ARN = os.getenv("MODEL_ARN")
REGION = os.getenv("AWS_DEFAULT_REGION")


client = boto3.client(
    "bedrock-agent-runtime",
    region_name=REGION
)

def query_kb(question):
    response = client.retrieve_and_generate(
        input={"text": question},
        retrieveAndGenerateConfiguration={
            "type": "KNOWLEDGE_BASE",
            "knowledgeBaseConfiguration": {
                "knowledgeBaseId": KNOWLEDGE_BASE_ID,
                "modelArn": MODEL_ARN
            }
        }
    )
    answer= response["output"]["text"]

    sources =[]
    try:
        citations=response['citations']
        for item in citations:
            for ref in item["retrievedReferences"]:

                sources.append(ref["content"]["text"])
    except:
        pass
    return answer, sources

    

# st.title("🥗 Diet RAG Chatbot")

# user_input = st.text_input("Ask your diet question:")

# if st.button("Ask"):
#     if user_input:
#         with st.spinner("Thinking..."):
#             answer = query_kb(user_input)
#             st.success(answer)


# ---------------- UI ---------------- #

st.set_page_config(page_title="Diet RAG Chatbot", layout="wide")

st.title("🥗 Diet RAG Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User input (chat style)
user_input = st.chat_input("Ask your diet question...")

if user_input:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.chat_message("user"):
        st.write(user_input)

    # Get response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer,sources = query_kb(user_input)
            st.write(answer)
            if sources:
                with st.expander("📄 Source Chunks"):
                    for i, src in enumerate(sources):
                        st.markdown(f"**Chunk {i+1}:**")
                        st.write(src)
                        st.markdown("---")

    # Save response
    st.session_state.messages.append({"role": "assistant", "content": answer})