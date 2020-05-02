DROP DATABASE IF EXISTS LIBRARY;
CREATE DATABASE LIBRARY;
USE LIBRARY;
CREATE TABLE BOOKS(isbn VARCHAR(10) primary key, title VARCHAR(1000) not null, status boolean);
CREATE TABLE AUTHORS(author_id INT UNSIGNED primary key, name VARCHAR(100));
CREATE TABLE BOOK_AUTHORS(isbn VARCHAR(10),author_id INT UNSIGNED  ,primary key(author_id,isbn),FOREIGN KEY(author_id) references AUTHORS(author_id),FOREIGN KEY(isbn) references BOOK(isbn));

CREATE TABLE STUDENTS(student_id VARCHAR(10) primary key ,first_name VARCHAR(100) NOT NULL,last_name VARCHAR(100) NOT NULL,email VARCHAR(1000) NOT NULL);

CREATE TABLE BOOK_ISSUED(issue_id INT unsigned AUTO_INCREMENT primary key,isbn VARCHAR(10) ,student_id VARCHAR(10) ,Date_out datetime, Date_due datetime, Date_return datetime,FOREIGN KEY(isbn) references BOOK(isbn),FOREIGN KEY(student_id) references STUDENTS(student_id));