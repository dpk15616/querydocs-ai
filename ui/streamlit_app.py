import os

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL", "http://localhost:8000")


def parse_api_error(response: requests.Response) -> str:
    try:
        payload = response.json()
    except ValueError:
        return response.text.strip() or "The backend returned an empty response."

    if isinstance(payload, dict):
        return payload.get("detail") or payload.get("message") or str(payload)
    return str(payload)


st.title("QueryDocs AI")

if "messages" not in st.session_state:
    st.session_state.messages = []

uploaded = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded:
    try:
        upload_response = requests.post(
            f"{API_URL}/upload",
            files={"file": uploaded},
            timeout=180,
        )
        if upload_response.ok:
            st.success("File uploaded and processed successfully.")
        else:
            st.error(
                f"Upload failed ({upload_response.status_code}): "
                f"{parse_api_error(upload_response)}"
            )
    except requests.RequestException as exc:
        st.error(f"Could not reach the backend at {API_URL}: {exc}")

col1, col2 = st.columns([6, 1])
with col2:
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a question about your document"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            payload = {
                "question": prompt,
                "chat_history": st.session_state.messages[:-1]
            }
            res = requests.post(f"{API_URL}/query", json=payload, timeout=60)
            if res.ok:
                response_data = res.json()
                answer = response_data.get("answer", "No answer returned.")
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            else:
                error_msg = f"Query failed ({res.status_code}): {parse_api_error(res)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": f"❌ {error_msg}"})
        except requests.RequestException as exc:
            error_msg = f"Could not reach the backend at {API_URL}: {exc}"
            st.error(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": f"❌ {error_msg}"})
        except ValueError:
            error_msg = "The backend returned a non-JSON response for this query."
            st.error(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": f"❌ {error_msg}"})
