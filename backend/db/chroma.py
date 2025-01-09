import chromadb
from langchain_core.embeddings import Embeddings
from langchain.vectorstores import Chroma

class ChromaClient:
    def __init__(self, persistent=False):
        
        if persistent:
            print(f'Creating a {'Persistent ' if persistent else ''}Chroma DB Client')
            self.client = chromadb.PersistentClient(path="./chroma")
        else:
            self.client = chromadb.Client()

class ChromaRetriever(ChromaClient):
    def __init__(self, collection_name):
        super().__init__()
        self.collection_name = collection_name
        self.retriever = self.get_retriever()

    def get_retriever(self):
        class DefChromaEF(Embeddings):
            def __init__(self, ef):
                self.ef = ef

            def embed_documents(self, texts):
                return self.ef(texts)

            def embed_query(self, query):
                return self.ef([query])[0]

        # Initialize the embedding function
        ef = chromadb.utils.embedding_functions.DefaultEmbeddingFunction()
        db = Chroma(client=self.client, collection_name=self.collection_name,embedding_function=DefChromaEF(ef))

        # Get the retriever from the Chroma database
        retriever = db.as_retriever()
        return retriever


class ChromaCollection(ChromaClient):
    def __init__(self, collection_name, create=False, delete_if_exists=False, *args):
        self.collection_name = collection_name
        super().__init__(*args)

        try:
            if delete_if_exists:
                create=True
                self._delete_collection()
            
            self.collection = self._get_or_create_collection(create)
            
        except Exception as e:
            raise RuntimeError(f"Failed to initialize collection: {str(e)}")
        
    def _delete_collection(self):
        try:
            print('Deleting existing collection..')
            self.client.delete_collection(name=self.collection_name)
        except Exception as e:
            print(f"Cannot delete collection: {e}")
        
    def _get_or_create_collection(self, create):
        try:
            return self.client.get_collection(name=self.collection_name)
        except Exception as e:
            if create:
                print('Collection does not exist, creating a new one..')
                return self.client.create_collection(name=self.collection_name)
            else:
                raise Exception(e)

    def add_documents(self, documents, metadatas, ids):
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
    
    def query_all(self):
        return self.collection.get(include=['metadatas', 'documents'])

    def query(self, query_texts, n_results):
        return self.collection.query(
            query_texts=query_texts,
            n_results=n_results
        )
