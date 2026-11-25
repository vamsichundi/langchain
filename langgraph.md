### Langgraph synopsis

## Typed annotations & lambda functions

1. 
2. TypedDict
3. Optional
4. Union
5. Any
6. List
7. Annotated
8. Sequence

```python
from typing import Union, TypedDict, Optional, Any
```

### python packages

1. from typing
2. from random
3. from pathlib
4. from IPython.display
5. from langgraph.graph
6. from langgraph.graph.message
7. from langgraph.prebuilt
8. from langchain_core.messages
9. from langchain_core.tools
10. from langchain_openai

## Elements in Langgraph
1. **state** - shared data structure that holds current info or context of entire application
2. **nodes** - Individual functions or operations that perform specific tasks within graph
3. **graph** - overarching  structure that maps how nodes are connected and executed (represents workflow)
4. **edges** - connections between nodes that determine flow of execution
5. **conditional edges** - specialized connections that decide the next node to execute based on condition or logic
6. **start** - start node is virtual entry point in langgraph marking workflow begins
7. **end** - end node signifies the conclusion of workflow
8. **tools** - specialized funcs or utilities to perform specific tasks (fetching api data)
    - Nodes are part of graph structure while tools are funcs used within nodes
9. **ToolNode** - special kind of node whose main job is to run a tool
10. **StateGraph** - Class in langGraph used to build and compile graph structure
    - manages nodes, edges, and state that workflow operates in unified way
11. **Runnable** - standard executable component to perform specific task within ai workflow (fundamental building block)

## Messages in Langgraph
1. **HumanMessage**    -  Provide Input from User
2. **SystemMessage**   -  Provide Instructions or context to model
3. **AIMessage**       -  Provide responses from AI model
4. **ToolMessage**     -  Result of oa tool call usage
5. **FunctionMessage** -  Result of function call

## Basic Langgraph

<img width="923" height="806" alt="image" src="https://github.com/user-attachments/assets/94ab28ee-c548-4edd-9424-1b0c6790a029" />
