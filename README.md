# LangGraph MCP Agent

This project is a Streamlit-based UI that connects to a Modular Computation Platform (MCP) tool server over stdio. It uses a LangGraph ReAct agent powered by Groq's LLaMA-3.3-70B model to process and compute structured prompts involving arithmetic and logic.

---

## Features

- LangGraph ReAct agent using `llama-3.3-70b-versatile` via Groq
- Supports dynamic tool loading from MCP servers
- Math tools (`add`, `multiply`) as an example
- Async agent execution with LangChain and MCP adapters
- Clean UI built with Streamlit

---

## Requirements

- Python 3.9 or higher
- Groq API Key
- `math_server.py` (tool server script)

---

## Environment Variables

Create a `.env` file in the root of the project:

```env
GROQ_API_KEY=your_groq_api_key_here
```
Run using streamlit run client.py

MIT license


