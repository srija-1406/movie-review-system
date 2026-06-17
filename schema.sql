-- ============================================================
-- Movie Review System - Database Schema
-- Author: samhita (Member 1)
-- Module: Database Design & Movies Table
-- ============================================================

CREATE DATABASE IF NOT EXISTS movie_review_db;
USE movie_review_db;

-- -------------------------
-- Table: genres
-- -------------------------
CREATE TABLE IF NOT EXISTS genres (
    genre_id INT AUTO_INCREMENT PRIMARY KEY,
    genre_name VARCHAR(50) NOT NULL UNIQUE
);

-- -------------------------
-- Table: directors
-- -------------------------
CREATE TABLE IF NOT EXISTS directors (
    director_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    nationality VARCHAR(50),
    birth_year INT
);

-- -------------------------
-- Table: movies
-- -------------------------
CREATE TABLE IF NOT EXISTS movies (
    movie_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    release_year INT NOT NULL,
    duration_min INT,
    language VARCHAR(50),
    description TEXT,
    poster_url VARCHAR(300),
    director_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (director_id) REFERENCES directors(director_id) ON DELETE SET NULL
);

-- -------------------------
-- Table: movie_genres (M:N)
-- -------------------------
CREATE TABLE IF NOT EXISTS movie_genres (
    movie_id INT NOT NULL,
    genre_id INT NOT NULL,
    PRIMARY KEY (movie_id, genre_id),
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id) ON DELETE CASCADE,
    FOREIGN KEY (genre_id) REFERENCES genres(genre_id) ON DELETE CASCADE
);

-- -------------------------
-- Table: users
-- Author: Srija (Member 2)
-- -------------------------
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    is_admin TINYINT(1) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- -------------------------
-- Table: reviews
-- Author: srujana (Member 3)
-- -------------------------
CREATE TABLE IF NOT EXISTS reviews (
    review_id INT AUTO_INCREMENT PRIMARY KEY,
    movie_id INT NOT NULL,
    user_id INT NOT NULL,
    rating DECIMAL(2,1) NOT NULL CHECK (rating >= 1.0 AND rating <= 10.0),
    review_text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    UNIQUE KEY one_review_per_user (movie_id, user_id)
);

-- -------------------------
-- View: movie average ratings
-- Author: srujana (Member 3)
-- -------------------------
CREATE OR REPLACE VIEW movie_ratings_summary AS
SELECT
    m.movie_id,
    m.title,
    m.release_year,
    m.language,
    d.name AS director_name,
    COUNT(r.review_id) AS total_reviews,
    ROUND(AVG(r.rating), 1) AS avg_rating
FROM movies m
LEFT JOIN directors d ON m.director_id = d.director_id
LEFT JOIN reviews r ON m.movie_id = r.movie_id
GROUP BY m.movie_id, m.title, m.release_year, m.language, d.name;

-- -------------------------
-- Trigger: prevent duplicate review update spam
-- Author: srujana (Member 3)
-- -------------------------
DELIMITER $$
CREATE TRIGGER before_review_insert
BEFORE INSERT ON reviews
FOR EACH ROW
BEGIN
    IF NEW.rating < 1.0 OR NEW.rating > 10.0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Rating must be between 1.0 and 10.0';
    END IF;
END$$
DELIMITER ;
