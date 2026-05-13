# Machine Learning

Skills: Machine learning
Start Date: March 24, 2026

# Terms

1. 

# Choosing a model

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

![image.png](Machine%20Learning/image.png)

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

# Unsupervised Learning

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

## Clustering

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

# Kmeans Clustering

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

[Machine Learning Tutorial Python - 13:  K Means Clustering Algorithm](https://www.youtube.com/watch?v=EItlUEPCIzM)

### Elbow Method

**🔽 What? 🔽**

- 

**🔁 What does it do? 🔁**

- 

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- to determine which number of k in Kmeans Cluster we need.

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

[Machine Learning Tutorial Python - 13:  K Means Clustering Algorithm](https://www.youtube.com/watch?v=EItlUEPCIzM)

# Data Leakage

**🔽 What? 🔽**

- term

**🔁 What does it do? 🔁**

- refers to a situation where information that should **not be accessible** to the **ML model** during **training** becomes **part of the training dataset**.

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- This misleading information artificially **impacts** the **model’s performance** metrics during **training and evaluation** but **causes it to fail** when exposed to **new, unseen data**.

🤔 **How does it work?** 🤔

- **Types** of Data Leakage :
    - **Target** Leakage. Target leakage occurs when information from the **target variable** is accidentally **included as a feature** during training, leading to **unrealistically high performance**.
        - Example :
            
            Let’s take a machine learning model predicting whether a **bank customer will repay their loan**, including a feature like “**repayment_status**” (which shows whether the customer **has already paid**) would cause **data leakage**. This is because the repayment status is linked to the outcome we are trying to predict, so the **model knows the answer before making the prediction**.
            
        - When It Occurs:
        When the **model has access** to **features** that are **directly related to the outcome** (e.g., including future repayment status in a loan prediction model).
    - **Feature** Leakage. Feature leakage, on the other hand, happens when a **feature** indirectly **contains information** too **closely related to** the **target**, making the model appear more accurate during training but **not generalizable** in real-world scenarios.
        - Example:
        Consider a machine learning model to predict whether a **product** will **be** **sold within** a **certain time frame**. One of the features in your dataset is “**total sales in last 30 days**,” which records the number of items sold in the previous 30 days. This feature is **clearly influenced by the target** variable, as a product with higher sales in the last 30 days is more likely to be sold in the next period. If this feature is included in the model, it is considered **feature leakage**, as it directly provides information that would not be available when making future predictions.
        - When it Occurs:
        When feature engineering introduces variables that contain **hidden dependencies** on the target variable, they can **unintentionally “leak” the answer**.
    - Train Test **Contamination**
        - Example :
        Consider building a model to predict whether a customer will churn based on their **account usage data**. We accidentally **include data from the test set** when **preprocessing the training data**, such as **calculating the mean usage**, imputing or **normalizing** the **data** using **both training** and **test** datasets **together**. This results in the model having prior knowledge of the test data during training.
        - When it Occurs :
        Train-test contamination happens when information from the test set “leaks” into the training set, either **during preprocessing, feature selection**, or any stage where the **model** can **unintentionally access** the **test** data **before** the **evaluation phase**.
    - Temporal **Cut-off**
        - Example :
        Consider **predicting stock prices** based on **historical data**, where you use **data up to the current date** for **both training and testing**. If we include **future stock prices** (e.g., data from the period after your model’s training phase) in the **training set**, the model may **inadvertently** learn patterns **from the future**, giving it an **unfair advantage** in predicting future stock prices.
        - When it Occurs :
        Occurs when **future data,** which **should not be available** during the **training phase,** is **used by the model**. This occurs when there’s **no proper separation** between the **training** and **test** datasets in **terms of time**, such as using **future information for training** a model that is supposed to make predictions based on historical data.
        - Impact :
        This leakage results in the model having an **unrealistic advantage** because it can **see the future** while training.

**✍️ How to use it? ✍️**

- **Preventing Data Leakage.** Some best practices to **avoid data leakage**:
    1. **Isolate** the **Test** Set **Early.** 
        
        Always set aside the test set before performing any data preprocessing or feature engineering. Treat the test set as completely unseen data.
        
    2. Use **Cross-Validation**
        
        Implement **cross-validation** to ensure the model is evaluated on data it hasn’t seen during training. Ensure the folds are correctly separated.
        
    3. **Time-Aware Splitting** 
        
        For time series data, better **split** the dataset **chronologically** to prevent future data from influencing past predictions.
        
        **Chronological Split:** Instead of **randomly splitting** the **data** into **training and testing sets** (as is common with non-time series data), you should ensure that the training data consists **only of past data** up to a certain point in time, while the **testing data is** from a **later period**. This way, the model can only use information that would have been available up to the point it’s making predictions for.
        
    4. **Feature Engineering on Training Data Only**
        - Perform data transformations (e.g., scaling, encoding, imputing) using **only the training data**.
        - Apply these transformations to the **test** data **without recalculating statistics**.
    5. **Collaborate Across Teams.**
        
        Involve domain experts to validate that features do not inadvertently leak target information.
        

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

[Data Leakage in Machine Leaning](https://medium.com/@speaktoharisudhan/data-leakage-in-machine-leaning-c382b65f4c09)

# Loss function

**🔽 What? 🔽**

- 

**🔁 What does it do? 🔁**

- 

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- 

🤔 **How does it work?** 🤔

- 

**✍️ How to use it? ✍️**

- Popular Loss functions
    
    ![image.png](Machine%20Learning/image%201.png)
    
- **Clustering Metrics**
    
    In unsupervised learning tasks such as clustering, the goal is to group similar data points together. Evaluating clustering performance is often more challenging than supervised learning since there is no explicit ground truth. However, clustering metrics provide a way to measure how well the model is grouping similar data points.
    
    ### **1. Silhouette Score**
    
    [**Silhouette Score**](https://www.geeksforgeeks.org/machine-learning/what-is-silhouette-score/) evaluates how well a data point fits within its assigned cluster considering how close it is to points in its own cluster (cohesion) and how far it is from points in other clusters (separation). A higher silhouette score (close to +1) shows well-clustered data while a score near -1 suggests that the data point is in the wrong cluster.
    
    Formula:
    
    > *Silhouette Score=b−amax⁡(a,b)Silhouette Score=max(a,b)b−a*
    > 
    
    Where:
    
    - a = Average distance between a sample and all other points in the same cluster
    - b = Average distance between a sample and all points in the nearest cluster
    
    ### **2. Davies-Bouldin Index**
    
    [**Davies-Bouldin Index**](https://www.geeksforgeeks.org/machine-learning/davies-bouldin-index/) measures the average similarity between each cluster and its most similar cluster. A lower Davies-Bouldin index shows better clustering as it suggests the clusters are well-separated and compact. The goal is to minimize the Davies-Bouldin index to achieve optimal clustering.
    
    Formula:
    
    > *Davies-Bouldin Index=1N∑i=1Nmax⁡i≠j(σi+σjd(ci,cj))Davies-Bouldin Index=N1∑i=1Nmaxi=j(d(ci,cj)σi+σj)*
    > 
    
    Where:
    
    - σi*σi* = Average distance of points in cluster i from the cluster centroid
    - d(ci,cj)*d*(*ci*,*cj*) = Distance between centroids of clusters i and j
    
    By mastering the appropriate evaluation metrics, we upgrade ourselves to fine-tune machine learning models which helps in ensuring they meet the needs of diverse applications and deliver optimal performance.
    

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

[Evaluation Metrics in Machine Learning - GeeksforGeeks](https://www.geeksforgeeks.org/machine-learning/metrics-for-machine-learning-model/)

[All Machine Learning Beginner Mistakes explained in 17 Min](https://www.youtube.com/watch?v=oMc9StPVzOU)

# Model Evaluation

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

## Regression Evaluation Metrics

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

### R-Squared

**🔽 What? 🔽**

- 

**🔁 What does it do? 🔁**

- 

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- 

🤔 **How does it work?** 🤔

- 

**✍️ How to use it? ✍️**

- Higher R2 is better
- Additionally, a higher R-squared value does not always equate to better predictions – as a rule of thumb, values **over 0.8** should be treated with **caution**.

**👍 Advantages 👍**

- 

**👎 Disadvantages 👎**

- One of the main drawbacks of R-squared is that it **assumes** that **all variables in the model** are **independent**, which is not always the case.
- the metric also has **trouble** detecting **non-linear relationships** and can give misleading results when working **with smaller datasets**.

**↔️ Alternatives ↔️**

- 

**✅ Best practices ✅**

- 

**🛠️ Use cases 🛠️**

- 

**🛑 Worst practices 🛑**

- 

Sources:

[R Squared: Understanding the Coefficient of Determination](https://arize.com/blog-course/r-squared-understanding-the-coefficient-of-determination/)

[Class3.  Supervised Learning](https://www.notion.so/Class3-Supervised-Learning-1a8745f820dc805f8c61e20cb4c60617?pvs=21) 

# Data Transformation

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

## Categorical Features Encoding

**🔽 What? 🔽**

- 

**🔁 What does it do? 🔁**

- 

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- 

🤔 **How does it work?** 🤔

- 

**✍️ How to use it? ✍️**

- Label Encoding - for ordinal variables.
- One-Hot Encoding - for nominal (non-ordinal types) low cardinality features. Code example
    
    ```python
    df = df.join(pd.get_dummies(df['categorical_variable_name'], dtype='int32', prefix='categorical_variable_name'))
    ```
    
- Binary encoding is better when we have many features. Code Example:
    
    ```python
    import category_encoders as ce
    
    binary_encoder = ce.BinaryEncoder()
    binary_encoded = binary_encoder.fit_transform(df[['categorical_variable_name']])
    
    df = pd.concat([df, binary_encoded], axis=1)
    ```
    
    ![image.png](Machine%20Learning/image%202.png)
    
    ![image.png](Machine%20Learning/image%203.png)
    

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

[Feature Encoding 101: Prepare Data For Machine Learning](https://www.youtube.com/watch?v=kGemHLOEF3w)

# Hyperparameters Tuning

**🔽 What? 🔽**

- 

**🔁 What does it do? 🔁**

- 

**🤷‍♂️ Why do we use it? 🤷‍♂️**

- 

🤔 **How does it work?** 🤔

- 

**✍️ How to use it? ✍️**

- We may use Optuna to use ranges for hyperparameters tuning.

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

[Hyperparameter Tuning Tips that 99% of Data Scientists Overlook](https://www.youtube.com/watch?v=D9xPjkOwpNk)