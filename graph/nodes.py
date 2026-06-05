from langchain_core.runnables import RunnableConfig

from graph.state import ChatFoodState,OrderManagementState,FoodSearchState,QAState
from graph.utils.chains import chat_food_cahin,order_management_chain,food_search_chain,QA_chain


from settings import settings


async def llm_call_chat_food(state:ChatFoodState,config:RunnableConfig):
    response = await chat_food_cahin.ainvoke(state["messages"], config)
    return {"messages": [response]}
    
async def llm_call_order_management(state:OrderManagementState,config: RunnableConfig):
    
    response = await order_management_chain.ainvoke(state["messages"], config)
    return {"messages": [response]}

async def llm_call_food_search(state:FoodSearchState,config: RunnableConfig):
    
    response = await food_search_chain.ainvoke(state["messages"], config)
    return {"messages": [response]}

def tool_call(state):
    
    outputs = []
    for tool_call in state["messages"][-1].tool_calls:
        tool_result = tools_by_name[tool_call["name"]].invoke(tool_call["args"])
        outputs.append(
            ToolMessage(
                content=tool_result,
                name=tool_call["name"],
                tool_call_id=tool_call["id"],
            )
        )
    return {"messages": outputs}
    
async def tool_call_async(state):
    
    outputs = []
    for tool_call in state["messages"][-1].tool_calls:
        tool_result = tools_by_name[tool_call["name"]].ainvoke(tool_call["args"])
        outputs.append(
            ToolMessage(
                content=tool_result,
                name=tool_call["name"],
                tool_call_id=tool_call["id"],
            )
        )
    return {"messages": outputs}    



async def web_search(state:QAState):
    pass

def search_knowledgebase(state:QAState):
    pass

async def llm_call_QA(state:QAState):
    
    response = await QA_chain.ainvoke(state["query"], config)
    return {"messages": [response]}







