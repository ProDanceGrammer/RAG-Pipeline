"""Test queries for RAG evaluation."""

# Test queries with expected relevant sections
# Format: (query, expected_sections, topic)

TEST_QUERIES = [
    # OOP queries
    {
        "query": "What is encapsulation in OOP?",
        "expected_sections": ["Encapsulation"],
        "topic": "OOP",
        "difficulty": "easy"
    },
    {
        "query": "How does inheritance work?",
        "expected_sections": ["Inheritance", "Multiple inheritance"],
        "topic": "OOP",
        "difficulty": "easy"
    },
    {
        "query": "What are the advantages of polymorphism?",
        "expected_sections": ["Polymorphism"],
        "topic": "OOP",
        "difficulty": "medium"
    },
    {
        "query": "Explain the Single Responsibility Principle",
        "expected_sections": ["**The Single Responsibility Principle**"],
        "topic": "OOP",
        "difficulty": "medium"
    },
    {
        "query": "What is better to use instead of inheritance?",
        "expected_sections": ["Inheritance", "Composition"],
        "topic": "OOP",
        "difficulty": "hard"
    },
    {
        "query": "How to implement the Singleton pattern?",
        "expected_sections": ["Singleton"],
        "topic": "OOP",
        "difficulty": "medium"
    },
    {
        "query": "What are abstract classes and when to use them?",
        "expected_sections": ["Abstract classes"],
        "topic": "OOP",
        "difficulty": "medium"
    },

    # Python queries
    {
        "query": "What are Python decorators?",
        "expected_sections": ["Decorator", "**Property decorator**"],
        "topic": "Python",
        "difficulty": "easy"
    },
    {
        "query": "How do list comprehensions work?",
        "expected_sections": ["List comprehension"],
        "topic": "Python",
        "difficulty": "easy"
    },
    {
        "query": "What is the difference between args and kwargs?",
        "expected_sections": ["*args", "**kwargs"],
        "topic": "Python",
        "difficulty": "medium"
    },
    {
        "query": "How to use context managers in Python?",
        "expected_sections": ["Context manager"],
        "topic": "Python",
        "difficulty": "medium"
    },
    {
        "query": "What are generators and why use them?",
        "expected_sections": ["Generator"],
        "topic": "Python",
        "difficulty": "medium"
    },
    {
        "query": "Explain Python's GIL",
        "expected_sections": ["GIL", "Global Interpreter Lock"],
        "topic": "Python",
        "difficulty": "hard"
    },

    # Database Optimization queries
    {
        "query": "What is database indexing?",
        "expected_sections": ["Indexing"],
        "topic": "Database",
        "difficulty": "easy"
    },
    {
        "query": "How does query optimization work?",
        "expected_sections": ["Query Optimization"],
        "topic": "Database",
        "difficulty": "medium"
    },
    {
        "query": "What are the best practices for database normalization?",
        "expected_sections": ["Normalization"],
        "topic": "Database",
        "difficulty": "medium"
    },
    {
        "query": "When should I use database partitioning?",
        "expected_sections": ["Partitioning"],
        "topic": "Database",
        "difficulty": "hard"
    },
    {
        "query": "What is the difference between clustered and non-clustered indexes?",
        "expected_sections": ["Indexing"],
        "topic": "Database",
        "difficulty": "hard"
    },

    # Machine Learning queries
    {
        "query": "What is machine learning?",
        "expected_sections": ["Machine Learning"],
        "topic": "ML",
        "difficulty": "easy"
    },
    {
        "query": "What is data leakage?",
        "expected_sections": ["Data Leakage"],
        "topic": "ML",
        "difficulty": "medium"
    },
    {
        "query": "Explain loss functions in machine learning",
        "expected_sections": ["Loss function"],
        "topic": "ML",
        "difficulty": "medium"
    },

    # Cross-topic queries (harder)
    {
        "query": "How to implement caching in Python?",
        "expected_sections": ["Caching", "Decorator"],
        "topic": "Python",
        "difficulty": "hard"
    },
    {
        "query": "What are the SOLID principles?",
        "expected_sections": ["Single Responsibility", "Open/Closed", "Liskov", "Interface Segregation", "Dependency Inversion"],
        "topic": "OOP",
        "difficulty": "hard"
    },
    {
        "query": "How to optimize database queries in Python applications?",
        "expected_sections": ["Query Optimization", "Indexing"],
        "topic": "Database",
        "difficulty": "hard"
    },
]


def get_queries_by_topic(topic: str):
    """Get queries for a specific topic."""
    return [q for q in TEST_QUERIES if q["topic"] == topic]


def get_queries_by_difficulty(difficulty: str):
    """Get queries by difficulty level."""
    return [q for q in TEST_QUERIES if q["difficulty"] == difficulty]


def get_all_queries():
    """Get all test queries."""
    return TEST_QUERIES
