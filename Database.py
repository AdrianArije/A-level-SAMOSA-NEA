import sqlite3

# Connect to a database
conn = sqlite3.connect("Database.db")

# Create a cursor
cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = ON")

# Create a table
# cursor.executescript("""
# CREATE TABLE Roles(
#     Role_ID INTEGER PRIMARY KEY,
#     Role_Name VARCHAR(40)
#     );

# CREATE TABLE Categories(
#     Category_ID INTEGER PRIMARY KEY,
#     Category_Name VARCHAR(40)
#     );

# CREATE TABLE Users (
#     User_ID INTEGER PRIMARY KEY,
#     Username VARCHAR(40) NOT NULL,
#     PasswordHash VARCHAR(255),
#     Role_ID INTEGER,
#     FOREIGN KEY (Role_ID) REFERENCES Roles(Role_ID)
# );

# CREATE TABLE MenuItems(
#     Item_ID INTEGER PRIMARY KEY,
#     Item_Name VARCHAR(40),
#     Item_Description VARCHAR(100),
#     Image VARCHAR(2083),
#     Quantity INTEGER,
#     Price DECIMAL(10,2),
#     Category_ID INTEGER,
#     FOREIGN KEY (Category_ID) REFERENCES Categories(Category_ID)
# );
 

# CREATE TABLE Orders(
#     Order_ID INTEGER PRIMARY KEY,
#     User_ID INTEGER,
#     Total_Price DECIMAL(10,2),
#     DateTime DATETIME,
#     Status BOOLEAN,
#     FOREIGN KEY (User_ID) REFERENCES Users(User_ID)
# );

# CREATE TABLE OrderItems(
#     OrderItems_ID INTEGER PRIMARY KEY,
#     Orders_ID INTEGER,
#     Item_ID INTEGER,
#     Quantity INTEGER,
#     Price DECIMAL(10,2),
#     FOREIGN KEY (Orders_ID) REFERENCES Orders(Order_ID),
#     FOREIGN KEY (Item_ID) REFERENCES MenuItems(Item_ID)
# );
# """)


# categories = [
#     (1, "Meals"),
#     (2, "Snacks"),
#     (3, "Drinks"),
#     (4, "Desserts")
# ]

# cursor.executemany("""
#     INSERT INTO Categories (Category_ID, Category_Name)
#     VALUES (?, ?)
# """, categories)

# menu_items = [
#     # Meals
# (1, "Chicken Wrap",
#  "Grilled chicken with lettuce and sauce in a tortilla.",
#  "Images/Chicken-Wrap.jpg", 15, 3.50, 1),

# (2, "Cheese Burger",
#  "Beef burger with cheese, lettuce and burger sauce.",
#  "Images/Cheese-Burger.jpg", 12, 4.25, 1),

# (3, "Margherita Pizza",
#  "Pizza topped with tomato sauce, mozzarella and herbs.",
#  "Images/Margherita-Pizza.jpg", 10, 4.50, 1),

# (4, "Chicken Pasta",
#  "Pasta with grilled chicken and a creamy tomato sauce.",
#  "Images/Chicken-Pasta.jpg", 8, 4.75, 1),

# (5, "Veggie Wrap",
#  "Mixed vegetables, lettuce and sauce in a tortilla.",
#  "Images/Veggie-Wrap.jpg", 10, 3.25, 1),

# # Snacks
# (6, "Crisps",
#  "Lightly salted potato crisps in a small packet.",
#  "Images/Crisps.jpg", 25, 1.00, 2),

# (7, "Cheese Toastie",
#  "Toasted bread filled with melted cheese.",
#  "Images/Cheese-Toastie.jpg", 15, 2.25, 2),

# (8, "Chicken Nuggets",
#  "Crispy chicken nuggets served as a small snack portion.",
#  "Images/Chicken-Nuggets.jpg", 20, 2.50, 2),

# (9, "Popcorn",
#  "Lightly salted popcorn in a convenient snack bag.",
#  "Images/Popcorn.jpg", 18, 1.50, 2),

# (10, "Fruit Cup",
#  "A fresh selection of chopped seasonal fruit.",
#  "Images/Fruit-Cup.jpg", 10, 2.00, 2),

# # Drinks
# (11, "Orange Juice",
#  "Refreshing orange juice served chilled.",
#  "Images/Orange-Juice.jpg", 15, 1.75, 3),

# (12, "Apple Juice",
#  "Refreshing apple juice served chilled.",
#  "Images/Apple-Juice.jpg", 15, 1.75, 3),

# (13, "Bottled Water",
#  "Still mineral water served in a sealed bottle.",
#  "Images/Bottled-Water.jpg", 30, 1.00, 3),

# (14, "Hot Chocolate",
#  "Warm chocolate drink topped with a light foam.",
#  "Images/Hot-Chocolate.jpg", 10, 2.25, 3),

# (15, "Iced Tea",
#  "Chilled tea drink with a refreshing fruity flavour.",
#  "Images/Iced-Tea.jpg", 12, 2.00, 3),

# # Desserts
# (16, "Chocolate Brownie",
#  "Soft chocolate brownie with a rich chocolate flavour.",
#  "Images/Chocolate-Brownie.jpg", 12, 2.00, 4),

# (17, "Chocolate Cookie",
#  "Soft baked cookie containing chocolate pieces.",
#  "Images/Chocolate-Cookie.jpg", 20, 1.50, 4),

# (18, "Vanilla Muffin",
#  "Soft vanilla muffin with a lightly sweet topping.",
#  "Images/Vanilla-Muffin.jpg", 15, 1.75, 4),

# (19, "Strawberry Yoghurt",
#  "Creamy yoghurt with a sweet strawberry flavour.",
#  "Images/Strawberry-Yoghurt.jpg", 10, 1.50, 4),

# (20, "Chocolate Cake",
#  "Moist chocolate cake with a smooth chocolate topping.",
#  "Images/Chocolate-Cake.jpg", 8, 2.50, 4)
# ]

# cursor.executemany("""
#     INSERT INTO MenuItems
#     (Item_ID, Item_Name, Item_Description, Image, Quantity, Price, Category_ID)
#     VALUES (?, ?, ?, ?, ?, ?, ?)
# """, menu_items)

# Save changes
conn.commit()

# Close the connection
conn.close()

print("Table added created successfully!")