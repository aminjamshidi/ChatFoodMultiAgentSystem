from langgraph.graph import START,END,StateGraph
from langgraph.checkpoint.memory import MemorySaver


from graph.nodes import llm_call_chat_food,tool_call_async
from graph.state import ChatFoodState,OrderManagementState
from graph.edges import should_continue




def creat_Chatfood_graph():
    
   
     
    chatfood_graph_builder=StateGraph(ChatFoodState)
    
    chatfood_graph_builder.add_node('LLM',llm_call_chat_food)
    chatfood_graph_builder.add_node('tool',tool_call_async)
    
    
    chatfood_graph_builder.add_edge(START,'LLM')
    chatfood_graph_builder.add_conditional_edges("LLM",should_continue) 
    chatfood_graph_builder.add_edge('tool','LLM')   
    
    memory=MemorySaver()
    graph=chatfood_graph_builder.compile(memory)
    return graph
    

ChatFood_graph=creat_Chatfood_graph()