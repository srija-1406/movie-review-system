"""
Movie Review System - Main Application
Author: Sneha (Member 2)
Module: App Setup, Configuration, Auth Routes
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = 'moviereview_secret_2024'

# ─── DB Config ────────────────────────────────────────────────
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',          # ← change to your MySQL password
    'database': 'movie_review_db',
    'cursorclass': pymysql.cursors.DictCursor
}

def get_db():
    return pymysql.connect(**DB_CONFIG)

# ─── Auth Decorators ──────────────────────────────────────────
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to continue.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('is_admin'):
            flash('Admin access only.', 'danger')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated

# ─── Home ─────────────────────────────────────────────────────
@app.route('/')
def home():
    db = get_db()
    cur = db.cursor()
    cur.execute("""
        SELECT * FROM movie_ratings_summary
        ORDER BY avg_rating DESC, total_reviews DESC
        LIMIT 8
    """)
    top_movies = cur.fetchall()
    cur.execute("SELECT * FROM genres ORDER BY genre_name")
    genres = cur.fetchall()
    db.close()
    return render_template('index.html', top_movies=top_movies, genres=genres)

# ─── Auth: Register ────────────────────────────────────────────
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        email    = request.form['email'].strip()
        fullname = request.form['full_name'].strip()
        password = request.form['password']

        if len(password) < 6:
            flash('Password must be at least 6 characters.', 'danger')
            return render_template('register.html')

        hashed = generate_password_hash(password)
        db = get_db()
        cur = db.cursor()
        try:
            cur.execute(
                "INSERT INTO users (username, email, password_hash, full_name) VALUES (%s,%s,%s,%s)",
                (username, email, hashed, fullname)
            )
            db.commit()
            flash('Account created! Please login.', 'success')
            return redirect(url_for('login'))
        except pymysql.err.IntegrityError:
            flash('Username or email already exists.', 'danger')
        finally:
            db.close()
    return render_template('register.html')

# ─── Auth: Login ──────────────────────────────────────────────
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        db.close()
        if user and check_password_hash(user['password_hash'], password):
            session['user_id']  = user['user_id']
            session['username'] = user['username']
            session['is_admin'] = bool(user['is_admin'])
            flash(f"Welcome back, {user['full_name'] or username}!", 'success')
            return redirect(url_for('home'))
        flash('Invalid username or password.', 'danger')
    return render_template('login.html')

# ─── Auth: Logout ─────────────────────────────────────────────
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

# ─── Movies: List & Search ────────────────────────────────────
# Author: Ravi (Member 1)
@app.route('/movies')
def movies():
    db = get_db()
    cur = db.cursor()
    query = request.args.get('q', '').strip()
    genre_id = request.args.get('genre', '')

    sql = "SELECT * FROM movie_ratings_summary WHERE 1=1"
    params = []
    if query:
        sql += " AND title LIKE %s"
        params.append(f'%{query}%')
    if genre_id:
        sql = """
            SELECT mrs.* FROM movie_ratings_summary mrs
            JOIN movie_genres mg ON mrs.movie_id = mg.movie_id
            WHERE mg.genre_id = %s
        """
        params = [genre_id]
        if query:
            sql += " AND mrs.title LIKE %s"
            params.append(f'%{query}%')

    sql += " ORDER BY avg_rating DESC"
    cur.execute(sql, params)
    movies_list = cur.fetchall()
    cur.execute("SELECT * FROM genres ORDER BY genre_name")
    genres = cur.fetchall()
    db.close()
    return render_template('movies.html', movies=movies_list, genres=genres, query=query, selected_genre=genre_id)

# ─── Movies: Detail ───────────────────────────────────────────
@app.route('/movie/<int:movie_id>')
def movie_detail(movie_id):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM movie_ratings_summary WHERE movie_id = %s", (movie_id,))
    movie = cur.fetchone()
    if not movie:
        flash('Movie not found.', 'danger')
        return redirect(url_for('movies'))
    cur.execute("""
        SELECT r.*, u.username, u.full_name
        FROM reviews r JOIN users u ON r.user_id = u.user_id
        WHERE r.movie_id = %s ORDER BY r.created_at DESC
    """, (movie_id,))
    reviews = cur.fetchall()
    cur.execute("""
        SELECT g.genre_name FROM genres g
        JOIN movie_genres mg ON g.genre_id = mg.genre_id
        WHERE mg.movie_id = %s
    """, (movie_id,))
    genres = cur.fetchall()
    user_review = None
    if session.get('user_id'):
        cur.execute("SELECT * FROM reviews WHERE movie_id=%s AND user_id=%s",
                    (movie_id, session['user_id']))
        user_review = cur.fetchone()
    db.close()
    return render_template('movie_detail.html', movie=movie, reviews=reviews,
                           genres=genres, user_review=user_review)

# ─── Movies: Add (Admin) ──────────────────────────────────────
@app.route('/admin/add-movie', methods=['GET', 'POST'])
@login_required
@admin_required
def add_movie():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM directors")
    directors = cur.fetchall()
    cur.execute("SELECT * FROM genres")
    genres = cur.fetchall()

    if request.method == 'POST':
        title       = request.form['title']
        year        = request.form['release_year']
        duration    = request.form['duration_min']
        language    = request.form['language']
        description = request.form['description']
        director_id = request.form['director_id'] or None
        genre_ids   = request.form.getlist('genres')

        cur.execute("""
            INSERT INTO movies (title, release_year, duration_min, language, description, director_id)
            VALUES (%s,%s,%s,%s,%s,%s)
        """, (title, year, duration, language, description, director_id))
        db.commit()
        movie_id = cur.lastrowid
        for gid in genre_ids:
            cur.execute("INSERT INTO movie_genres VALUES (%s,%s)", (movie_id, gid))
        db.commit()
        db.close()
        flash(f'"{title}" added successfully!', 'success')
        return redirect(url_for('movie_detail', movie_id=movie_id))

    db.close()
    return render_template('add_movie.html', directors=directors, genres=genres)

# ─── Reviews: Submit ──────────────────────────────────────────
# Author: Arjun (Member 3)
@app.route('/movie/<int:movie_id>/review', methods=['POST'])
@login_required
def submit_review(movie_id):
    rating      = float(request.form['rating'])
    review_text = request.form.get('review_text', '').strip()
    db = get_db()
    cur = db.cursor()
    try:
        cur.execute("""
            INSERT INTO reviews (movie_id, user_id, rating, review_text)
            VALUES (%s,%s,%s,%s)
            ON DUPLICATE KEY UPDATE rating=%s, review_text=%s, updated_at=NOW()
        """, (movie_id, session['user_id'], rating, review_text, rating, review_text))
        db.commit()
        flash('Your review has been saved!', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
    finally:
        db.close()
    return redirect(url_for('movie_detail', movie_id=movie_id))

# ─── Reviews: Delete ──────────────────────────────────────────
@app.route('/review/<int:review_id>/delete', methods=['POST'])
@login_required
def delete_review(review_id):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM reviews WHERE review_id=%s", (review_id,))
    review = cur.fetchone()
    if review and (review['user_id'] == session['user_id'] or session.get('is_admin')):
        movie_id = review['movie_id']
        cur.execute("DELETE FROM reviews WHERE review_id=%s", (review_id,))
        db.commit()
        flash('Review deleted.', 'info')
    db.close()
    return redirect(url_for('movie_detail', movie_id=review['movie_id']))

# ─── Profile ──────────────────────────────────────────────────
@app.route('/profile')
@login_required
def profile():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM users WHERE user_id=%s", (session['user_id'],))
    user = cur.fetchone()
    cur.execute("""
        SELECT r.*, m.title, m.release_year
        FROM reviews r JOIN movies m ON r.movie_id = m.movie_id
        WHERE r.user_id = %s ORDER BY r.created_at DESC
    """, (session['user_id'],))
    reviews = cur.fetchall()
    db.close()
    return render_template('profile.html', user=user, reviews=reviews)

if __name__ == '__main__':
    app.run(debug=True)
