from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

# Load PDFs
loader1 = PyPDFLoader("data/RAG_TRANSFORMER1.pdf")
loader2 = PyPDFLoader("data/RAG_TRANSFORMER2.pdf")

documents = loader1.load() + loader2.load()

# Split
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = splitter.split_documents(documents)

# Embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en"
)

# Chroma
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db"
)

# Retriever
retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 5,
        "fetch_k": 15
    }
)

# Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

prompt = PromptTemplate(
    template="""
You are an expert transformer insulation engineer.

Use all retrieved context to answer.

If information appears across multiple chunks,
combine it into a complete answer.

If the answer cannot be found,
say so explicitly.

Context:
{context}

Question:
{question}

Answer:
""",
    input_variables=["context", "question"]
)

def ask_rag(question: str):

    docs = retriever.invoke(question)

    context = "\n\n".join(
        doc.page_content for doc in docs
    )

    prompt_text = prompt.format(
        context=context,
        question=question
    )

    response = llm.invoke(prompt_text)

    return response.content