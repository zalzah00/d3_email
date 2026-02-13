import os
import asyncio
import gradio as gr
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt.chat_agent_executor import create_react_agent
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

load_dotenv()

client = MultiServerMCPClient({
    "EmailTools": {
        "command": "python",
        "args": ["email_tools_server.py"],
        "transport": "stdio",
    }
})

CACHED_TOOLS = None

async def chat_function(message, history):
    global CACHED_TOOLS
    try:
        # 2. Only fetch tools if they haven't been loaded yet
        if CACHED_TOOLS is None:
            CACHED_TOOLS = await client.get_tools()
        
        # 3. Use the stable model name and cached tools
        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
        agent = create_react_agent(llm, CACHED_TOOLS)

        messages = [SystemMessage(content="You are Agent Zero. You help manage emails.")]
        
        # 4. Robust History Parser
        for turn in history:
            if isinstance(turn, dict):
                content = turn.get("content", "")
                if turn.get("role") == "user":
                    messages.append(HumanMessage(content=content))
                else:
                    messages.append(AIMessage(content=content))
            else:
                messages.append(HumanMessage(content=turn[0]))
                messages.append(AIMessage(content=turn[1]))
        
        messages.append(HumanMessage(content=message))

        # 5. Run the agent
        result = await agent.ainvoke({"messages": messages})
        return result["messages"][-1].content

    except Exception as e:
        return f"❌ Agent Error: {str(e)}"

demo = gr.ChatInterface(
    fn=chat_function,
    title="Agent Zero: Gmail MCP",
    description="Summarize your inbox or send emails."
)

if __name__ == "__main__":
    demo.launch()