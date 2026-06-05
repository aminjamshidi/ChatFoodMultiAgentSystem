from typing import List
from typing_extensions import TypedDict,Any
from langgraph.graph import MessagesState



class ChatFoodState(MessagesState):
    pass    
class OrderManagementState(MessagesState):
    pass  
class FoodSearchState(MessagesState):
    pass


class QAState(MessagesState):
    pass
class FoodRecommendations(MessagesState):
    pass