import streamlit as st
import requests
import json
import sseclient

# API endpoint and key
API_URL = "https://api.together.xyz/v1/chat/completions"
API_KEY = st.secrets["TOGETHER_API_KEY"]

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def get_ai_response(messages):
    data = {
        "model": "meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",
        "messages": messages,
        "max_tokens": 512,
        "temperature": 0.7,
        "top_p": 0.7,
        "top_k": 50,
        "repetition_penalty": 1,
        "stop": ["<|eot_id|>"],
        "stream": True
    }

    response = requests.post(API_URL, headers=headers, json=data, stream=True)
    client = sseclient.SSEClient(response)

    full_response = ""
    for event in client.events():
        if event.data != "[DONE]":
            try:
                chunk = json.loads(event.data)
                content = chunk['choices'][0]['delta'].get('content', '')
                full_response += content
                yield content
            except json.JSONDecodeError:
                pass

st.title("Consulta de Leyes de Guatemala")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Eres un asistente experto en leyes guatemaltecas. Proporciona información precisa y actualizada sobre la legislación de Guatemala."}
    ]

# Display chat messages from history on app rerun
for message in st.session_state.messages[1:]:  # Skip the system message
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Ingrese su consulta sobre leyes guatemaltecas:"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in get_ai_response(st.session_state.messages):
            full_response += response
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})

st.sidebar.title("Acerca de")
st.sidebar.info(
    "Esta aplicación utiliza inteligencia artificial para responder preguntas sobre las leyes de Guatemala. "
    "La información proporcionada se basa en el conocimiento del modelo de lenguaje y puede no estar completamente actualizada. "
    "Para información legal oficial y actualizada, consulte siempre las fuentes gubernamentales oficiales."
)
st.sidebar.title("Instrucciones")
st.sidebar.markdown(
    """
    1. Ingrese su pregunta sobre leyes guatemaltecas en el campo de chat.
    2. El asistente AI responderá con la información solicitada.
    3. Puede hacer preguntas de seguimiento o iniciar nuevos temas en cualquier momento.
    4. Recuerde que esta es una herramienta informativa y no sustituye el asesoramiento legal profesional.
    """
)
