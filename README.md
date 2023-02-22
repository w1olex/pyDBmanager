REQUIREMENTS FOR RUNNING THE PROGRAM:

To run the program, a MySQL database called alfa_3 is needed, which is included with the file, either as a script or as an export.

The necessary applications to run the script are MySQL Workbench (preferably version 8.0 or higher). Since I hosted my database on localhost, I used XAMPP application in which I started the MySQL server.

After running the script, the alfa_3 database is created, and a user (user: uzivatel, password: alfa123) is created with the following command:

CREATE USER 'uzivatel'@'localhost' IDENTIFIED BY 'alfa123';

The user is then granted privileges with the following command:

GRANT ALL PRIVILEGES ON alfa_3.* TO 'uzivatel'@'localhost';

After that, 6 tables and 2 views are created.

All of the above mentioned things are absolutely necessary for the functionality of the program.

The user interface to the database is written in Python (version 3.8.10) and was programmed in the PyCharm development environment (version 2020.2.3).

To enable the connection with the database, the mysql-connector-python module was installed, which can be installed using the command:

pip install mysql-connector-python

The subsequent configuration of the database connection is entered manually into the console after the program is started. All instructions that the program requires from the user are displayed in the console.

USER INTERFACE:

Setting the configuration file: The program allows the user to set their own configuration file. The user can set user, password, host, and database (if the user has not set a password, leave the password field empty).

Menu: The main menu has a total of 6 options:

Work with tables (customer, product, order, delivery, supplier) The user can select, insert, update, and delete all tables in the database. 
If the user wants to delete a customer who is already listed in an order, the program will alert the user of where and what exactly needs to be deleted first.
The user can use the select statement to display the exact ID of each order. Load data into CSV file to tables [customer, product, supplier] 
The user can load data from their csv file into tables and products. The file must be named 'customer.csv', 'product.csv', or 'supplier.csv' and must be 
located in the /imports/ folder. Perform a transaction between two accounts The user can transfer credit from one customer account to another. 
If the customer has insufficient credit, a rollback will be performed (returning data to its state before the transaction). 
Display current data in all tables The user can view all current data in the database. Generate a summary report of orders and deliveries 
The user can generate 2 reports: a) details of the order This report is used to display the order and its associated data. 
Contains information from 4 tables: order, customer, order_products, product Presents data: order.id, 
order.order_date, customer.name, product.name, product.price, order.quantity, order.status
