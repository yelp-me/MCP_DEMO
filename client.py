import streamlit as st
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# Initialize model
model = ChatGroq(model="llama-3.3-70b-versatile")

# Define server parameters
server_params = StdioServerParameters(
    command="python",
    args=["math_server.py"]
)

# Core logic to run the agent
async def invoke_agent(prompt):
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await load_mcp_tools(session)
            agent = create_react_agent(model, tools)

            response = await agent.ainvoke({"messages": prompt})
            messages = response["messages"]

            tool_calls = []
            final_answer = None

            for msg in messages:
                if isinstance(msg, AIMessage) and hasattr(msg, "tool_calls"):
                    for call in msg.tool_calls:
                        tool_calls.append(f"Tool: {call['name']}, Args: {call['args']}")

            for msg in reversed(messages):
                if isinstance(msg, AIMessage) and msg.content.strip():
                    final_answer = msg.content.strip()
                    break

            return tool_calls, final_answer

# Streamlit UI
st.title("LangGraph MCP Agent")

prompt = st.text_input("Enter a prompt", "First add 3 and 5. Then multiply the result by 12.")

if st.button("Run Agent"):
    if prompt.strip():
        with st.spinner("Running agent..."):
            tool_calls, final_answer = asyncio.run(invoke_agent(prompt))
            st.subheader("Tool Calls:")
            for call in tool_calls:
                st.text(call)

            st.subheader("Final Answer:")
            st.success(final_answer)
