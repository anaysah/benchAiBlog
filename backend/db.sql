CREATE DATABASE benchAiBlog_db CHARACTER SET UTF8MB4 COLLATE utf8mb4_general_ci;
CREATE USER 'django_user'@'localhost' IDENTIFIED WITH mysql_native_password BY 'String@123';
GRANT ALL PRIVILEGES ON *.* TO 'django_user'@'localhost';
FLUSH PRIVILEGES;