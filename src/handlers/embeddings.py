from langchain.embeddings import HuggingFaceEmbeddings, SentenceTransformerEmbeddings

class EmbeddingModel:
    def __init__(self, model_type, model_name):
        self.model_type = model_type
        self.model_name = model_name
        self.embedding_model = self._select_model()

    def _select_model(self):
        """Select the appropriate embedding model based on the model type."""
        if self.model_type == 'sentence transformer':
            return SentenceTransformerEmbeddings(model_name=self.model_name)
        elif self.model_type == 'huggingface transformer':
            return HuggingFaceEmbeddings(model_name=self.model_name)
        else:
            raise ValueError("Invalid model type. Choose 'sentence-transformers' or 'huggingface'.")

    def get_embedding(self):
        return self.embedding_model