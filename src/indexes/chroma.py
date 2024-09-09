import os
from langchain.vectorstores import Chroma
import sqlite3

class ChromaManager:
    def __init__(self, db_path='rag.db', storage_dir='db', table_name="vectorstore"):
        self.db_path = db_path
        self.storage_dir = storage_dir
        self.table_name = table_name
        self._initialize_db()
        self._ensure_storage_dir()

    def _initialize_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS {self.table_name} (
                            id TEXT PRIMARY KEY,
                            file_name TEXT,
                            store_type TEXT,
                            model_type TEXT,
                            model_name TEXT,
                            file_path TEXT)''')
        conn.commit()
        conn.close()

    def _ensure_storage_dir(self):
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir)

    def save_local(self,model_type, model_name, embeddings, documents, file_name):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        # Generate a unique ID for the file
        file_id = self._generate_file_id()

        # Save Chroma index using Langchain's Chroma integration
        chroma_save = Chroma.from_documents(documents=documents, embedding=embeddings,persist_directory=os.path.join(self.storage_dir, file_id))
        chroma_save.persist()

        # Save the metadata to SQLite
        cursor.execute(f"SELECT file_name FROM {self.table_name} WHERE file_name = '{file_name}'")
        file_exist = cursor.fetchone()
        if file_exist:
            return "already embeding completed for this file"
        
        cursor.execute(f"INSERT INTO {self.table_name} (id, file_name, file_path, store_type, model_type, model_name) VALUES (?, ?, ?, ?,?,?)",
                       (file_id, file_name, os.path.join(self.storage_dir, file_id), "chroma",model_type,model_name))
        conn.commit()
        conn.close()
        return "completed."

    def __load_local(self, file_id, embedding_model):
        """
        Loads the Chroma index from the local file using the file ID.
        """
        # Connect to SQLite to find the correct index file path
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(f"SELECT file_path FROM {self.table_name} WHERE id = ?", (file_id,))
        result = cursor.fetchone()
        conn.close()

        if result is None:
            raise ValueError(f"No Chroma index found for ID: {file_id}")
        
        file_path = result[0]

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Chroma index file not found at: {file_path}")
    
        chroma_vectorstore = Chroma(persist_directory=file_path, embedding_function=embedding_model)
        return chroma_vectorstore

    def search_documents(self, file_id,embedding_model, query_embedding, k=5):
        """
        Searches for the top k relevant documents in the Chroma index using the query embedding.
        """
        chroma_vectorstore = self.__load_local(file_id, embedding_model=embedding_model)

        results = chroma_vectorstore.similarity_search_by_vector_with_relevance_scores(query_embedding, k=k)

        return results

    def _generate_file_id(self):
        # Simple file ID generator
        return os.urandom(16).hex()
