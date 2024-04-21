CREATE DATABASE rate_my_course;

CREATE TABLE Users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(255)
);

CREATE TABLE Professors (
    professor_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE Classes (
    course_number INT PRIMARY KEY AUTO_INCREMENT,
    course_name VARCHAR(255) NOT NULL,
    course_description TEXT
);

CREATE TABLE ClassProfessors (
    class_id INT,
    professor_id INT,
    PRIMARY KEY (class_id, professor_id),
    FOREIGN KEY (class_id) REFERENCES Classes(course_number),
    FOREIGN KEY (professor_id) REFERENCES Professors(professor_id)
);

CREATE TABLE Comments (
    comment_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    course_number INT,
    rating DECIMAL(3, 2),
    final_grade CHAR(2),
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (course_number) REFERENCES Classes(course_number)
);
-- Inserting sample data into Users
INSERT INTO Users (name, email, password, role) VALUES
('John Doe', 'john.doe@example.com', 'hashed_password1', 'student'),
('Jane Smith', 'jane.smith@example.com', 'hashed_password2', 'professor'),
('Mike Brown', 'mike.brown@example.com', 'hashed_password3', 'student');

-- Inserting sample data into Professors
INSERT INTO Professors (name) VALUES
('Dr. Alice Johnson'),
('Prof. Brian Taylor'),
('Dr. Cindy Lee');

-- Inserting sample data into Classes
INSERT INTO Classes (course_name, course_description) VALUES
('Introduction to Computer Science', 'An introductory course on the fundamentals of computer science'),
('Database Systems', 'In-depth study of database design and the use of database management systems'),
('Calculus I', 'A study of the principles of calculus, including limits, derivatives, and integrals');

-- Inserting sample data into ClassProfessors
-- NOTE: The actual IDs for classes and professors should be used here.
INSERT INTO ClassProfessors (class_id, professor_id) VALUES
(1, 1), -- Class 1 is taught by Professor 1
(2, 2), -- Class 2 is taught by Professor 2
(3, 3); -- Class 3 is taught by Professor 3

-- Inserting sample data into Comments
-- NOTE: The actual user_id and course_number should be used here.
INSERT INTO Comments (user_id, course_number, rating, final_grade) VALUES
(1, 1, 4.5, 'A'),
(2, 1, 3.7, 'B'),
(1, 2, 4.0, 'A-'),
(3, 3, 4.8, 'A');
