-- ============================================================
-- Movie Review System - Sample Data
-- Author: samhita (Member 1)
-- ============================================================

USE movie_review_db;

-- Genres
INSERT INTO genres (genre_name) VALUES
('Action'), ('Drama'), ('Comedy'), ('Thriller'), ('Sci-Fi'),
('Romance'), ('Horror'), ('Animation'), ('Biography'), ('Crime');

-- Directors
INSERT INTO directors (name, nationality, birth_year) VALUES
('Christopher Nolan', 'British-American', 1970),
('S.S. Rajamouli', 'Indian', 1973),
('Martin Scorsese', 'American', 1942),
('Quentin Tarantino', 'American', 1963),
('Mani Ratnam', 'Indian', 1956);

-- Movies
INSERT INTO movies (title, release_year, duration_min, language, description, director_id) VALUES
('Inception', 2010, 148, 'English', 'A thief enters dreams to plant an idea in a target\'s mind.', 1),
('The Dark Knight', 2008, 152, 'English', 'Batman faces the Joker, a criminal mastermind who wreaks chaos.', 1),
('RRR', 2022, 187, 'Telugu', 'Two legendary freedom fighters and their extraordinary journey.', 2),
('Baahubali', 2015, 159, 'Telugu', 'An epic tale of two brothers divided by fate.', 2),
('Goodfellas', 1990, 146, 'English', 'The rise and fall of a mob associate over decades.', 3),
('Pulp Fiction', 1994, 154, 'English', 'Intertwining tales of crime in Los Angeles.', 4),
('Roja', 1992, 152, 'Tamil', 'A woman fights to free her husband who is taken hostage.', 5),
('Interstellar', 2014, 169, 'English', 'Astronauts travel through a wormhole near Saturn seeking a new home.', 1);

-- Movie Genres
INSERT INTO movie_genres (movie_id, genre_id) VALUES
(1, 5), (1, 4), (1, 1),  -- Inception: Sci-Fi, Thriller, Action
(2, 1), (2, 4), (2, 10), -- Dark Knight: Action, Thriller, Crime
(3, 1), (3, 2),           -- RRR: Action, Drama
(4, 1), (4, 2),           -- Baahubali: Action, Drama
(5, 10), (5, 2),          -- Goodfellas: Crime, Drama
(6, 10), (6, 2), (6, 4),  -- Pulp Fiction: Crime, Drama, Thriller
(7, 2), (7, 6),           -- Roja: Drama, Romance
(8, 5), (8, 2), (8, 4);   -- Interstellar: Sci-Fi, Drama, Thriller

-- Admin user (password: admin123 - hashed via werkzeug)
INSERT INTO users (username, email, password_hash, full_name, is_admin) VALUES
('admin', 'admin@moviereview.com', 'pbkdf2:sha256:260000$placeholder', 'Admin User', 1);
