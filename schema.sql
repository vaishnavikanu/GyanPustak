-- GYANPUSTAK DATABASE - FINAL NORMALIZED


DROP DATABASE IF EXISTS gyan_pustak;
CREATE DATABASE gyan_pustak;
USE gyan_pustak;


-- UNIVERSITY

CREATE TABLE University (
    universityID INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(150) UNIQUE NOT NULL,
    address TEXT,
    city VARCHAR(50),
    state VARCHAR(50),
    zipCode VARCHAR(10),
    representativefirstName VARCHAR(100),
    representativelastName VARCHAR(100),
    representativeEmail VARCHAR(100),
    representativePhone VARCHAR(15)
);


-- DEPARTMENT

CREATE TABLE Department (
    departmentID INT PRIMARY KEY AUTO_INCREMENT,
    universityID INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    headName VARCHAR(100),
    FOREIGN KEY (universityID) REFERENCES University(universityID) ON DELETE CASCADE,
    UNIQUE (universityID, name)
);


-- STUDENT (NO universityID → removed TD)

CREATE TABLE Student (
    studentID INT PRIMARY KEY AUTO_INCREMENT,
    firstName VARCHAR(50),
    lastName VARCHAR(50),
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(15),
    dob DATE,
    gender ENUM('M','F','Other'),
    address TEXT,
    departmentID INT,
    major VARCHAR(100),
    enrollmentYear INT,
    status ENUM('active','inactive','graduated'),
    currentYear INT,
    FOREIGN KEY (departmentID) REFERENCES Department(departmentID)
);


-- EMPLOYEE

CREATE TABLE Employee (
    employeeID INT PRIMARY KEY AUTO_INCREMENT,
    firstName VARCHAR(50),
    lastName VARCHAR(50),
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(15),
    gender ENUM('M','F','Other'),
    salary DECIMAL(10,2),
    aadhaar VARCHAR(12) UNIQUE,
    address TEXT,
    empType ENUM('admin','support'),
    joinDate DATE,
    status ENUM('active','inactive')
);


-- ADMIN

CREATE TABLE Admin (
    adminID INT PRIMARY KEY AUTO_INCREMENT,
    employeeID INT UNIQUE,
    isSuperAdmin BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (employeeID) REFERENCES Employee(employeeID) ON DELETE CASCADE
);


-- CUSTOMER SUPPORT

CREATE TABLE CustomerSupport (
    supportID INT PRIMARY KEY AUTO_INCREMENT,
    employeeID INT UNIQUE,
    department VARCHAR(50),
    FOREIGN KEY (employeeID) REFERENCES Employee(employeeID) ON DELETE CASCADE
);


-- INSTRUCTOR (NO universityID → removed TD)

CREATE TABLE Instructor (
    instructorID INT PRIMARY KEY AUTO_INCREMENT,
    firstName VARCHAR(50),
    lastName VARCHAR(50),
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(15),
    departmentID INT,
    specialization VARCHAR(100),
    FOREIGN KEY (departmentID) REFERENCES Department(departmentID)
);


-- COURSE

CREATE TABLE Course (
    courseID INT PRIMARY KEY AUTO_INCREMENT,
    courseCode VARCHAR(20),
    courseName VARCHAR(150),
    creditHours INT,
    year INT,
    semester INT
);


-- RELATION TABLES

CREATE TABLE DepartmentCourse (
    departmentID INT,
    courseID INT,
    PRIMARY KEY (departmentID, courseID),
    FOREIGN KEY (departmentID) REFERENCES Department(departmentID) ON DELETE CASCADE,
    FOREIGN KEY (courseID) REFERENCES Course(courseID) ON DELETE CASCADE
);

CREATE TABLE CourseInstructor (
    courseID INT,
    instructorID INT,
    PRIMARY KEY (courseID, instructorID),
    FOREIGN KEY (courseID) REFERENCES Course(courseID) ON DELETE CASCADE,
    FOREIGN KEY (instructorID) REFERENCES Instructor(instructorID) ON DELETE CASCADE
);


-- BOOK 

CREATE TABLE Book (
    bookID INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255),
    isbn VARCHAR(20) UNIQUE,
    publisher VARCHAR(100),
    publicationDate DATE,
    edition INT,
    language VARCHAR(50),
    type ENUM('new','used'),
    purchaseOption ENUM('rent','buy'),
    format ENUM('hardcover','softcover','electronic'),
    price DECIMAL(10,2),
    rentalPrice DECIMAL(10,2),
    quantity INT,
    rating DECIMAL(3,2)
);


-- AUTHOR

CREATE TABLE Author (
    authorID INT PRIMARY KEY AUTO_INCREMENT,
    authorName VARCHAR(100)
);

-- BOOKAUTHOR

CREATE TABLE BookAuthor (
    bookID INT,
    authorID INT,
    PRIMARY KEY (bookID, authorID),
    FOREIGN KEY (bookID) REFERENCES Book(bookID) ON DELETE CASCADE,
    FOREIGN KEY (authorID) REFERENCES Author(authorID) ON DELETE CASCADE
);


-- KEYWORD

CREATE TABLE Keyword (
    keywordID INT PRIMARY KEY AUTO_INCREMENT,
    keyword VARCHAR(100)
);

-- BOOKKEYWORD

CREATE TABLE BookKeyword (
    bookID INT,
    keywordID INT,
    PRIMARY KEY (bookID, keywordID),
    FOREIGN KEY (bookID) REFERENCES Book(bookID) ON DELETE CASCADE,
    FOREIGN KEY (keywordID) REFERENCES Keyword(keywordID) ON DELETE CASCADE
);


-- CATEGORY

CREATE TABLE Category (
    categoryID INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    description TEXT,
    parentCategoryID INT,
    FOREIGN KEY (parentCategoryID) REFERENCES Category(categoryID)
);

-- BookCategory

CREATE TABLE BookCategory (
    bookID INT,
    categoryID INT,
    PRIMARY KEY (bookID, categoryID),
    FOREIGN KEY (bookID) REFERENCES Book(bookID),
    FOREIGN KEY (categoryID) REFERENCES Category(categoryID)
);


-- COURSE BOOK

CREATE TABLE CourseBook (
    courseBookID INT PRIMARY KEY AUTO_INCREMENT,
    courseID INT,
    bookID INT,
    instructorID INT,
    year INT,
    semester INT,
    bookType ENUM('required','recommended','reference'),
    FOREIGN KEY (courseID) REFERENCES Course(courseID),
    FOREIGN KEY (bookID) REFERENCES Book(bookID),
    FOREIGN KEY (instructorID) REFERENCES Instructor(instructorID)
);


-- CART

CREATE TABLE Cart (
    cartID INT PRIMARY KEY AUTO_INCREMENT,
    studentID INT UNIQUE,
    dateCreated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    dateLastUpdated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (studentID) REFERENCES Student(studentID)
);

-- CARTITEM

CREATE TABLE CartItem (
    cartItemID INT PRIMARY KEY AUTO_INCREMENT,
    cartID INT,
    bookID INT,
    quantity INT,
    purchaseType ENUM('rent','buy'),
    FOREIGN KEY (cartID) REFERENCES Cart(cartID) ON DELETE CASCADE,
    FOREIGN KEY (bookID) REFERENCES Book(bookID)
);

-- ORDER

CREATE TABLE `Order` (
    orderID INT PRIMARY KEY AUTO_INCREMENT,
    studentID INT,
    orderNumber VARCHAR(20) UNIQUE,
    dateCreated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    dateFulfilled DATETIME,
    dateShipped DATETIME,
    shippingType ENUM('standard','2-day','1-day','express'),
    shippingAddress TEXT,
    shippingCost DECIMAL(10,2),
    orderStatus ENUM('pending','confirmed','processing','shipped','delivered','cancelled'),
    totalAmount DECIMAL(12,2),
    discountAmount DECIMAL(10,2),
    finalAmount DECIMAL(12,2),
    FOREIGN KEY (studentID) REFERENCES Student(studentID)
);

-- ORDERBOOK

CREATE TABLE OrderBook (
    orderBookID INT PRIMARY KEY AUTO_INCREMENT,
    orderID INT,
    bookID INT,
    quantity INT,
    purchaseType ENUM('rent','buy'),
    pricePerUnit DECIMAL(10,2),
    subtotal DECIMAL(12,2),
    FOREIGN KEY (orderID) REFERENCES `Order`(orderID) ON DELETE CASCADE,
    FOREIGN KEY (bookID) REFERENCES Book(bookID)
);

-- PAYMENT

CREATE TABLE Payment (
    paymentID INT PRIMARY KEY AUTO_INCREMENT,
    orderID INT UNIQUE,
    amount DECIMAL(12,2),
    paymentMethod ENUM('card','upi','netbanking','wallet','cod'),
    cardNumber VARCHAR(19),
    cardExpiry VARCHAR(5),
    cardHolderName VARCHAR(100),
    cardType ENUM('visa','mastercard','amex','debit'),
    upiID VARCHAR(100),
    bankName VARCHAR(100),
    paymentStatus ENUM('successful','failed','pending','refunded'),
    transactionID VARCHAR(50) UNIQUE,
    paymentDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (orderID) REFERENCES `Order`(orderID)
);

-- REVIEW

CREATE TABLE Review (
    reviewID INT PRIMARY KEY AUTO_INCREMENT,
    studentID INT,
    bookID INT,
    rating INT,
    reviewText LONGTEXT,
    isVerifiedPurchase BOOLEAN,
    datePosted TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (studentID) REFERENCES Student(studentID),
    FOREIGN KEY (bookID) REFERENCES Book(bookID)
);

-- TICKET + HISTORY

CREATE TABLE TicketCategory (
    categoryID INT PRIMARY KEY AUTO_INCREMENT,
    categoryName VARCHAR(50),
    description TEXT
);

CREATE TABLE Ticket (
    ticketID INT PRIMARY KEY AUTO_INCREMENT,
    studentID INT,
    employeeID INT,
    categoryID INT,
    title VARCHAR(100),
    description TEXT,
    status VARCHAR(20),
    adminEmployeeID INT,
    solution TEXT,
    dateLogged DATETIME DEFAULT CURRENT_TIMESTAMP,
    completionDate DATETIME,
    FOREIGN KEY (studentID) REFERENCES Student(studentID),
    FOREIGN KEY (employeeID) REFERENCES Employee(employeeID),
    FOREIGN KEY (adminEmployeeID) REFERENCES Employee(employeeID),
    FOREIGN KEY (categoryID) REFERENCES TicketCategory(categoryID)
);

CREATE TABLE TicketHistory (
    historyID INT PRIMARY KEY AUTO_INCREMENT,
    ticketID INT,
    previousStatus VARCHAR(20),
    newStatus VARCHAR(20),
    changedByEmployeeID INT,
    changeDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ticketID) REFERENCES Ticket(ticketID) ON DELETE CASCADE,
    FOREIGN KEY (changedByEmployeeID) REFERENCES Employee(employeeID)
);


-- UNIVERSITY

INSERT INTO University (name,address,city,state,zipCode,representativefirstName,representativelastName,representativeEmail,representativePhone) VALUES
('Delhi University','North Campus','Delhi','Delhi','110007','Dr Rajesh','kumar','rajesh@du.ac.in','9876543210'),
('IIT Delhi','Hauz Khas','Delhi','Delhi','110016','Prof Priya ','Singh','priya@iitd.ac.in','9876543211'),
('Jamia Millia Islamia','Jamia Nagar','Delhi','Delhi','110025','Prof Ahmed ','Khan','ahmed@jmi.ac.in','9876543212');


-- DEPARTMENT

INSERT INTO Department (universityID,name,headName) VALUES
(1,'CSE','Dr Amit Sharma'),(1,'ECE','Dr Rajesh Singh'),(1,'EEE','Dr Neeraj Verma'),
(1,'ME','Dr Suresh Patel'),(1,'CE','Dr Anil Kumar'),(1,'MM','Dr Deepak Mishra'),
(2,'CSE','Dr Priya Sharma'),(2,'ECE','Dr Kavita Joshi'),(2,'EEE','Dr Manoj Tiwari'),
(2,'ME','Dr Rohit Gupta'),(2,'CE','Dr Pankaj Agarwal'),(2,'MM','Dr Vinay Kulkarni'),
(3,'CSE','Dr Sneha Reddy'),(3,'ECE','Dr Arjun Nair'),(3,'EEE','Dr Kiran Rao'),
(3,'ME','Dr Vikram Mehta'),(3,'CE','Dr Rahul Das'),(3,'MM','Dr Shubham Jain');


-- STUDENT

INSERT INTO Student (firstName,lastName,email,phone,dob,gender,address,departmentID,major,enrollmentYear,status,currentYear) VALUES
('Aarav','Singh','aarav@du.ac.in','9876543220','2005-05-15','M','Delhi',1,'CSE',2023,'active',2),
('Priya','Sharma','priya@du.ac.in','9876543221','2004-08-20','F','Delhi',2,'ECE',2022,'active',3),
('Rahul','Verma','rahul@du.ac.in','9876543226','2005-02-11','M','Delhi',3,'EEE',2023,'active',2),
('Rohan','Kumar','rohan@iitd.ac.in','9876543222','2006-01-10','M','Delhi',7,'CSE',2024,'active',1),
('Ananya','Gupta','ananya@iitd.ac.in','9876543227','2005-03-21','F','Delhi',8,'ECE',2023,'active',2),
('Vikas','Yadav','vikas@iitd.ac.in','9876543228','2004-09-18','M','Delhi',11,'CE',2022,'active',3),
('Neha','Patel','neha@jmi.ac.in','9876543223','2005-12-08','F','Delhi',16,'ME',2023,'active',2),
('Kiran','Rao','kiran@jmi.ac.in','9876543225','2005-07-14','F','Delhi',15,'EEE',2023,'active',2),
('Imran','Ali','imran@jmi.ac.in','9876543229','2004-06-30','M','Delhi',13,'CSE',2022,'active',3);


-- EMPLOYEE (ADMIN + SUPPORT)

INSERT INTO Employee (firstName,lastName,email,phone,gender,salary,aadhaar,address,empType,joinDate,status) VALUES
('Vikram','Singh','vikram@gyan.com','9988776655','M',50000,'111122223333','Delhi','admin','2020-01-15','active'),
('Neha','Gupta','neha@gyan.com','9988776656','F',40000,'222233334444','Delhi','support','2021-03-20','active'),
('Arjun','Patel','arjun@gyan.com','9988776657','M',42000,'333344445555','Delhi','support','2021-06-10','active'),
('Rahul','Saxena','rahul@gyan.com','9988776658','M',55000,'444455556666','Delhi','admin','2019-08-22','active'),
('Sneha','Reddy','sneha@gyan.com','9988776659','F',38000,'555566667777','Delhi','support','2022-01-05','active');

INSERT INTO Admin (employeeID,isSuperAdmin) VALUES
(1,TRUE),
(4,FALSE);

INSERT INTO CustomerSupport (employeeID,department) VALUES
(2,'Orders'),(3,'Technical'),(5,'Accounts');


-- INSTRUCTOR 

INSERT INTO Instructor (firstName,lastName,email,phone,departmentID,specialization) VALUES
('Amit','Sharma','amit@du.ac.in','9001',1,'Data Structures'),
('Rajesh','Singh','rajesh@du.ac.in','9002',2,'Digital Electronics'),
('Neeraj','Verma','neeraj@du.ac.in','9003',3,'Power Systems'),
('Suresh','Patel','suresh@du.ac.in','9004',4,'Thermodynamics'),
('Anil','Kumar','anil@du.ac.in','9005',5,'Structural Engineering'),
('Deepak','Mishra','deepak@du.ac.in','9006',6,'Metallurgy'),
('Priya','Sharma','priya@iitd.ac.in','9101',7,'Algorithms'),
('Kavita','Joshi','kavita@iitd.ac.in','9102',8,'Communication Systems'),
('Manoj','Tiwari','manoj@iitd.ac.in','9103',9,'Electrical Machines'),
('Rohit','Gupta','rohit@iitd.ac.in','9104',10,'Fluid Mechanics'),
('Pankaj','Agarwal','pankaj@iitd.ac.in','9105',11,'Geotechnical'),
('Vinay','Kulkarni','vinay@iitd.ac.in','9106',12,'Material Science'),
('Sneha','Reddy','sneha@jmi.ac.in','9201',13,'Operating Systems'),
('Arjun','Nair','arjun@jmi.ac.in','9202',14,'Signal Processing'),
('Kiran','Rao','kiran@jmi.ac.in','9203',15,'Power Electronics'),
('Vikram','Mehta','vikram@jmi.ac.in','9204',16,'Machine Design'),
('Rahul','Das','rahul@jmi.ac.in','9205',17,'Transportation'),
('Shubham','Jain','shubham@jmi.ac.in','9206',18,'Metallurgy');


-- COURSE + MAPPINGS

INSERT INTO Course (courseCode,courseName,creditHours,year,semester) VALUES
('CS101','Data Structures',4,2025,1),('EC101','Digital Electronics',4,2025,1),
('EE101','Electrical Circuits',4,2025,1),('ME101','Thermodynamics',4,2025,1),
('CE101','Structural Engineering',4,2025,1),('MM101','Material Science',3,2025,1),
('CS201','Algorithms',4,2025,1),('EC201','Communication Systems',4,2025,1),
('EE201','Electrical Machines',4,2025,1),('ME201','Fluid Mechanics',4,2025,1),
('CE201','Geotechnical Engineering',4,2025,1),('MM201','Metallurgy',3,2025,1),
('CS301','Operating Systems',4,2025,1),('EC301','Signal Processing',4,2025,1),
('EE301','Power Electronics',4,2025,1),('ME301','Machine Design',4,2025,1),
('CE301','Transportation Engineering',4,2025,1),('MM301','Metallurgical Engineering',3,2025,1);

INSERT INTO DepartmentCourse VALUES
(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),
(7,7),(8,8),(9,9),(10,10),(11,11),(12,12),
(13,13),(14,14),(15,15),(16,16),(17,17),(18,18);

INSERT INTO CourseInstructor VALUES
(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),
(7,7),(8,8),(9,9),(10,10),(11,11),(12,12),
(13,13),(14,14),(15,15),(16,16),(17,17),(18,18);


-- BOOK + AUTHOR + KEYWORD + CATEGORY

INSERT INTO Book (title,isbn,publisher,publicationDate,edition,language,type,purchaseOption,format,price,rentalPrice,quantity,rating) VALUES
('Data Structures and Algorithm Analysis','9780201612516','Pearson','2012-01-15',3,'English','new','buy','hardcover',800,100,50,4.5),
('Digital Electronics','9780070141706','McGraw-Hill','2013-05-10',2,'English','new','buy','softcover',700,90,40,4.3),
('Electrical Engineering Principles','9780199493128','Oxford','2014-06-20',2,'English','new','rent','hardcover',750,110,30,4.4),
('Engineering Thermodynamics','9788131705671','McGraw-Hill','2015-03-15',3,'English','new','buy','hardcover',850,120,35,4.6),
('Structural Analysis','9789332542546','Pearson','2016-08-10',1,'English','used','buy','softcover',600,80,25,4.2),
('Introduction to Metallurgy','9788126518477','Wiley','2017-09-05',2,'English','new','rent','hardcover',900,150,20,4.7);

INSERT INTO Author (authorName) VALUES
('Mark Allen Weiss'),('Anil K Maini'),('Del Toro'),
('P K Nag'),('S S Bhavikatti'),('S H Avner');

INSERT INTO BookAuthor VALUES
(1,1),(2,2),(3,3),(4,4),(5,5),(6,6);

INSERT INTO Keyword (keyword) VALUES
('Data Structures'),('Digital Circuits'),('Electrical Machines'),
('Thermodynamics'),('Structural Engineering'),('Metallurgy');

INSERT INTO BookKeyword VALUES
(1,1),(2,2),(3,3),(4,4),(5,5),(6,6);

INSERT INTO Category (name,description) VALUES
('Computer Science','CS books'),
('Electronics','ECE books'),
('Electrical','Electrical books'),
('Mechanical','Mechanical books'),
('Civil','Civil books'),
('Metallurgy','Metallurgy books');

INSERT INTO BookCategory VALUES
(1,1),(2,2),(3,3),(4,4),(5,5),(6,6);

INSERT INTO CourseBook (courseID,bookID,instructorID,year,semester,bookType) VALUES
(1,1,1,2025,1,'required'),
(2,2,2,2025,1,'required'),
(3,3,3,2025,1,'required'),
(4,4,4,2025,1,'required'),
(5,5,5,2025,1,'required'),
(6,6,6,2025,1,'required');


-- CART + ORDER + PAYMENT + REVIEW + TICKET

INSERT INTO Cart (studentID) VALUES (1),(2),(3),(4),(5),(6),(7),(8),(9);

INSERT INTO CartItem (cartID,bookID,quantity,purchaseType) VALUES
(1,1,1,'buy'),(2,2,1,'rent'),(3,3,1,'buy'),
(4,4,1,'rent'),(5,5,1,'buy'),(6,6,1,'rent');

INSERT INTO `Order` (studentID,orderNumber,shippingType,dateCreated,dateShipped,dateFulfilled,orderStatus,totalAmount,finalAmount) VALUES
(1,'ORD001','2-day',NOW(),NOW(),DATE_ADD(NOW(),INTERVAL 2 DAY),'delivered',800,800),
(2,'ORD002','standard',NOW(),NULL,NULL,'processing',700,700),
(3,'ORD003','1-day',NOW(),NOW(),DATE_ADD(NOW(),INTERVAL 1 DAY),'shipped',750,750),
(4,'ORD004','express',NOW(),NOW(),DATE_ADD(NOW(),INTERVAL 1 DAY),'pending',850,850),
(5,'ORD005','standard',NOW(),NOW(),DATE_ADD(NOW(),INTERVAL 3 DAY),'delivered',600,600);

INSERT INTO OrderBook (orderID,bookID,quantity,purchaseType,pricePerUnit,subtotal) VALUES
(1,1,1,'buy',800,800),
(2,2,1,'buy',700,700),
(3,3,1,'rent',750,750),
(4,4,1,'buy',850,850),
(5,5,1,'buy',600,600);

INSERT INTO Payment (orderID,amount,paymentMethod,paymentStatus,transactionID) VALUES
(1,800,'card','successful','TXN001'),
(2,700,'upi','successful','TXN002'),
(3,750,'netbanking','pending','TXN003'),
(4,850,'card','failed','TXN004'),
(5,600,'upi','successful','TXN005');

INSERT INTO Review (studentID,bookID,rating,reviewText,isVerifiedPurchase) VALUES
(1,1,5,'Excellent',TRUE),
(2,2,4,'Good',TRUE),
(3,3,5,'Best',TRUE),
(4,4,4,'Nice',FALSE),
(5,5,3,'Average',TRUE);

INSERT INTO TicketCategory (categoryName,description) VALUES
('Products','Book issues'),
('Orders','Delivery issues'),
('Cart','Cart issues'),
('Account','User issues'),
('Other','General queries');

INSERT INTO Ticket (studentID,employeeID,categoryID,title,description,status) VALUES
(1,NULL,1,'Book issue','Not available','new'),
(2,2,2,'Order delay','Late','assigned'),
(3,3,3,'Cart issue','Not adding','new');

INSERT INTO TicketHistory (ticketID,previousStatus,newStatus,changedByEmployeeID) VALUES
(2,'new','assigned',2),
(3,'new','assigned',3);