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
