from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ( ChatPromptTemplate,HumanMessagePromptTemplate, MessagesPlaceholder)
from langchain.agents import OpenAIFunctionsAgent, AgentExecutor
from dotenv import load_dotenv
from tools.sql import run_query_tool, list_tables, describe_tables_tool
from langchain.schema import SystemMessage

load_dotenv()
chat= ChatOpenAI()
tools = [run_query_tool, describe_tables_tool]
tables = list_tables()
# print(tables)


prompt = ChatPromptTemplate(
    messages=[
        SystemMessage(content=(
            "You are an AI agent that has access to a SQLite database.\n"
            f"The database has tables of: {tables}\n"
            "DO not manke any assumptions about what tables or columns exist. Instead use the 'desscribe_tables' function"
        )),
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
    tools=tools
)

agent_executor("How many users have provided a shipping address?")