CREATE DATABASE rate_my_course;

-- Creating Users table
CREATE TABLE Users (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Creating Courses table
CREATE TABLE Courses (
    course_id VARCHAR(50) PRIMARY KEY,
    course_name VARCHAR(255) NOT NULL,
    course_description TEXT,
    professor_name VARCHAR(255)
);

-- Creating Reviews table
CREATE TABLE Reviews (
    review_id SERIAL PRIMARY KEY,
    course_id VARCHAR(50) NOT NULL,
    user_id INT NOT NULL,
    rating INT,
    final_grade CHAR(2),
    comment TEXT,
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (course_id) REFERENCES Courses(course_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);


-- Inserting sample data into Users
INSERT INTO Users (name, email, password) VALUES
('Landon Nalewaja', 'landon@example.com', 'hashed_password1'),
('Ronni Elhadidy', 'ronni@example.com', 'hashed_password2'),
('Kendall Tart', 'kendall@example.com', 'hashed_password3'),
('Test User', 'test@example.com', 'hashed_password4');

-- Inserting sample data into Courses
INSERT INTO Courses (course_id, course_name, course_description, professor_name) VALUES
('ITSC-3146', 'Intro to Operating Systems and Networking', 'This course introduces students to the fundamental concepts of operating systems and networking.', 'Harini Ramaprasad'),
('ITSC-3155', 'Intro to Software Engineering', 'This course covers the basics of software engineering methods and practices, including software lifecycle, development models, and team roles.', 'Jacob Krevat');

-- Inserting sample data into Reviews
INSERT INTO Reviews (course_id, user_id, rating, final_grade, comment) VALUES
('ITSC-3146', 1, 3, 'B', 'This course was hard.'),
('ITSC-3146', 2, 4, 'A', 'It was so much work!'),
('ITSC-3146', 3, 2, 'C', 'I thought it was not too bad.'),
('ITSC-3155', 1, 3, 'B', 'This course was hard.'),
('ITSC-3155', 2, 4, 'A', 'It was so much work!'),
('ITSC-3155', 3, 2, 'C', 'I thought it was not too bad.');
