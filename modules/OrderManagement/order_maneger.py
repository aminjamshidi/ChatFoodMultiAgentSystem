from langchain_core.tools import tool
from pydantic import BaseModel, Field
from modules.OrderManagement.sqlite_maneger import SQLite_Maneger

from settings import settings

class Order_Maneger:
    
    def __init__(self):
        
        self.order_database=SQLite_Maneger(db_path=settings.RESTAURANT_DATABASE)
        self.table_name=settings.ORDER_TABLES_NAME
        self.field_name_username="username"
        self.field_name_status='status'
        self.field_name_comment="coments"
    
    def check_status_order(self,username):
        
        results=self.order_database.retrieve(columns=self.field_name_status,table=self.table_name,filter_column= self.field_name_username,filter_value=username)
        return settings.ORDER_STATUS[int(results[0][self.field_name_status])]
        
    def register_order(self,values):
        
        self.order_database.add(table=self.table_name,values=values)
        
    def cancel_order(self,username):
    
       self.order_database.update(table=self.table_name,column=self.field_name_status,filter_column=self.field_name_username,new_value=0,filter_value=username)  
    
    def add_comment(self,comment,username):
         
        try:
            if self.check_status_order(username=username)=="completed":
                self.order_database.update(table=self.table_name,column=self.field_name_comment,filter_column=self.field_name_username,new_value=comment,filter_value=username)
                return True,"your comments successfully recorded."
            else:
                return True,"you can not leave a review,because now you do not check it."
        except:
            return False,"there are a problems in database, now this action is not possible."
    def retrieve_order_specification():
        pass
    


# class CheckStatusInput(BaseModel):
#     username:str = Field(description="username of the customer, for checking the status of the customer's order.")
    
# @tool("check_status_order", args_schema=SearchInput, return_direct=True)
# def check_status_order(username):
    
#         """Retrieves status of the customer's order.

#         Takes username of the customer

#         Returns:
#             A string that is status of the order.
#     """
    
#         field_name_username="username"
#         field_name_status='status'
#         field_name_comment="coments"
#         table_name=settings.ORDER_TABLES_NAME
        
#         order_database=SQLite_Maneger(db_path=settings.RESTAURANT_DATABASE)
#         results=order_database.retrieve(columns=field_name_status,table=table_name,filter_column= field_name_username,filter_value=username)
        
        
#         return settings.ORDER_STATUS[int(results[0][self.field_name_status])]
            