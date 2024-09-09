import os
from langchain.vectorstores import FAISS
import sqlite3


class FaissManager:
    def __init__(self, db_path='rag.db', storage_dir='db',table_name = "vectorstore"):
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

    def save_local(self,model_type, model_name, embeddings,documents, file_name):
        # Generate a unique ID for the file
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(f"SELECT file_name FROM {self.table_name} WHERE  file_name = '{file_name}'")
        file_exist = cursor.fetchone()
        if file_exist:
            return "already embeding completed for this file"
        
        file_id = self._generate_file_id()
        faiss_save = FAISS.from_documents(documents=documents, embedding= embeddings)
        faiss_save.save_local(index_name=file_id,folder_path="db")

        # Save the metadata to SQLite
        cursor.execute(f"INSERT INTO {self.table_name} (id, file_name, file_path,store_type, model_type, model_name) VALUES (?, ?, ?, ?, ?, ?)",
                       (file_id, file_name, 'db',"fiass",model_type,model_name))
        conn.commit()
        conn.close()
        return "completed."
    
    
    def __load_local(self, file_id,emmbeding_model):
        """
        Loads the FAISS index from the local file using the file ID.
        """
        # Connect to SQLite to find the correct index file path
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(f"SELECT file_path FROM {self.table_name} WHERE id = ?", (file_id,))
        result = cursor.fetchone()
        conn.close()

        if result is None:
            raise ValueError(f"No FAISS index found for ID: {file_id}")
        
        file_path = result[0]
        # Ensure the file path exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"FAISS index file not found at: {file_path}")
        
        # Load the FAISS index using Langchain's FAISS load_local method
        faiss_vectorstore = FAISS.load_local(file_path, emmbeding_model,index_name=file_id,allow_dangerous_deserialization=True)
        return faiss_vectorstore
    
    def search_documents(self, file_id,emmbeding_model, query_embedding, k=5):
        """
        Searches for the top k relevant documents in the FAISS index using the query embedding.
        """
        # Load the FAISS index from the local file
        faiss_vectorstore = self.__load_local(file_id,emmbeding_model=emmbeding_model)

        # Perform the search on the index for the top k nearest neighbors
        results = faiss_vectorstore.similarity_search_with_score(query_embedding, k=k)

        return results


    def _generate_file_id(self):
        # Simple file ID generator
        return os.urandom(16).hex()