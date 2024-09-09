from src.indexes import chroma, faiss

class VectorStore:
    def __init__(self, store_type):
        self.store_type = store_type
        self.store = self._select_store()

    def _select_store(self):
        """Select the appropriate vector store based on the store type."""
        if self.store_type == 'faiss':
            return faiss.FaissManager()
        elif self.store_type == 'chroma':
            return chroma.ChromaManager()
        else:
            raise ValueError("Invalid store type. Choose 'faiss' or 'chroma'.")
        
    def save_local(self,model_type, model_name, embeddings, docuements,file_name )-> None:
        output = self.store.save_local(model_type, model_name,embeddings,docuements,file_name)
        return output
    
    def search(self, id,emmbeding_model,  query, k) -> list:
        return self.store.search_documents(file_id=id,embedding_model=emmbeding_model,query_embedding=query,k=k)