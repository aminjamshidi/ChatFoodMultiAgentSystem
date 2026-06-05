from graph.state import ChatFoodState


def should_continue(state: ChatFoodState):
    messages = state["messages"]
    if not messages[-1].tool_calls:
        return "end"
    return "tool"