from langgraph.graph import StateGraph,START,END
from langchain_core.messages import BaseMessage,HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from typing import TypedDict,Annotated
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
from langgraph.prebuilt import ToolNode,tools_condition
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool
import requests
import os

load_dotenv()


@tool 
def calculator(first_num:float,second_num:float,operation:str)->dict:
    """This function is going to perform math calculation such as add,sub,multiply,divide"""
    try:
        if operation=="add":
            result=first_num+second_num
        elif operation=='sub':
            result=first_num-second_num
        elif operation=="multiply":
            result=first_num*second_num
        elif operation=='divide':
            if second_num==0:
                raise Exception({'Error':"second_num not can't be zero"})
            result = first_num / second_num
        else:
            return {'Error':"it is not valid operation"}
    except Exception as e:
        return str(e)

    return {'result':result}

search_tool=DuckDuckGoSearchRun()


@tool
def getweather(city:str)->dict:
    """Get the current weather of a particular city."""

    url = "https://api.weatherapi.com/v1/current.json"

    params = {
        "key": os.getenv("WEATHER_API_KEY"),
        "q": city
    }

    response=requests.get(url,params=params)

    return response.json()




tools=[getweather,calculator,search_tool]



model=ChatGoogleGenerativeAI(
    model="gemini-2.5-flash"
)

model_tool_bind=model.bind_tools(tools)


class chatState(TypedDict):
    messages: Annotated[
            list[BaseMessage],
            add_messages
        ]


def talkwithLLM(state:chatState):
    msg=state['messages']
    # from_message can take mutiple msg
    prompt=ChatPromptTemplate.from_messages([
        ('system',"""You are a helpful, friendly, and intelligent AI assistant.

            Your job is to answer the user's questions accurately and clearly.

            Guidelines:
            - Understand the user's question before answering.
            - Give direct and useful answers.
            - Explain concepts step-by-step when the user is learning something.
            - Keep answers concise unless the user asks for more detail.
            - If you are unsure about something, be honest rather than making up information.
            - Maintain context from the previous conversation.
            - Use examples or code when they make the explanation easier to understand.
            - Be polite and professional.
            """),
               *msg

                ])
    
    chain=prompt|model_tool_bind
    response=chain.invoke({})

    return {'messages':[response]}


Tool_Node=ToolNode(tools)

graph=StateGraph(chatState)

graph.add_node('chitchat',talkwithLLM)
graph.add_node('tools',Tool_Node)

graph.add_edge(START,'chitchat')
graph.add_conditional_edges('chitchat',tools_condition)
graph.add_edge('tools','chitchat')


conn=sqlite3.connect(database='chatdb.db',check_same_thread=False)

checkpoint=SqliteSaver(conn)

chatbot=graph.compile(checkpointer=checkpoint)


def find_all_thread():
    threads=set()
    for point in checkpoint.list(None):
        threads.add(point.config['configurable']['thread_id'])
    return threads











        #          START
        #            │
        #            ▼
        #      ┌───────────┐
        #      │ chitchat  │
        #      │    LLM    │
        #      └─────┬─────┘
        #            │
        #      tools_condition
        #         /       \
        #       YES        NO
        #        │          │
        #        ▼          ▼
        #   ┌─────────┐    END
        #   │  tools  │
        #   │ToolNode │
        #   └────┬────┘
        #        │
        #        ▼
        #     chitchat