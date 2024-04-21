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
INSERT INTO Users (name, email, password, role) VALUES
('John Doe', 'john.doe@example.com', 'hashed_password1', 'student'),
('Jane Smith', 'jane.smith@example.com', 'hashed_password2', 'student'),
('Mike Brown', 'mike.brown@example.com', 'hashed_password3', 'student'),
('Sarah Connor', 'sarah.connor@example.com', 'hashed_password4', 'professor');

-- Inserting sample data into Courses
INSERT INTO Courses (course_code, course_name, course_description) VALUES
('CS101', 'Introduction to Computer Science', 'This course introduces the fundamental concepts of computer science and computational thinking. It covers a broad range of foundational topics such as algorithms, data structures, software engineering, and databases.'),
('MATH104', 'Calculus I', 'Calculus I covers differential and integral calculus in one variable, with applications involving functions of one variable.'),
('HIST202', 'World History', 'This course offers a comprehensive overview of global history from the 18th century to the present, including major economic, social, and political developments.'),
('BIO115', 'General Biology', 'An introduction to the fundamental principles of biology, focusing on the structure and function of the human body, genetics, evolution, and ecology.');

-- Inserting sample data into Reviews
INSERT INTO Reviews (course_id, user_id, rating, comment) VALUES
(1, 1, 4.5, 'Great introduction to computer science. Well-structured class and highly informative.'),
(1, 2, 4.0, 'Informative class but very challenging for beginners who have no background in programming.'),
(2, 1, 3.5, 'Solid course, though the pace was a bit fast. Good for students with some calculus background.'),
(2, 3, 4.0, 'Helpful course with lots of resources. The professor was very clear with instructions.'),
(3, 2, 5.0, 'Extremely insightful and wonderfully taught. Covers a lot of material but in an understandable way.'),
(3, 4, 4.5, 'Loved this history course! It was thorough and the reading materials were excellent.'),
(4, 3, 2.0, 'Not the best biology course. It seemed disorganized and the labs didn’t always work as planned.'),
(4, 4, 3.0, 'Average course. Hopefully, it gets better with the new curriculum outline proposed for next year.');

-- Notes:
-- Be sure to replace 'hashed_passwordX' with actual hashed passwords if storing real user data.
-- The course_id and user_id values in the Reviews table are referring to the IDs generated when rows are inserted into the Users and Courses tables respectively.
-- Ensure that foreign key relations are properly maintained, meaning the user_ids and course_ids in the Reviews table should exist in the Users and Courses tables respectively.
