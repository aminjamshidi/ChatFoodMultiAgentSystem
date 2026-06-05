from langchain.tools import tool
from modules.OrderManagement.order_maneger import Order_Maneger



ordermaneger_obj=Order_Maneger()

@tool
def add_comment(comment,username):
    ordermaneger_obj.add_comment(comment=comment,username=username)
    

order_management_tools_set=[add_comment]
food_search_tools_set=[]