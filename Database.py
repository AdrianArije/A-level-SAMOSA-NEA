import sqlite3

# Connect to a database
conn = sqlite3.connect("Database.db")

# Create a cursor
cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = ON")

# Create a table
cursor.executescript("""
CREATE TABLE Roles(
    Role_ID INTEGER PRIMARY KEY,
    Role_Name VARCHAR(40)
    );

CREATE TABLE Categories(
    Category_ID INTEGER PRIMARY KEY,
    Category_Name VARCHAR(40)
    );

CREATE TABLE Users (
    User_ID INTEGER PRIMARY KEY,
    Username VARCHAR(40) NOT NULL,
    PasswordHash VARCHAR(255),
    Role_ID INTEGER,
    FOREIGN KEY (Role_ID) REFERENCES Roles(Role_ID)
);

CREATE TABLE MenuItems(
    Item_ID INTEGER PRIMARY KEY,
    Item_Name VARCHAR(40),
    Item_Description VARCHAR(100),
    Image VARCHAR(2083),
    Quantity INTEGER,
    Price DECIMAL(10,2),
    Category_ID INTEGER,
    FOREIGN KEY (Category_ID) REFERENCES Categories(Category_ID)
);
 

CREATE TABLE Orders(
    Order_ID INTEGER PRIMARY KEY,
    User_ID INTEGER,
    Total_Price DECIMAL(10,2),
    DateTime DATETIME,
    Status BOOLEAN,
    FOREIGN KEY (User_ID) REFERENCES Users(User_ID)
);

CREATE TABLE OrderItems(
    OrderItems_ID INTEGER PRIMARY KEY,
    Orders_ID INTEGER,
    Item_ID INTEGER,
    Quantity INTEGER,
    Price DECIMAL(10,2),
    FOREIGN KEY (Orders_ID) REFERENCES Orders(Order_ID),
    FOREIGN KEY (Item_ID) REFERENCES MenuItems(Item_ID)
);
""")

# Save changes
conn.commit()

# Close the connection
conn.close()

print("Table created successfully!")