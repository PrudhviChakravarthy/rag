import sqlite3
from src.handlers.vector_stores import VectorStore
from src.handlers.embeddings import EmbeddingModel
from src.llms import google_gemini,openai_chatgpt,anthropic_claude
from src.utils import   query_templates

def get_files():
    conn = sqlite3.connect("rag.db")
            # Save the metadata to SQLite
    cursor = conn.cursor()
    cursor.execute(f"SELECT file_name FROM vectorstore")
    files = cursor.fetchall()
    return [file[0] for file in files]

def get_chunks(message,file_name,k):
    conn = sqlite3.connect("rag.db")
            # Save the metadata to SQLite
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM vectorstore WHERE file_name = '{file_name}'")
    file_details = cursor.fetchone()
    if not file_details:
        return None
    id, file_name, store, model_type, model_name, path = file_details
    emmbedings = EmbeddingModel(model_type=model_type,model_name=model_name)
    emmbeding_model = emmbedings.get_embedding()
    
    emmbed_query = emmbeding_model.embed_query(message)
    
    vectorstore = VectorStore(store)
    results =vectorstore.search(id,emmbeding_model,emmbed_query,k)
    print(results)
    docs = "/n".join(f"doc {i}  :" + doc[0].page_content for i,doc in enumerate(results))
    return docs

def chat_with_llm(query , history, file_name,top_k, top_p, temp, llm ):
    if llm == "gemini":
        chat_model = google_gemini.GetModel()
    # elif llm == "claude":
    #     chat_model = anthropic_claude.GetModel()
    # elif llm == "openai":
    #     chat_model = openai_chatgpt.GetModel()
    
    chat = chat_model.load_model(temp,top_p)
    docs = get_chunks(query,file_name,top_k)
    template = query_templates.QUERY_TEMPLATE.format(context = docs ,query = query , history = "/n".join(f"Ai - {data[0]} , User - {data[1]}" for data in history))
    retriver = chat.invoke(template)
    if len(history):
        history.append((query,retriver.content))
        return history
    else:
        return [(query,retriver.content)]
    
