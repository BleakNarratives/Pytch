"""
[DNA_TAG]
ORIGIN: Moto4_A9
PILLAR: valet_concierge
PATH: MotherBrain.py
LAST_SYNC: 2026-08-02T01:13:33Z
[/DNA_TAG]
"""
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

# State definition (tracks messages and task status)
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    next: str  # "researcher", "analyzer", or END

# Tools
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
search = TavilySearch(max_results=2)

# MotherBrain node: Decides and delegates
def motherbrain_node(state: AgentState):
    msg = state["messages"][-1]
    # Simple routing: If query needs data, go to researcher; else analyze
    if "weather" in msg.content.lower() or "search" in msg.content.lower():
        return {"messages": [AIMessage(content="Delegating to Researcher...")], "next": "researcher"}
    else:
        return {"messages": [AIMessage(content="Analyzing directly...")], "next": "analyzer"}

# Researcher node: Uses search tool
def researcher_node(state: AgentState):
    query = state["messages"][-1].content
    results = search.invoke(query)
    return {
        "messages": [
            AIMessage(content=f"Research results: {results}"),
            ToolMessage(content=str(results), tool_call_id="search_1")
        ],
        "next": "analyzer"
    }

# Analyzer node: Summarizes with LLM
def analyzer_node(state: AgentState):
    prompt = "Summarize the research for the user: " + "\n".join([m.content for m in state["messages"][-1:]])
    summary = model.invoke([HumanMessage(content=prompt)])
    return {"messages": [summary], "next": END}

# Build the graph
workflow = StateGraph(AgentState)
workflow.add_node("motherbrain", motherbrain_node)
workflow.add_node("researcher", researcher_node)
workflow.add_node("analyzer", analyzer_node)

# Edges: MotherBrain routes, then sequential
workflow.set_entry_point("motherbrain")
workflow.add_conditional_edges("motherbrain", lambda s: s["next"], {"researcher": "researcher", "analyzer": "analyzer"})
workflow.add_edge("researcher", "analyzer")
workflow.add_edge("analyzer", END)

# Compile and run
app = workflow.compile()

# Invoke
result = app.invoke(
    {"messages": [HumanMessage(content="What's the weather like in Tokyo today?")]},
    {"configurable": {"thread_id": "mb-thread"}}
)
print(result["messages"][-1].content)  # MotherBrain-coordinated summary