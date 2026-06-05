from graph.state import QAState

def should_continue(state):
    messages = state["messages"]
    if not messages[-1].tool_calls:
        return "end"
    return "tool"

def QA_action_selection(state:QAState):
    
    pass