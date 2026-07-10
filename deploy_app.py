import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain.agents import create_agent
from langchain_community.tools import DuckDuckGoSearchRun
import wikipedia

load_dotenv()

st.set_page_config(page_title="AI Agent", page_icon="🤖")
st.title("🤖 AI Agent with Tools")
st.caption("Powered by Gemini + Calculator + Web Search + Wikipedia")

# ---- Build agent once ----
@st.cache_resource
def build_agent():
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

    @tool
    def calculator(expression: str) -> str:
        """Useful for math questions. Input must be a valid math expression like 4837*92."""
        try:
            return str(eval(expression))
        except Exception as e:
            return f"Error: {e}"

    @tool
    def web_search(query: str) -> str:
        """Useful for current news and real-time information. Input should be a search query."""
        try:
            return DuckDuckGoSearchRun().run(query)
        except Exception as e:
            return f"Error: {e}"

    @tool
    def wikipedia_search(query: str) -> str:
        """Useful for factual questions about people, places, history, and general knowledge."""
        try:
            return wikipedia.summary(query, sentences=3)
        except wikipedia.DisambiguationError as e:
            return f"Ambiguous. Try more specific. Options: {e.options[:5]}"
        except wikipedia.PageError:
            return f"No Wikipedia page found for: {query}"
        except Exception as e:
            return f"Error: {e}"

    return create_agent(
        model=llm,
        tools=[calculator, web_search, wikipedia_search],
        system_prompt="You are a helpful assistant with access to tools. Use the right tool for each question. Always give a clean, direct final answer."
    )

agent = build_agent()

# ---- Sidebar info ----
with st.sidebar:
    st.header("🛠️ Available Tools")
    st.success("🧮 Calculator — math expressions")
    st.info("🔍 Web Search — current news & events")
    st.warning("📖 Wikipedia — facts & general knowledge")
    st.divider()
    st.caption("The agent decides which tool to use based on your question.")

# ---- Chat history ----
if "messages" not in st.session_state:
    st.session_state["messages"] = []

for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ---- Input ----
question = st.chat_input("Ask me anything...")

if question:
    st.session_state["messages"].append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        with st.spinner("Agent is thinking..."):
            try:
                result = agent.invoke({
                    "messages": [{"role": "user", "content": question}]
                })
                # Extract clean text from last message
                last_message = result["messages"][-1]
                if hasattr(last_message, "content"):
                    content = last_message.content
                    # Handle list format from web search
                    if isinstance(content, list):
                        answer = " ".join(
                            item["text"] for item in content
                            if isinstance(item, dict) and "text" in item
                        )
                    else:
                        answer = content
                else:
                    answer = str(last_message)

                st.write(answer)
                st.session_state["messages"].append({
                    "role": "assistant",
                    "content": answer
                })
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")