from db.chroma import ChromaCollection
import uuid

def add_docs_to_chroma_db(collection_name, documents, metadatas):
    chroma_obj = ChromaCollection(collection_name, delete_if_exists=True)
    chroma_obj.add_documents(
        documents=documents, 
        metadatas=metadatas, 
        ids=[str(uuid.uuid4()) for _ in range(len(documents))]
    )

    return chroma_obj


def get_sla_info_from_chromadb(chroma_obj):
    query = "Get all the details related to a service level agreement like SLA Name, Parties Involved, System Concerned, Description, Associated Metrics and Page Number"
    result = chroma_obj.query(query, n_results=15)

    final_res = {}
    for i in range(len(result['documents'][0])):
        content = {
            str(result['metadatas'][0][i]['page_number']): result['documents'][0][i]
        }
        
        final_res.update(content)

    return final_res