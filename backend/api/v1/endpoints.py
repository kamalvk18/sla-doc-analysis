from io import BytesIO
from fastapi import APIRouter, File, UploadFile, Request
from fastapi.responses import JSONResponse
from utils.chroma import add_docs_to_chroma_db
from utils.llm import generate_sla_insights_json, generate_sla_qna_response
from utils.extract import extract_doc_meta_from_pdf
import json

router = APIRouter()


@router.post("/get_sla_insights_json/")
async def get_sla_insights_json(file: UploadFile = File(...)):
    with BytesIO(await file.read()) as pdf_data:
        documents, metadatas = extract_doc_meta_from_pdf(pdf_data)

    # Add extracted documents to ChromaDB
    chroma_obj = add_docs_to_chroma_db('sla_docs', documents, metadatas)
    
    # Generate SLA insights based on the stored data
    sla_insights = generate_sla_insights_json(chroma_obj)
    sla_insights_json = json.loads(sla_insights)
    
    return JSONResponse(content=sla_insights_json)


@router.post("/get_sla_qna_response")
async def get_sla_qna_response(request: Request):
    body = await request.body()
    user_question = json.loads(body)
    response = generate_sla_qna_response('sla_docs', user_question['question'])
    return response
