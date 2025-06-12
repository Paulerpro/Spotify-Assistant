from langchain_mistralai.chat_models import ChatMistralAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

import os
from dotenv import load_dotenv

from tools.spotify import SpotifyTools

load_dotenv()
mistal_key = os.getenv("MISTRAL_API_KEY")

llm = ChatMistralAI(api_key=mistal_key, model_name="mistral-medium", temperature=0, max_retries=2)

spotify_tools = SpotifyTools()
# messages = [
#     (
#         "system",
#         "You are a helpful assistant that translates English to French. Translate the user sentence.",
#     ),
#     ("human", "I love programming."),
# ]

# response = llm.invoke(messages)

# print(response.content)

tools = [spotify_tools.get_episodes]

agent = create_tool_calling_agent(
    llm=llm,
    tools=tools,
    prompt=ChatPromptTemplate.from_messages([
        ("system", "You're a Spotify assistant. Use the `get_episodes` tool when a user asks about podcast episodes. Always extract the podcast name from the user question."),
        ("human", "What are the episodes available on 'The Daily'?"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ])

)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

result = agent_executor.invoke({"input" : "What are the names of episodes on The Daily"})
print(result)
