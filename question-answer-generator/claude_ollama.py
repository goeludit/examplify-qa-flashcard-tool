import os
from pinecone import Pinecone, ServerlessSpec
from PyPDF2 import PdfReader
import numpy as np
from typing import List, Dict
from langchain_community.llms import Ollama
import requests
import json

# from app import get_test_name, get_test_type, get_numer_questions

class PDFRagSystem:
    def __init__(self, 
                 pinecone_api_key: str, 
                 index_name: str = "nlp",
                 ollama_host: str = "http://localhost:11434",
                 cloud: str = 'aws',
                 region: str = 'us-east-1'):
        """
        Initialize RAG system with Pinecone and Ollama embeddings
        
        :param pinecone_api_key: Pinecone API key
        :param index_name: Name of Pinecone index
        :param ollama_host: Ollama server host
        :param cloud: Cloud provider
        :param region: Cloud region
        """
        try:
            # Initialize Pinecone 
            self.pc = Pinecone(api_key=pinecone_api_key)
            self.index_name = index_name
            self.ollama_host = ollama_host
            
            # Check if index exists, create if not
            existing_indexes = self.pc.list_indexes().names()
            
            if index_name not in existing_indexes:
                self.pc.create_index(
                    name=index_name, 
                    dimension=768,  # Dimension for nomic-embed-text
                    metric='cosine',
                    spec=ServerlessSpec(
                        cloud=cloud,
                        region=region
                    )
                )
            
            # Connect to index
            self.index = self.pc.Index(index_name)
        
        except Exception as e:
            print(f"Pinecone initialization error: {e}")
            raise
        
        # Initialize Ollama LLM and Embedding
        self.llm = Ollama(model="llama3.1")
    
    def embed_text(self, text: str) -> List[float]:
        """
        Generate embeddings using Ollama's nomic-embed-text
        
        :param text: Text to embed
        :return: Embedding vector
        """
        try:
            response = requests.post(
                f"{self.ollama_host}/api/embeddings", 
                json={
                    "model": "nomic-embed-text",
                    "prompt": text
                }
            )
            response.raise_for_status()
            return response.json()['embedding']
        except Exception as e:
            print(f"Embedding error: {e}")
            return []
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extract text from PDF file
        
        :param pdf_path: Path to PDF file
        :return: Extracted text
        """
        try:
            reader = PdfReader(pdf_path)
            text = "".join(page.extract_text() for page in reader.pages if page.extract_text())
            return text
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            return ""
    
    def split_text_into_chunks(self, text: str, chunk_size: int = 500) -> List[str]:
        """
        Split text into manageable chunks
        
        :param text: Input text
        :param chunk_size: Size of each text chunk
        :return: List of text chunks
        """
        # Split text into sentences
        sentences = text.split('. ')
        
        chunks = []
        current_chunk = []
        current_length = 0
        
        for sentence in sentences:
            # Add sentence to current chunk
            current_chunk.append(sentence)
            current_length += len(sentence)
            
            # If chunk is large enough, save it
            if current_length > chunk_size:
                chunks.append('. '.join(current_chunk) + '.')
                current_chunk = []
                current_length = 0
        
        # Add remaining chunk
        if current_chunk:
            chunks.append('. '.join(current_chunk) + '.')
        
        return chunks
    
    def store_embeddings_in_pinecone(self, text: str) -> List[str]:
        """
        Create embeddings and store in Pinecone
        
        :param text: Input text to embed
        :return: List of vector IDs
        """
        try:
            # Split text into chunks
            chunks = self.split_text_into_chunks(text)
            
            # Generate embeddings
            vectors = []
            for i, chunk in enumerate(chunks):
                embedding = self.embed_text(chunk)
                
                if embedding:
                    vectors.append({
                        "id": f"id-{i}", 
                        "values": embedding, 
                        "metadata": {"chunk": chunk}
                    })
            
            # Upsert vectors to Pinecone
            if vectors:
                self.index.upsert(vectors)
            
            return [v['id'] for v in vectors]
        except Exception as e:
            print(f"Error storing embeddings: {e}")
            return []
    
    def query_pinecone(self, query: str, top_k: int = 3) -> List[str]:
        """
        Retrieve relevant chunks from Pinecone
        
        :param query: Query to search
        :param top_k: Number of top results to retrieve
        :return: List of relevant text chunks
        """
        try:
            # Embed query using Ollama
            query_embedding = self.embed_text(query)
            
            if not query_embedding:
                return []
            
            # Search Pinecone
            results = self.index.query(
                vector=query_embedding, 
                top_k=top_k, 
                include_metadata=True
            )
            
            # Extract and return chunks
            return [match['metadata']['chunk'] for match in results['matches']]
        except Exception as e:
            print(f"Error querying Pinecone: {e}")
            return []
    
    def generate_questions_and_answers(self, prompt,text: str) -> List[Dict[str, str]]:
        """
        Generate questions and answers using Ollama
        
        :param text: Input text for context
        :return: List of Q&A dictionaries
        """
        try:
            # Truncate text if too long to prevent context overflow
            
            # Prompt for Q&A generation

            
            # Generate response
            response = self.llm(prompt)
            
            return response
        except Exception as e:
            print(f"Error generating Q&A: {e}")
            return []

def generate_text(pdf_path, questions_number, difficulty, type_question):
    """
    # Configuration (replace with your actual keys)

    """

    PINECONE_API_KEY = "pcsk_32TS5F_9b3g5bEBCudMCzxvzDmWeFGpzcdtYYmzx9EYGMR4ri9jaWV2rThYVZdDfEcvFnC"""
    # PDF_PATH = "/Users/vidyothsateesh/Downloads/1-s2.0-S0967070X15300627-main.pdf"
    OLLAMA_HOST = "http://localhost:11434"


    
    try:
        # Initialize RAG system
        rag_system = PDFRagSystem(
            pinecone_api_key=PINECONE_API_KEY,
            ollama_host=OLLAMA_HOST
        )
        
        # Extract text from PDF
        print("Extracting text from PDF...")
        pdf_text = rag_system.extract_text_from_pdf(pdf_path)
        context = pdf_text[:4000]

        prompt1 = f"""
        Based on the following context, generate {questions_number} {difficulty} level distinct {type_question} and their  answers:

        Context: {context}

        Please provide the output in the following JSON format:
        [
            {{
                "question": "Question 1",
                "answer": " answer to Question "
                "options": ["Option 1", "Option 2", "Option 3", "Option 4"]
            }},
            ...
        ]

        Do not change the key names in the JSON output. Only return the JSON object and nothing else.
        """

        # Preview first 500 characters
        print("PDF Text Preview:")
        print(pdf_text[:500])
        
        # Store embeddings in Pinecone
        print("\nStoring embeddings in Pinecone...")
        rag_system.store_embeddings_in_pinecone(pdf_text)
        

        # Generate questions and answers
        print("\nGenerating Questions and Answers...")
        qna = rag_system.generate_questions_and_answers(prompt1, pdf_text)
        print(qna)
        
        # Optional: Demonstrate querying
        # print("\nQuerying Pinecone...")
        # sample_query = "What is the main topic of this document?"
        # retrieved_chunks = rag_system.query_pinecone(sample_query)
        # print(qna)
        # print(type(qna))
        return qna
    
    except Exception as e:
        print(f"An error occurred: {e}")

