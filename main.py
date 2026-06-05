import asyncio
from langchain_core.messages import HumanMessage,AIMessage

from graph.graphs import ChatFood_graph




config = {"configurable": {"thread_id": "abc123"}}
async def main():
        
        query="I want to add a comment for my order"
        input_message=[HumanMessage(query)]
        output=await graph.ainvoke({"messages": input_message,"current_part":"CHATFOOD"},config)
        print(output["messages"][-1].content)
        while(query!='q'):
            query=input()
            input_message=[HumanMessage(query)]
            response=await graph.ainvoke({"messages":input_message},config)
            print(response["messages"][-1].content)
            print('-------------------------------------------------------')

        
              
if __name__ == "__main__":
    
 
    asyncio.run(main())
