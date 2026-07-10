from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain.agents import create_agent
from langchain_community.tools import DuckDuckGoSearchRun
import wikipedia

load_dotenv()

def build_agent():
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

    # ---- Tool 1: Calculator ----
    @tool
    def calculator(expression: str) -> str:
        """Useful for math questions. Input must be a valid math expression like 4837*92."""
        try:
            result = eval(expression)
            return str(result)
        except Exception as e:
            return f"Error: {e}"

    # ---- Tool 2: Web Search ----
    @tool
    def web_search(query: str) -> str:
        """Useful for current news and real-time information. Input should be a search query."""
        try:
            search = DuckDuckGoSearchRun()
            return search.run(query)
        except Exception as e:
            return f"Error: {e}"

    # ---- Tool 3: Wikipedia ----
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

    tools = [calculator, web_search, wikipedia_search]

    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt="You are a helpful assistant with access to tools. Use the right tool for each question."
    )

    return agent