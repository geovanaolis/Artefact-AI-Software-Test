import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_core.tools import tool
from langchain_huggingface import HuggingFaceEmbeddings

# Ajusta o caminho base para a raiz do projeto (um nível acima de src/)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

load_dotenv()

# 1. Inicializar banco de dados SQLite em memória com os CSVs usando o caminho correto
import sqlite3
import pandas as pd

def init_sqlite_db(data_dir=DATA_DIR):
    conn = sqlite3.connect(":memory:")
    csv_files = {
        "products": "products.csv",
        "categories": "categories.csv",
        "customers": "customers.csv",
        "orders": "orders.csv",
        "order_items": "order_items.csv",
        "promotions": "promotions.csv"
    }
    for table_name, filename in csv_files.items():
        filepath = os.path.join(data_dir, filename)
        if os.path.exists(filepath):
            df = pd.read_csv(filepath)
            df.to_sql(table_name, conn, index=False, if_exists="replace")
    return conn

db_conn = init_sqlite_db()

# 2. Configurar RAG para as políticas da loja (busca automática do arquivo PDF na pasta data)
pdf_files = [f for f in os.listdir(DATA_DIR) if f.endswith(".pdf")]
if not pdf_files:
    raise FileNotFoundError(f"Nenhum arquivo PDF encontrado na pasta: {DATA_DIR}")

pdf_path = os.path.join(DATA_DIR, pdf_files[0])
print(f"Carregando PDF de políticas: {pdf_path}")

loader = PyPDFLoader(pdf_path)
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
texts = text_splitter.split_documents(documents)

# Inicializa embeddings locais gratuitos do HuggingFace
from langchain_huggingface import HuggingFaceEmbeddings
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Criação garantida do vectorstore
vectorstore = Chroma.from_documents(texts, embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

# 3. Definir Ferramentas (Tools) com o decorador @tool
@tool
def database_query(query: str) -> str:
    """Useful for querying operational data such as products, prices, stock availability, customer details, promotions, and order statuses using SQL tables (products, categories, customers, orders, order_items, promotions)."""
    try:
        cursor = db_conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        return str(result)
    except Exception as e:
        return f"Error executing query: {str(e)}"

@tool
def store_policies_search(query: str) -> str:
    """Useful for looking up store policies, opening hours, payment rules, shipping conditions, and warranty guidelines from the store manual."""
    docs = retriever.invoke(query)
    return "\n".join([d.page_content for d in docs])

tools = [database_query, store_policies_search]

# Importar o SYSTEM_PROMPT de forma correta
try:
    from prompts import SYSTEM_PROMPT
except ImportError:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from prompts import SYSTEM_PROMPT

# 4. Inicializar o modelo Gemini com suporte a Tools
llm = ChatGoogleGenerativeAI(model="gemini-3.8-flash", temperature=0.3)
llm_with_tools = llm.bind_tools(tools)

def run_agent(user_message: str):
    """Executa o agente processando mensagens e chamadas de ferramentas se necessário."""
    messages = [
        ("system", SYSTEM_PROMPT),
        ("human", user_message)
    ]
    
    response = llm_with_tools.invoke(messages)
    messages.append(response)
    
    if response.tool_calls:
        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            
            selected_tool = next((t for t in tools if t.name == tool_name), None)
            if selected_tool:
                tool_output = selected_tool.invoke(tool_args)
                messages.append(("tool", tool_output, tool_call["id"]))
        
        final_response = llm_with_tools.invoke(messages)
        return final_response.content
    
    return response.content

if __name__ == "__main__":
    print("=" * 60)
    print("Empório da Música Virtual Assistant (Gemini Native Tools) Initialized!")
    print("Digite sua pergunta abaixo ou 'sair' para encerrar.")
    print("=" * 60 + "\n")
    
    while True:
        try:
            pergunta = input("\nUsuário: ")
            if pergunta.lower() in ["sair", "exit", "quit"]:
                print("Encerrando o assistente. Até logo!")
                break
            
            if not pergunta.strip():
                continue
                
            resposta = run_agent(pergunta)
            print(f"\nAgente:\n{resposta}")
        except KeyboardInterrupt:
            print("\nEncerrando o assistente. Até logo!")
            break
        except Exception as e:
            print(f"\n[Erro]: {str(e)}")