from langgraph.graph import START,END,StateGraph
from langgraph.checkpoint.memory import MemorySaver
from langchain.tools import tool

from graph.nodes import llm_call_order_management,llm_call_food_search,tool_call,tool_call_async
from graph.state import OrderManagementState,FoodSearchState
from graph.edges import should_continue



def creat_OrderManager_subgraph():
    
    ordermanager_graph_builder=StateGraph(OrderManagementState)
    
    ordermanager_graph_builder.add_node('LLM',llm_call_order_management)
    ordermanager_graph_builder.add_node('tool',tool_call)
    
    
    ordermanager_graph_builder.add_edge(START,'LLM')
    ordermanager_graph_builder.add_conditional_edges("LLM",should_continue) 
    ordermanager_graph_builder.add_edge('tool','LLM')   
    
    memory=MemorySaver()
    graph=ordermanager_graph_builder.compile(memory)
    return graph
@tool()
async def OrderManager_Tool(customer_order:str):  
    orderManager_subgraph_tool=creat_OrderManager_subgraph()
    response=await orderManager_subgraph_tool.ainvoke({'messages'})
    return response["messages"][-1].content
   
def creat_FoodSearch_subgraph():
    
    foodsearch_graph_builder=StateGraph(FoodSearchState)
    
    foodsearch_graph_builder.add_node('LLM',llm_call_food_search)
    foodsearch_graph_builder.add_node('tool',tool_call_async)
    
    
    foodsearch_graph_builder.add_edge(START,'LLM')
    foodsearch_graph_builder.add_conditional_edges("LLM",should_continue) 
    foodsearch_graph_builder.add_edge('tool','LLM')   
    
    memory=MemorySaver()
    graph=foodsearch_graph_builder.compile(memory)
    return graph
@tool()
async def FoodSearch_Tool(customer_searching_query:str):  
    foodsearch_subgraph_tool=creat_FoodSearch_subgraph()
    response=await foodsearch_subgraph_tool.ainvoke({'messages'})
    return response["messages"][-1].content
    


subgraphs=[OrderManager_Tool,FoodSearch_Tool]