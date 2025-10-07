HTML Semantic Search - Full Stack Project
=========================================
A Full-Stack Web Application that performs semantic search on any website’s HTML content using
AI embeddings and FAISS.
Instead of keyword matching, this system understands the meaning of queries and returns the most
relevant text chunks from the target website.
----------------------------------------------------------------------------------
Project Overview
----------------------------------------------------------------------------------
The HTML Semantic Search project combines React (frontend) and FastAPI (backend) with
Machine Learning models to enable intelligent search across web pages.
Users can enter a website URL and a search query to get the top 10 most semantically relevant
sections from the website.
This system uses Sentence Transformers to generate embeddings and FAISS to perform efficient
similarity searches.
----------------------------------------------------------------------------------
Features
----------------------------------------------------------------------------------
• Extracts HTML content from any website
• Cleans and preprocesses text using BeautifulSoup
• Generates vector embeddings using Sentence Transformers (all-MiniLM-L6-v2)
• Performs fast similarity search using FAISS
• Displays top 10 relevant chunks with scores and source URLs
• Built with React + FastAPI full-stack integration
• CORS enabled for frontend-backend communication
----------------------------------------------------------------------------------
Architecture
----------------------------------------------------------------------------------
Frontend (React)
↓ Axios
Backend (FastAPI)
↓
Web Scraper (Requests + BeautifulSoup)
↓
Tokenizer (Sentence Transformers)
↓
Embeddings (Hugging Face model)
↓
FAISS Vector Store (Similarity Search)
↓
Response → Frontend (Top 10 Relevant Texts)
----------------------------------------------------------------------------------
Tech Stack
----------------------------------------------------------------------------------
Frontend: React.js, Axios, HTML, CSS, JavaScript
Backend: FastAPI, Python, BeautifulSoup, Sentence Transformers, FAISS, Uvicorn
----------------------------------------------------------------------------------
Installation & Setup
----------------------------------------------------------------------------------
1. Clone the Repository:
git clone https://github.com/your-username/html-semantic-search.git
cd html-semantic-search
2. Setup Backend:
cd backend/app
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
3. Setup Frontend:
cd frontend
npm install
npm start
----------------------------------------------------------------------------------
How It Works
----------------------------------------------------------------------------------
1. User inputs URL + query on the frontend.
2. Backend fetches HTML, removes unnecessary tags.
3. Text is split into 500-token chunks.
4. Each chunk is embedded using Sentence Transformers.
5. FAISS performs similarity search to find top 10 closest matches.
6. Results are sent back and displayed beautifully on the React UI.
----------------------------------------------------------------------------------
Results
----------------------------------------------------------------------------------
• Achieves meaningful semantic search (not just keyword-based).
• Handles various websites with minimal preprocessing.
• Efficient embedding and retrieval using FAISS.
• Clean, simple React interface for better usability.
----------------------------------------------------------------------------------
Future Enhancements
----------------------------------------------------------------------------------
• Add support for JS-rendered pages (Playwright or Selenium)
• Store embeddings in Milvus / Pinecone for cloud scalability
• Add pagination and caching for faster searches
• Deploy on Render, Vercel, or AWS
• Add user authentication and search history tracking