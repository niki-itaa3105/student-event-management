CREATE DATABASE IF NOT EXISTS eventdb;
USE eventdb;

CREATE TABLE IF NOT EXISTS users (
  id         INT AUTO_INCREMENT PRIMARY KEY,
  name       VARCHAR(100) NOT NULL,
  email      VARCHAR(100) NOT NULL UNIQUE,
  password   VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS events (
  id          INT AUTO_INCREMENT PRIMARY KEY,
  title       VARCHAR(150) NOT NULL,
  description TEXT,
  category    VARCHAR(50),
  event_date  DATE,
  location    VARCHAR(150),
  seats       INT DEFAULT 100
);

CREATE TABLE IF NOT EXISTS registrations (
  id            INT AUTO_INCREMENT PRIMARY KEY,
  user_id       INT NOT NULL,
  event_id      INT NOT NULL,
  phone         VARCHAR(15),
  college       VARCHAR(150),
  department    VARCHAR(100),
  year          VARCHAR(20),
  food_pref     VARCHAR(20),
  registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY unique_reg (user_id, event_id),
  FOREIGN KEY (user_id)  REFERENCES users(id),
  FOREIGN KEY (event_id) REFERENCES events(id)
);

INSERT INTO events (title, description, category, event_date, location, seats) VALUES
('Tech Fest 2025',       'Annual college tech festival with hackathons and coding contests.', 'Technical',  '2025-06-15', 'Main Auditorium',  200),
('Cultural Night',       'A vibrant evening of music, dance and drama performances.',        'Cultural',   '2025-06-20', 'Open Air Theatre', 500),
('Workshop: Docker 101', 'Hands-on DevOps workshop covering Docker and CI/CD basics.',       'Workshop',   '2025-06-25', 'CS Lab - Block A',  50),
('Sports Day 2025',      'Inter-department cricket, football and athletics competitions.',   'Sports',     '2025-07-01', 'College Ground',   300),
('Alumni Meet 2025',     'Connect with seniors and explore career guidance sessions.',       'Networking', '2025-07-10', 'Conference Hall',  150);
