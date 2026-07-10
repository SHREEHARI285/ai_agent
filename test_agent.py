from agent import build_agent

agent = build_agent()

questions = [
    "What is 1234 multiplied by 567?",
    "Who is Sundar Pichai?",
    "What is the latest news about AI?"
]

for q in questions:
    print(f"\nQ: {q}")
    result = agent.invoke({"messages": [{"role": "user", "content": q}]})
    # Get the last message which is the final answer
    print(f"A: {result['messages'][-1].content}")