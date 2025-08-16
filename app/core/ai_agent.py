from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import create_react_agent
from langchain_core.messages.ai import AIMessage
from app.common.logger import get_logger

logger = get_logger(__name__)


def create_ai_agent(llm_id, messages, allow_search, system_prompt, groq_api_key):
    logger.info('Creating AI Agent function Triggered')

    #  Initialize Groq LLM
    llm = ChatGroq(model_name=llm_id, groq_api_key=groq_api_key)

    #  Add search tool only if allowed
    tools = [TavilySearchResults(max_results=2)] if allow_search else []

    #  Create ReAct agent
    agent = create_react_agent(
        model=llm,
        tools=tools,
        state_modifier=system_prompt
    )

    #  Use structured messages directly
    state = {"messages": messages}
    response = agent.invoke(state)

    #  Extract AI’s response text
    msgs = response.get("messages", [])
    ai_msgs = [msg.content for msg in msgs if isinstance(msg, AIMessage)]

    return ai_msgs[-1] if ai_msgs else "No response from AI"
