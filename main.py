from langchain_mistralai.chat_models import ChatMistralAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.document_loaders import TextLoader, PyPDFLoader, UnstructuredFileLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
# from langchain_community.document_loaders import PyPDFLoader

import os
from dotenv import load_dotenv

from tools.spotify import SpotifyTools

load_dotenv()
mistal_key = os.getenv("MISTRAL_API_KEY")

llm = ChatMistralAI(api_key=mistal_key, model_name="mistral-medium", temperature=0, max_retries=2)

loader = UnstructuredFileLoader("data/Web API _ Spotify for Developers.pdf")  # <- your text file path
documents = loader.load()

# 2. Split into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = text_splitter.split_documents(documents)

# 3. Embed and store in FAISS vectorstore
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = FAISS.from_documents(docs, embedding_model)
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

# 6. Create RetrievalQA Chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="stuff"
)

# 7. Ask your question
query = "How does Spotify's doc work?"
result = qa_chain.run(query)
print("\nAnswer:\n", result)

# spotify_tools = SpotifyTools()

# tools = [spotify_tools.get_episodes]

# agent = create_tool_calling_agent(
#     llm=llm,
#     tools=tools,
#     prompt=ChatPromptTemplate.from_messages([
#         ("system", "You're a Spotify assistant. Use the `get_episodes` tool when a user asks about podcast episodes. Always extract the podcast name from the user question."),
#         ("human", "What are the episodes available on 'The Daily'?"),
#         MessagesPlaceholder(variable_name="agent_scratchpad")
#     ])

# )

# agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# result = agent_executor.invoke({"input" : "What are the names of episodes on The Daily"})
# print(result)
