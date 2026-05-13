# RAG prototype plan


We have to build a prototype of RAG pipeline to show my team leader my knowledge level in RAG techniques. 

I decided to build it with my Notion files about Python Basics, OOP topics, Machine Learning techniques and workflows and database optimization techniques. Generally files are a Research in Software engineering in Python, OOP, Machine Learning and Database optimization.

Documents description:

- Documents are written with English language, including Python programming language and SQL.
- Documents will not increase or expand. It is static dataset.
- Documents are well-structured Markdown Notion files, which have repeatative structure.
- Each topic of a domain has same number of sections (not everyone of them are filled with information):
    - Name
    - Date (may be ignored)
    - 🔽 What? 🔽 - describes a topic with a noun and domain of usage sometimes
    - 🔁 What does it do? 🔁 - describes its action ability, mostly starts with a verb to emphasize an action of a technology
    - 🤷‍♂️ Why do we use it? 🤷‍♂️ - purposes of usage of a technology mixed with advantages
    - 🤔 How does it work? 🤔 - explains core logic or examples to understand a technology
    - ✍️ How to use it? ✍️ - shows examples of code usage, workflows or implementation techniques, and examples of related libraries or frameworks
    - 👍 Advantages 👍 - represents advantages of a technology
    - 👎 Disadvantages 👎 - represents disadvantages of a technology
    - ↔️ Alternatives ↔️- represents alternatives of a technology
    - ✅ Best practices ✅ - represents best practices of a technology
    - 🛠️ Use cases 🛠️ - represents use cases and domains of usage of a technology
    - 🛑 Worst practices 🛑- represents worst practies of a technology, or techniques which are better to exclude during engineering
    - Sources - represents bookmarks of links to sources, may be included in answers, to provide reasoning of answers.
- Rarely tables and pictures appear there
- Images me be excluded as they visualize the data in a text mostly, but tables are important

Requirements of a RAG pipeline prototype:

1. Low curve of RAG knowledge to understand script
2. OOP programming
3. SOLID and KISS+DRY principles trade-off (high priority)
4. Standardized shared logging logic across the project. (high priority)
5. Readable code
6. Reliable code
7. Repeatable code. So after new interactions it will give the same result. May be seed would be a need.
8. Free-to-test and experiment. Use open-source solutions if they are relevant and would not take days to test.
9. Fault tolerance
10. Speed and low latency is better than 100% accuracy.
11. Build in retry mechanisms, fallback strategies, and monitoring to keep things running smoothly
12. To use RAG implement input() function to interact with it through a console. I want to ask general questions like “What is encapsulation?”, “what is better to use instead of inheritance?” etc.
13. Build unittests 
14. Build integration tests if needed
15. Provide well reasoning on each of steps and add it into the documentation and README.md
16. When a query is received, it is also transformed into an embedding vector, which can be compared with the stored vectors to retrieve the most semantically similar chunks.
17. Tables have to be handled gracefully.

Initial Plan

1. Input documents
    1. Look through my files in @data\raw
    2. Verify all files included in a pipeline.
    3. Count words and file sizes to understand resources consumption in the future.
2. Choose and implement chunking strategy
    1. Determine documents and content types
    2. Determine Query complexity
    3. Determine available resources
    4. Determine size of model’s context window
    5. **Choose relevant Chunk Sizes**
    6. **Multiple Vector Stores**: Maintain **separate vector stores** for **different chunk sizes**. This allows for **flexible retrieval strategies** where a query can first pull from multiple stores before ranking results based on relevance, balancing context and granularity effectively.
    7. List most relevant chunking strategies and suggest which are better to use and why. Here is my list of strategies I know. Maybe you know others. Compare them and suggest which are more relevant for our dataset.
        1. Fixed-size chunking
        2. Sentence-based Chunking
        3. Semantic chunking
        4. Recursive chunking or Recursive Character Splitter
        5. Document structure-based chunking
        6. Sliding-window chunking
        7. Hierarchical and contextual chunking
        8. Topic-based and modality-specific chunking
        9. Agentic and AI-Driven Dynamic Chunking
    8. Experiment with different relevant chunking strategies.
    9. Choose relevant Chunking strategy to such Notion pages of educational notes.
    10. Focus on these core principles during selecting chunking strategy
        - **Semantic coherence:** Each chunk should **group related concepts** and maintain a **logical flow of information**.
        - **Contextual preservation:** A chunk should include **enough surrounding information** to retain meaning when separated from the original document.
        - **Computational optimization:** Chunk size should balance **semantic richness** with **efficiency**, ensuring the system can process **chunks quickly** without **exceeding memory or token limits**.
    11. **Use cross-validation.** It helps ensure that improvements **aren’t just one-off** successes but hold up across different use cases.
    12. Implement Chunking strategy metrics to evaluate the speed and accuracy of results depending on a strategy and its parameters.
        - **Context precision** measures how many of the retrieved chunks are actually relevant to the query, while **context recall** measures how many relevant chunks from the knowledge base were successfully retrieved.
        - Closely related is **context relevancy**, which focuses on how well the **retrieved chunks** align with the **user’s intent**, making it especially useful when **tuning retrieval** settings like top-K values.
        - Other chunk-specific metrics, such as **chunk utilization,** measure how **much** of a chunk’s **content** the model actually **used to** **generate** its response; if **utilization** is **low**, the chunk may be **too broad** or **noisy**.
        - On the other hand, **chunk attribution** evaluates whether the **system correctly identifies** which chunks contributed to the final answer. These chunk-level evaluations help confirm whether chunks are **not only retrieved** but also **meaningfully applied**.
        - **Optimization** also plays a key role and often means balancing **speed** with **accuracy**. **Experimenting** with **chunk sizes**, **overlap percentages**, and **retrieval parameters** to improve both **computational efficiency** and **semantic richness** is critical. Additionally, **A/B testing** is necessary as it provides **concrete feedback**, while iterative adjustments ensure the strategy improves over time instead of stagnating.
3. Experiment with different relevant embedding models to choose the best one to use with my dataset
    1. Select relevant embedding model according to requirements and document datatype.
    2. Do we use any of model that I know listed below, or you will suggest some of not listed? Comapre them and explain why should we ignore ones, and use others.
        1. Word2Vec (Skip-gram or CBOW)
        2. GloVe
        3. FastText
        4. BERT
        5. GPT
        6. ELMo
        7. Doc2vec
        8. InferSent
    3. Key factors to consider during selection an Embedding model
        1. Model Type: **Bi-Encoder vs. Cross-Encoder**
            
            **Bi-Encoders** are typically preferred for RAG applications as they allow for faster retrieval by encoding queries and documents separately, which is beneficial for **similarity search tasks**. 
            
            In contrast, **Cross-Encoders** evaluate pairs of inputs together, which can be more **accurate** but **slower** due to their computational overhead.
            
        2. **Benchmark Performance**
            
            Utilize benchmarks like the **Massive Text Embedding Benchmark (MTEB)** to assess model performance in specific tasks relevant to your domain. Look for models that excel in the “**Retrieval**” task and check metrics such as **NDCG@10**, which indicates how well the model retrieves relevant documents.
            
        3. **Model Size and Latency**
            
            The size of the embedding model directly **impacts both latency and inference time**. **Smaller** models typically offer **lower latency**, making them suitable for applications requiring **quick responses**. **Larger models** may perform **better** in benchmarks but can lead to **slower processing times** and require **more computational resources.**
            
        4. **Vocabulary** Overlap
            
            Ensure that the embedding model’s **vocabulary** aligns well with the **terminology** used in your specific domain or dataset. A model trained on a vocabulary that closely matches your data will likely yield better performance in retrieval tasks.
            
        5. **Dimensionality** of Embeddings.
            
            Consider the embedding dimensions; while **higher dimensions** can capture **more nuanced relationships**, they also **increase computational demands**. A balance must be struck between capturing **complexity** and **maintaining operational efficiency**.
            
        6. **Maximum Token Limit**
            
            Evaluate the max tokens parameter, which indicates the maximum size of document chunks that can be embedded. For most RAG applications, smaller chunks (e.g., a paragraph or less) are preferable for precise retrieval.
            
        7. Custom Evaluation
            
            Conduct custom evaluations on your specific dataset to validate model performance rather than solely relying on academic benchmarks. This helps ensure that the chosen model performs well in real-world scenarios relevant to your application
            
        8. **Cost** Considerations
            
            Factor in the costs associated with storage and computation when selecting an embedding model. Depending on your requirements, you may need to prioritize performance or accept trade-offs for cost efficiency
            
        9. **Hybrid Search Capabilities**
            
            In cases where the data includes specialized terms or acronyms **not well represented** in the embedding model’s training data, incorporating keyword search alongside similarity search can improve retrieval outcomes without adding significant computational overhead.
            
    4. **Cache embeddings smartly.** Save embeddings alongside their source text to avoid reprocessing unchanged content.
4. Provide relevant vectorization techniques
    1. Workflow of implementation
        1. Prepare searchable indexes
        2. Choosing between single-vector and multi-vector indexing
        3. Integrating and optimizing your retrieval system. 
        4. **Monitoring** performance is key to maintaining an efficient system. Keep an eye on metrics such as 
            - query response times,
            - index update speeds,
            - and the relevance of search results.
            
            If performance starts to lag, you may need to adjust your chunking strategy, increase database resources, or refine your embedding model.
            
5. Choose vector database
    1. When selecting a vector database, consider factors like 
        - **query latency,**
        - **data volume,**
        - **and budget constraints**.
6. Test Semantic Search
7. Test RAG pipeline
8. Utilize unittests
    
    ```python
    launch all tests, if any of them fail, provide editions keeping the requirements of the project (principles, trade-off between SOLID and KISS etc.), repeat. Goal here is to rebuild a project until it will run successfully all the tests. 
    ```
    
9. Implement interaction with a script through console.

Ask me if I forgot anything to mention to make your work more efficient and effective. Ask your questions one by one.