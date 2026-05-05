# 🎬 Movie Recommendation System

🌐 **Live App:** https://movie-recommendation-system-3ukmuugohzyczrgtjr6swp.streamlit.app/

A web-based movie recommendation system built using Machine Learning techniques, combining:

- Content-Based Filtering  
- Collaborative Filtering  

Deployed using Streamlit for real-time interaction.

---

## 🚀 Features

### 🔹 Content-Based Recommendation
- Input: Movie name  
- Uses genre similarity to recommend similar movies  
- Handles typos using fuzzy matching  

### 🔹 Collaborative Filtering (User-Based)
- Input: User ID  
- Finds similar users using cosine similarity  
- Recommends movies based on similar users’ preferences  
- Uses **weighted scoring (rating × similarity)**  



## 🧠 How It Works

### 1. Content-Based Filtering
- Extract genres from dataset  
- Convert to vectors using MultiLabelBinarizer  
- Compute similarity using cosine similarity  
- Recommend top similar movies  

---

### 2. Collaborative Filtering
- Create user-item matrix  
- Compute user-user similarity  
- Select top similar users  
- Generate candidate movies  
- Rank using weighted average:
Score = Σ(rating × similarity) / Σ(similarity)


---

## 📂 Project Structure
movie-recommendation-system/
│
├── app.py
├── movies.csv
├── ratings.csv
├── requirements.txt
├── recom1.ipynb
├── README.md

---

## ⚙️ Installation & Run
pip install -r requirements.txt
streamlit run app.py


---

## 🛠️ Tech Stack

- Python  
- Pandas  
- Scikit-learn  
- Streamlit  

---

## 🔥 Future Improvements

- Hybrid recommendation system  
- Better UI/UX  
- Cold-start problem handling  

---

## 👨‍💻 Author

Anshuman Rohilla
