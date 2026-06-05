from typing_extensions import TypedDict
from langgraph.graph import MessagesState



class ChatFoodState(MessagesState):
    pass    
class OrderManagementState(MessagesState):
    pass  
class FoodSearchState(MessagesState):
    pass

class QAState(TypedDict):
    
    query:str
    reinforced_query:str
    context:str
    answer:str
    
class FoodRecommendations(MessagesState):
    pass