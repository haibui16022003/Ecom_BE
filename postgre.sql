-- Create the Users table
CREATE TABLE Users (
    UserID INT PRIMARY KEY,
    Username VARCHAR(255) NOT NULL,
    Password VARCHAR(255) NOT NULL,
    Role VARCHAR(50),
    roleCode VARCHAR(50),
    active BOOLEAN,
    displayName VARCHAR(255),
    address VARCHAR(255),
    phoneNumber VARCHAR(20)
);

-- Create the Category table
CREATE TABLE Category (
    CategoryID INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Create the Product table
CREATE TABLE Product (
    ProductID INT PRIMARY KEY,
    CategoryID INT,
    name VARCHAR(255) NOT NULL,
    quantity INT,
    price DECIMAL(10, 2),
    active BOOLEAN,
    createTime TIMESTAMP,
    imgProduct VARCHAR(255),
    FOREIGN KEY (CategoryID) REFERENCES Category(CategoryID)
);

-- Create the WishList table
CREATE TABLE WishList (
    WishID INT PRIMARY KEY,
    UserID INT,
    ProductID INT,
    FOREIGN KEY (UserID) REFERENCES User(UserID),
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
);

-- Create the Cart table
CREATE TABLE Cart (
    CartID INT PRIMARY KEY,
    totalPrice DECIMAL(10, 2),
    userID INT,
    FOREIGN KEY (userID) REFERENCES User(UserID)
);

-- Create the CartDetail table
CREATE TABLE CartDetail (
    CartDetailID INT PRIMARY KEY,
    CartID INT,
    ProductID INT,
    Subtotal DECIMAL(10, 2),
    Quantity INT,
    FOREIGN KEY (CartID) REFERENCES Cart(CartID),
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
);

-- Create the Invoice table
CREATE TABLE Invoice (
    InvoiceID INT PRIMARY KEY,
    UserID INT,
    date TIMESTAMP,
    TotalPrice DECIMAL(10, 2),
    status VARCHAR(50),
    FOREIGN KEY (UserID) REFERENCES User(UserID)
);

-- Create the InvoiceDetail table
CREATE TABLE InvoiceDetail (
    InvoiceDetailID INT PRIMARY KEY,
    InvoiceID INT,
    ProductID INT,
    Quantity INT,
    Subtotal DECIMAL(10, 2),
    FOREIGN KEY (InvoiceID) REFERENCES Invoice(InvoiceID),
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
);
