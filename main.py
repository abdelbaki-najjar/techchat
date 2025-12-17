import streamlit as st
try:
    from openai.error import OpenAIError
except ImportError:
    OpenAIError = Exception  # استخدام استثناء عام إذا لم يتم التعرف على OpenAIError
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_openai import ChatOpenAI
#from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Set up ChatOpenAI
chat = ChatOpenAI(temperature=0.5)

# Style setup
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("🥰🥰يمكنك طرح أي سؤال وسأجيب عنه")

# Initialize conversation in session state
if 'flowmessages' not in st.session_state:
    st.session_state['flowmessages'] = [
        SystemMessage(content="أنت معلم خبير في إعداد مذكرات بيداغوجية وانتاج تمرينات ومسائل نموذجية")
    ]

conversation = st.session_state['flowmessages']

# Function to load OpenAI model and get response
def get_chatmodel_response(question):
    try:
        conversation.append(HumanMessage(content=question))
        answer = chat(conversation)
        conversation.append(AIMessage(content=answer.content))
        return answer.content
    except OpenAIError as e:
        if 'rate limits' in str(e):
            return "نعتذر، لقد تجاوزنا الحد المجاني للاستخدام. سيعود التطبيق للعمل قريبًا، يرجى المحاولة لاحقًا."
        else:
            return f"حدث خطأ أثناء التواصل مع النظام: {str(e)}"

# Display chat history
for message in conversation[1:]:
    if isinstance(message, HumanMessage):
        with st.chat_message("user", avatar="🤔"):
            st.write(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.write(message.content)

# Input field for user query
prompt = st.chat_input("أرجوك حاول أن تجعل سؤالك واضحا قدر الإمكان")
if prompt:
    # Display user message in chat message container
    with st.chat_message("user", avatar="🤔"):
        st.markdown(prompt)
    # Get AI response
    response = get_chatmodel_response(prompt)
    with st.chat_message("assistant"):
        st.markdown(response)
