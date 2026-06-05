from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate,MessagesPlaceholder,ChatPromptTemplate
from core.prompts import SYSTEM_PROMPT_CHATFOOD,SYSTEM_PROMPOT_ORDER_MANAGER,SYSTEM_PROMPT_FOOD_SEARCH,SYSTEM_PROMPT_QA
from graph.utils.tools import order_management_tools_set,food_search_tools_set
from graph.subgraphs import subgraphs
from settings import settings

def get_chat_model_chain(model,system_prompt,temperature,variables_name_list,tools):
    
    
    llm=ChatOpenAI(
        model=model,
        temperature=temperature,
        api_key=settings.OPENROUTER_API_KEY,
        base_url=settings.OPENROUTER_BASE_URL
    )
    if tools: 
        model = llm.bind_tools(tools)
    
    prompt = ChatPromptTemplate.from_messages(
        [("system", system_prompt), MessagesPlaceholder(variable_name="messages")]
    )
    return prompt | model 



chat_food_cahin=get_chat_model_chain(model=settings.REASONING_TEXT_MODEL,
                                     system_prompt=SYSTEM_PROMPT_CHATFOOD,
                                     temperature=0.3,
                                     variables_name_list=['messages'],
                                     tools=subgraphs)

order_management_chain=get_chat_model_chain(model=settings.SMALL_TEXT_MODEL,
                               system_prompt=SYSTEM_PROMPOT_ORDER_MANAGER,
                               temperature=0.1,
                               variables_name_list=['messages'],
                               tools=order_management_tools_set)



food_search_chain=get_chat_model_chain(model=settings.SMALL_TEXT_MODEL,
                               system_prompt=SYSTEM_PROMPT_FOOD_SEARCH,
                               temperature=0.2,
                               variables_name_list=['messages'],
                               tools=food_search_tools_set)

QA_chain=get_chat_model_chain(model=settings.SMALL_TEXT_MODEL,
                              system_prompt=SYSTEM_PROMPT_QA,
                              temperature=0.2,
                              variables_name_list=[],
                              tools=[])

