from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ( ChatPromptTemplate,HumanMessagePromptTemplate, MessagesPlaceholder)
from langchain.agents import OpenAIFunctionsAgent, AgentExecutor
from dotenv import load_dotenv
from tools.sql import run_query_tool, list_tables, describe_tables_tool
from tools.report import write_report_tool
from langchain.schema import SystemMessage
from langchain.memory import ConversationBufferMemory
from handlers.chat_model_start_handler import ChatModelStartHandler

load_dotenv()

handler = ChatModelStartHandler()
chat= ChatOpenAI(
    callbacks=[handler]
)
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
tools = [run_query_tool, describe_tables_tool, write_report_tool]
tables = list_tables()
# print(tables)


prompt = ChatPromptTemplate(
    messages=[
        SystemMessage(content=(
            "You are an AI agent that has access to a SQLite database.\n"
            f"The database has tables of: {tables}\n"
            "DO NOT make any assumptions about what tables or columns exist. Instead use the 'desscribe_tables' function"
        )),
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad") #this is like a memory for messages
    ]
)

agent = OpenAIFunctionsAgent(
    llm=chat,
    prompt=prompt,
    tools=tools
)

agent_executor = AgentExecutor(
    agent=agent,
    verbose=True,
    tools=tools,
    memory=memory
)

# agent_executor("Who are the top 5 users with most orders. Write the results to a report file.")
# agent_executor("How many users have provided a shipping address?")
agent_executor("How many orders are there?")
agent_executor("and tell me how many of them are after 2024")