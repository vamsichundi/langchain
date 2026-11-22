### Langchain modules

1. langchain.chat_models
2. langchain_google_genai
3. langchain.agents
4. langchain.messages
5. langchain.tools

### Python useful packages and how to use

```
from pprint import pprint
from dotenv import load_dotenv
``` 

### Initializing & invoking models chatmodels
```
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

```
from langchain_google_genai import ChatGoogleGenerativeAI

model = ChatGoogleGenerativeAI(model = "gemini-3-pro-preview")
```

### Creating Agents

we have 3 options to create agents
```
from langchain.agents import create_agent

agent_1 = create_agent(model=model)
agent_2 = create_agent(model="claude-sonnet-4-5")
agent_3 = create_agent("gpt-5-nano")
```

### Invoking Agents & Passing Human Messages

```
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

```
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

```
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

```
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

              
