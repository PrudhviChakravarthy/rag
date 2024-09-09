import gradio as gr
import sqlite3
from frontend.create_emmbeddings import create_embedding
from frontend.uploadfiles  import create_upload_files
from frontend.index import get_indexes
from frontend.chat import chat_with_model
def initialize_db():
        conn = sqlite3.connect('rag.db')
        cursor = conn.cursor()
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS vectorstore (
                            id TEXT PRIMARY KEY,
                            file_name TEXT,
                            store_type TEXT,
                            model_type TEXT,
                            model_name TEXT,
                            file_path TEXT)''')
        conn.commit()
        conn.close()
        

initialize_db()

with gr.Blocks() as demo:
    state = gr.State('Welcome')
    with gr.Tabs() as tabs:
        
        indexes = get_indexes(tabs)
        upload_files = create_upload_files(tabs)
        emmbeding = create_embedding(tabs)
        chat = chat_with_model(tabs)

demo.launch()