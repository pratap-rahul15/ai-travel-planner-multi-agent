import os

# Creating a state graph for a simple conversation (memory) with a language model (LLM) and a human user. The graph will have states for the LLM's response, the human's response, and the system's response. The graph will also have transitions between these states based on the messages exchanged.
from typing import TypedDict, Annotated
import operator


import dotenv
import psycopg
from langgraph.graph import StateGraph, START, END
# To connect to a PostgreSQL database to the langraph application, we will use the psycopg library. We will create a PostgresSaver class that will handle the saving of the graph's state to the database. This class will have methods for connecting to the database, saving the graph's state, and retrieving the graph's state.
from langgraph.checkpoint.postgres import PostgresSaver
from langchain_core.messages import (
    AnyMessage,
    HumanMessage,
    AIMessage,
    SystemMessage,
)

# We will use the ChatGroq class from the langchain_groq library to create a language model that can generate responses based on the messages exchanged in the conversation. The ChatGroq class will be used to create an instance of the language model that will be used in the state graph.
from langchain_groq import ChatGroq

# We will also use some tools to enhance the capabilities of the language model. For example, we can use the tavily_tool to search for information on the web and the flight_tool to search for flights. These tools will be integrated into the state graph to allow the language model to use them when generating responses.
from tools.tavily_tool import tavily_search
from tools.flight_tool import search_flights

from dotenv import load_dotenv
load_dotenv()

# Which llm to use for the conversation. We will use the ChatGroq class from the langchain_groq library to create an instance of the language model that will be used in the state graph. The model parameter specifies which version of the model to use, and in this case, we are using the "llama-3.3-70b-versatile" model.
llm = ChatGroq(
    model="llama-3.3-70b-versatile"
)

#  To connect to the PostgreSQL database, we will create an instance of the PostgresSaver class. This class will handle the saving of the graph's state to the database. We will pass the connection parameters for the database, such as the host, port, database name, user, and password, which are retrieved from environment variables.
DATABASE_URL = os.getenv("DATABASE_URL")

# Now we will create a state graph for the conversation. The state graph will have states for the LLM's response, the human's response, and the system's response. The graph will also have transitions between these states based on the messages exchanged. We will use the StateGraph class from the langgraph library to create the state graph.
class TravelState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    user_query: str
    flight_results: str
    hotel_results: str
    itinerary: str
    llm_calls: int
# Now lets's create all the individual agent, which is also called as the worker node, which is responsible for handling a specific task in the conversation.

# Flight Agent
def flight_agent(state: TravelState):
    query = state["user_query"]
    flight_data = search_flights(query)
    return {
        "flight_results": flight_data,
        "messages" : [
            AIMessage(content=f"Flight results fetched for your query")
        ],
        "llm_calls": state.get("llm_calls", 0) + 1
    }

# Hotel Agent
def hotel_agent(state: TravelState):
    query = f"Best hotels for {state['user_query']}"
    hotel_results = tavily_search(query)

    return {
        "hotel_results": hotel_results,
        "messages": [
            AIMessage(content="Hotel information fetched")
        ],
        "llm_calls": state.get("llm_calls", 0) + 1
    }

# Itinerary Agent
def itinerary_agent(state: TravelState):

    prompt = f"""
    Create a travel itinerary. 
    User Query:
    {state['user_query']}

    Flight Results:
    {state['flight_results']}

    Hotel Results:
    {state['hotel_results']}
    """

    response = llm.invoke([
        SystemMessage(
            content="You are an expert travel planner"
        ),
        HumanMessage(content=prompt)
    ])

    return {
        "itinerary": response.content,
        "messages": [response],
        "llm_calls": state.get("llm_calls", 0) + 1
    }

# Final Response Agent
def final_agent(state: TravelState):

    final_prompt = f"""
    Generate final travel response.

    Flights:
    {state['flight_results']}

    Hotels:
    {state['hotel_results']}

    Itinerary:
    {state['itinerary']}
    """

    response = llm.invoke([
        HumanMessage(content=final_prompt)
    ])

    return {
        "messages": [response],
        "llm_calls": state.get("llm_calls", 0) + 1
    }



# Now to see the whole picture, we will create a state graph that connects all these agents together. The graph will have transitions between the states based on the messages exchanged in the conversation.
graph = StateGraph(TravelState)

# Now add all the nodes(agents in a graph in the langraph)
graph.add_node("flight_agent", flight_agent)
graph.add_node("hotel_agent", hotel_agent)
graph.add_node("itinerary_agent", itinerary_agent)
graph.add_node("final_agent", final_agent)

# Now we will define the transitions between the states in the graph. The transitions will be based on the messages exchanged in the conversation. For example, after the user query is received, we will transition to the flight_agent to fetch flight information, then to the hotel_agent to fetch hotel information, and finally to the itinerary_agent to create a travel itinerary based on the fetched information.
# Now connect these nodes inside the langraph
graph.add_edge(START, "flight_agent")
graph.add_edge("flight_agent", "hotel_agent")
graph.add_edge("hotel_agent", "itinerary_agent")    
graph.add_edge("itinerary_agent", "final_agent")
graph.add_edge("final_agent", END)


_conn = psycopg.connect(
    DATABASE_URL,
    autocommit=True
)

checkpointer = PostgresSaver(_conn)
checkpointer.setup()

# To compile the graph.
app = graph.compile(checkpointer=checkpointer)


if __name__ == "__main__":
    config = {
        "configurable": {
            "thread_id": "user_rahul"
        }
    }

    user_input = input("Enter travel request: ")

    result = app.invoke(
        {
            "messages": [
                HumanMessage(content=user_input)
            ],
            "user_query": user_input,
            "flight_results": "",
            "hotel_results": "",
            "itinerary": "",
            "llm_calls": 0
        },
        config=config
    )

    print("\nFINAL RESPONSE:\n")

    for msg in result["messages"]:
        print(msg.content)