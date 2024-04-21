CREATE DATABASE rate_my_course;

-- Users table, assuming a role differentiation if you want to distinguish between students, faculty, etc.
CREATE TABLE Users (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(255)
);

-- Courses table, where the main attributes of a course are stored.
CREATE TABLE Courses (
    course_id SERIAL PRIMARY KEY,
    course_code VARCHAR(255) NOT NULL,
    course_name VARCHAR(255) NOT NULL,
    course_description TEXT
);

-- Reviews table, which links the users and the courses. 
-- This stores the rating and comments about the course.
CREATE TABLE Reviews (
    review_id SERIAL PRIMARY KEY,
    course_id INT NOT NULL,
    user_id INT NOT NULL,
    rating DECIMAL(3, 2), -- For example, a 4.5 out of 5 rating.
    comment TEXT,
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (course_id) REFERENCES Courses(course_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);


-- Inserting sample data into Users
-- Assuming the function generate_password_hash exists in your SQL context, or replace this accordingly if executing outside.
INSERT INTO Users (user_id, name, email, password) VALUES
(1, 'Landon Nalewaja', 'landon@example.com', 'hashed_password_landon'), -- Replace 'hashed_password_landon' with an actual hash
(2, 'Ronni Elhadidy', 'ronni@example.com', 'hashed_password_ronni'),   -- Replace 'hashed_password_ronni' with an actual hash
(3, 'Kendall Tart', 'kendall@example.com', 'hashed_password_kendall'), -- Replace 'hashed_password_kendall' with an actual hash
(4, 'Test User', 'test@example.com', 'hashed_password_test');          -- Replace 'hashed_password_test' with an actual hash

-- Inserting sample data into Courses
INSERT INTO Courses (course_id, course_name, course_description, professor_name) VALUES
('ITSC-3146', 'Intro to Operating Systems and Networking', 'Class Description', 'Harini Ramaprasad'),
('ITSC-3155', 'Intro to Software Engineering', 'Class Description', 'Jacob Krevat');

-- Inserting sample data into Reviews
INSERT INTO Reviews (course_id, user_id, rating, comment, final_grade) VALUES
('ITSC-3146', 1, 3, 'This course was hard.', 'B'),
('ITSC-3146', 2, 4, 'It was so much work!', 'A'),
('ITSC-3146', 3, 2, 'I thought it was not too bad.', 'C'),
('ITSC-3155', 1, 3, 'This course was hard.', 'B'),
('ITSC-3155', 2, 4, 'It was so much work!', 'A'),
('ITSC-3155', 3, 2, 'I thought it was not too bad.', 'C');
