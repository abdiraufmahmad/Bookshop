from flask import Flask, render_template, request
from Stock import Books 
import sqlite3

app = Flask(__name__)

#Calling function
booksdata = Books()
isAdmin = None
shoppingcart = [] # Variable in array

#Setting up global variable
def setAdmin(value):
    global isAdmin  
    isAdmin = value
    
#isAdmin will be one if a user logins

#Home Page
@app.route("/home")
def home():
    return showBooks() # Returning show books function to home page to display the current books in stock

#Code to show entered form onto stock level html page

def showForm():
    con = sqlite3.connect("./database/mydatabase.db") 
    con.row_factory = sqlite3.Row #Setting up sqlite to use rows as main data structure
    cur = con.cursor() # It sets up so i can query database
    cur.execute("SELECT * from newbooks ;") # Executes database to select specific information from table newbooks
    rows = cur.fetchall(); # Grabs the data for my query in like python structure
    print(rows) # prints rows
    return render_template("stocklevel.html", rows=rows, isAdmin=isAdmin)
    
#Code to show the current books in stocklevel    
def showBooks():
    con = sqlite3.connect("./database/mydatabase.db") #Establish connection to database
    con.row_factory = sqlite3.Row #Setting up sqlite to use rows as main data structure
    cur = con.cursor() #Set up to query database
    cur.execute("SELECT * from books ;") # Executes database to select specific information from table newbooks
    rows = cur.fetchall(); # Grabs the data for my query in like python structure
    print(rows)  # prints rows
    return render_template("home.html", rows=rows, isAdmin=isAdmin)


#Form to add stock
def do_add_stock(formInfo): # Defined do_add_stock and gave argument formInfo.
    
    bookname = formInfo['book_name'] # Save form information entered into bookname and store into column
    aname = formInfo['author_name']
    Publication = formInfo['date']
    isbn = formInfo['isbn_13']
    img = formInfo['photo']
    trade = formInfo['trade_price']
    retail= formInfo['retail_price']
    quantity = formInfo['quantity']
    bookdscrp = formInfo['bookdscrp']
     
    con = sqlite3.connect("./database/mydatabase.db")  # Connecting my sql database 
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT isbn_13 FROM newbooks where isbn_13 = ?;", (isbn,)) 
    rows = cur.fetchall();
    
    if len(rows) > 0: #if length of rows is more than 0 then the database is executed
        
        # Update code goes here for isbn_13 if an existing book is added
        con = sqlite3.connect("./database/mydatabase.db") 
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("UPDATE newbooks SET isbn_13 = ?  where isbn_13 = ? ;", (isbn,))
        con.commit()
        con.close()
    
    else: # and if length of rows is not equal to 0 then the database is closed
        con.close()    
        
    
    con = sqlite3.connect("./database/mydatabase.db") 
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("INSERT INTO newbooks values(?,?,?,?,?,?,?,?,?);", (bookname,aname,Publication,isbn, img,trade,retail,quantity,bookdscrp))
    print("TEST 1")# Printing Test 1 to see if the values are inputted into the terminal
    con.commit()
    print("TEST 2") # Printing Test 2 to see if the values are inputted into the terminal
    con.close()
    print("TEST 3")# Printing Test 3 to see if the values are inputted into the terminal

#Should display added stock onto stocklevel.html  #redirect to stock level page  
@app.route("/stocklevel", methods = ['POST']) # Form
def addStock(): #Defined function add stock to call upon later
    do_add_stock(request.form) # Get data requested by do_add_stock
    return showForm() #Function to show inputted form and redirect it to stock level page 

#Add Stock Page 
@app.route("/addstock") #Setting up App Route to url add stock
def do_stock(): # Assigned function 
    return render_template("addstock.html", isAdmin = isAdmin )

#Url to redirect to stock level page
@app.route("/stocklevel") #Page
def stocklevels():# Assigned function stock levels 
    return showForm() # Returning function created early to show information entered on add stock page onto stock level page



def do_user_login(formData): # When function ran later we will give the form data parameter is equal to the formdata the user entered
    
    username = formData['username'] #Get username form data and assigning to variable , # What user enters into form
    password = formData['pwd']
    
    con = sqlite3.connect("./database/mydatabase.db") 
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * from accounts where username = ? and password = ?;", (username,password))
    rows = cur.fetchall(); # [ { name: 'admin', password: 'p455sw0rd', ..., isAdmin: 1 } ]
    if len(rows) > 0: #If length of rows is more than 0 
        global isAdmin #We assign global vairable is admin
        isAdmin = rows[0][4] # Accessing first item in the array = object. 
        print(isAdmin)
        return True #if the above is true then we return true
    else: #otherwise we return False
        return False  
    print (rows)

#route url to login page
@app.route("/")
def login():
    return render_template("login.html")

#Route to user-login page
@app.route("/user-login", methods = ['POST'])
def let_user_login(): #Defined function let user login
    login_result = do_user_login(request.form)
    if login_result == True: #if 
        return render_template("home.html", isAdmin=isAdmin) # After user logins in correctly should redirect the user to the home page
    else: 
        return "FALSE" # If user does not login with correct credentials return FALSE
    
# Take form data and stores it into database
def do_add_account(formData): # Function 
    
    username = formData['username'] #Get get username stores it into form data and pass to username 
    password = formData['pwd']
    email = formData['email']
    name = formData['name']
    admin = 0 # boo lean value
    
    if ('user-admin' in formData):
        admin = 1
    
      
    con = sqlite3.connect("./database/mydatabase.db") 
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("INSERT INTO accounts values(?,?,?,?,?);", (username,password,email,name, admin)) # Insert into accounts table column registration form
    con.commit()
    con.close()
        

#Sets up url to run specific logic        
@app.route("/add-account", methods = ['POST']) # Making add account method post
def addAccount():
    do_add_account(request.form) #Request information added into form data
    return render_template("home.html") #Return to home page


#Registration 
#APP ROUTE TO REGISTERATION .HTML 
#FUNCTION CALLED REGISTER CREATED 

@app.route("/register")
def register():
    return render_template("registration.html")

#Shopping Cart HTML Route & To make Books added to cart stay when page is refreshedf
@app.route("/shoppingcart")
def shopping_cart():
    con = sqlite3.connect("./database/mydatabase.db") #Establish connection to database
    con.row_factory = sqlite3.Row #Setting up sqlite to use rows as main data structure
    cur = con.cursor() #Set up to query database
    print (shoppingcart)
    cur.execute("SELECT * from products WHERE id IN ({0})".format(', '.join('?' for _ in shoppingcart)), shoppingcart)# I got the code from .format until the for_in from stack overflow for how to use a list in a sql query 
    rows = cur.fetchall(); # Grabs the data for my query in like python structure
    print(rows)  # prints rows
    return render_template("shoppingcart.html", products=rows, isAdmin=isAdmin)

   

@app.route("/shoppingcart", methods = ['POST']) #Post method Shopping Cart 
def shopping_button():
    return showCart(request.args.get("id")) #use request.arg.get for information from the url
                   


def showCart(id):
    shoppingcart.append(id)#Adding id to shopping cart list
    con = sqlite3.connect("./database/mydatabase.db") #Establish connection to database
    con.row_factory = sqlite3.Row #Setting up sqlite to use rows as main data structure
    cur = con.cursor() #Set up to query database
    print (shoppingcart)
    cur.execute("SELECT * from products WHERE id IN ({0})".format(', '.join('?' for _ in shoppingcart)), shoppingcart)# I got the code from .format until the for_in from stack overflow for how to use a list in a sql query 
    rows = cur.fetchall(); # Grabs the data for my query in like python structure
    print(rows)  # prints rows
    return render_template("shoppingcart.html", products=rows, isAdmin=isAdmin)


@app.route("/delete", methods = ['POST'])
def delete_cart():
    id_to_delete = shoppingcart.index(request.args.get('id')) # saving to variable 
    del shoppingcart[id_to_delete] # delete function
    con = sqlite3.connect("./database/mydatabase.db") #Establish connection to database
    con.row_factory = sqlite3.Row #Setting up sqlite to use rows as main data structure
    cur = con.cursor() #Set up to query database
    cur.execute("SELECT * from products WHERE id IN ({0})".format(', '.join('?' for _ in shoppingcart)), shoppingcart)# I got the code from .format until the for_in from stack overflow for how to use a list in a sql query 
    rows = cur.fetchall(); # Grabs the data for my query in like python structure
    return render_template("shoppingcart.html", products=rows, isAdmin=isAdmin)



if __name__ ==  '__main__':
    app.run(debug=true)











































