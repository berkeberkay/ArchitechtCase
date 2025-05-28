from fastapi import FastAPI, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import chromadb
from sentence_transformers import SentenceTransformer
from chatbot_logic import ChatbotLogic
from embeddings import EmbeddingUtil
from llm_handler import MistralHandler

app = FastAPI()
chatbot = ChatbotLogic()
embedding_util = EmbeddingUtil()
llm = MistralHandler()

# ChromaDB ayarları
chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection("sss_collection")

# CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔹 Pydantic modeli (Swagger UI'da body alanını gösterir!)
class ChatRequest(BaseModel):
    session_id: str
    message: str

class ChatResponse(BaseModel):
    reply: str
    source: str = "database"  # "database" veya "llm"

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    try:
        session = chatbot.get_session(req.session_id)
        # ilk önce chatbot akışını dene
        try:
            chatbot_response = chatbot.process_message(req.session_id, req.message)
            if chatbot_response != "Üzgünüm, bir hata oluştu. Başvuruyu yeniden başlatabilir miyiz?":
                return ChatResponse(reply=chatbot_response, source="database")
        except Exception as flow_error:
            print(f"Flow error: {str(flow_error)}")
        # chatbot akışı başarısız olduysa, SSS'lerde ara
        query_embedding = embedding_util.get_embedding(req.message)
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=1
        )
        # SSS'lerde yanıt bulunursa, onu döndür
        if results["documents"] and results["documents"][0]:
            sss_response = results["documents"][0][0]
            return ChatResponse(reply=sss_response, source="database")
        
        context = chatbot.get_session_context(req.session_id)
        prompt = llm.format_prompt(req.message, context)
        llm_response = llm.generate_response(prompt)
        
        return ChatResponse(reply=llm_response, source="llm")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
