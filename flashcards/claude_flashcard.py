import os
from pinecone import Pinecone, ServerlessSpec
from PyPDF2 import PdfReader
import numpy as np
from typing import List, Dict
from langchain_community.llms import Ollama
import json
import re

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
        
        # Initialize Ollama LLM
        self.llm = Ollama(model="llama3.1")
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extract text from PDF file
        
        :param pdf_path: Path to PDF file
        :return: Extracted text
        """
        try:
            # Open the PDF file
            reader = PdfReader(pdf_path)
            
            # Extract text from all pages
            text = ""
            for page in reader.pages:
                # Extract text from each page and append
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            
            return text.strip()
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            return ""
    
    def split_text_into_chunks(self, text: str, chunk_size: int = 300) -> List[str]:
        """
        Split text into manageable chunks
        
        :param text: Input text
        :param chunk_size: Size of each text chunk
        :return: List of text chunks
        """
        # Split text into sentences
        sentences = re.split(r'[.!?]\s+', text)
        
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
        

        print(len(chunks))  
        return chunks

    def generate_topic_modeling(self, chunks: List[str]) -> List[Dict[str, str]]:
        """
        Generate topics using LLM for each chunk

        :param chunks: List of text chunks
        :return: List of topics for each chunk
        """
        try:
            chunk_topics = []
            for chunk in chunks:
                prompt = f"""Analyze the following text chunk and provide a concise 1-3 words topic that best represents its main idea or theme:

                    Please provide the output in the following JSON format:
            
                {{
                    "Text Chunk": "{chunk}",
                    "Topic": "topic"
                }}
            
        
            Do not change the key names in the JSON output. Only return the JSON object and nothing else. Avoid returning any additional text or characters and ensure no unncessary line breaks are present in the output."""

                response = self.llm(prompt)
                print(response)
                import ast
                data_dict = ast.literal_eval(response)
                print(data_dict)

                data_dict = json.loads(str(response))
                chunk_topics.append(data_dict)
                print(chunk_topics)


                # chunk_topics.append({"chunk": chunk, "topic": response['topic'].strip()})
                # chunk_topics[response['Topic']] = response['Text Chunk'].strip()
                




            print("Final response chunks")
            return chunk_topics
        
        except Exception as e:
            print(f"Error generating topic modeling: {e}")
            return []

    def summarize_text(self, pdf_path: str):
        """
        Summarize text using topic modeling

        :param pdf_path: Path to PDF
        """
        # Extract text from PDF
        text = self.extract_text_from_pdf(pdf_path)

        # Split text into chunks
        chunks = self.split_text_into_chunks(text)

        # Generate topics
        return self.generate_topic_modeling(chunks)

def generate_flashcards(pdf_path):
    # Configuration (replace with your actual keys)
    PINECONE_API_KEY = "pcsk_32TS5F_9b3g5bEBCudMCzxvzDmWeFGpzcdtYYmzx9EYGMR4ri9jaWV2rThYVZdDfEcvFnC"
    # PDF_PATH = "/Users/vidyothsateesh/Downloads/1984.pdf"


    try:
        # Initialize RAG system
        rag_system = PDFRagSystem(pinecone_api_key=PINECONE_API_KEY)

        # Generate text summarization using topic modeling
        print("Extracting and Summarizing Topics...")
        summaries = rag_system.summarize_text(pdf_path)

        return summaries

        # Print results
        # for item in summaries:
        #     print("\nChunk:", item['chunk'])
        #     print("Topic:", item['topic'])
        #     # Create a dictionary with topic and chunk keys
        #     flashcards = [{"topic": item['topic'], "chunk": item['chunk']} for item in summaries]

        #     # Print the flashcards dictionary
        #     print("\nFlashcards Dictionary:", flashcards)
        


    except Exception as e:
        print(f"An error occurred: {e}")


# generate_flashcards("NLP Presentation.pdf")