from langchain.agents import AgentState, create_agent
from langchain.messages import HumanMessage, ToolMessage
from langchain.tools import ToolRuntime, tool
from langgraph.types import Command
from dotenv import load_dotenv
from tavily import TavilyClient
from typing import Any, Dict
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_community.utilities import SQLDatabase
from pprint import pprint
from pathlib import Path
import asyncio


load_dotenv()

tavily_client = TavilyClient()

DB_PATH = Path(__file__).parent / "resources" / "Chinook.db"
db = SQLDatabase.from_uri(f"sqlite:///{DB_PATH}")
client = MultiServerMCPClient(
    {
        "travel_server": {
                "transport": "streamable_http",
                "url": "https://mcp.kiwi.com"
            }
    },
    tool_interceptors=[],
)

# `await` only works inside an async function in a .py file (notebooks allow it at top level)
tools = asyncio.run(client.get_tools())


@tool("web_search", description="Search the web for information")
def web_search(query: str) -> Dict[str, Any]:
    """Search the web for information"""
    return tavily_client.search(query)


@tool("get_playlist", description="Get a playlist for a given genre")
def get_playlist(query: str) -> str:
   try:
       return db.run(query)
   except Exception as e:
       return f"Error: {e}"
   

class WeddingState(AgentState):
    origin: str
    destination: str
    guest_count: int
    genre: str

travel_agent = create_agent(
    name="travel_agent",
    model="gpt-5-nano",
    system_prompt="""
        You are a travel agent. Search for flights to the desired destination wedding location.
        You are not allowed to ask any more follow up questions, you must find the best flight options based on the following criteria:
        - Price (lowest, economy class)
        - Duration (shortest)
        - Date (time of year which you believe is best for a wedding at this location)
        To make things easy, only look for one ticket, one way.
        You may need to make multiple searches to iteratively find the best options.
        You will be given no extra information, only the origin and destination. It is your job to think critically about the best options.
        If the MCP tool fails, returns malformed output, or does not give you usable flight results, try the tool again.
        Once you have found the best options, let the user know your shortlist of options.
        """,
    tools=tools
)

venue_agent = create_agent(
    name="venue_agent",
    model="gpt-5-nano",
    system_prompt="""
    You are a venue specialist. Search for venues in the desired location, and with the desired capacity.
    You are not allowed to ask any more follow up questions, you must find the best venue options based on the following criteria:
    - Price (lowest)
    - Capacity (exact match)
    - Reviews (highest)
    You may need to make multiple searches to iteratively find the best options. 
    You have a suggested limit of 12 web searches. Count every web_search call you make.
    After 12 searches, you should stop searching and summarize the best options you have
    found so far.
    """,
    tools=[web_search]
)

playlist_agent = create_agent(
    name="playlist_agent",
    model="gpt-5-nano",
    tools=[get_playlist],
    system_prompt="""
    You are a playlist specialist. Query the sql database and curate the perfect playlist for a wedding given a genre.
    Once you have your playlist, calculate the total duration and cost of the playlist, each song has an associated price.
    If you run into errors when querying the database, try to fix them by making changes to the query.
    Do not come back empty handed, keep trying to query the db until you find a list of songs.

    This is a SQLite database. Before writing any data queries, first discover the schema.
    """
)

@tool("search_flights", description="Travel agent to search for flights to the desired destination wedding location")
async def search_flights(runtime: ToolRuntime) -> str:
    # MCP tools are async-only, so this sub-agent must be called with ainvoke
    origin = runtime.state["origin"]
    destination = runtime.state["destination"]
    guest_count = runtime.state["guest_count"]
    response = await travel_agent.ainvoke({
        "messages": [HumanMessage(content=f"Search for flights from {origin} to {destination} for {guest_count} guests.")]
    })
    return response["messages"][-1].content
    

@tool("search_venues", description="Venue specialist to search for venues in the desired location and with the desired capacity")
def search_venues(runtime: ToolRuntime) -> str:
    destination = runtime.state["destination"]
    guest_count = runtime.state["guest_count"]
    response = venue_agent.invoke({
        "messages": [HumanMessage(content=f"Search for venues in {destination} with a capacity of {guest_count}.")]
    })
    return response["messages"][-1].content

@tool("suggest_playlist", description="Playlist specialist to curate the perfect playlist for a wedding given a genre")
def suggest_playlist(runtime: ToolRuntime) -> str:
    genre = runtime.state["genre"]
    response = playlist_agent.invoke({
        "messages": [HumanMessage(content=f"Curate the perfect playlist for a wedding with the genre {genre}.")]
    })
    return response["messages"][-1].content


@tool("update_wedding_state", description="Update the wedding state with the origin, destination, guest count, and genre")
def update_wedding_state(origin: str, destination: str, guest_count: int, genre: str, runtime: ToolRuntime) -> Command:
    return Command(update = {
        "origin": origin,
        "destination": destination,
        "guest_count": guest_count,
        "genre": genre,
        "messages": [ToolMessage(f"Updated wedding state with origin: {origin}, destination: {destination}, guest count: {guest_count}, genre: {genre}", tool_call_id=runtime.tool_call_id)]
    })

main_agent = create_agent(
    name="wedding_coordinator",
    model="gpt-5-nano",
    system_prompt="""
    You are a wedding coordinator. 
    First find all the information you need to update the state. When you have the information, update the state.
    Once that has completed and returned, you can delegate the tasks 
    to your specialists for flights, venues, and playlists.
    Once you have received their answers, coordinate the perfect wedding for me.
    """,
    tools=[update_wedding_state, search_flights, search_venues, suggest_playlist],
    state_schema=WeddingState,
)


async def main():
    response = await main_agent.ainvoke(
        {"messages": [HumanMessage(content="I'm flying from London. I want to plan a wedding in Paris, France for 100 guests, and I want a jazz playlist.")]},
        config={
            "tags": ["wedding_planner"],
            "recursion_limit": 30,
        },
    )
    print(response["messages"][-1].content)
if __name__ == "__main__":
    asyncio.run(main())
