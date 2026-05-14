"""Topic detection for query filtering."""
from typing import Optional
import logging

logger = logging.getLogger(__name__)

# Topic keywords for classification
TOPIC_KEYWORDS = {
    'ML': [
        'machine learning', 'model', 'training', 'loss function',
        'data leakage', 'overfitting', 'underfitting', 'neural network',
        'loss', 'gradient', 'backpropagation', 'dataset', 'feature'
    ],
    'OOP': [
        'class', 'inheritance', 'polymorphism', 'encapsulation',
        'SOLID', 'abstraction', 'interface', 'object-oriented',
        'single responsibility', 'open closed', 'liskov',
        'interface segregation', 'dependency inversion',
        'GRASP', 'design pattern', 'coupling', 'cohesion'
    ],
    'Python': [
        'decorator', 'comprehension', 'args', 'kwargs', 'generator',
        'iterator', 'lambda', 'python', 'list comprehension',
        'dict comprehension', 'yield', 'async', 'await'
    ],
    'Database': [
        'database', 'index', 'query', 'optimization', 'transaction',
        'normalization', 'join', 'SQL', 'partitioning', 'sharding',
        'ACID', 'table', 'schema', 'foreign key'
    ]
}


def detect_topic(query: str) -> Optional[str]:
    """
    Detect topic from query text using keyword matching.

    Args:
        query: Query text

    Returns:
        Topic name ('ML', 'OOP', 'Python', 'Database') or None if no topic detected
    """
    query_lower = query.lower()

    # Count keyword matches per topic
    topic_scores = {}
    for topic, keywords in TOPIC_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in query_lower)
        if score > 0:
            topic_scores[topic] = score

    # Return topic with highest score
    if topic_scores:
        best_topic = max(topic_scores, key=topic_scores.get)
        logger.debug(f"Detected topic '{best_topic}' for query: {query[:50]}... (score: {topic_scores[best_topic]})")
        return best_topic

    logger.debug(f"No topic detected for query: {query[:50]}...")
    return None
