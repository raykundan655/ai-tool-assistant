import streamlit as st
from tool_backend import chatbot,find_all_thread
from langchain_core.messages import HumanMessage,AIMessage
import uuid



def generat_thread_id():
    thread_id=uuid.uuid4()
    return thread_id


def add_thread(thread_id):
    if thread_id not in st.session_state['chat_thread']:
        st.session_state['chat_thread'].append(thread_id)


def reset_chat():
    thread_id=generat_thread_id()
    st.session_state['thread_id']=thread_id
    st.session_state['history'] = [] 
    add_thread(thread_id)


def load_convo(thread_id):
    state=chatbot.get_state(
        config={'configurable':{'thread_id':thread_id}}
    )

    return state.values.get('messages',[])




if 'history' not in st.session_state:
    st.session_state['history']=[]


if 'thread_id' not in st.session_state:
    st.session_state['thread_id']=generat_thread_id()

if 'chat_thread' not in st.session_state:
    st.session_state['chat_thread']=list(find_all_thread())

add_thread(st.session_state['thread_id'])




st.sidebar.title('My Chat ')
if st.sidebar.button('New Chat'):
    reset_chat()
    st.sidebar.header('MyConvo..')

for thread_id in st.session_state['chat_thread'][::-1]:
    if st.sidebar.button(str(thread_id)):
        st.session_state['thread_id']=thread_id

        message=load_convo(thread_id)

        temp_msg=[]

        for msg in message:
            role=""
            if isinstance(msg,HumanMessage):
                role='user'
            else:
                role='assistant'

            temp_msg.append({'role':role,'text':msg.content})

        st.session_state['history']=temp_msg







for ele in st.session_state['history']:
    role=ele['role']
    if role=='user':
         with st.chat_message('user'):
            st.write(ele['text'])
    else:
         with st.chat_message('assistant'):
             st.write(ele['text'])




user_input=st.chat_input('Typing...')

# CONFIG = {
#     'configurable': {
#         'thread_id': st.session_state['thread_id']
#     }
# }

# it help in observability
CONFIG = {
    'configurable': {
        'thread_id': st.session_state['thread_id']
    },
    'metadata':{'thread_id': st.session_state['thread_id']},
    'run_name':'chat_turn'
}


if user_input:
   
    with st.chat_message('user'):
        st.session_state['history'].append({'role':'user','text':user_input})
        st.write(user_input)

    with st.chat_message('assistant'):
        response=""

        for msg,metadata in chatbot.stream(
                    {'messages': [HumanMessage(content=user_input)]},
                    CONFIG,
                    stream_mode='messages'
            ):
             if isinstance(msg, AIMessage)  and isinstance(msg.content, str):
                response += msg.content
                st.write(msg.content)

        st.session_state['history'].append({'role':'assistant','text':response})


    
    



