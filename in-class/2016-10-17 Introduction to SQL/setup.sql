DROP TABLE sio_student;
DROP TABLE sio_course;
DROP TABLE sio_course_students;

/* Create the student table */
CREATE TABLE sio_student (
    andrew_id varchar NOT NULL,
    first_name varchar NOT NULL,
    last_name varchar NOT NULL,
    PRIMARY KEY (andrew_id)
);

/* Create the course table */
CREATE TABLE sio_course (
    course_number varchar NOT NULL,
    course_name varchar NOT NULL,
    instructor varchar NOT NULL,
    PRIMARY KEY (course_number)
);

/* Create Student to course relationship */
CREATE TABLE sio_course_students (
    course_id varchar NOT NULL,
    student_id varchar NOT NULL,
    FOREIGN KEY (course_id) REFERENCES sio_course (course_number),
    FOREIGN KEY (student_id) REFERENCES sio_student (andrew_id)
);

/* Add some sample data */
INSERT INTO sio_student (andrew_id, first_name, last_name) VALUES ('bcforres', 'Bailey', 'Forrest');
INSERT INTO sio_student (andrew_id, first_name, last_name) VALUES ('sjl1', 'Shannon', 'Lee');
INSERT INTO sio_student (andrew_id, first_name, last_name) VALUES ('ecwong', 'Elliot', 'Wong');
INSERT INTO sio_student (andrew_id, first_name, last_name) VALUES ('arthurle', 'Arthur', 'Lee');
INSERT INTO sio_student (andrew_id, first_name, last_name) VALUES ('shilal', 'Salem', 'Hilal');
INSERT INTO sio_student (andrew_id, first_name, last_name) VALUES ('smklein', 'Sean', 'Klein');


INSERT INTO sio_course (course_number, course_name, instructor) VALUES ('15-437', 'Web Applications', 'Charlie Garrod');
INSERT INTO sio_course (course_number, course_name, instructor) VALUES ('15-410', 'OS', 'Dave Eckhardt');

INSERT INTO sio_course_students (course_id, student_id) VALUES ('15-410', 'bcforres');
INSERT INTO sio_course_students (course_id, student_id) VALUES ('15-410', 'sjl1');
INSERT INTO sio_course_students (course_id, student_id) VALUES ('15-410', 'smklein');
INSERT INTO sio_course_students (course_id, student_id) VALUES ('15-437', 'arthurle');
INSERT INTO sio_course_students (course_id, student_id) VALUES ('15-437', 'ecwong');
INSERT INTO sio_course_students (course_id, student_id) VALUES ('15-437', 'shilal');
