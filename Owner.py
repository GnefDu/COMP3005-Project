import psycopg2


# Print menu
def menu():
    print("\n(1) View selection of books")
    print("(2) Add a book to inventory")
    print("(3) Remove a book from inventory")
    print("(4) View sales by publisher")
    print("(5) View sales by author")
    print("(6) View sales genre")
    print("(7) View all time sales")
    print("(8) Add book stock to inventory")
    print("(0) Exit")

# Function owner performs queries based on user choice
def owner(choice, cursor):
    # Print all books
    if choice == "1":
        cursor.execute("SELECT * FROM book")
        result = cursor.fetchall()
        for i in range(len(result)):
            print("ISBN: " + str(result[i][0]) + ", Title: " + result[i][1] + ", Author: " + result[i][2] + ", Genre: " + result[i][3] + ", Pages: ", str(result[i][4]) + 
			", Price: $" + str(result[i][5]) + ", In Stock: " + str(result[i][6]))
    # Add a new book to inventory
    elif choice == "2":
        print("Adding book to inventory")
        book_isbn = input("ISBN: ")
        book_title = input("Title: ")
        book_author = input("Author: ")
        book_genre = input("Genre: ")
        book_pages = input("# Pages: ")
        book_price = input("Selling price: ")
        stock = 0
        
        cursor.execute("Select publisher_ID, name from publisher")
        result = cursor.fetchall()
        for i in range(len(result)):
            print("(" + str(i + 1) + ") Publisher name: " + result[i][1])
        publisher_select = input("Select the publisher of the book: ")
        if int(publisher_select) <= len(result) and int(publisher_select) > 0:
            publisher_id = result[int(publisher_select) - 1][0]
            cursor.execute("Insert into book values (%s, %s, %s, %s, %s, %s, %s, %s)", (book_isbn, book_title, book_author, book_genre, book_pages, book_price, str(stock), publisher_id))
            print(book_title + " has been added to inventory")
        else:
            print("Not a valid choice")
        
    # Remove a book from inventory
    elif choice == "3":
        cursor.execute("SELECT * FROM book")
        result = cursor.fetchall()
        for i in range(len(result)):
            print("(" + str(i + 1) + ") ISBN: " + str(result[i][0]) + ", Title: " + result[i][1] + ", Author: " + result[i][2] + ", Genre: " + result[i][3] + ", Pages: ", str(result[i][4]) + 
			", Price: " + str(result[i][5]) + ", In Stock: " + str(result[i][6]))	
        user_input = input("\nPlease choose a book to remove from inventory:\n")
        book_index = int(user_input) - 1
        if book_index + 1 > len(result):
            print("You have chosen a book that does exist in our inventory. Please try again")
            return
        print("You have removed: ")
        print("ISBN: " + str(result[book_index][0]) + ", Title: " + result[book_index][1] + ", Author: " + result[book_index][2] + 
			", Genre: " + result[book_index][3] + ", Pages: ", str(result[book_index][4]) + 
			", Price: " + str(result[book_index][5]) + ", In Stock: " + str(result[book_index][6]))
        cursor.execute("delete from book where ISBN = " + (str(result[book_index][0])))
    # View sales and profit margins per publisher
    elif choice == "4":
        cursor.execute("Select publisher_ID, name from publisher")
        result = cursor.fetchall()
        for i in range(len(result)):
            print("(" + str(i + 1) + ") Publisher name: " + result[i][1])
        publisher_select = input("Select the publisher to view sales data for: ")
        sales = 0
        count = 0
        if int(publisher_select) <= len(result) + 1 and int(publisher_select) > 0:
            cursor.execute("select book.price, sum(order_amount), publisher_ID from order_contains inner join book on order_contains.isbn = book.isbn where publisher_id = " + str(int(publisher_select)) +
            "group by publisher_Id, book.price")
            result = cursor.fetchall()
            for i in range(len(result)):
                sales += float(result[i][0]) * int(result[i][1])
                count += int(result[i][1])
            cursor.execute("Select commission_percent, name from publisher where publisher_id = " + publisher_select)
            commission = cursor.fetchone()
            print("Total sales for " + commission[1] + ": $" + str(round(sales, 2)))
            print("Total profit for " + commission[1] + ": $" + str(sales - (5*count) - (sales * float(commission[0]) / 100 )))
        else:
            print("Not a valid choice")
            return
    # View sales and profit margins by author
    elif choice == "5":
        cursor.execute("Select author from book")
        result = cursor.fetchall()
        for i in range(len(result)):
            print("(" + str(i + 1) + ") Author name: " + result[i][0])
        author_select = input("Select the author to view sales data for: ")
        sales = 0
        count = 0
        if int(author_select) <= len(result) + 1 and int(author_select) > 0:
            author = result[int(author_select) - 1][0]
            cursor.execute("select book.price, sum(order_amount), author from order_contains inner join book on order_contains.isbn = book.isbn where author = '" + author +
            "' group by author, book.price")
            result = cursor.fetchall()
            for i in range(len(result)):
                sales += float(result[i][0]) * int(result[i][1])
                count += int(result[i][1])
            print("Total sales for " + author + ": $" + str(round(sales, 2)))
            print("Total profit for " + author + ": $" + str(sales - (5*count)))
        else:
            print("Not a valid choice")
            return
    # View sales and profit margins by genre
    elif choice == "6":
        cursor.execute("Select distinct genre from book")
        result = cursor.fetchall()
        for i in range(len(result)):
            print("(" + str(i + 1) + ") Genre: " + result[i][0])
        genre_select = input("Select the genre to view sales data for: ")
        sales = 0
        count = 0
        if int(genre_select) <= len(result) + 1 and int(genre_select) > 0:
            genre = result[int(genre_select) - 1][0]
            cursor.execute("select book.price, sum(order_amount), genre from order_contains inner join book on order_contains.isbn = book.isbn where genre = '" + genre +
            "' group by genre, book.price")
            result = cursor.fetchall()
            for i in range(len(result)):
                sales += float(result[i][0]) * int(result[i][1])
                count += int(result[i][1])
            print("Total sales for " + genre + ": $" + str(round(sales, 2)))
            print("Total profit for " + genre + ": $" + str(sales - (5*count)))
        else:
            print("Not a valid choice")
            return
    # View sales and profit margins
    elif choice == "7":
        cursor.execute("select book.price, sum(order_amount) from order_contains  inner join book on order_contains.isbn = book.isbn group by book.price")
        result = cursor.fetchall()
        sales = 0
        count = 0
        for i in range(len(result)):
            sales += float(result[i][0]) * int(result[i][1])
            count += int(result[i][1])
        print("Total sales: $" + str(round(sales, 2)))
        print("Total profit: $" + str(sales - (5*count)))
    # Add stock to inventory
    elif choice == "8":
        cursor.execute("SELECT * FROM book")
        result = cursor.fetchall()
        for i in range(len(result)):
            print("(" + str(i + 1) + ") ISBN: " + str(result[i][0]) + ", Title: " + result[i][1] + ", Author: " + result[i][2] + ", Genre: " + result[i][3] + ", Pages: ", str(result[i][4]) + 
			", Price: " + str(result[i][5]) + ", In Stock: " + str(result[i][6]))	
        user_input = input("\nPlease choose a book:\n")
        book_index = int(user_input) - 1
        if book_index + 1 > len(result):
            print("You have chosen a book that does exist in our inventory. Please try again")
            return
        print("You have chosen: ")
        print("ISBN: " + str(result[book_index][0]) + ", Title: " + result[book_index][1] + ", Author: " + result[book_index][2] + 
			", Genre: " + result[book_index][3] + ", Pages: ", str(result[book_index][4]) + 
			", Price: " + str(result[book_index][5]) + ", In Stock: " + str(result[book_index][6]))
        number_ordered = input("How many would you like to add to stock? ")
        cursor.execute("Update book set stock = stock + (%s) where ISBN = (%s)", (number_ordered, str(result[book_index][0])))
        print("Stock updated, email sent to publisher")
    elif choice == "0":
        quit()
        
      
    else:
        print("Please enter a valid choice")

try:
    conn = psycopg2.connect(
	dbname = "Project",
	user = "postgres",
	password = "7676",
	host = "localhost",
	port = "5432"
	)
    cur = conn.cursor()
    while True:
        menu()
        choice = input("Please enter your selection: ")
        owner(choice, cur)
        conn.commit()

 

except psycopg2.OperationalError:
	print("Unable to connect\n Now exitting")
	quit()