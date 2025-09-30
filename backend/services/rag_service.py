import os
import logging
from typing import List, Dict, Any, Optional
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain.schema import Document
from models.schemas import ConversationMessage, UserContext
from pinecone import Pinecone
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.text_utils import humanize_response

logger = logging.getLogger(__name__)

class RAGService:
    def __init__(self):
        self.llm = None
        self.embeddings = None
        self.vectorstore = None
        self.prompt = None
        
    async def initialize(self):
        """Initialize the RAG service with Gemini and Pinecone"""
        try:
            # Initialize Gemini LLM (free tier)
            google_api_key = os.getenv("GOOGLE_API_KEY")
            if not google_api_key:
                raise ValueError("GOOGLE_API_KEY not found in environment variables")
            
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-2.0-flash-exp",  # Using free tier model
                google_api_key=google_api_key,
                temperature=0.3,
                convert_system_message_to_human=True
            )
            
            # Initialize Google Gemini embeddings
            self.embeddings = GoogleGenerativeAIEmbeddings(
                model="models/embedding-001",
                google_api_key=google_api_key
            )
            logger.info("Using Google Gemini embeddings with Pinecone")
            
            # Initialize Pinecone
            pinecone_api_key = os.getenv("PINECONE_API_KEY")
            if not pinecone_api_key:
                raise ValueError("PINECONE_API_KEY not found in environment variables")
            
            # Initialize Pinecone client
            pc = Pinecone(api_key=pinecone_api_key)
            
            # Connect to the existing index
            index_name = os.getenv("PINECONE_INDEX_NAME", "awshacathon")
            index = pc.Index(index_name)
            
            # Initialize PineconeVectorStore
            self.vectorstore = PineconeVectorStore(
                index=index,
                embedding=self.embeddings,
                text_key="text"
            )
            logger.info("Successfully initialized Pinecone vector store")
            
            # Create QA chain
            self._create_qa_chain()
            
            # Initialize knowledge base if empty
            await self._initialize_knowledge_base()
            
            logger.info("RAG service initialized successfully with Pinecone")
            
        except Exception as e:
            logger.error(f"Failed to initialize RAG service: {e}")
            # Initialize simple fallback
            logger.warning("Falling back to simple document store")
            await self._load_initial_data_simple()
            self._create_qa_chain()
    
    def _create_qa_chain(self):
        """Create the QA chain with custom prompt"""
        template = """You are a helpful and knowledgeable Hong Kong tourism assistant. Use the provided context to answer questions about Hong Kong attractions, culture, food, transportation, and travel tips.

Context from Hong Kong Tourism Knowledge Base:
{context}

Conversation History:
{chat_history}

Human Question: {question}

Please provide a helpful, accurate, and detailed answer about Hong Kong tourism. Include practical tips, recommendations, and any relevant cultural insights. If you don't have enough information to answer the question, say so honestly and suggest alternative resources.

Answer:"""

        self.prompt = PromptTemplate(
            template=template,
            input_variables=["context", "chat_history", "question"]
        )
    
    async def _initialize_knowledge_base(self):
        """Initialize the knowledge base with Hong Kong tourism data"""
        try:
            if self.vectorstore is None:
                logger.info("Vector store not available, using simple document store")
                await self._load_initial_data_simple()
                return
                
            # Check if vector store has any documents
            try:
                # Try to do a simple search to check if there are documents
                test_results = self.vectorstore.similarity_search("Hong Kong", k=1)
                if len(test_results) == 0:
                    logger.info("Initializing Hong Kong tourism knowledge base...")
                    await self._load_initial_data_pinecone()
                else:
                    logger.info(f"Knowledge base already contains documents")
            except Exception as e:
                logger.info("Could not check existing documents, loading initial data...")
                await self._load_initial_data_pinecone()
                
        except Exception as e:
            logger.error(f"Failed to initialize knowledge base: {e}")
            # Fallback to simple document store
            await self._load_initial_data_simple()
    
    async def _load_initial_data_simple(self):
        """Load initial data into simple document store when vectorstore is not available"""
        tourism_data = [
            {
                "title": "Victoria Peak",
                "content": "Victoria Peak is Hong Kong's premier tourist attraction, offering spectacular 360-degree views of the city skyline, Victoria Harbour, and surrounding islands. Best visited during sunset or at night when the city lights create a magical atmosphere. Take the historic Peak Tram (operating since 1888) to reach the summit. Allow 2-3 hours for the visit. Located at 128 Peak Road. Open daily. Sky Terrace 428 offers the best panoramic views for a small fee."
            },
            {
                "title": "Star Ferry",
                "content": "The iconic Star Ferry has been operating across Victoria Harbour since 1888, connecting Hong Kong Island and Tsim Sha Tsui. This historic ferry ride offers stunning views of both skylines and is one of the most affordable ways to enjoy the harbour. Operating hours: 6:30 AM to 11:30 PM. Very affordable at around HK$3-4 per trip. Great for photography, especially during Symphony of Lights show at 8 PM daily."
            },
            {
                "title": "Dim Sum Culture",
                "content": "Dim sum is a cornerstone of Hong Kong cuisine, traditionally enjoyed during yum cha (tea drinking) sessions. Popular dishes include har gow (shrimp dumplings), siu mai (pork dumplings), char siu bao (BBQ pork buns), and egg tarts. Best experienced at traditional tea houses like Maxim's Palace or Lin Heung Tea House. Usually served from 9 AM to 3 PM. Part of Hong Kong's UNESCO Intangible Cultural Heritage."
            }
        ]
        
        self.simple_docs = []
        for item in tourism_data:
            doc = Document(
                page_content=item["content"],
                metadata={"title": item["title"]}
            )
            self.simple_docs.append(doc)
        
        logger.info(f"Loaded {len(self.simple_docs)} documents into simple store")
    
    async def _load_initial_data_pinecone(self):
        """Load initial Hong Kong tourism data into Pinecone"""
        # Sample Hong Kong tourism data
        tourism_data = [
            {
                "title": "Victoria Peak",
                "content": "Victoria Peak is Hong Kong's premier tourist attraction, offering spectacular 360-degree views of the city skyline, Victoria Harbour, and surrounding islands. Best visited during sunset or at night when the city lights create a magical atmosphere. Take the historic Peak Tram (operating since 1888) to reach the summit. Allow 2-3 hours for the visit. Located at 128 Peak Road. Open daily. Sky Terrace 428 offers the best panoramic views for a small fee."
            },
            {
                "title": "Star Ferry",
                "content": "The iconic Star Ferry has been operating across Victoria Harbour since 1888, connecting Hong Kong Island and Tsim Sha Tsui. This historic ferry ride offers stunning views of both skylines and is one of the most affordable ways to enjoy the harbour. Operating hours: 6:30 AM to 11:30 PM. Very affordable at around HK$3-4 per trip. Great for photography, especially during Symphony of Lights show at 8 PM daily."
            },
            {
                "title": "Temple Street Night Market",
                "content": "Temple Street Night Market in Yau Ma Tei is Hong Kong's most famous night market, coming alive after 6 PM. Famous for street food, fortune telling, Chinese opera performances, and shopping for souvenirs, electronics, and clothing. Must-try foods include curry fish balls, stinky tofu, and claypot rice. Best visited between 7 PM to 10 PM. Located in Yau Ma Tei, accessible via MTR. Bargaining is expected and part of the experience."
            },
            {
                "title": "Dim Sum Culture",
                "content": "Dim sum is an essential Hong Kong culinary experience, traditionally enjoyed during morning or afternoon tea time (yum cha). Popular dishes include har gow (shrimp dumplings), siu mai (pork dumplings), char siu bao (BBQ pork buns), and egg tarts. Best experienced at traditional tea houses like Maxim's Palace, Lin Heung Tea House, or Tim Ho Wan (the world's cheapest Michelin-starred restaurant). Ordering is typically done using dim sum cards or by pointing to dishes on passing carts."
            },
            {
                "title": "Hong Kong Disneyland",
                "content": "Hong Kong Disneyland is a magical theme park located on Lantau Island, featuring classic Disney attractions with unique Asian touches. The park includes themed lands like Fantasyland, Tomorrowland, and the exclusive Mystic Point. Popular attractions include Space Mountain, It's a Small World, and the Iron Man Experience. Best to visit on weekdays to avoid crowds. Accessible via MTR Disneyland Resort Line. Allow a full day for the experience."
            },
            {
                "title": "Symphony of Lights",
                "content": "The Symphony of Lights is a multimedia light and sound show that illuminates Hong Kong's skyline every evening at 8 PM. Recognized by Guinness World Records as the world's largest permanent light show, it features more than 40 buildings on both sides of Victoria Harbour. Best viewing spots include Tsim Sha Tsui Promenade, Avenue of Stars, and Hong Kong Space Museum. The show lasts about 13 minutes and is free to watch. Available in multiple languages."
            },
            {
                "title": "Ocean Park",
                "content": "Ocean Park is a marine mammal park, oceanarium, animal theme park and amusement park in Hong Kong. It features thrilling rides, animal exhibits, and educational shows. The park is divided into two main areas: The Waterfront and The Summit, connected by cable car and ocean express funicular train. Popular attractions include the Giant Panda Adventure, Hair Raiser roller coaster, and dolphin shows. Located in Aberdeen, accessible by bus or taxi."
            },
            {
                "title": "Ladies' Market",
                "content": "Ladies' Market in Mongkok is one of Hong Kong's most popular street markets, known for bargain shopping and street food. The market stretches along Tung Choi Street and offers clothing, accessories, souvenirs, and electronics at competitive prices. Bargaining is expected and part of the fun. Open daily from around 12 PM to 11 PM. Best accessed via Mongkok MTR station. Try local street snacks like fish balls, egg waffles, and stinky tofu while shopping."
            },
            {
                "title": "Big Buddha and Po Lin Monastery",
                "content": "The Tian Tan Buddha (Big Buddha) is a large bronze statue located at Ngong Ping on Lantau Island. Standing 34 meters tall, it's one of the largest seated bronze Buddha statues in the world. The adjacent Po Lin Monastery is a significant Buddhist temple known for its vegetarian cuisine. Accessible via Ngong Ping 360 cable car, which offers stunning views during the 25-minute ride. Allow half a day for the visit including travel time."
            },
            {
                "title": "Central-Mid-Levels Escalator",
                "content": "The Central-Mid-Levels escalator system is the longest outdoor covered escalator system in the world, stretching 800 meters from Central to the Mid-Levels residential area. It operates downward from 6-10 AM and upward from 10:20 AM-midnight. The journey takes about 20 minutes and passes through various neighborhoods including SoHo (South of Hollywood Road), known for its restaurants, bars, and nightlife. Free to use and a great way to explore different levels of Hong Kong Island."
            }
        ]
        
        # Create documents
        documents = []
        for item in tourism_data:
            doc = Document(
                page_content=item["content"],
                metadata={"title": item["title"], "category": "tourism"}
            )
            documents.append(doc)
        
        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        
        docs = text_splitter.split_documents(documents)
        
        # Add documents to Pinecone
        if self.vectorstore:
            await self.vectorstore.aadd_documents(docs)
            logger.info(f"Added {len(docs)} document chunks to Pinecone")
        else:
            logger.warning("Vector store not available, documents not added")
    
    async def chat(
        self,
        query: str,
        conversation_history: List[ConversationMessage] = None,
        user_context: Optional[UserContext] = None
    ) -> Dict[str, Any]:
        """Process a chat query using RAG"""
        try:
            if conversation_history is None:
                conversation_history = []
            
            # Build chat history string  
            chat_history = ""
            for msg in conversation_history[-5:]:  # Last 5 messages for context
                # Handle both dictionary and Pydantic model instances
                if isinstance(msg, dict):
                    role = "Human" if msg.get("role") == "user" else "Assistant"
                    content = msg.get("content", "")
                else:
                    role = "Human" if msg.role == "user" else "Assistant"
                    content = msg.content
                chat_history += f"{role}: {content}\n"
            
            # Enhance query with user context
            enhanced_query = query
            if user_context:
                context_info = []
                
                # Handle both dictionary and Pydantic model instances
                if isinstance(user_context, dict):
                    location = user_context.get("location")
                    interests = user_context.get("interests", [])
                    budget_range = user_context.get("budget_range")
                else:
                    # Pydantic model instance
                    location = getattr(user_context, "location", None)
                    interests = getattr(user_context, "interests", [])
                    budget_range = getattr(user_context, "budget_range", None)
                
                if location:
                    context_info.append(f"Current location: {location}")
                if interests:
                    context_info.append(f"Interests: {', '.join(interests)}")
                if budget_range:
                    context_info.append(f"Budget: {budget_range}")
                
                if context_info:
                    enhanced_query = f"{query}\n\nUser context: {'; '.join(context_info)}"
            
            # Get relevant documents
            if self.vectorstore:
                relevant_docs = self.vectorstore.similarity_search(enhanced_query, k=4)
            elif hasattr(self, 'simple_docs') and self.simple_docs:
                # Simple keyword matching for fallback
                relevant_docs = []
                query_lower = enhanced_query.lower()
                for doc in self.simple_docs:
                    if any(word in doc.page_content.lower() for word in query_lower.split()):
                        relevant_docs.append(doc)
                # If no matches, return all documents
                if not relevant_docs:
                    relevant_docs = self.simple_docs[:3]  # Return first 3 docs
            else:
                # Final fallback: create a generic Hong Kong document
                relevant_docs = [Document(
                    page_content="Hong Kong is a vibrant city with many attractions including Victoria Peak, Star Ferry, Temple Street Night Market, and excellent dim sum restaurants. It's known for its skyline, harbor views, and unique blend of Eastern and Western cultures.",
                    metadata={"title": "Hong Kong Tourism"}
                )]
            
            # Build context from relevant documents
            context = "\n\n".join([doc.page_content for doc in relevant_docs])
            
            # Format the prompt
            formatted_prompt = self.prompt.format(
                context=context,
                chat_history=chat_history,
                question=enhanced_query
            )
            
            # Get response from LLM
            response = await self.llm.ainvoke(formatted_prompt)
            
            # Extract sources
            sources = []
            for doc in relevant_docs:
                sources.append({
                    "title": doc.metadata.get("title", "Hong Kong Tourism Info"),
                    "content": doc.page_content[:200] + "...",
                    "relevance_score": 0.8  # Placeholder score
                })
            
            return {
                "answer": humanize_response(response.content),
                "sources": sources,
                "context_used": len(relevant_docs)
            }
            
        except Exception as e:
            logger.error(f"Error in chat: {e}")
            return {
                "answer": "I apologize, but I'm experiencing some technical difficulties. Please try asking your question again, or contact support if the issue persists.",
                "sources": [],
                "context_used": 0
            }
    
    async def add_document(self, title: str, content: str, metadata: Dict[str, Any] = None) -> bool:
        """Add a new document to the knowledge base"""
        try:
            if metadata is None:
                metadata = {}
            
            metadata["title"] = title
            doc = Document(page_content=content, metadata=metadata)
            
            if self.vectorstore:
                await self.vectorstore.aadd_documents([doc])
                logger.info(f"Added document '{title}' to Pinecone")
                return True
            elif hasattr(self, 'simple_docs'):
                self.simple_docs.append(doc)
                logger.info(f"Added document '{title}' to simple store")
                return True
            else:
                logger.warning("No vector store available to add document")
                return False
                
        except Exception as e:
            logger.error(f"Error adding document: {e}")
            return False
    
    async def search_documents(self, query: str, k: int = 5) -> List[Document]:
        """Search for relevant documents"""
        try:
            if self.vectorstore:
                return self.vectorstore.similarity_search(query, k=k)
            elif hasattr(self, 'simple_docs') and self.simple_docs:
                # Simple keyword matching
                query_lower = query.lower()
                relevant_docs = []
                for doc in self.simple_docs:
                    if any(word in doc.page_content.lower() for word in query_lower.split()):
                        relevant_docs.append(doc)
                return relevant_docs[:k]
            else:
                return []
                
        except Exception as e:
            logger.error(f"Error searching documents: {e}")
            return []
