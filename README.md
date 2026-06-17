# 🎬 CineReview — Movie Review System

A full-stack DBMS project built with **Python Flask**, **MySQL**, and **Bootstrap 5**.
Users can browse movies, search by genre, and submit/edit their own reviews and ratings.

---

## 👥 Team Members

| Member | Role | Module |
|--------|------|--------|
| **samhita** | Member 1 | Database design, schema, movies module |
| **Srija** | Member 2 | Authentication, UI/frontend, app config |
| **srujana** | Member 3 | Reviews, ratings, profile module |

---

## 🛠️ Tech Stack

- **Backend:** Python 3, Flask
- **Database:** MySQL
- **Frontend:** HTML5, CSS3, Bootstrap 5, Jinja2 templating
- **Libraries:** PyMySQL, Werkzeug (password hashing)

---

## ⚙️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/movie-review-system.git
cd movie-review-system
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up the database
Open MySQL and run:
```bash
mysql -u root -p < database/schema.sql
mysql -u root -p < database/seed_data.sql
```

### 4. Configure database password
Open `app.py` and update:
```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'YOUR_MYSQL_PASSWORD',
    'database': 'movie_review_db',
    ...
}
```

### 5. Run the app
```bash
python app.py
```

Open your browser at **http://localhost:5000**

---

## 📂 Project Structure

```
movie_review_system/
├── app.py                  # Flask app, routes, DB logic
├── requirements.txt
├── database/
│   ├── schema.sql          # Table definitions, view, trigger
│   └── seed_data.sql       # Sample data
├── static/
│   ├── css/style.css       # Custom dark cinematic theme
│   └── js/main.js
└── templates/
    ├── base.html           # Shared layout/navbar/footer
    ├── index.html          # Home page
    ├── movies.html         # Browse/search movies
    ├── movie_detail.html   # Movie page + reviews
    ├── login.html
    ├── register.html
    ├── profile.html
    └── add_movie.html      # Admin: add new movie
```

---

## 🗄️ Database Schema

6 tables: `genres`, `directors`, `movies`, `movie_genres` (M:N), `users`, `reviews`
Plus a view `movie_ratings_summary` and a trigger validating rating range (1.0–10.0).

---

## ✨ Features

- User registration & login (hashed passwords)
- Browse movies, filter by genre, search by title
- Submit, edit, and delete reviews with 1–10 ratings
- Average rating auto-calculated via SQL view
- Admin-only "Add Movie" page
- User profile showing review history
