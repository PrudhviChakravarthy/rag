from src.handlers.embeddings import EmbeddingModel
from src.handlers.document_split import DocumentProcessor
from src.handlers.vector_stores import VectorStore
from pathlib import Path

def select_embedding(model_name,model_type):
    embeding_model = EmbeddingModel(model_name = model_name, model_type= model_type )
    return embeding_model.get_embedding()




def get_files():
    files  = [file.name for file in Path("files").iterdir() if file.is_file()]
    print(files)
    return files


def embed_documents(file_name,embeding_type, embedding_model,store,chunk_size, chunk_overlap):
    if not embedding_model:
        return "no model seleted. aborting"
    embedings = select_embedding(model_name=embedding_model,model_type= embeding_type)
    print("embedding model selected.")
    splitter = DocumentProcessor(f"files/{file_name}")
    chunks = splitter.split_text(chunk_size,chunk_overlap)
    print("splitting document completed")
    store = VectorStore(store)
    output = store.save_local(embeding_type,embedding_model,embedings,chunks,file_name)
    print("storing in vector store completed.")
    return output
    
    