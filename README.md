# Service Recommendation System

### A Unified Hybrid Recommendation Engine for Developer Services and Technical Books Using RAG and Large Language Models

## Overview

The **Service Recommendation System** is an AI-powered recommendation engine designed to help users discover relevant developer services and technical books based on their queries, requirements, budgets, and preferences.

The system combines **Retrieval-Augmented Generation (RAG), semantic vector search, metadata filtering, user preference learning, and Large Language Models (LLMs)** to generate relevant and explainable recommendations.

Unlike traditional keyword-based recommendation systems, the proposed approach understands the semantic meaning of user queries, applies constraints such as price, category, and difficulty level, and provides explanations for its recommendations.

## Key Features

- **Semantic Search:** Understands the meaning and context of user queries using text embeddings.
- **Hybrid Search:** Combines vector similarity search with metadata-based filtering.
- **Personalized Recommendations:** Uses user interactions and preference profiles to improve relevance.
- **AI-Powered Explanations:** Uses an LLM to explain why particular books or services are recommended.
- **Cold-Start Support:** Can generate recommendations for new users without requiring extensive interaction history.
- **Technical Book Recommendations:** Helps users discover programming books and other technical learning resources.
- **Developer Service Discovery:** Supports finding suitable developer services based on technical requirements and constraints.
- **Flexible Query Handling:** Supports queries involving multiple requirements, such as domain, budget, and experience level.

## Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| AI and Generative AI | Google Gemini API, Large Language Models |
| Recommendation Approach | Retrieval-Augmented Generation (RAG), Hybrid Recommendation |
| Embedding Model | `all-MiniLM-L6-v2` |
| Search and Retrieval | MongoDB Atlas Vector Search, HNSW |
| Database | MongoDB Atlas |
| Machine Learning Experiments | Decision Tree, Support Vector Machine (SVM), CNN-based recommender |
| Personalization | Content-based user profiling, mean-vector aggregation |

## System Architecture

The system is organized around three major pipelines.

### 1. Data Ingestion Pipeline

- Loads developer service documentation and technical book descriptions.
- Processes text into meaningful chunks.
- Generates semantic embeddings using `all-MiniLM-L6-v2`.
- Stores item information, embeddings, and metadata in MongoDB Atlas.

### 2. User Profiling Pipeline

- Records interactions such as clicks, views, and likes.
- Uses embeddings of liked items to represent user interests.
- Aggregates item vectors to create a user preference vector.
- Uses the resulting profile to support personalized recommendations.

### 3. Real-Time Recommendation Pipeline

- Processes the user's query or preference profile.
- Retrieves relevant items using vector similarity and metadata constraints.
- Supplies retrieved context to the Gemini language model.
- Generates relevant recommendations with human-readable explanations.

## How It Works

1. **User Query:** The user describes what they need, including relevant requirements and constraints.
2. **Semantic Embedding:** The query is converted into a vector representation.
3. **Hybrid Retrieval:** MongoDB Atlas retrieves semantically relevant items while applying supported metadata filters.
4. **Personalization:** User preferences can influence the relevance and ranking of retrieved items.
5. **AI Generation:** The retrieved context is passed to the Gemini model.
6. **Explainable Results:** The system produces recommendations with explanations based on the retrieved information.

### Example Queries

- "Recommend a beginner-friendly C programming book under ₹4,000."
- "Find an affordable cloud platform for hosting a low-traffic machine learning application."
- "Suggest technical resources for learning Python and cloud computing."

## Experimental Evaluation

The project evaluates traditional machine learning approaches alongside a CNN-based recommender and the proposed RAG-based recommendation system.

| Model | Evaluation Metric | Reported Result |
|---|---|---:|
| Decision Tree | Macro F1-score | 0.284 |
| SVM | Macro F1-score | 0.332 |
| CNN-based recommender | NDCG@5 | 0.182 |
| RAG-based recommender | NDCG@5 | 0.515 |
| RAG-based recommender | HitRate@5 | 0.80 |

The reported experiments show that the RAG-based approach achieved stronger recommendation-ranking results than the evaluated baselines on the reported metrics.


## Installation and Setup

### Prerequisites

- Python 3.10 or a compatible version supported by the project dependencies
- Git
- A MongoDB Atlas account with a configured database and vector search index
- A Google Gemini API key

### 1. Clone the Repository

```bash
git clone https://github.com/KrishnaBalaSai/Service-Recommendation-System.git
cd Service-Recommendation-System
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment on Windows:

```cmd
venv\Scripts\activate
```

On macOS or Linux:

```bash
source venv/bin/activate
```

### 3. Install Dependencies

If the repository contains a `requirements.txt` file, run:

```bash
pip install -r requirements.txt
```

Ensure the dependency file includes the packages required by the actual application.

### 4. Configure Environment Variables

Create a `.env` file in the project root and configure the MongoDB connection string, database settings, and Gemini API key using the variable names expected by the application.

Example placeholders:

```env
MONGO_URI=your_mongodb_atlas_connection_string
DB_NAME=your_database_name
GEMINI_API_KEY=your_gemini_api_key
```

Replace the placeholders with your own configuration. Do not commit `.env` or expose API keys and database credentials.

### 5. Run the Application

Use the entry-point script and launch command provided by the project. For example, if the repository's entry point is `app.py`:

```bash
python app.py
```

Check the actual project structure and dependencies before using this example command.

## Future Enhancements

- Improve recommendation quality through additional evaluation and ranking strategies.
- Expand the collection of technical books and developer services.
- Enhance user preference learning with more interaction data.
- Improve filtering for price, domain, category, and experience level.
- Evaluate performance and scalability on larger datasets.
- Improve recommendation explanations and user feedback mechanisms.

## Project Information

**Project Type:** Final-Year B.Tech Capstone Project

**Repository:** [Service-Recommendation-System](https://github.com/KrishnaBalaSai/Service-Recommendation-System)

**GitHub Profile:** [KrishnaBalaSai](https://github.com/KrishnaBalaSai)

**Portfolio:** [View Portfolio](https://krishnabalasai.github.io/Portfolio/)

## Conclusion

The Service Recommendation System demonstrates how semantic retrieval, metadata filtering, personalization, and generative AI can be combined to build a more useful and explainable recommendation experience. The project explores the limitations of traditional recommendation approaches and evaluates a hybrid RAG-based architecture for discovering technical books and developer services.

---
