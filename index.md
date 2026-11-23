### Langchain modules

1. langchain.chat_models
2. langchain_google_genai
3. langchain.agents
4. langchain.messages
5. langchain.tools
6. langgraph.types
7. langgraph.checkpoint.memory
8. tavily

### Python useful packages and how to use

```python
from pprint import pprint
from dotenv import load_dotenv
``` 

### Initializing & invoking models chatmodels
```python
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

model = init_chat_model(
    "gpt-5-nano",
    model_kwargs={
      "temperature": 0.5,
      "max_tokens": 5000,
      "use_responses_api": True
    }
)
response = model.invoke("Hello, how are you?")

print(response)
print(response.content)
pprint(response.response_metadata)
```

## For google gen ai

```python
from langchain_google_genai import ChatGoogleGenerativeAI

model = ChatGoogleGenerativeAI(model = "gemini-3-pro-preview")
```

### Creating Agents

we have 3 options to create agents
```python
from langchain.agents import create_agent

agent_1 = create_agent(model=model)
agent_2 = create_agent(model="claude-sonnet-4-5")
agent_3 = create_agent("gpt-5-nano")
```

### Invoking Agents & Passing Human Messages

```python
from langchain.agents import create_agent
from langchain.messages import HumanMessage

agent = create_agent("gpt-5-nano")
response = agent.invoke({
    "messages": [
        HumanMessage(content="Hello, how are you?")
    ]
})

pprint(response['messages'])
```

# Responses includes HumanMessage and AIMessage
```json
{
  "messages": [
    {
      "type": "HumanMessage",
      "content": "Hello, how are you?",
      "additional_kwargs": {},
      "response_metadata": {},
      "id": "e9441bab-539e-42e2-877d-97571b27714a"
    },
    {
      "type": "AIMessage",
      "content": "Hi there! I’m here and ready to help. How can I assist you today?",
      "additional_kwargs": {
        "refusal": null
      },
      "response_metadata": {
        "token_usage": {
          "completion_tokens": 283,
          "prompt_tokens": 12,
          "total_tokens": 295,
          "completion_tokens_details": {
            "accepted_prediction_tokens": 0,
            "audio_tokens": 0,
            "reasoning_tokens": 256,
            "rejected_prediction_tokens": 0
          },
          "prompt_tokens_details": {
            "audio_tokens": 0,
            "cache_write_tokens": null,
            "cached_tokens": 0
          }
        },
        "model_provider": "openai",
        "model_name": "gpt-5-nano-2025-08-07",
        "system_fingerprint": null,
        "id": "chatcmpl-En7Yd3AZecyr60W9BV3KYAlGEZB33",
        "service_tier": "default",
        "finish_reason": "stop",
        "logprobs": null
      },
      "id": "lc_run--01a204bd-160a-7753-a801-9446af316d9a-0",
      "tool_calls": [],
      "invalid_tool_calls": [],
      "usage_metadata": {
        "input_tokens": 12,
        "output_tokens": 283,
        "total_tokens": 295,
        "input_token_details": {
          "audio": 0,
          "cache_read": 0
        },
        "output_token_details": {
          "audio": 0,
          "reasoning": 256
        }
      }
    }
  ]
}
```

### Passing array of Human / AI messages to Agent model

```python
from langchain.agents import create_agent
from langchain.messages import HumanMessage

agent = create_agent("gpt-5-nano")
response = agent.invoke({
    "messages": [
        HumanMessage(content="What's the capital of the moon?")
        AIMessage(content="The capital of the moon is Luna City."),
        HumanMessage(content="Interesting, tell me more about Luna city")
    ]
})

pprint(response)
```

### Streaming Output from Model Response

```python
from langchain.agents import create_agent
from langchain.messages import AIMessage, HumanMessage

agent = create_agent("gpt-5-nano")
inputs = {"messages": [HumanMessage(content="What's the capital of the Moon?"),
    AIMessage(content="The capital of the Moon is Luna City."),
    HumanMessage(content="Interesting, tell me more about Luna City")]}

# stream_mode="messages" yields (token_chunk, metadata) as the LLM generates
for token, metadata in agent.stream(inputs, stream_mode="messages"):
    if token.content:
        print(token.content, end="", flush=True)
print()
```

### To increase model performance pass a system prompt when creating agent

```python
system_prompt = """

you are sr react developer, please analyze the UI developer

User: what are the tech stack in the project?
sr react developer: These are the tech stack React, Redux, ....
"""

dev_agent = create_agent(
  model = "gpt-5-nano",
  system_prompt = system_prompt
)
```


### Understanding Tools

Tools can allow our agent to access data, execute data, even tasks, call agents, call api's

<img width="1948" height="1508" alt="image" src="https://github.com/user-attachments/assets/56d34e3c-ba35-43d1-9017-26a9acb1521d" />

## Creating tools & Adding to agents

```python
from langchain.tools import tool
from langchain.agents import create_agent
from langchain.messages import HumanMessage 

@tool("square_root")
def tool1(x: float) -> float:
    """ Calculate the square root of a number """
    return x ** 0.5

@tool("square_root", description = "Calculate the square root of a number ")
def tool1(x: float) -> float:
    return x ** 0.5

# tool1.invoke({ "x": 100 })

agent = create_agent(
  model = "gpt-5-nano",
  system_prompt = "You are able to maths functions",
  tools = [tool1]
)

response.invoke({
    "messages": [HumanMessage(content = "what is the square root of 467")]
})

print(response['messages'[[-1].content)
print(response['messages'])
print(response['messages'].tool_calls)

# it will return toolmessage in response
```

### Searching Web for latest info (Using Tavily)

```python
from dotenv import load_dotenv
from langchain.tools import tool
from langchain.agents import create_agent
from langchain.messages import HumanMessage 


load_dotenv()

agent = create_agent(
  model = "gpt-5-nano",
  system_prompt = "You are able to maths functions"
)

response = agent.invoke({
    "messages": [HumanMessage(content = "who is the president of current mayor (president of houston city")]
})

print(response['messages'][-1].content)
```

### Using Tavily tool for web crawl

```python
from dotenv import load_dotenv
from langchain.tools import tool
from langchain.agents import create_agent
from langchain.messages import HumanMessage 
from tavily import TavilyClient
from typing import List, Dict, Any


load_dotenv()

tavily_client = TavilyClient()


@tool("web_search", description="Search the web for information")
def web_search(query: str) -> List[Dict[str, Any]]:
    return tavily_client.search(query)

web_search.invoke("What is the capital of Andhra Pradesh?")

agent = create_agent(
  model = "gpt-5-nano",
  system_prompt = "You are able to search the web for information",
  tools = [web_search]
)

response = agent.invoke({
    "messages": [HumanMessage(content = "What is the capital of Andhra Pradesh?")]
})

#print(response['messages'][-1].content)
Amaravati is the capital of Andhra Pradesh.

Context:
- Hyderabad served as the shared capital for Andhra Pradesh and Telangana until June 2, 2024.
- In 2026, Amaravati was legally recognized as the sole capital of Andhra Pradesh (retroactively from June 2, 2024).
```

### Messages to be saved (Inmemory Checkpoint saver) Temporarrily 

``` python

from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver

agent = create_agent(
    "gpt-5-nano",
    checkpointer = InMemorySaver(),
)

config = {
    "configurable": { "thread_id": "1"}}
}
messages = {
    "messages": []
}
response = agent.invoke(messages, config)
print(response)

```

### passing images to model

```python


from dotenv import load_dotenv
from langchain.tools import tool
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from ipywidgets import FileUpload
from IPython.display import display
import base64

load_dotenv()

uploader = FileUpload(accept=".jpg,.png", multiple=False)
display(uploader)

uploaded_file = uploader.value[0]
file_name = uploaded_file["metadata"]["name"]
file_content = uploaded_file["content"]

file_binary = bytes(file_content)
file_base64 = base64.b64encode(file_binary).decode("utf-8")

agent = create_agent(
    model="gpt-5-nano", system_prompt="You are able to search the web for information"
)

multiModalInput = {
    "messages": [
        HumanMessage(
            content=[
                {"type": "text", "text": "What is this image about?"},
                {
                    "type": "image",
                    "base64": file_base64,
                    "mime_type": uploaded_file["metadata"]["type"],
                },
            ]
        )
    ]
}

response = agent.invoke(multiModalInput)
print(response.content[0].text)

```

Example for small agent related to personal chef

```python
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from dotenv import load_dotenv
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
from tavily import TavilyClient
from typing import Any, Dict
from pprint import pprint

load_dotenv()

tavily_client = TavilyClient()

@tool("get_recipe", description="Get a recipe for a given dish")
def get_recipe(ingredient: str) -> Dict[str, Any]:
    """Get a recipe for a given ingredient"""
    return tavily_client.search(ingredient)

question = {
    "messages": [
        HumanMessage(content="What is a good recipe for pulihora?")   
    ]
}
config = {
    "configurable": {
        "thread_id": "1"
    }
}

system_prompt = "You are a personal chef that can help me with recipes and cooking tips."
agent = create_agent(
    model="gpt-5-nano",
    system_prompt=system_prompt,
    tools=[get_recipe],
    checkpointer=InMemorySaver(),
)

response = agent.invoke(question, config=config)
pprint(response['messages'][-1].content)
```

### Multi Agent Example

```python
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from dotenv import load_dotenv
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
from tavily import TavilyClient
from typing import Any, Dict
from pprint import pprint

load_dotenv()
tavily_client = TavilyClient()

@tool("web_search", description="Search the web for information")
def web_search(query: str) -> Dict[str, Any]:
    """Search the web for information"""
    return tavily_client.search(query)

@tool("get_recipe", description="Get a recipe for a given dish")
def get_recipe(ingredient: str) -> Dict[str, Any]:
    """Get a recipe for a given ingredient"""
    return tavily_client.search(ingredient)

agent_chef = create_agent(
    model="gpt-5-nano",
    system_prompt="You are a personal chef that can help me with recipes and cooking tips.",
    tools=[get_recipe],
)

agent_web = create_agent(
    model="gpt-5-nano",
    system_prompt="You are a helpful assistant.",
    tools=[web_search],
)

@tool("call_web_search", description="Call the web search agent")
def call_web_search(query: str) -> Dict[str, Any]:
    response = agent_web.invoke({"messages": [HumanMessage(content=query)]})
    return response["messages"][-1].content

@tool("call_personal_chef", description="Call the personal chef agent")
def call_personal_chef(ingredient: str) -> Dict[str, Any]:
    response = agent_chef.invoke({"messages": [HumanMessage(content=ingredient)]})
    return response["messages"][-1].content

agent_multi = create_agent(
    model="gpt-5-nano",
    system_prompt="You are a helpful assistant that can call other agents to get information.",
    tools=[call_web_search, call_personal_chef],
)

response = agent_multi.invoke({"messages": [HumanMessage(content="What is a good recipe for pulihora?")]})

pprint(response["messages"][-1].content)
```
