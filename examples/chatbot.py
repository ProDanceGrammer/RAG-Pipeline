"""Example: Building a simple RAG chatbot."""
from src.core.model_factory import ModelFactory
from src.rag.embedder import Embedder
from src.rag.vector_store import FAISSVectorStore
from src.rag.retriever import Retriever
from src.rag.indexer import DocumentIndexer
from src.processing.chunking import TextChunker
from src.inference.inference_engine import InferenceEngine


class RAGChatbot:
    """Simple RAG-powered chatbot."""

    def __init__(self, config_path="config/model_config.yaml"):
        """Initialize the chatbot."""
        print("Initializing RAG Chatbot...")

        factory = ModelFactory(config_path)
        self.llm = factory.create_default_model()

        self.embedder = Embedder(self.llm, batch_size=100)
        self.vector_store = FAISSVectorStore(dimension=1536)
        self.chunker = TextChunker(chunk_size=512, chunk_overlap=50)
        self.retriever = None
        self.engine = None

        print("Chatbot initialized!")

    def load_knowledge_base(self, documents):
        """Load documents into the knowledge base."""
        print(f"Loading {len(documents)} documents...")

        indexer = DocumentIndexer(self.vector_store, self.embedder, self.chunker)
        indexer.index_documents(documents)

        self.retriever = Retriever(self.vector_store, self.embedder, top_k=3)
        self.engine = InferenceEngine(self.llm, self.retriever)

        print("Knowledge base loaded!")

    def chat(self, message, use_rag=True):
        """Process a chat message."""
        if not self.engine:
            return "Please load a knowledge base first."

        return self.engine.query(message, use_rag=use_rag)

    def chat_with_context(self, message):
        """Get response with retrieved context."""
        if not self.engine:
            return {"answer": "Please load a knowledge base first.", "context": []}

        result = self.engine.query_with_metadata(message, use_rag=True)
        return {
            "answer": result["answer"],
            "context": result["retrieved_documents"]
        }


def main():
    """Run the chatbot."""
    # Sample knowledge base
    knowledge_base = [
        {
            "text": "Python is a high-level, interpreted programming language known for its simplicity and readability. It's widely used in data science, web development, and automation.",
            "source": "python_intro.txt"
        },
        {
            "text": "Machine learning is a subset of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed.",
            "source": "ml_basics.txt"
        },
        {
            "text": "Neural networks are computing systems inspired by biological neural networks. They consist of interconnected nodes (neurons) organized in layers.",
            "source": "neural_nets.txt"
        },
        {
            "text": "Natural language processing (NLP) is a branch of AI that helps computers understand, interpret, and generate human language.",
            "source": "nlp_intro.txt"
        }
    ]

    # Initialize chatbot
    chatbot = RAGChatbot()
    chatbot.load_knowledge_base(knowledge_base)

    print("\n" + "="*50)
    print("RAG Chatbot Ready!")
    print("Type 'exit' to quit, 'context' to see retrieved context")
    print("="*50 + "\n")

    # Chat loop
    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() == 'context':
            message = input("Enter question to see context: ").strip()
            result = chatbot.chat_with_context(message)

            print(f"\nBot: {result['answer']}\n")
            print("Retrieved Context:")
            for i, doc in enumerate(result['context'], 1):
                print(f"  [{i}] Similarity: {doc['similarity']:.3f}")
                print(f"      Source: {doc['metadata']['source']}")
                print(f"      Text: {doc['metadata']['text'][:100]}...\n")
        else:
            response = chatbot.chat(user_input)
            print(f"\nBot: {response}\n")


if __name__ == "__main__":
    main()
