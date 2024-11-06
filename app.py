from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.utilities import SQLDatabase
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import GoogleGenerativeAI

import streamlit as st

api_key = st.secrets["GOOGLE_API_KEY"] 

def init_database(user: str, password: str, host: str, port: str, database: str) -> SQLDatabase:
  db_uri = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"
  return SQLDatabase.from_uri(db_uri)

def get_sql_chain(db):
  template = """
    You are a data analyst at a company. You are interacting with a user who is asking you questions about the company's database.
    Based on the table schema below, write a SQL query that would answer the user's question. Take the conversation history into account.
    
    <SCHEMA>{schema}</SCHEMA>
    
    Conversation History: {chat_history}
    
    Write only the SQL query and nothing else. Do not wrap the SQL query in any other text, not even backticks.
    
    For example:
    1.Question: List all t-shirts available.
    SQL Query: SELECT * FROM t_shirts;

    2.Question: What are the distinct brands of t-shirts available?
    SQL Query: SELECT DISTINCT brand FROM t_shirts;
    
    3.Question: Show all t-shirts of the brand 'Nike'.
    SQL Query: SELECT * FROM t_shirts WHERE brand = 'Nike';
    
    4.Question: List all red t-shirts in stock.
    SQL Query: SELECT * FROM t_shirts WHERE color = 'Red';
    
    5.Question: Get the cheapest t-shirt for each brand.
    SQL Query: SELECT brand, MIN(price) AS cheapest_price FROM t_shirts GROUP BY brand;
    
    6.Question: Which t-shirts are priced between $20 and $30?
    SQL Query: SELECT * FROM t_shirts WHERE price BETWEEN 20 AND 30;
    
    7.Question: Show the top 5 most expensive t-shirts.
    SQL Query: SELECT * FROM t_shirts ORDER BY price DESC LIMIT 5;
    
    8.Question: List all sizes of Levi's t-shirts available in white color.
    SQL Query: SELECT size FROM t_shirts WHERE brand = 'Levi' AND color = 'White';
    
    9.Question: Show the stock quantity of all blue t-shirts.
    SQL Query: SELECT color, size, stock_quantity FROM t_shirts WHERE color = 'Blue';
    
    10.Question: What is the highest discount available?
    SQL Query: SELECT MAX(pct_discount) AS max_discount FROM discounts;
    
    11.Question: Which t-shirts have a discount greater than 20%?
    SQL Query: SELECT t_shirts.* FROM t_shirts JOIN discounts ON t_shirts.t_shirt_id = discounts.t_shirt_id WHERE pct_discount > 20;
    
    12.Question: Show t-shirts with the smallest stock.
    SQL Query: SELECT * FROM t_shirts ORDER BY stock_quantity ASC LIMIT 1;
    
    13.Question: What are the average prices for each color?
    SQL Query: SELECT color, AVG(price) AS avg_price FROM t_shirts GROUP BY color;
    
    14.Question: How many t-shirts are available in each size?
    SQL Query: SELECT size, COUNT(*) AS count FROM t_shirts GROUP BY size;
    
    Your turn:
    
    Question: {question}
    SQL Query:
    """
    
  prompt = ChatPromptTemplate.from_template(template)
  
  llm = GoogleGenerativeAI(model="gemini-pro", google_api_key=api_key)

  # llm = ChatGroq(model="mixtral-8x7b-32768", temperature=0)
  
  def get_schema(_):
    return db.get_table_info()
  
  return (
    RunnablePassthrough.assign(schema=get_schema)
    | prompt
    | llm
    | StrOutputParser()
  )
    
def get_response(user_query: str, db: SQLDatabase, chat_history: list):
  sql_chain = get_sql_chain(db)
  
  template = """
    You are a data analyst at a company. You are interacting with a user who is asking you questions about the company's database.
    Based on the table schema below, question, sql query, and sql response, write a natural language response.
    <SCHEMA>{schema}</SCHEMA>

    Conversation History: {chat_history}
    SQL Query: <SQL>{query}</SQL>
    User question: {question}
    SQL Response: {response}"""
  
  prompt = ChatPromptTemplate.from_template(template)
  
  llm = GoogleGenerativeAI(model="gemini-pro", google_api_key=api_key)

  
  chain = (
    RunnablePassthrough.assign(query=sql_chain).assign(
      schema=lambda _: db.get_table_info(),
      response=lambda vars: db.run(vars["query"]),
    )
    | prompt
    | llm
    | StrOutputParser()
  )
  
  return chain.invoke({
    "question": user_query,
    "chat_history": chat_history,
  })
    
  
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
      AIMessage(content="Hello! I'm a SQL assistant. Ask me anything about your database."),
    ]

# load_dotenv()

st.set_page_config(page_title="Chatbot", page_icon=":speech_balloon:")

st.title("MySQL Chatbot with Gemini-Pro")

with st.sidebar:
    st.subheader("Settings")
    st.write("This is a simple chat application using MySQL. **Connect** to the database and start chatting.")
    
    st.text_input("Host", value="junction.proxy.rlwy.net", key="Host")
    st.text_input("Port", value="45109", key="Port")
    st.text_input("User", value="root", key="User")
    # st.text_input("Password", type="password", value=st.secrets["PASSWORD"], key="Password")
    st.text_input("Database", value="railway", key="Database")
    
    if st.button("Connect"):
        with st.spinner("Connecting to database..."):
            db = init_database(
                st.session_state["User"],
                st.secrets["PASSWORD"],
                st.session_state["Host"],
                st.session_state["Port"],
                st.session_state["Database"]
            )
            st.session_state.db = db
            st.success("Connected to database!")

for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.markdown(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.markdown(message.content)

user_query = st.chat_input("Type a message...(Example: How many artists are there?)")
if user_query is not None and user_query.strip() != "":
    st.session_state.chat_history.append(HumanMessage(content=user_query))
    
    with st.chat_message("Human"):
        st.markdown(user_query)
        
    with st.chat_message("AI"):
        response = get_response(user_query, st.session_state.db, st.session_state.chat_history)
        st.markdown(response)
        
    st.session_state.chat_history.append(AIMessage(content=response))