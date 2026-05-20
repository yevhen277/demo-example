-- Created by GitHub Copilot in SSMS - review carefully before executing

-- 1. 创建 Accounts 表
CREATE TABLE Accounts (
    username NVARCHAR(100) NOT NULL PRIMARY KEY,
    password NVARCHAR(255) NOT NULL,
    role NVARCHAR(50) NOT NULL,
    student_id NVARCHAR(100) NULL 
);

-- 2. 创建 Students 表
CREATE TABLE Students (
    student_id NVARCHAR(100) NOT NULL PRIMARY KEY,
    name NVARCHAR(100) NOT NULL,
    gender NVARCHAR(10) NOT NULL,
    major NVARCHAR(100) NOT NULL,
    account_username NVARCHAR(100) NOT NULL,
    -- 建立与 Accounts 的外键关联
    CONSTRAINT FK_Students_Accounts FOREIGN KEY (account_username) REFERENCES Accounts(username)
);

-- 3. 创建 Courses 表
CREATE TABLE Courses (
    course_id NVARCHAR(100) NOT NULL PRIMARY KEY,
    name NVARCHAR(200) NOT NULL,
    time INT NOT NULL,
    score INT NOT NULL,
    teacher NVARCHAR(100) NOT NULL,
    location NVARCHAR(200) NOT NULL,
    shared NVARCHAR(100) NOT NULL,
    capacity INT NOT NULL DEFAULT 30
);

-- 4. 创建 Enrollments 表
CREATE TABLE Enrollments (
    enrollment_id NVARCHAR(100) NOT NULL PRIMARY KEY,
    student_id NVARCHAR(100) NOT NULL,
    course_id NVARCHAR(100) NOT NULL,
    score INT NOT NULL,
    source_college_id NVARCHAR(100) NOT NULL,
    target_college_id NVARCHAR(100) NOT NULL,
    origin NVARCHAR(100) NOT NULL,
    status NVARCHAR(50) NOT NULL DEFAULT 'ENROLLED',
    -- 设置默认值为 UTC 当前时间，以匹配 Python 中的 default_factory=utc_now
    created_at DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    updated_at DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    
    -- 建立主外键关系
    CONSTRAINT FK_Enrollments_Students FOREIGN KEY (student_id) REFERENCES Students(student_id),
    CONSTRAINT FK_Enrollments_Courses FOREIGN KEY (course_id) REFERENCES Courses(course_id)
);