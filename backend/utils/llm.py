from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from db.chroma import ChromaRetriever
from utils.prompt import init_prompt, qna_prompt
from utils.chroma import get_sla_info_from_chromadb

def init_llm():
    llm = ChatGroq(
        model="llama-3.1-70b-versatile",
        temperature=0,
        groq_api_key="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"
    )
    return llm

def generate_sla_insights_json(chroma_obj):
    prompt_extract = init_prompt()
    llm = init_llm()
    query = "what are the SLA Name, Parties Involved, System Concerned, Description, Associated Metrics and Page Number"
    
    sla_docs = get_sla_info_from_chromadb(chroma_obj)

    chain = prompt_extract | llm
    result = chain.invoke(
        {
            "sla_docs": sla_docs,
            "user_question": query
        }
    )

    return result.content

def generate_sla_qna_response(collection_name, question):
    llm = init_llm()
    prompt_template = qna_prompt()
    retriever = ChromaRetriever(collection_name).retriever

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt_template
        | llm
        | StrOutputParser()
    )

    res = rag_chain.invoke(question)
    return res