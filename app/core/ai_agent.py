from langchain_groq import ChatGroq
from langchain_community.tools.tavily import TavilySearchResults

from langchain.prebuilt import create_react_agent
from langchain_core.messages import AIMessage
from app.config.settings import Settings

def create_ai_agent(llm_id, query, allow_search, system_prompt):
    llm = ChatGroq(model = llm_id)
    tools = [TavilySearchResults(max_results=2)] if allow_search else [] 

    agent = create_react_agent(
        model = llm,
        tools = tools, 
        state_modifier = system_prompt
    )

    state = {'message': query}
    response = agent.invoke(state)
    messages = response.get('messages')
    ai_message = [message.content for message in messages if isinstance(message, AIMessage)]
    return ai_message[-1]