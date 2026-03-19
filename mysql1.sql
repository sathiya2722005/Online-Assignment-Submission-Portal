create database assignmment1;
use assignment1;
CREATE TABLE register (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    reg_no VARCHAR(20) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    department VARCHAR(50) NOT NULL,
    password VARCHAR(100) NOT NULL
);
select*from register;


CREATE TABLE staff1 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    staff_id VARCHAR(20) NOT NULL UNIQUE,
    staff_name VARCHAR(100) NOT NULL,
    department VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL
);
select*from staff1;
#staff create assignments#
CREATE TABLE assign1(
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    subject VARCHAR(255) NOT NULL,
    department VARCHAR(255) NOT NULL,
    due_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

select* from assign1;
truncate table assign1;
#---student submission---#
CREATE TABLE submit1 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    assignment_title VARCHAR(100),
    student_name VARCHAR(100),
    reg_no VARCHAR(20),
    email VARCHAR(100),
    department VARCHAR(50),
    year VARCHAR(20),
    section VARCHAR(10),
    pdf_file VARCHAR(255),
    marks INT DEFAULT NULL,
    status VARCHAR(20) DEFAULT 'Pending',
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

select*from submit1;
CREATE TABLE submit2 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    assignment_title VARCHAR(255) NOT NULL,   -- Name of the assignment
    student_name VARCHAR(255) NOT NULL,       -- Student's name
    reg_no VARCHAR(50) NOT NULL,              -- Student's registration number
    pdf_file VARCHAR(255) NOT NULL,           -- Uploaded PDF filename
    marks INT DEFAULT NULL,                    -- Marks given by staff
    status ENUM('Pending','Completed','Approved','Rejected') DEFAULT 'Pending', -- Status of submission
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
select *from submit2;
CREATE DATABASE IF NOT EXISTS assignment_portal;

USE assignment_portal;

CREATE TABLE contact(
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    subject VARCHAR(255),
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
select * from contact;
CREATE TABLE submit3 (
    id INT AUTO_INCREMENT PRIMARY KEY,

    student_name VARCHAR(100) NOT NULL,
    reg_no VARCHAR(50) NOT NULL,

    assignment_title VARCHAR(200) NOT NULL,

    pdf_file VARCHAR(255) NOT NULL,

    marks INT DEFAULT NULL,

    status ENUM('Pending','Approved','Rejected') DEFAULT 'Pending',

    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
select *from submit3;


