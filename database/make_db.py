import sqlite3 


try:
    con = sqlite3.connect('mydatabase.db')
    con.execute('CREATE TABLE accounts (username TEXT, password TEXT, email TEXT, name TEXT, isAdmin INT)')
    print ('Table created successfully');
    con.commit()
    con.close()
    
    con = sqlite3.connect('mydatabase.db')
    con.execute('CREATE TABLE newbooks (book_name TEXT, author_name TEXT, date INT, isbn_13 INT primary key, photo TEXT NOT NULL, trade_price INT, retail_price INT, quantity INT,bookdscr TEXT)')
    con.commit()
    con.close()
    print ('Table created successfully');
    
    con = sqlite3.connect('mydatabase.db')
    con.execute('CREATE TABLE books (id INT, name TEXT, author TEXT, rating INT, Quantity INT, photo TEXT NOT NULL )')
    con.commit()
    con.close()
    print ('Table created successfully');
    
    con = sqlite3.connect('mydatabase.db')
    con.execute('CREATE TABLE products (id INT,  name TEXT, photo TEXT, price INT, quantity INT )')
    con.commit()
    con.close()
    print ('Table created successfully');
    
    
    

    
except:
    pass








