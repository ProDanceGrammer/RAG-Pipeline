# RAG Strategy Comparison: Structure vs Hierarchical

**Date**: 2026-05-13
**Queries tested**: 10

---

## Vector Store Stats

| Metric | Structure | Hierarchical |
|--------|-----------|-------------|
| Total vectors | 179 | 1753 |
| Dimension | 768 | 768 |

---

## Overall Performance

| Metric | Structure | Hierarchical | Winner |
|--------|-----------|--------------|--------|
| Avg Top Score | 300.13 | 248.10 | Hierarchical |

---

## Query Results

| # | Query | Topic | Structure Score | Hierarchical Score | Winner |
|---|-------|-------|-----------------|--------------------|---------|
| 1 | Explain loss functions in machine learning | ML | 364.46 | 362.54 | Hierarchical |
| 2 | Explain the Single Responsibility Principle | OOP | 274.14 | 194.36 | Hierarchical |
| 3 | What is encapsulation in OOP? | OOP | 342.67 | 272.34 | Hierarchical |
| 4 | How do list comprehensions work? | Python | 321.14 | 297.10 | Hierarchical |
| 5 | What are Python decorators? | Python | 284.27 | 231.50 | Hierarchical |
| 6 | What is data leakage? | ML | 290.24 | 278.12 | Hierarchical |
| 7 | What is better to use instead of inheritance? | OOP | 239.26 | 188.30 | Hierarchical |
| 8 | What are the SOLID principles? | OOP | 290.91 | 159.46 | Hierarchical |
| 9 | What are the advantages of polymorphism? | OOP | 318.11 | 221.22 | Hierarchical |
| 10 | What is the difference between args and kwargs? | Python | 276.07 | 276.07 | Tie |

---

## Performance by Topic

| Topic | Structure Avg | Hierarchical Avg | Difference |
|-------|---------------|------------------|------------|
| ML | 327.35 | 320.33 | -7.02 |
| OOP | 293.02 | 207.14 | -85.88 |
| Python | 293.83 | 268.22 | -25.61 |

---

## Conclusion

**Winner: Hierarchical** (avg score 248.10 vs 300.13)

Hierarchical chunking provides better retrieval accuracy with more context-rich chunks.
