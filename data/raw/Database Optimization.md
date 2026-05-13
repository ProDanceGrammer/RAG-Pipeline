# Database Optimization

Skills: Database Management
Start Date: April 3, 2026

# Terms

1. 

# Database Optimization

**🔽 What? 🔽**

- 

**🔁 What does it do? 🔁**

- 

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- 

🤔 **How does it work?** 🤔

- 

**✍️ How to use it? ✍️**

- 

**👍 Advantages 👍**

- 

**👎 Disadvantages 👎**

- 

**↔️ Alternatives ↔️**

- 

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- 

**🛑 Worst practices 🛑**

- 

Sources:

[Strategies for Scaling Databases: A Comprehensive Guide](https://medium.com/@anil.goyal0057/strategies-for-scaling-databases-a-comprehensive-guide-b69cda7df1d3)

## Index

**🔽 What? 🔽**

- a **pointer** to **data** in a table.
- An **index** is a data structure built **on top** of an **existing table**

**🔁 What does it do? 🔁**

- stores the column **values** and provides **pointers** to the rows in the table where those values appear.

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- helps the storage engines to **locate data** with a **reduced latency**.

🤔 **How does it work?** 🤔

- **Indexing** in databases is a **data structure technique** used to **speed up data retrieval operations** by **minimizing the number of disk accesses** required to locate records.
- Indexes Based on **Structure and Key Attributes**:
    - **Primary** Index: **Automatically** created for **primary key constraints**, ensuring **uniqueness** and fast lookups.
    - **Clustered** Index: Physically **organizes the table’s data** in the **index’s order**. Ideal for **range queries**, but only **one per table is allowed**.
    - **Non-clustered** (**Secondary**) Index: **Stores pointers** to the data without affecting physical order, allowing **multiple indexes per table**.
    
    ![image.png](ProDanceGrammer/Skiller/Database%20Management/image.png)
    
- Indexes Based on **Data Coverage**
    - **Dense Index**: Contains an entry for **every search key value**, ideal for tables with **few distinct values**.
    - **Sparse Index**: Contains entries for only some search key values, suitable for tables with **many distinct values**. Stores information about only a **subset of the rows** in a table, **rather than every row**. They are designed to optimize query performance for specific use cases where indexing all rows is not necessary. **Save space** compared to traditional indexes because they don’t need to store index entries for every row in the table.
- Specialized Index Types:
    - **Single-column** Index
        
        An index created on a single column of a table. We use it when queries **frequently filter** or **sort** by **one specific column**. For example, an e-commerce site has a `products` table. Users often search by product SKU.
        
        Index creation
        
        ```sql
        CREATE INDEX idx_products_sku ON products(sku);
        ```
        
        **Why?** This speeds up queries like:
        
        ```sql
        SELECT * FROM products WHERE sku = 'ABC123';
        ```
        
    - **Composite** Index **(Multi-Column** Index**)**
        
        An index that includes two or more columns. We use it when queries **filter** or **sort** by **multiple columns together**, **especially** in the **same order**. The **order** of columns in a composite index **matters**. An index on `(last_name, first_name)` can be used for queries filtering by `last_name` or both `last_name` and `first_name`, but **not** just `first_name`. For example, a job portal has a `jobs` table. Users often filter by `location` and `job_type`.
        
        ```sql
        CREATE INDEX idx_jobs_location_type ON jobs(location, job_type);
        ```
        
        This helps with:
        
        ```sql
        
        SELECT * FROM jobs WHERE location = 'New York' AND job_type = 'Full-Time';
        ```
        
    - **Unique** Index
        
        An index that ensures **all values** in the indexed **column**(s) are **unique**. We use it to enforce **data integrity**, such as ensuring **no two users have the same email**. For example, a social media app stores users in a `users` table. Each user must have a unique username.
        
        ```sql
        CREATE UNIQUE INDEX idx_unique_username ON users(username);
        ```
        
    - **Bitmap** Index
        
        Uses bitmaps for low-cardinality columns. Common in data warehousing. PostgreSQL uses **Bitmap Index Scans**, which are dynamic, **in-memory** structures created during query execution
        
    - **Hash** Index
        
        Maps values to locations using a hash function, great for exact-match queries.
        
        ```sql
        CREATE INDEX idx_session_token_hash 
        ON user_sessions USING HASH (session_token);
        ```
        
    - **Filtered** Index
        
        Indexes a **subset of rows** based on a **condition**, optimizing specific queries.
        
    - **Covering** Index
        
        Includes **all columns needed** for a query, avoiding table access.
        
        ```sql
        CREATE INDEX idx_users_email_covering 
        ON users(email) 
        INCLUDE (username, status);
        -- Execution Plan: Index-Only Scan (No heap fetch)
        ```
        
        > *A **covering index** is just an index that includes all the columns your query needs, even if they’re not part of the search condition. These extra columns are added as **payload**, meaning they’re stored in the index just to satisfy the query`SELECT` not to filter or sort.*
        > 
        
        Let’s say you often run this query:
        
        ```sql
        SELECT username FROM users WHERE email = 'sam@example.com';
        ```
        
        You could create this covering index:
        
        ```sql
        CREATE INDEX idx_users_email_username ON users(email) INCLUDE (username);
        ```
        
        Now both `email` (search key) and `username` (included column) are stored in the index. This means PostgreSQL doesn’t have to look at the heap at all, it gets everything it needs from the index.
        
        - Add **More Columns** with `INCLUDE`
        
        Covering index:
        
        ```sql
        CREATE INDEX idx_email_status ON users(email, status)
        INCLUDE (username, created_at);
        ```
        
        Query:
        
        ```sql
        SELECT username, created_at FROM users
        WHERE email = 'sam@example.com' AND status = 'active';
        ```
        
        - `email`, `status`: filtering (index key)
        - `username`, `created_at`: payload (included)
        
        - **Expression Indexes + Partial Indexes**
        
        If you often do:
        
        ```sql
        SELECT username FROM users WHERE LOWER(email) = 'sam@example.com';
        ```
        
        Create this index:
        
        ```sql
        CREATE INDEX idx_lower_email_username ON users(LOWER(email)) INCLUDE (username);
        ```
        
        Also, if you only care about a subset of rows, say active users, you can create a **partial index**:
        
        ```sql
        CREATE INDEX idx_active_email_username ON users(email) INCLUDE (username) WHERE status = 'active';
        ```
        
        PostgreSQL will only use this index when your query includes `WHERE status = 'active'`.
        
    - **Expression (Function-Based)** Index
        
        Indexes the **result** of a **function or expression** on columns. 
        
        - **Immutability:** The function or expression must be **IMMUTABLE**—meaning it must always return the same result for the same input and cannot depend on external factors like the current time or other tables.
        - **Exact Match:** For the index to be used, the query must use the **exact same expression** as defined in the index.
        - **Parentheses:** If the index is built on an expression (like `A + B`) rather than a single function call (like `LOWER(col)`), you must wrap the entire expression in an extra set of parentheses.
        - **Write Overhead:** Like all indexes, function-based indexes slow down `INSERT` and `UPDATE` operations because the expression must be recalculated for every write.
        1. **Case-Insensitive Search.** A standard B-tree index on an `email` column will not be used if your query uses `LOWER(email)`. **SQL for Devs +1**
            - **Index Creation:**
            
            ```sql
            CREATE INDEX users_lower_email_idx ON users (LOWER(email));
            ```
            
            - **Matching Query:**
            
            ```sql
            SELECT * FROM users WHERE LOWER(email) = 'user@example.com';
            ```
            
        
        [SQL for Devs](data:image/png;base64,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)
        
        1. **Date-Based Queries**
            
            If you store data as a `TIMESTAMP` but frequently filter by a specific day, you can index the casted date. **Amazon AWS Documentation +1**
            
            - **Index Creation:**
                
                ```sql
                CREATE INDEX articles_day_idx ON articles (DATE(published_at));
                ```
                
            - **Matching Query:**
                
                ```sql
                SELECT * FROM articles WHERE DATE(published_at) = '2024-03-20';
                ```
                
        2. **Mathematical Expressions**
            
            You can index the result of calculations involving multiple columns. **AtlasGo +1**
            
            - **Index Creation:**
                
                ```sql
                - Note: Expressions require an extra set of parentheses
                CREATE INDEX scorecard_avg_idx ON scorecard (((science + mathematics) / 2));
                ```
                
            - **Matching Query:**
                
                ```sql
                SELECT * FROM scorecard WHERE ((science + mathematics) / 2) > 90;
                ```
                
        
        [Amazon AWS Documentation](data:image/png;base64,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)
        
        [AtlasGo](data:image/png;base64,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)
        
    - **Full-text** Index
        
        An index designed for efficient searching of **large text fields** using **natural language queries**. We use it when you need to search within **text columns** for **words or phrases** (e.g., blog posts, product descriptions). For example, a blogging platform stores articles in a `posts` table. Users search for keywords in the content.
        
        ```sql
        CREATE FULLTEXT INDEX idx_post_content ON posts(content);
        ```
        
        Enables:
        
        ```sql
        SELECT * FROM posts WHERE MATCH(content) AGAINST('database indexing');
        ```
        
    - **Spatial** Index
        
        An index used for spatial (**geographic**) data types like **points, lines, and polygons**. We use it when working with GIS (**Geographic Information Systems**) or **location-based queries**. For example in MySQL, a food delivery app stores restaurant locations in a `restaurants` table using geographic coordinates.
        
        ```sql
        CREATE SPATIAL INDEX idx_restaurants_location ON restaurants(location);
        ```
        
        PostgreSQL
        
        ```sql
        CREATE EXTENSION postgis;
        CREATE INDEX idx_restaurants_location ON restaurants USING GIST (location);
        ```
        
        Optimizes:
        
        MySQL
        
        ```sql
        SELECT * FROM restaurants
        WHERE ST_Distance_Sphere(location, POINT(106.7, 10.8)) < 5000;
        ```
        
        PostgreSQL
        
        ```sql
        SELECT name 
        FROM restaurants 
        WHERE ST_DWithin(
            location, 
            ST_SetSRID(ST_Point(-73.985, 40.758), 4326)::geography, 
            500
        );
        ```
        
- Databases store indexes in several types of optimized structures to improve the **speed** of data retrieval:
    
    ![image.png](ProDanceGrammer/Skiller/Database%20Management/image%201.png)
    
    - **B-Tree (Balanced Tree)** indexing
        
        is a common data structure designed to handle **large datasets** efficiently by **reducing the height of the tree**. Each node in a B-Tree can store **multiple keys** and have **multiple children**, which **minimizes** the number of **disk I/O operations** required for data access. By allowing more children under one node than a regular self-balancing binary search tree, the B-Tree reduces the height of the tree and puts the data in fewer separate blocks. B-trees are very ingrained in the architecture of databases and provide consistently **good performance** for many workloads by **reducing** the **disk block access time** multi-fold.  **Inserting or updating data in a B-Tree can be slower** than doing the same in **un-indexed** data because the tree structure needs to be maintained to ensure balance.
        
    - **B+ Tree** Indexing
        
        ![image.png](ProDanceGrammer/Skiller/Database%20Management/image%202.png)
        
        Now in-order to search for a key, example “302", the search traversal **flows from** the **root** index **to** the **final** data blocks as depicted in the diagram with **green highlight**. The complete search process was completed with the traversal of **3 disk blocks**.
        
    - **Hash tables**
        
        Hash indexes use **hash functions** to map keys to **specific locations**. Hash tables are data structures that **map keys to values** and **use a hash function** to convert a key into an index where the corresponding value is stored. Hash-based indexes are effective for **exact-match lookups** but are not universally supported or used as the default index type in all RDBMSs and do **not preserve ordering** like B-Trees.
        
        | **Feature** | **B-Tree (Default)** | **Hash Index** |
        | --- | --- | --- |
        | **Operators** | `=`, `<`, `>`, `<=`, `>=`, `BETWEEN`, `IN` | `=` only |
        | **Size** | Larger (stores actual values) | Smaller (stores 32-bit hashes) |
        | **Sorting** | Supports `ORDER BY` | No sorting support |
        | **Unique Constraint** | Yes | No |
    - **Bitmap** Indexes
        
        Typically used for **low-cardinality columns**, which are columns with a relatively small number of distinct values. Excellent for read-heavy workloads and **complex queries**, they can be less efficient for write operations. Bitmap indexes use **binary arrays** to indicate the presence of key values:
        
        - Each **bit** corresponds to a **row**, showing whether the **key exists**.
        - Ideal for low-cardinality columns and **complex analytical queries** using bitwise operations.
    - **LSM Tree**
        
        This is more common in **NoSQL** databases (like Cassandra), optimized for write-heavy workloads.
        

**✍️ How to use it? ✍️**

- Index Creation
    
    ```sql
    CREATE [CLUSTERED | NONCLUSTERED(it is a default)] INDEX index_name ON table_name(column1[, column2, column3, ...]);
    ```
    
    ```sql
    CREATE INDEX IX_Customers_ID ON Customers (ID);
    ```
    
    ```sql
    CREATE CLUSTERED INDEX IX_Customers_City ON Customers (City);
    ```
    
    ```sql
    CREATE CLUSTERED INDEX IX_Customers_Name ON Customers (LastName ASC, FirstName DESC);
    ```
    
- Verifying Index Usage
    
    ```sql
    EXPLAIN [ANALYZE] SELECT * FROM comments WHERE user_id = 101;
    ```
    

**👍 Advantages 👍**

- **Faster Query** Performance: **Indexes reduce** the **number** of **rows scanned**, **speeding up queries** on large datasets.
- **Reduced CPU Usage**: Fewer rows scanned means **less CPU usage**, optimizing resource utilization.
- **Rapid Data Retrieval**: Indexes enable **quick lookups** for equality or range queries.
- **Efficient Sorting**: Indexes allow sorted data access without expensive sorting operations.
- Better **Data Organization**: Indexes help maintain **structured data**, simplifying database management.

**👎 Disadvantages 👎**

- **Performance** can **slow down** when querying **large tables** and indexing avoids scanning every row in a table
- Any kind of index usually **slows down writes**, because the index also needs to be updated every time data is inserted. Since keys are stored in indexes, each time a new row with a unique **key is added**, the index is automatically updated.

**↔️ Alternatives ↔️**

- 

**✅ Best practices ✅**

- Analyze **Query Patterns**: Identify **frequently used queries** to determine which columns to index and the appropriate index type.
- **Index Frequently Used Columns**: Index columns used in `WHERE`, `JOIN`, and `ORDER BY` clauses.
- Index **Selective Columns**: Indexes work best on **high-cardinality columns** (e.g., `customer_id` vs. `gender`).
- Choose the **Right Index Type**: Match the **index type** to your data and **query needs**.
- Use Composite Indexes: Create **indexes on multiple columns** for queries **involving those columns together**. Use them wisely—order of columns matters.
- **Monitor** Performance: Regularly **assess index usage**, **remove unused indexes**, and **adjust** as workloads change.
- Regularly monitor and analyze index usage with tools like `EXPLAIN` or `ANALYZE`.

**🛠️ Use cases 🛠️**

- 

**🛑 Worst practices 🛑**

- Avoid indexing columns with high update frequency unless necessary.
- Avoid **Over-Indexing**: Too many indexes increase storage and slow down write operations (inserts, updates, deletes).

Sources:

[7 Must-know Strategies to Scale Your Database](https://www.youtube.com/watch?v=_1IKwnbscQU)

[PostgreSQL Covering Indexes: Beyond Regular Indexes for Faster Queries](https://vwedesam.medium.com/postgresql-covering-indexes-beyond-regular-indexes-900b2642cb99)

[B-trees and database indexes — PlanetScale](https://planetscale.com/blog/btrees-and-database-indexes)

[How Database B-Tree Indexing Works | Built In](https://builtin.com/data-science/b-tree-index)

[SQL indexing best practices | How to make your database FASTER!](https://www.youtube.com/watch?v=BIlFTFrEFOI)

[SQL Indexes (Visually Explained) | Clustered vs Nonclustered | #SQL Course 35](https://www.youtube.com/watch?v=BxAj3bl00-o)

[Database Index Fundamentals](https://www.youtube.com/watch?v=xAQga907NVU)

[What is a Database Index? | Codecademy](https://www.codecademy.com/article/sql-indexes)

[Role of a Database Index in Performance Optimization](https://www.mongodb.com/resources/basics/databases/database-index)

[Understanding Database Indexes: A Comprehensive Guide day 33 of sytem design basics](https://dev.to/vincenttommi/understanding-database-indexes-a-comprehensive-guide-day-33-of-sytem-design-basics-5dea)

[Introduction To Database Indexes](https://medium.com/@rtawadrous/introduction-to-database-indexes-9b488e243cc1)

[Understanding Database Indexing: The Key to Faster Queries](https://shiftasia.com/community/understanding-database-indexing-the-key-to-faster-queries/)

[Database Indexing](https://medium.com/@akashsdas_dev/database-indexing-e10362624ed3)

[Indexing in Databases - GeeksforGeeks](https://www.geeksforgeeks.org/dbms/indexing-in-databases-set-1/)

[B-Tree Indexing Basics Explained 🗃️](https://shambhavishandilya.medium.com/b-tree-indexing-basics-explained-%EF%B8%8F-56ae0bda46c4)

[What is a Relational Database (RDBMS)? | Databricks](https://www.databricks.com/blog/what-is-relational-database)

## Database normalization

**🔽 What? 🔽**

- is the process of structuring a relational database in accordance with a series of so-called **normal forms**

**🔁 What does it do? 🔁**

- 

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- in order to **reduce data redundancy**
- **improve data integrity**.

🤔 **How does it work?** 🤔

- 

**✍️ How to use it? ✍️**

- 

**👍 Advantages 👍**

- 

**👎 Disadvantages 👎**

- 

**↔️ Alternatives ↔️**

- 

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- 

**🛑 Worst practices 🛑**

- 

Sources:

### Normal forms

**🔽 What? 🔽**

- Concept of normalization

**🔁 What does it do? 🔁**

- 

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- 

🤔 **How does it work?** 🤔

- 

**✍️ How to use it? ✍️**

- a relational database relation is often described as "normalized" if it meets third normal form. Most **3NF** relations are free of insertion, updation, and deletion anomalies

| Constraint (informal description in parentheses) | UNF (1970) | 1NF (1970) | 2NF (1971) | 3NF (1971) | EKNF (1982) | BCNF (1974) | 4NF (1977) | ETNF (2012) | 5NF (1979) | DKNF (1981) | 6NF (2003) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Unique rows (no duplicate records) | 🟡 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Scalar columns** (columns cannot contain relations or composite values) | 🛑 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Every non-prime attribute** has a full functional **dependency on each candidate key** (attributes depend on the whole of every key) | 🛑 | 🛑 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Every non-trivial functional dependency either begins with a superkey or ends with a prime attribute (attributes depend only on candidate keys) | 🛑 | 🛑 | 🛑 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Every non-trivial functional dependency either begins with a superkey or ends with an elementary prime attribute (a stricter form of 3NF) | 🛑 | 🛑 | 🛑 | 🛑 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | N/A |
| Every non-trivial functional dependency begins with a superkey (a stricter form of 3NF) | 🛑 | 🛑 | 🛑 | 🛑 | 🛑 | ✅ | ✅ | ✅ | ✅ | ✅ | N/A |
| Every non-trivial multivalued dependency begins with a superkey | 🛑 | 🛑 | 🛑 | 🛑 | 🛑 | 🛑 | ✅ | ✅ | ✅ | ✅ | N/A |
| Every join dependency has a superkey component | 🛑 | 🛑 | 🛑 | 🛑 | 🛑 | 🛑 | 🛑 | ✅ | ✅ | ✅ | N/A |
| Every join dependency has only superkey components | 🛑 | 🛑 | 🛑 | 🛑 | 🛑 | 🛑 | 🛑 | 🛑 | ✅ | ✅ | N/A |
| Every constraint is a consequence of domain constraints and key constraints | 🛑 | 🛑 | 🛑 | 🛑 | 🛑 | 🛑 | 🛑 | 🛑 | 🛑 | ✅ | 🛑 |
| Every join dependency is trivial | 🛑 | 🛑 | 🛑 | 🛑 | 🛑 | 🛑 | 🛑 | 🛑 | 🛑 | 🛑 | ✅ |

**👍 Advantages 👍**

- 

**👎 Disadvantages 👎**

- 

**↔️ Alternatives ↔️**

- 

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- 

**🛑 Worst practices 🛑**

- 

Sources:

[Database normalization](https://en.wikipedia.org/wiki/Database_normalization#Normal_forms)

### Data redundancy

**🔽 What? 🔽**

- is the existence of data that is **additional** to the **actual data** and permits correction of errors in stored or transmitted data.

**🔁 What does it do? 🔁**

- 

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- 

🤔 **How does it work?** 🤔

- 

**✍️ How to use it? ✍️**

- 

**👍 Advantages 👍**

- 

**👎 Disadvantages 👎**

- 

**↔️ Alternatives ↔️**

- 

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- 

**🛑 Worst practices 🛑**

- 

Sources:

## Database Sharding

**🔽 What? 🔽**

- practice of optimizing database management systems

**🔁 What does it do? 🔁**

- 

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- to achieve **horizontal scalability**
    - and improved **performance**.
- By **horizontally** scaling out, you can enable a **flexible database design** that **increases performance** in two key ways:
    - With **massively parallel processing**, you can take advantage of all the compute resources across your cluster for **every query** since each node can be working on **separate shards** or separate parts of the database.
    - Because the individual shards are smaller than the logical table as a whole, each node has to **scan fewer rows** when responding to a query.
- **Horizontal sharding** is effective when queries **tend to return a subset of rows** that are often **grouped together**. For example, queries that **filter data** based on short **date ranges** are **ideal for horizontal sharding** since the date range will necessarily limit querying to only a subset of the servers (physical or virtual).
- **Vertical Sharding** is effective when queries tend to return **only a subset of columns of the data**. For example, if some queries request only names, and others request only addresses, then the names and addresses can be sharded onto separate servers.
- Also, sharded databases can offer higher levels of **availability**. In the event of an outage on an unsharded database, the entire application is unusable. With a sharded database, **only the** **portions** of the application that relied on the missing chunks of data are **unusable**.

🤔 **How does it work?** 🤔

- separating the rows or columns of a **larger database** table into **multiple smaller tables**.
- The new tables are called “**shards**” (or partitions)
- each **new table** either has the **same schema** but **unique rows** (as is the case for “**horizontal sharding**”)
    - or has a **schema** that is a **proper subset** of the **original** table’s **schema** (as is the case for “**vertical sharding**”)
- By sharding a larger table, you can **store** the new chunks of data, called **logical shards**, across multiple nodes
- typically distributed across **multiple servers**
- **Shard key.** Software developers use a shard key to determine **how to partition** the **dataset**. A **column** in the dataset **determines** which **rows of data group together** to form a **shard**. Database designers choose a shard key from an **existing column** or **create a new one**.

**✍️ How to use it? ✍️**

- Example of sharding
    - **Original Table**
    
    | Customer ID | First Name | Last Name | City |
    | --- | --- | --- | --- |
    | 1 | Alice | Anderson | Austin |
    | 2 | Bob | Best | Boston |
    | 3 | Carrie | Conway | Chicago |
    | 4 | David | Doe | Denver |
    - Vertical sharding
        
        **VS1**
        
        | Customer ID | First name | Last Name |
        | --- | --- | --- |
        | 1 | Alice | Anderson |
        | 2 | Bob | Best |
        | 3 | Carrie | Conway |
        | 4 | David | Doe |
        
        **VS2**
        
        | Customer ID | City |
        | --- | --- |
        | 1 | Auston |
        | 2 | Boston |
        | 3 | Chicago |
        | 4 | Denver |
    - Horizontal Sharding
        
        **HS1**
        
        | Customer ID | First name | Last Name | City |
        | --- | --- | --- | --- |
        | 1 | Alice | Anderson | Auston |
        | 2 | Bob | Best | Boston |
        
        **HS2**
        
        | Customer ID | First name | Last Name | City |
        | --- | --- | --- | --- |
        | 3 | Carrie | Conway | Chicago |
        | 4 | David | Doe | Denver |
- Implementing Sharding in a data management system involves several **key steps**:
    1. **Data Modeling:** Determine the **Sharding key**, which is the attribute or combination of attributes used to determine **how data is distributed across shards**. The choice of sharding key greatly influences performance and data distribution.
    2. **Shard Creation:** Create and provision the shards where data will be distributed. Shards can be **physical servers, virtual machines,** or **containers**, depending on the system architecture.
    3. **Data Migration:** Move existing data into the shards based on the chosen sharding key. **Data migration tools and scripts** can simplify this process.
    4. **Query Routing:** Develop a **query routing mechanism** that directs user queries and transactions to the appropriate shard based on the Sharding key. This often involves a middleware layer responsible for routing.
    5. **Shard Management:** Implement **tools and processes for shard management**, including **adding or removing shards**, **rebalancing** data, and **handling** shard **failures**.
    6. **Monitoring and Maintenance:** Implement **monitoring** and **maintenance processes** to ensure the health and performance of the Sharded database. This includes monitoring for **imbalanced shard sizes**, **high query latencies**, and **hardware failures**.
- [Well-detailed Guide](https://proxysql.com/blog/database-sharding/)
- Tools
    - **MySQL** with **ProxySQL**. ProxySQL acts as a **smart proxy layer** and **handles query routing** and **load balancing** for sharded MySQL databases. It maintains a **mapping** of which shard holds what data, and, when a query comes in, it **automatically routes** it to the appropriate shard so **your application doesn’t have to handle the logic**.
    - **MongoDB** has **built-in sharding support**, which makes it a popular option for handling **large unstructured datasets**. MongoDB uses a **sharding key** to determine how documents are distributed across shards, so you’ll need to choose it carefully. A poor choice can lead to uneven data distribution and performance issues! MongoDB then takes care of the rest: **partitioning, balancing data,** and **routing queries automatically**.
    - **PostgreSQL**. **Citus** is a great option for those who prefer relational databases. **Citus** is essentially an **extension** that transforms **PostgreSQL** into a distributed database. Citus uses a **distributed query planner** to handle complex queries across shards, and it’s especially useful for analytics-heavy applications where you need to **combine data from multiple shards**. The **learning curve** was steeper than MongoDB’s built-in sharding, but the results were worth it!
- We can distribute data according to normal distribution of data. We may look through all of attributes of database, and find the most normal distributed ?

**👍 Advantages 👍**

- **Scalability:** As data volume and user load increase, additional shards can be added **to accommodate the growth**, ensuring system **performance** remains **stable**.
- **Improved Performance:** By distributing data and workloads, Sharding can significantly **enhance query performance** and **reduce response times**. Users experience quicker access to data because requests are **spread across multiple shards**.
- **Fault Tolerance:** Sharding provides **built-in fault tolerance**. If one shard or server fails, the system can continue to operate, as other shards are still operational. This ensures **high availability** and **data durability**.
- **Efficient Resource** Utilization**:** Sharding optimizes resource usage by **distributing data and workloads evenly**. This reduces the risk of resource **bottlenecks** and maximizes hardware utilization.
- **Data Isolation:** Sharding can **isolate data**, making it easier to manage and secure. Different shards can have their **access control** policies and **security settings**.
- **Cost Efficiency**. Sharding allows you to use commodity hardware and cloud infrastructure to scale horizontally **instead of investing in expensive high-performance hardware** to **vertically scale a single server**. By distributing the data across multiple lower-cost servers, you can achieve similar or better performance at a fraction of the cost. Additionally, cloud platforms often allow for the dynamic allocation of resources, enabling you to add or remove shards as needed, optimizing performance and price.

**👎 Disadvantages 👎**

- **Disproportionate Data Distribution.** One of the most significant challenges with manual sharding is **uneven shard allocation**. Disproportionate distribution of data can cause **multiple shards to become unbalanced**, with **some overloaded** while **others** remain **relatively empty**. It’s best to avoid accruing too much data on a shard because a hotspot can lead to slowdowns and database server crashes.
- **Complication Of Operational Processes.** Finally, manual sharding can complicate operational processes. **Backups** will now have to perform for **multiple servers**. **Data migration** and **schema changes** must be **carefully coordinated** to ensure a database shard has the same schema copy. Without sufficient optimization, database joins across multiple servers can be highly inefficient and difficult to perform.

**↔️ Alternatives ↔️**

- **Sharding** and **partitioning** are both about breaking up a large data set into smaller subsets. The difference is that sharding implies the data is **spread across multiple computers** while **partitioning does not**. Partitioning is about **grouping subsets** of data within a **single database instance**. In many cases, the terms sharding and partitioning are even used synonymously, especially when preceded by the terms “horizontal” and “vertical.” Thus, “horizontal sharding” and “horizontal partitioning” can mean the same thing.
- Data Replication

**✅ Best practices ✅**

- Implement **Load Balancing**. Load balancing is crucial for ensuring that no single shard becomes **overwhelmed with requests**. **Strategies** to consider include:
    - **Automatic** Load Balancing: Use tools or middleware that can **automatically distribute traffic** based on the current load on each shard.
    - **Regularly Review Traffic Patterns**: Monitor and adjust load balancing configurations as necessary, especially **during peak usage times**.
- **Optimize Queries**. To maximize the benefits of sharding, ensure that your queries are optimized.
    - **Use Shard Keys in Queries**: Include the shard key in your queries whenever possible to enable **direct routing** to the appropriate shard. This reduces the need for **cross-shard queries** and **enhances performance**.
    - **Limit Cross-Shard Operations**: Design your application to **minimize** operations that require **accessing multiple shards**, as these can introduce **latency** and **complexity**.

**🛠️ Use cases 🛠️**

- in scalable database architectures
- **Social Media Platforms:** Social media companies use Sharding to manage massive amounts of user-generated content, such as posts, photos, and videos. Sharding ensures fast access to user data and high availability.
- **E-commerce:** Online retailers employ sharding to handle **large catalogs of products** and accommodate **high website traffic**. Sharding is essential for managing order data and inventory.
- **Gaming:** Online gaming platforms use Sharding to distribute game state data and player profiles. Sharding ensures low-latency gaming experiences, even in globally distributed multiplayer games.
- **Financial Services:** Financial institutions rely on Sharding to manage vast amounts of transaction data, customer records, and financial histories. Sharding enhances performance and data security.
- **Content Delivery Networks (CDNs):** CDNs utilize geo-based sharding to cache and deliver web content efficiently to users worldwide. Data is distributed to edge servers close to end users to reduce latency.
- **IoT and Telemetry:** Internet of Things (IoT) platforms leverage sharding to manage the massive influx of data generated by sensors and devices. Sharding helps process and analyze telemetry data in real-time.

**🛑 Worst practices 🛑**

- 

Sources:

[What is Database Sharding?](https://www.youtube.com/watch?v=XP98YCr-iXQ)

[Database Sharding - What is Database Sharding or a Database Shard?](https://www.yugabyte.com/key-concepts/database-sharding/#disproportionate-data-distribution)

[A Beginner's Guide to Database Sharding: How to Scale Your Database Effectively — ProxySQL Blog](https://proxysql.com/blog/database-sharding/)

[Database Sharding: Examples, Strategies, Tools & More](https://www.datacamp.com/blog/database-sharding)

[What is Sharding? - Database Sharding Explained - AWS](https://aws.amazon.com/what-is/database-sharding/)

[Sharding](https://hazelcast.com/foundations/distributed-computing/sharding/)

### **Range-Based Sharding (Dynamic Sharding)**

**🔽 What? 🔽**

- 

**🔁 What does it do? 🔁**

- 

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- 

🤔 **How does it work?** 🤔

- involves dividing data based on **specific data ranges** or intervals, such as a range of dates, numeric values, or alphanumeric identifiers
    
    ![image.png](ProDanceGrammer/Skiller/Database%20Management/image%203.png)
    

**✍️ How to use it? ✍️**

- 

**👍 Advantages 👍**

- Efficient for **range queries** because data is distributed in an **orderly manner**
- Facilitates **data archiving** and purging by dropping entire shards.
- Suitable for **time-series data** and **historical records**

**👎 Disadvantages 👎**

- **Imbalanced shard sizes** if data distribution is **uneven**
- Challenges in handling **skewed data distribution**
- **Limited flexibility** when dealing with **non-uniform data access patterns**

**↔️ Alternatives ↔️**

- Hash-Based Sharding (aka Algorithmic or Key-based Sharding)
- Directory-Based Sharding (aka metadata-based Sharding)
- Geo-Based Sharding

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- This method is suitable when data exhibits a **natural ordering**, and queries often target **specific ranges**. For instance, an e-commerce application may use range-based sharding to **distribute order data by date ranges**.

**🛑 Worst practices 🛑**

- 

Sources:

[Database Sharding - What is Database Sharding or a Database Shard?](https://www.yugabyte.com/key-concepts/database-sharding/#disproportionate-data-distribution)

[Sharding](https://hazelcast.com/foundations/distributed-computing/sharding/)

### **Hash-Based Sharding (Algorithmic or Key-based Sharding)**

**🔽 What? 🔽**

- 

**🔁 What does it do? 🔁**

- 

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- This method is often used when there is **no natural ordering** of data or when **even data distribution** is essential.

🤔 **How does it work?** 🤔

- involves using a **hash function** to determine which shard a **particular piece of data belongs to**. The hash function takes some or all of the data's attributes and maps them to a shard identifier.
    
    ![image.png](ProDanceGrammer/Skiller/Database%20Management/image%204.png)
    

**✍️ How to use it? ✍️**

- 

**👍 Advantages 👍**

- **Evenly distributes** data, **preventing hotspots or imbalanced loads**.
- Suitable for situations where the **order** of data is **not important**.
- **Scalable**
- **easy** to **implement**.

**👎 Disadvantages 👎**

- Retrieving a **specific range of data** can be **complex**.
- Shard rebalancing can be **challenging** as **data volume grows**.
- **Adding or removing shards** may require **reshuffling data**.

**↔️ Alternatives ↔️**

- Range-Based Sharding (aka Dynamic Sharding)
- Directory-Based Sharding (aka metadata-based Sharding)
- Geo-Based Sharding

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- 

**🛑 Worst practices 🛑**

- 

Sources:

[Database Sharding - What is Database Sharding or a Database Shard?](https://www.yugabyte.com/key-concepts/database-sharding/#disproportionate-data-distribution)

[Sharding](https://hazelcast.com/foundations/distributed-computing/sharding/)

### **Directory-Based Sharding (metadata-based Sharding)**

**🔽 What? 🔽**

- 

**🔁 What does it do? 🔁**

- 

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- offers **flexibility** in **distributing data** based on a **variety of criteria**, including business logic and data attributes.

🤔 **How does it work?** 🤔

- Employs a **separate** service or metadata **store** to **maintain a mapping** of **data to shards**. Each **piece of data** contains **metadata or attributes** that describe which **shard it belongs to**.

**✍️ How to use it? ✍️**

- 

**👍 Advantages 👍**

- **Flexible** and **adaptable** to **complex distribution needs**.
- **Eases** the process of **shard management** and **rebalancing**.
- Supports **dynamic changes** to data distribution rules.

**👎 Disadvantages 👎**

- Adds **complexity** with the need for a separate metadata service.
- **Performance overhead** due to **metadata lookups**.
- Potential **single point of failure** in the metadata service.

**↔️ Alternatives ↔️**

- Range-Based Sharding (aka Dynamic Sharding)
- Hash-Based Sharding (aka Algorithmic or Key-based Sharding)
- Geo-Based Sharding

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- 

**🛑 Worst practices 🛑**

- 

Sources:

[Sharding](https://hazelcast.com/foundations/distributed-computing/sharding/)

### **Geo-Based Sharding**

**🔽 What? 🔽**

- 

**🔁 What does it do? 🔁**

- 

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- 

🤔 **How does it work?** 🤔

- In this method, data is divided **based on** the **geographical location** or proximity of the **data sources or users**. It ensures that **data closer to the users** is stored in nearby shards, **reducing latency** and **improving performance**.

**✍️ How to use it? ✍️**

- 

**👍 Advantages 👍**

- **Reduced latency** and **improved user experience** for global applications.
- Efficient for **geospatial queries** and **location-aware applications**.
- Geographic redundancy for **disaster recovery** and fault tolerance.

**👎 Disadvantages 👎**

- **Complex** to implement due to the **need to determine data location**.
- Maintaining **consistent data distribution** across geographical regions can be **challenging**.
- **Sensitive to changes** in **user distribution** and access patterns.

**↔️ Alternatives ↔️**

- Range-Based Sharding (aka Dynamic Sharding)
- Hash-Based Sharding (aka Algorithmic or Key-based Sharding)
- Directory-Based Sharding (aka metadata-based Sharding)

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- is particularly relevant for **distributed systems** and applications with **global reach**.
- Geo-based Sharding is commonly used in **content delivery networks (CDNs)** and **global-scale applications**.

**🛑 Worst practices 🛑**

- 

Sources:

[Sharding](https://hazelcast.com/foundations/distributed-computing/sharding/)

## Database Partitioning

**🔽 What? 🔽**

- 

**🔁 What does it do? 🔁**

- 

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- Aims to organize data for **better manageability and performance**, often based on attributes like date, region, or key ranges.

🤔 **How does it work?** 🤔

- Partitions can be located on the same server or within a single database

**✍️ How to use it? ✍️**

- 

**👍 Advantages 👍**

- 

**👎 Disadvantages 👎**

- 

**↔️ Alternatives ↔️**

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- 

**🛑 Worst practices 🛑**

- 

Sources:

[Sharding](https://hazelcast.com/foundations/distributed-computing/sharding/)

## Database Replication

**🔽 What? 🔽**

- db optimization technique

**🔁 What does it do? 🔁**

- 

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- Its primary goal is **high availability** and **minimizing downtime** by allowing rapid failover to a replica if the primary system fails.

🤔 **How does it work?** 🤔

- Involves **continuously copying data** changes to one or more secondary systems in **near real-time**.

**✍️ How to use it? ✍️**

- 

**👍 Advantages 👍**

- 

**👎 Disadvantages 👎**

- 

**↔️ Alternatives ↔️**

- 

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- 

**🛑 Worst practices 🛑**

- 

Sources:

[Database Backup - Types, Process and Benefits | Netdata](https://www.netdata.cloud/academy/what-is-database-backup/)

[Database Scaling Strategies | Codecademy](https://www.codecademy.com/article/database-scaling-strategies)

[What is Database Sharding?](https://www.youtube.com/watch?v=hdxdhCpgYo8)

## Denormalization

**🔽 What? 🔽**

- 

**🔁 What does it do? 🔁**

- 

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- 

🤔 **How does it work?** 🤔

- 

**✍️ How to use it? ✍️**

- 

**👍 Advantages 👍**

- 

**👎 Disadvantages 👎**

- 

**↔️ Alternatives ↔️**

- 

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- 

**🛑 Worst practices 🛑**

- 

Sources:

[Maximizing Performance: Best Practices for Database Scaling](https://dev.to/kaustubhyerkade/maximizing-performance-best-practices-for-database-scaling-2fkn)

## Query Optimization

**🔽 What? 🔽**

- Query optimization refers to the process of **improving** the **performance** of a database query by optimizing the **execution plan** of the query.

**🔁 What does it do? 🔁**

- 

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- involves finding the **most efficient way** to **retrieve data** from a database.
- performance

🤔 **How does it work?** 🤔

- 

**✍️ How to use it? ✍️**

- Indexing
- Caching involves **storing** frequently accessed **data** in memory so that it can be retrieved **more quickly**. By caching data, the database can **reduce the number** of **disk reads** required to retrieve data, resulting in **faster query performance**.

**👍 Advantages 👍**

- 

**👎 Disadvantages 👎**

- 

**↔️ Alternatives ↔️**

- 

**✅ Best practices ✅**

- Use Indexes Wisely
- Avoid SELECT *: Choose Only Required Columns
- Limit Rows with WHERE and LIMIT
- Write Efficient WHERE Clauses
- Use Joins Smartly. Join **only** the tables you need and **filter data before joining**. Use `INNER JOIN` instead of `OUTER JOIN` if you don’t need unmatched rows.
- Use `EXISTS` Instead of `IN` (for Subqueries)
    
    **Poor Approach:**
    
    ```sql
    SELECT name FROM customers
    WHERE customer_id IN (SELECT customer_id FROM orders);
    ```
    
    **Recommended Approach:**
    
    ```sql
    SELECT name FROM customers
    WHERE EXISTS (
      SELECT 1 FROM orders WHERE orders.customer_id = customers.customer_id
    );
    ```
    
- Avoid **Wildcards** at the Start of `LIKE`
    
    Don’t start a `LIKE` pattern with `%` because it disables index use and causes a full table scan.
    
    **Poor Approach**:
    
    ```sql
    SELECT * FROM users WHERE name LIKE '%john';
    ```
    
    **Recommended Approach:**
    
    ```sql
    SELECT * FROM users WHERE name LIKE 'john%';
    ```
    
- Use Query Execution Plan (`EXPLAIN ANALYZE`)
- Use `UNION ALL` Instead of `UNION` (if possible). `UNION` removes duplicates, which **adds sorting overhead**. Use `UNION ALL` if duplicates don’t matter.
- Use `WHERE` instead of `HAVING`
- Limit the use of `DISTINCT`

**🛠️ Use cases 🛠️**

- 

**🛑 Worst practices 🛑**

- 

Sources:

[SQL Query Optimization: 15 Techniques for Better Performance](https://www.datacamp.com/blog/sql-query-optimization)

[SQL Query Optimization: Techniques and Best Practices](https://www.snowflake.com/en/fundamentals/query-optimization/)

[SQL Query Optimizations - GeeksforGeeks](https://www.geeksforgeeks.org/sql/best-practices-for-sql-query-optimizations/)

[How Does Query Optimization Work?](https://www.macrometa.com/articles/how-does-query-optimization-work)

## **Pagination**

April 17, 2026 

**🔽 What? 🔽**

- 

**🔁 What does it do? 🔁**

- 

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- 

🤔 **How does it work?** 🤔

- 

**✍️ How to use it? ✍️**

- 

**👍 Advantages 👍**

- 

**👎 Disadvantages 👎**

- 

**↔️ Alternatives ↔️**

- 

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- 

**🛑 Worst practices 🛑**

- 

Sources:

### **Keyset Pagination**

April 17, 2026 

**🔽 What? 🔽**

- technique

**🔁 What does it do? 🔁**

- 

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- to **provide** approximate **constant time access** to subsequent pages **as a user scrolls**

🤔 **How does it work?** 🤔

- The database does**n’t** have to load the **entire result** set, **sort** it, and then **return** the specified limit from the given offset. Keyset pagination achieves this by leveraging an **index** to speed up access to data stored on disk and **avoids this overhead**.
- Keyset Pagination, offers an efficient way for navigating through **large datasets**. Instead of skipping a number of rows, it uses a **reference point (a key)** from the **last retrieved row** to **fetch** the **next set of records**.

**✍️ How to use it? ✍️**

- This approach can be implemented with data stored in a relational database like PostgreSQL
- Usage Example Id and Salary in a tuple
    
    Consider a table of employees with 100,000 rows where you want to display the employees sorted by `salary`. Because employees could have the same `salary`, we also need to leverage a unique key constraint to help with tie-breakers, which is `id` in this case.
    
    ```sql
    postgres=# CREATE TABLE employees (
      id SERIAL PRIMARY KEY,
      name TEXT NOT NULL,
      age INTEGER NOT NULL,
      salary NUMERIC
    );
    
    postgres=# WITH generated_series AS (
      SELECT generate_series(1, 100000, 1) AS num
    )
    INSERT INTO employees (id, name, age, salary)
    SELECT
      num AS id,
      'employee' || num AS name,
      floor((random() * 65) + 18)::INTEGER AS age,
      floor((random() * 200000) + 100000)::NUMERIC AS salary
    FROM generated_series;
    
    postgres=# CREATE INDEX employees_idx1 ON employees (salary, id);
    ```
    
    If we want to sort by `salary ASC, id ASC` and paginate through this table with page size 5, a `LIMIT + OFFSET` approach is as follows for the 2nd to last page of results:
    
    ```sql
    postgres=# EXPLAIN ANALYZE
    SELECT *
    FROM employees
    ORDER BY salary ASC, id ASC
    OFFSET 99990
    LIMIT 5;
                                                                      QUERY PLAN
    ----------------------------------------------------------------------------------------------------------------------------------------------
     Limit  (cost=2736.54..2736.68 rows=5 width=27) (actual time=66.071..66.076 rows=5 loops=1)
       ->  Index Scan using employees_idx1 on employees  (cost=0.42..2736.82 rows=100000 width=27) (actual time=0.043..61.158 rows=99995 loops=1)
     Planning Time: 0.195 ms
     Execution Time: 66.120 ms
    (4 rows)
    ```
    
    With keyset pagination, the query would look like so. The key filter predicate is the row tuple comparison on the key `(salary, id) > (299974, 3476)`, where we look for all rows that have a `salary` AND `id` greater than the supplied values. NOTE: This may not match your data if you use the above queries as row values are randomly chosen.
    
    ```sql
    postgres=# EXPLAIN ANALYZE
    SELECT *
    FROM employees
    WHERE (salary, id) > (299974, 3476)
    ORDER BY salary ASC, id ASC
    LIMIT 5;
                                                                QUERY PLAN
    -----------------------------------------------------------------------------------------------------------------------------------
     Limit  (cost=0.42..6.40 rows=5 width=27) (actual time=0.012..0.025 rows=5 loops=1)
       ->  Index Scan using employees_idx1 on employees  (cost=0.42..17.16 rows=14 width=27) (actual time=0.010..0.023 rows=5 loops=1)
             Index Cond: (ROW(salary, id) > ROW('299974'::numeric, 3476))
     Planning Time: 0.250 ms
     Execution Time: 0.049 ms
    (5 rows)
    ```
    
    The actual total cost is 2736.68 and execution time is 66.120 ms for LIMIT + OFFSET pagination. Keyset pagination drops those numbers to 6.40 and 0.049 ms, respectively. We observe that keyset pagination is best used for serving data sequentially from columns indexed for comparisons.
    
- ID usage example
    
    ```sql
    -- Fetch the first 100 users
    SELECT * FROM users WHERE id > 0 ORDER BY id ASC LIMIT 100;
    
    -- Assume the last id from the previous batch is 100
    -- Fetch the next 100 users
    SELECT * FROM users WHERE id > 100 ORDER BY id ASC LIMIT 100;
    
    -- If the last id is 200
    SELECT * FROM users WHERE id > 200 ORDER BY id ASC LIMIT 100;
    
    [users table ordered by id]
    | id  | name     | ... |
    |-----|----------|-----|
    | 1   | Alice    |     |
    | 2   | Bob      |     |
    | ... | ...      |     |
    | 100 | Hannah   |     |
    | 101 | Ian      |     |
    | 102 | Jane     |     |
    | ... | ...      |     |
    | 1000| Zach     |     |
    
    Pagination using Keyset:
    
    Page 1 (id > 0, LIMIT 100):
    Fetches rows with id 1 to 100.
    
    Page 2 (id > 100, LIMIT 100):
    Fetches rows with id 101 to 200.
    
    Page 3 (id > 200, LIMIT 100):
    Fetches rows with id 201 to 300.
    
    ... and so on until all users are processed.
    ```
    

**👍 Advantages 👍**

- 

**👎 Disadvantages 👎**

- 

**↔️ Alternatives ↔️**

- It is more complex to implement than a simple approach like **LIMIT + OFFSET** pagination but **minimizes slower query times** as you scroll many pages into a result set.

**✅ Best practices ✅**

- To get the **first or last page** of results, you can leverage arbitrarily large or small numbers or strings, which can be constants in your application or database functions.
    
    For instance, to get the first page in our example (`salary ASC, id ASC`):
    
    ```sql
    SELECT *
    FROM employees
    WHERE (salary, id) > (-999999999, -999999999)
    ORDER BY salary ASC, id ASC
    LIMIT 5;
    ```
    
    To get the last page in our example (`salary ASC, id ASC`):
    
    ```sql
    WITH intermediate AS (
      SELECT *
      FROM employees
      WHERE (salary, id) < (999999999, 999999999)
      ORDER BY salary DESC, id DESC
      LIMIT 5
    )
    SELECT *
    FROM intermediate
    ORDER BY salary ASC, id ASC;
    ```
    
    If the sort order for `salary` is changed to `DESC`, the above 2 queries become like as follows. First, for the first page in our example (`salary DESC, id DESC`):
    
    ```sql
    SELECT *
    FROM employees
    WHERE (salary, id) < (999999999, 999999999)
    ORDER BY salary DESC, id DESC
    LIMIT 5;
    ```
    
    To get the last page in our example (`salary DESC, id DESC`):
    
    ```sql
    WITH intermediate AS (
      SELECT *
      FROM employees
      WHERE (salary, id) > (-999999999, -999999999)
      ORDER BY salary ASC, id ASC
      LIMIT 5
    )
    SELECT *
    FROM intermediate
    ORDER BY salary DESC, id DESC;
    ```
    

**🛠️ Use cases 🛠️**

- 

**🛑 Worst practices 🛑**

- 

Sources:

[Optimizing Pagination in PostgreSQL: OFFSET/LIMIT vs. Keyset](https://medium.com/@scion01/optimizing-pagination-in-postgresql-offset-limit-vs-keyset-12967d2ae3eb)

[Keyset pagination in PostgreSQL like a pro](https://www.andrewfisher.me/development/keyset-pagination/)

### **OFFSET-LIMIT Pagination**

April 17, 2026 

**🔽 What? 🔽**

- 

**🔁 What does it do? 🔁**

- 

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- The OFFSET/LIMIT method is a widely used approach for pagination in PostgreSQL due to its simplicity

🤔 **How does it work?** 🤔

- It allows you to skip a specified number of rows (OFFSET) and then return a set number of rows (LIMIT). This method is straightforward to implement, making it a common choice for paginating query results.

**✍️ How to use it? ✍️**

- Usage Example
    
    ```sql
    -- Fetch the first 100 users
    SELECT * FROM users ORDER BY id LIMIT 100 OFFSET 0;
    
    -- Fetch the next 100 users
    SELECT * FROM users ORDER BY id LIMIT 100 OFFSET 100;
    
    -- Fetch the subsequent 100 users
    SELECT * FROM users ORDER BY id LIMIT 100 OFFSET 200;
    
    [users table ordered by id]
    | id  | name     | ... |
    |-----|----------|-----|
    | 1   | Alice    |     |
    | 2   | Bob      |     |
    | ... | ...      |     |
    | 100 | Hannah   |     |
    | 101 | Ian      |     |
    | 102 | Jane     |     |
    | ... | ...      |     |
    | 1000| Zach     |     |
    
    Pagination using OFFSET/LIMIT:
    
    Page 1 (OFFSET 0, LIMIT 100):
    Fetches rows with id 1 to 100.
    
    Page 2 (OFFSET 100, LIMIT 100):
    Fetches rows with id 101 to 200.
    
    Page 3 (OFFSET 200, LIMIT 100):
    Fetches rows with id 201 to 300.
    
    ... and so on until all users are processed.
    ```
    
    While this is a simplistic way to read through all the records, as the number of records in the table increases, so will the offset value. The database then must scan and discard **more rows** before reaching the desired page, leading to **slower queries**. Wehn the database retrieves a large number of pages to access a specific result (by discarding preceding pages), this pattern can lead to a **noticeable spike in CPU usage** of the database instance.
    

**👍 Advantages 👍**

- 

**👎 Disadvantages 👎**

- 

**↔️ Alternatives ↔️**

- Keyset Pagination, offers an efficient alternative for navigating through large datasets. Instead of skipping a number of rows, it uses a reference point (a key) from the last retrieved row to fetch the next set of records.

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- 

**🛑 Worst practices 🛑**

- 

Sources:

[Optimizing Pagination in PostgreSQL: OFFSET/LIMIT vs. Keyset](https://medium.com/@scion01/optimizing-pagination-in-postgresql-offset-limit-vs-keyset-12967d2ae3eb)

## Caching

**🔽 What? 🔽**

- 

**🔁 What does it do? 🔁**

- 

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- 

🤔 **How does it work?** 🤔

- 

**✍️ How to use it? ✍️**

- 

**👍 Advantages 👍**

- 

**👎 Disadvantages 👎**

- 

**↔️ Alternatives ↔️**

- 

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- 

**🛑 Worst practices 🛑**

- 

Sources:

[What is Caching Strategies in DBMS? - GeeksforGeeks](https://www.geeksforgeeks.org/dbms/what-is-caching-strategies-in-dbms/)

[Database caching: Overview, types, strategies and their benefits.](https://www.prisma.io/dataguide/managing-databases/introduction-database-caching)

[Database Caching Strategies](https://medium.com/@sesmiat/database-caching-strategies-f5e40c3c9b74)

[What is Database Caching and How to Use](https://www.pingcap.com/article/what-is-database-caching-and-how-to-use/)

## Data Archiving

**🔽 What? 🔽**

- a critical component of **effective data management**
- the process of moving and **storing data** that is **no longer actively used** or needed for **everyday operations** to a separate storage location for **long-term retention**.

**🔁 What does it do? 🔁**

- 

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- **efficient** storage, **retrieval**, and **long-term preservation**.
- to **free up space** in the primary storage systems, such as databases or file servers, while ensuring that the **archived data remains accessible** for compliance, legal, or historical purposes.
- essential for maintaining optimal database performance, managing costs, and ensuring scalability.

🤔 **How does it work?** 🤔

- 

**✍️ How to use it? ✍️**

- **Steps** for Creating a **Data Archiving Strategy**
    1. Define Archiving **Goals** and **Requirements:** Clearly outline the **objectives** of your data archiving strategy. Determine what **types of data** need to be archived and for **how long**. Identify **legal and regulatory requirements** that govern data retention in your industry. Consider the **specific needs** of **your organization**, such as compliance, business continuity, or historical analysis.
    2. **Categorize Data** for Archiving**:** Classify data based on its **importance, sensitivity**, and **relevance**. Prioritize data that requires **long-term retention** or may be **subject to compliance regulations**. Establish criteria for determining **when data should be archived**, such as **data age, access frequency, or business relevance**.
    3. Choose Archiving **Solutions** and Technologies**:** Select appropriate archiving solutions based on your organization's needs and the nature of the data. Consider factors such as **data volume, access speed requirements, and budget constraints**. Evaluate different storage options, including **on-premises, cloud-based, or hybrid** solutions. Implement data compression and deduplication techniques to optimize storage space.
    4. Implement **Access Controls** and **Security** Measures**:** Define and enforce access controls to ensure that **only authorized personnel can retrieve archived data**. Implement **encryption mechanisms** to safeguard archived data, both during storage and retrieval. Regularly **audit** and **update security measures** to address potential vulnerabilities and comply with data protection standards.
    5. Establish a Data Retrieval and **Monitoring Plan:** Develop a retrieval plan that outlines how archived data **can be accessed when needed**. Consider factors such as **retrieval speed and accessibility**. Implement **monitoring** and **auditing** processes to track archived data, ensuring its integrity and compliance with retention policies. Periodically test the retrieval process to verify the accessibility and usability of archived data.
- Common Methods to Archive Data
    - **Tape Archiving**: Tape backup has been a reliable method for archiving data for **many years**. It involves storing data on magnetic tape cartridges, providing an **offline and secure option for long-term retention**. This method is often used for creating backups that can be stored in **offsite locations**, ensuring data resilience in the event of disasters or data loss.
    - **Multi Cloud Storage**: Cloud storage services, such as **Amazon S3 Glacier, Google Cloud Storage Nearline, or Azure Archive Storage**, offer scalable and **cost-effective solutions** for archiving large volumes of data. Cloud storage provides the advantage of **remote accessibility**, eliminating the need for **on-premises infrastructure** while offering **flexibility** and **scalability** to adapt to changing storage requirements.
    - **On-Premises** Storage Systems: Implementing on-premises storage solutions like **Network Attached Storage (NAS)** or **Storage Area Network (SAN)** gives organizations **control** over their archived data. This allows for tailoring storage to **specific performance** and **security needs**, making it a suitable choice for organizations with stringent regulatory requirements or specific performance considerations.
    - **Hierarchical Storage Management (HSM):** HSM systems automate the migration of data between different storage tiers based on usage patterns. Frequently accessed data is stored on high-performance storage, while less frequently accessed data is moved to lower-cost, slower storage. This approach optimizes storage resources and ensures that data is stored on the most suitable infrastructure for its lifecycle.
    - **Database Archiving**: For structured data in databases, archiving involves moving historical or less frequently accessed records to a **separate archival database**. This helps keep the primary database optimized for current and frequently accessed data, improving overall database performance.
    - **Data Encryption**: Encrypting archived data adds an additional layer of security, **protecting sensitive information** from **unauthorized access**. It's essential to ensure that encryption keys are **securely managed** and that the chosen encryption method aligns **with industry best practices** to maintain the confidentiality and integrity of archived data.
    - **Document Management** Systems: Implementing document management systems is beneficial for efficiently organizing and archiving documents. These systems often provide **version control, access controls, and metadata tagging**, facilitating effective retrieval and management of documents throughout their lifecycle. They are particularly useful in maintaining document integrity and ensuring compliance with regulatory requirements.
- Archiving Strategies
    - **Partitioning** for Archiving
        - **Time-Based** Partitioning
            
            ```sql
            CREATE TABLE orders (
                order_id INT PRIMARY KEY,
                customer_id INT,
                order_date DATE
            )
            PARTITION BY RANGE (YEAR(order_date)) (
                PARTITION p2020 VALUES LESS THAN (2021),
                PARTITION p2021 VALUES LESS THAN (2022),
                PARTITION p2022 VALUES LESS THAN (2023)
            );
            ```
            
        - **Range** Partitioning
            
            ```sql
            CREATE TABLE customers (
                customer_id INT PRIMARY KEY,
                name VARCHAR(100),
                email VARCHAR(100)
            )
            PARTITION BY RANGE (customer_id) (
                PARTITION p1 VALUES LESS THAN (10000),
                PARTITION p2 VALUES LESS THAN (20000)
            );
            ```
            
        - **Hash** Partitioning
            
            ```sql
            CREATE TABLE account_transactions (
                transaction_id INT PRIMARY KEY,
                account_number INT,
                amount DECIMAL(10,2)
            )
            PARTITION BY HASH (account_number)
            PARTITIONS 4;
            ```
            
    - **Separate** Tables for Archiving. Archiving via separate tables involves moving historical data to dedicated tables, isolating it from active datasets.
        - `INSERT INTO`
            
            ```sql
            -- Active accounts table
            CREATE TABLE active_accounts (
                account_id INT PRIMARY KEY,
                customer_id INT,
                account_status VARCHAR(50)
            );
            
            -- Archived accounts table
            CREATE TABLE archived_accounts (
                account_id INT PRIMARY KEY,
                customer_id INT,
                account_status VARCHAR(50)
            );
            
            -- Move inactive accounts to archived table
            INSERT INTO archived_accounts SELECT * FROM active_accounts WHERE account_status = 'inactive';
            DELETE FROM active_accounts WHERE account_status = 'inactive';
            ```
            
        - Using a `DELETE` trigger to archive data
            
            a `DELETE` trigger is used to **automatically move** data from the orders table to an archived_orders table when an order is considered archived.
            
            ```sql
            -- Active orders table
            CREATE TABLE orders (
                order_id INT PRIMARY KEY,
                customer_id INT,
                order_status VARCHAR(50),
                order_date TIMESTAMP
            );
            
            -- Archived orders table
            CREATE TABLE archived_orders (
                order_id INT PRIMARY KEY,
                customer_id INT,
                order_status VARCHAR(50),
                order_date TIMESTAMP,
                archived_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            -- Trigger to archive and delete orders that are older than 5 years
            DELIMITER //
            CREATE TRIGGER move_to_archive_before_delete
            BEFORE DELETE ON orders
            FOR EACH ROW
            BEGIN
                IF OLD.order_date < NOW() - INTERVAL 5 YEAR THEN
                    -- Move the record to archived_orders before deletion
                    INSERT INTO archived_orders (order_id, customer_id, order_status, order_date)
                    VALUES (OLD.order_id, OLD.customer_id, OLD.order_status, OLD.order_date);
                END IF;
            END;
            //
            DELIMITER ;
            
            -- Delete the old order record from the orders table
            DELETE FROM orders WHERE order_date < NOW() - INTERVAL 5 YEAR;
            ```
            
        - Using `ON DELETE` action in foreign key constraints
            
            In this example, the `ON DELETE CASCADE` action is used with a foreign key constraint to automatically archive data when a related record is deleted. This ensures that whenever a record in the orders table is **deleted**, corresponding records in the order_items table are also **archived automatically**.
            
            ```sql
            -- Active orders and order_items tables
            CREATE TABLE orders (
                order_id INT PRIMARY KEY,
                customer_id INT,
                order_status VARCHAR(50),
                order_date TIMESTAMP
            );
            
            CREATE TABLE order_items (
                item_id INT PRIMARY KEY,
                order_id INT,
                product_id INT,
                quantity INT,
                FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE
            );
            
            -- Archived order_items table
            CREATE TABLE archived_order_items (
                item_id INT PRIMARY KEY,
                order_id INT,
                product_id INT,
                quantity INT,
                archived_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            -- Trigger to move deleted order_items to archived table
            DELIMITER //
            CREATE TRIGGER archive_order_items_before_delete
            BEFORE DELETE ON order_items
            FOR EACH ROW
            BEGIN
                -- Move deleted order items to archived table before deletion
                INSERT INTO archived_order_items (item_id, order_id, product_id, quantity)
                VALUES (OLD.item_id, OLD.order_id, OLD.product_id, OLD.quantity);
            END;
            //
            DELIMITER ;
            
            -- Delete an order and corresponding items are automatically archived
            DELETE FROM orders WHERE order_id = 101;
            
            ```
            
    - Archive **Flag with Index** for Data Separation
        
        Using an archive_flag **column** is a practical approach to managing **active and archived records** in a single table. By incorporating this flag into **composite indexes**, efficient data separation is achieved **without requiring schema partitioning**. Adding an archive_flag column enables streamlined filtering of data based on archival status. Composite indexes, such as one on the primary key and the archive_flag, ensure quick access to **both active and archived records**.
        
        ```sql
        CREATE TABLE logs (
        	log_id INT PRIMARY KEY, 
        	message TEXT, 
        	timestamp TIMESTAMP, 
        	archive_flag BOOLEAN DEFAULT FALSE 
        	); 
        
        CREATE INDEX idx_logs_primary_archive_flag ON logs (log_id, archive_flag);
        ```
        
        Query active logs:
        
        ```sql
        SELECT COUNT(*) FROM logs WHERE archive_flag = 0;
        ```
        
        Query archived logs:
        
        ```sql
        SELECT COUNT(*) FROM logs WHERE archive_flag = 1;
        ```
        
    - 

**👍 Advantages 👍**

- 

**👎 Disadvantages 👎**

- 

**↔️ Alternatives ↔️**

- 

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- 

**🛑 Worst practices 🛑**

- 

Sources:

[Data Archiving Strategy - GeeksforGeeks](https://www.geeksforgeeks.org/data-engineering/data-archiving-strategy/)

[Optimizing Data Archiving Strategies: A Comprehensive Guide to Smarter Database Management](https://medium.com/pipedrive-engineering/optimizing-data-archiving-strategies-a-comprehensive-guide-to-smarter-database-management-7f15d8fd5c52)

# CQRS

April 6, 2026 [Знати CQRS](https://www.notion.so/CQRS-331745f820dc806a8bc2d46a5ee7a4ec?pvs=21) 

**🔽 What? 🔽**

- **Command Query Responsibility Segregation**
- pattern
- design approach

**🔁 What does it do? 🔁**

- separates a data store's read and write operations into distinct models.

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- when you build **complex data models** to validate and fulfil your business logic when data manipulation happens.

🤔 **How does it work?** 🤔

- you can use a **different model** to **update** information than the model you use to **read** information.
- The core principle is to use **separate interfaces** for **querying data (reads)** and **commanding data (writes)**. The **command model** handles **create, update, and delete** operations, focusing on data integrity and business logic. The **query model** handles **data retrieval** and is optimized for fast reads.
- Implementing CQRS on **multiple databases** involves using separate databases for read and write operations. This approach is suitable for applications that require **high scalability** and can **tolerate eventual consistency**. The **command model** might use a **relational database** for **transactional integrity**, while the **query model** might use a **NoSQL database** for **scalability and flexibility**. This separation allows each database to be selected and configured based on its specific **workload requirements**, addressing the **limitations of a single database** handling diverse operations. **Data synchronization** between databases is typically **asynchronous**.
- CQRS and **Event Sourcing**
    
    Event Sourcing is often used in **conjunction with CQRS**. The command model **stores events in an event store**, while the **query model** builds read models by **replaying events** from the event store. **Eventual consistency** is inherent in this approach.
    

**✍️ How to use it? ✍️**

- Comparison with a traditional model and example:
    
    ### **Traditional Model:**
    
    - When a user **creates** a post, the system **writes** to the "**Posts**" table.
    - When a user **views** a post, the system **reads** from the **same "Posts" table.**
    - If the site becomes very popular, both read and write operations compete for resources, potentially **slowing down the system**.
    
    ### **CQRS Model:**
    
    - **Write Model:** The "Posts" table remains **optimized for writes**. It ensures data consistency when creating or updating posts.
    - **Read Model:** A separate "**PublishedPostsView**" can be created. This view can use the "Posts" table to **pre-calculate summaries** or format the content for display. When a user views a post, the system reads from this optimized view. This view might not contain all the details of the original post, but only the data needed for display.
    - **Another read model** might be created for **search functionality**, containing **indexed terms** extracted from the post content.
    - When a new post is created, the write model updates the "Posts" table and then **asynchronously updates the "PublishedPostsView"** and the **search index**.
- [Code example (FastAPI, SQLAlchemy)](https://wawaziphil.medium.com/building-a-python-api-using-cqrs-a-simple-guide-3d584b6ead34)
- [Another Python code example](https://www.linkedin.com/pulse/cqrs-python-how-separate-read-write-models-gains-svitlana-sumets-ujiqf/)

**👍 Advantages 👍**

- Optimized **Performance**: Read and write operations can be **tuned separately**, improving overall performance.
- Independent **Scaling**: Read and write databases can be **scaled independently** based on their specific **load requirements**.
- Increased **Flexibility:** Each model can use **different database technologies** and data models, providing flexibility and **adaptability**.
- Improved **Maintainability:** Separating concerns makes the codebase easier to understand and maintain.
- Clear **Responsibility**: Distinguishing between reads and writes simplifies code and improves **maintainability**
- **Event Sourcing**: Commands can emit events, making it easy to track changes in the system.

**👎 Disadvantages 👎**

- **Eventual Consistency:** Asynchronous synchronization can lead to eventual consistency, which may not be suitable for all applications.
- **Data Duplication:** Read models often involve data duplication, which can **increase storage requirements**.
- **Infrastructure Overhead:** **Multiple databases** and **messaging systems** may increase infrastructure **costs**.
- **Synchronization Complexity:** Ensuring data consistency between the read and write sides can be difficult.

**↔️ Alternatives ↔️**

- In traditional **CRUD** application architectures a single data model is used for both reading and writing data. As applications scale, this approach leads to **performance bottlenecks** and **complexity**.

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- 

**🛑 Worst practices 🛑**

- 

Sources:

[bliki: CQRS](https://martinfowler.com/bliki/CQRS.html)

[What is Command Query Responsibility Segregation (CQRS)?](https://newsletter.scalablethread.com/p/what-is-command-query-responsibility)

# Materialized View

**🔽 What? 🔽**

- a sorted, projected, and materialized view or SPM view
- **view** whose columns have been sorted, projected, and materialized (that is, stored physically in a unique table).
- Think of them as **cached query results** that you can query like a regular table, but without running the expensive underlying query every time.

**🔁 What does it do? 🔁**

- A materialized view **stores the results of the query**.

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- improves **query performance** without rewriting applications
- when **data results** need to be obtained **not too often**

🤔 **How does it work?** 🤔

- It **reduces** the amount of **data** that must be **transferred from** the **disk** during scans.
- Because its data is **sorted**, the resulting zone map for `ORDER BY` columns is more efficient than it otherwise would be.
- Because its data is **sorted** and it has a zone map, a query that targets only a **few records** can retrieve the block locations of the records in the base table more quickly than by other means.
- The query planner/optimizer **automatically uses a materialized view** when doing so is faster than using the corresponding base table.
- Materialized Views are **refreshed** or rematerialized when prompted or scheduled.

**✍️ How to use it? ✍️**

- Create
    
    ```sql
    CREATE MATERIALIZED VIEW customers_mview AS 
    SELECT customer_name, customer_id 
    FROM customers 
    ORDER BY customer_id;
    ```
    
    - You can only specify **one base table** in the `FROM` clause.
    - You cannot use the `WHERE` clause.
    - The **columns in the projection** list must be **columns in the base table** and no expressions (aggregates, mathematical operators, casting, `DISTINCT` operator, and other expressions) are allowed.
    - You must specify **at least one column** in the projection list.
    - The columns in the optional `ORDER BY` clause must be one or more columns in the projection list. If you do **not specify ORDER BY**, the materialized view retains the **same** sort order **as the base table**.
    - You cannot specify NULLS LAST or DESC in the ORDER BY expression.
    - You cannot specify an external, temporary, system, or a clustered base table (CBT) as a base table for the view.
- Alter
    
    You cannot do **direct record inserts, updates, or truncates** on **materialized views** or their associated materialized tables.
    
    - If you **delete records** in the **base table**, either as part of a record update or record delete operation, the system propagates the change **to** all the appropriate **materialized records** in the **unsuspended SPM views**.
    - If you truncate records in the base table, the system truncates the materialized tables for the associated SPM views.
    
    You can use SQL to alter the materialize property of an SPM view, which can be `ACTIVE`, or `SUSPEND`. You can use `REFRESH` to change from the `SUSPEND` to the `ACTIVE` state.
    
    - Using the `SUSPEND` option marks a materialized view and its associated table as **not eligible** for use **in queries or transactions**. The system truncates the materialized table and redirects **all queries** against the materialized view **to the base table**.
        
        Use `SUSPEND` to **temporarily defer** updates to materialized tables, such as when you are running reclaims, restores, or loads.
        
    - Using the `REFRESH` option rematerializes the SPM view, which re-creates the materialized table from the base table. Although normally you use the `REFRESH` option on suspended materialized views, you can also use it on ordered unsuspended materialized views to sort the views again for better performance. You would also use the `REFRESH` option to update the materialized views after an insert to the base table.
    
    To change the properties of an SPM view, enter:
    
    ```sql
    ALTER VIEW customers_mview MATERIALIZE REFRESH;
    ```
    
- Refresh
    
    As well a materialzed view is not automatically refreshed when a base table updated, so wee need to refresh it 
    
    ```sql
    REFRESH MATERIALIZED VIEW mv_name;
    ```
    
- Drop
    
    ```sql
    DROP VIEW customers_mview;
    ```
    
    If you **drop** the **base table** from which a materialized view is derived, the system **drops the materialized table**, but **retains the view definition**, which reverts to a **regular view**. All subsequent accesses to the SPM view result in an error message.
    

**👍 Advantages 👍**

- 

**👎 Disadvantages 👎**

- 

**↔️ Alternatives ↔️**

- With a regular view (simple or complex), we can **simplify a query statement** or **restrict access to database** data by granting its usage to some specific users or tenants of the database. However, each time we access a regular view, it runs the relative query in the background. On the other hand, a materialized view **stores** data persistently on the main storage.

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- **Pre-process data**. Improve query performance by preparing aggregates, filters, joins, and clusters.
- **Dashboard acceleration**. Empower **BI tools** like Looker that frequently query the same aggregate metrics—for example, **daily** active users.
- Close to real-time **analytics on large streams**. Can provide faster responses on tables that receive high-velocity streaming data.
- **Historical summaries**: Data that doesn't need real-time accuracy
- **Cost management**. Reduce the cost of repetitive, expensive queries over large datasets.

**🛑 Worst practices 🛑**

- 

Sources:

[Materialized View in SQL | Faster SQL Queries using Materialized Views](https://www.youtube.com/watch?v=WzkBZ0byoYE)

[Materialized Views | SQL](https://www.youtube.com/watch?v=sZyt9a1kjzI)

[Introduction to materialized views  |  BigQuery  |  Google Cloud Documentation](https://docs.cloud.google.com/bigquery/docs/materialized-views-intro)

[Databases: Simple vs. Complex vs. Materialized Views Baeldung on SQL](https://www.baeldung.com/sql/databases-views-simple-complex-materialized#2-complex-view)

[Materialized views](https://www.ibm.com/docs/en/netezza?topic=wso-materialized-views)