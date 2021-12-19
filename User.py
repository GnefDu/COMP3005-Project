import psycopg2
import random
import datetime

# Prints menu
def menu(login):
	if login == True:
		print("\n(1) View our selection of books")
		print("(2) Add a book to your cart")
		print("(3) View your cart")
		print("(4) Empty your cart")
		print("(5) Checkout")
		print("(6) Logout")
		print("(7) Add payment info")
		print("(8) View orders")
		print("(0) Exit")
	else:
		print("\n(1) View our selection of books")
		print("(2) Login")
		print("(3) Create account")
		print("(0) Exit")

# Guest function
def guest(choice, cursor):
	# View books
	if(choice == "1"):
		cursor.execute("SELECT * FROM book")
		result = cursor.fetchall()
		for i in range(len(result)):
			print("ISBN: " + str(result[i][0]) + ", Title: " + result[i][1] + ", Author: " + result[i][2] + ", Genre: " + result[i][3] + ", Pages: ", str(result[i][4]) + 
			", Price: $" + str(result[i][5]) + ", In Stock: " + str(result[i][6]))
		return False, None
	# Login to an existing account
	elif(choice == "2"):
		user_input = input("Please enter you account ID: \n")
		cursor.execute("SELECT account_ID FROM user_account WHERE account_ID = " + user_input)
		result = cursor.fetchone()
		if(result != None):			
			print("You are now logged in as user ID: " + str(result[0]))
			login = True
			account = result
			return login, account[0]
		else:
			print("That account does not exist")
			return False, None
	# Create a new account
	elif(choice == "3"):
		cursor.execute("SELECT account_ID FROM user_account")
		result = cursor.fetchall()
		user_account = result[-1][0] + 1
		user_name = input("Please enter your name: \n")
		user_email = input("Please enter your email address: \n")
		user_phone = input("Please enter your phone number: \n")
		cursor.execute("INSERT INTO user_account VALUES (%s, %s, %s, %s)", (user_account, user_name, user_email, user_phone))
		print("Your account ID is: " + str(user_account))
		return False, None
	# Quit program
	elif(choice == "0"):
		quit()
	else:
		print("Please enter a valid choice")
		return False, None

# Register user
def user(choice, cursor, ID):
	# View books
	if(choice == "1"):
		cursor.execute("SELECT * FROM book")
		result = cursor.fetchall()
		for i in range(len(result)):
			print("ISBN: " + str(result[i][0]) + ", Title: " + result[i][1] + ", Author: " + result[i][2] + ", Genre: " + result[i][3] + ", Pages: ", str(result[i][4]) + 
			", Price: $" + str(result[i][5]) + ", In Stock: " + str(result[i][6]))
	# Add books to cart
	# Inventory is printed when a user chooses a number correponding to a book
	elif(choice == "2"):
		cursor.execute("SELECT * FROM book")
		result = cursor.fetchall()
		for i in range(len(result)):
			print("(" + str(i + 1) + ") ISBN: " + str(result[i][0]) + ", Title: " + result[i][1] + ", Author: " + result[i][2] + ", Genre: " + result[i][3] + ", Pages: ", str(result[i][4]) + 
			", Price: " + str(result[i][5]) + ", In Stock: " + str(result[i][6]))	
		user_input = input("\nPlease choose a book:\n")
		book_index = int(user_input) - 1
		if book_index + 1 > len(result):
			print("You have chosen a book that does exist in our inventory. Please try again")
			return True, ID
		print("You have chosen: ")
		print("ISBN: " + str(result[book_index][0]) + ", Title: " + result[book_index][1] + ", Author: " + result[book_index][2] + 
			", Genre: " + result[book_index][3] + ", Pages: ", str(result[book_index][4]) + 
			", Price: " + str(result[book_index][5]) + ", In Stock: " + str(result[book_index][6]))
		number_ordered = input("How many would you like to order? ")
		if (int(number_ordered) <= result[book_index][6]):
			cursor.execute("SELECT * from in_cart where account_ID = (%s) and ISBN = (%s)", (ID, result[book_index][0]))
			check = cursor.fetchone()
			if check == None:
				cursor.execute("INSERT INTO in_cart VALUES (%s, %s, %s)", (result[book_index][0], ID, int(number_ordered)))
				cursor.execute("UPDATE book set stock = stock - (%s) where ISBN = (%s)", (int(number_ordered), result[book_index][0]))
			else:
				cursor.execute("UPDATE in_cart set cart_amount = cart_amount + (%s) where ISBN = (%s) and account_ID = (%s)", (int(number_ordered), result[book_index][0], ID))
				cursor.execute("UPDATE book set stock = stock - (%s) where ISBN = (%s)", (int(number_ordered), result[book_index][0]))
			print("You have added new items to your cart")
		elif int(number_ordered) <= result[book_index][6]:
			print("You are selecting a book that does not exist in our inventory")
		else:
			print("You are attempting to add more items than we have stock for, please try again")
	# View user cart
	elif(choice == "3"):
		cursor.execute("SELECT ISBN, cart_amount FROM in_cart where in_cart.account_ID = " + str(ID))
		result = cursor.fetchall()
		total = 0
		if result != None:
			for i in range(len(result)):
				cursor.execute("SELECT * from book where ISBN = " +  str((result[i][0])))
				book = cursor.fetchone()
				total += result[i][1] * book[5]
				print("ISBN: " + str(book[0]) + ", Title: " + book[1] + ", Author: " + book[2] + ", Genre: " + book[3] + ", Pages: ", str(book[4]) + 
					", Price: $" + str(book[5]) + " IN CART: " + str(result[i][1]))
			if(total == 0):
				print("\nYou have no items in your cart")
			print("\nCART TOTAL: $" + str(total))		

	# Empty user's cart
	elif choice == "4":
		cursor.execute("SELECT ISBN, cart_amount from in_cart where in_cart.account_ID = " + str(ID))
		result = cursor.fetchall()
		for i in range(len(result)):
			cursor.execute("UPDATE book set stock = stock + (%s) where ISBN = (%s)", (result[i][1], result[i][0]))
		cursor.execute("DELETE from in_cart where in_cart.account_ID = " + str(ID))
		print("Your cart has been emptied")

	# Checkout user card
	elif choice == "5":
		##  Print the cart
		cursor.execute("SELECT count(*) from in_cart where in_cart.account_ID = " + str(ID))
		count = cursor.fetchone()
		if count[0] == 0:
			print("Your cart is empty")
			return True, ID
		cursor.execute("SELECT ISBN, cart_amount FROM in_cart where in_cart.account_ID = " + str(ID))
		cart = cursor.fetchall()
		total = 0
		if cart != None:
			for i in range(len(cart)):
				cursor.execute("SELECT * from book where ISBN = " + str((cart[i][0])))
				book = cursor.fetchone()

				total += cart[i][1] * book[5]
			print("\nCART TOTAL: $" + str(total))

		# Show payment options
		cursor.execute("SELECT * from billing_info where billing_info.account_ID = " + str(ID))
		card = cursor.fetchall()
		if card != []:
			print("Here are your saved payment options: ")
			for i in range(len(card)):
				print("(" + str(i + 1) + ") Card: " + card[i][0] + ", Billing Address: " + card[i][1] + ", Shipping Address: " + card[i][2])

			card_choice = input("Please choose a card for payment: ")

			if int(card_choice) <= len(card) and int(card_choice) > 0:
				print("You have chosen card# : " + card[int(card_choice) - 1][0])

				cursor.execute("SELECT ISBN, cart_amount FROM in_cart where in_cart.account_ID = " + str(ID))
				cart_contents = cursor.fetchall()

				#Create a book_order
				cursor.execute("SELECT * from book_order")
				result = cursor.fetchall()
				order_number = result[-1][0] + 1
				now = datetime.datetime.now()
				datefmt = '%Y-%m-%d'
				date = now.strftime(datefmt)
				tracking_ID = random.randint(0, 2147483646)
				cursor.execute("Insert into book_order values (%s, %s, %s, %s, %s)", (order_number, date, tracking_ID, card[int(card_choice) - 1][0], ID))

				# Create order contains
				for i in range(len(cart)):
					cursor.execute("INSERT into order_contains values (%s, %s, %s)", (cart[i][0], order_number, cart[i][1]))
				# Send money to publisher
				commission = 0
				for i in range(len(cart)):
					cursor.execute("SELECT publisher_ID from book where ISBN = " + str((cart[i][0])))
					pub_ID = cursor.fetchone()[0]

					cursor.execute("SELECT price from book where ISBN = " + str((cart[i][0])))
					price = cursor.fetchone()[0]

					cursor.execute("Select commission_percent from publisher where publisher_ID = " + str(pub_ID))
					comm_percent = cursor.fetchone()[0]
					commission += round((comm_percent/100) * (float(price) * cart[i][1]), 2)

					cursor.execute("UPDATE bank_account set balance = balance + (%s) where publisher_ID = (%s)", (commission, pub_ID))
				
				# Delete cart
				cursor.execute("SELECT ISBN, cart_amount from in_cart where in_cart.account_ID = " + str(ID))
				result = cursor.fetchall()
				for i in range(len(result)):
					cursor.execute("UPDATE book set stock = stock + (%s) where ISBN = (%s)", (result[i][1], result[i][0]))
				cursor.execute("DELETE from in_cart where in_cart.account_ID = " + str(ID))

				print("Your order has been completed Order ID: " + str(order_number))


			else:
				print("Card option not available")


		else:
			print("You don't have any payment options. Please add one before attempting to checkout")


	# Logout
	elif choice == "6":
		print("You have been logged out")
		return False, None
	
	# Add a payment option
	elif choice == "7":
		print("Creating new payment option")
		card_num = input("Enter your card number: ")
		billing_add = input("Enter your billing address: ")
		shipping_add = input("Enter your shipping address: ")
		cursor.execute("SELECT count(*) from billing_info WHERE billing_info.card_number = '" + card_num + "'")
		result = cursor.fetchone()
		if result[0] == 0:
			cursor.execute("Insert into billing_info VALUES (%s, %s, %s, %s)", (card_num, billing_add, shipping_add, ID))
			print("Payment option added")
		else:
			print("Payment option already exists")


	# View previous orders and tracking numbers
	elif choice == "8":
		cursor.execute("Select count(*) from book_order where account_ID = " + str(ID))
		result = cursor.fetchone()[0]
		if result == 0:
			print("You don't have any orders")
			return True, ID
		cursor.execute("Select order_ID, tracking_ID from book_order where account_ID = " + str(ID))
		orders = cursor.fetchall()
		for i in range(len(orders)):
			print("(" + str(i + 1) + ") Order ID: " + str(orders[i][0]) + " Tracking #: " + str(orders[i][1]))
		# User select a previous order to view
		user = input("Please select an order to view contents: ")
		if int(user) <= len(orders) and int(user) > 0:
			cursor.execute("Select book.ISBN, title, author, order_amount from order_contains inner join book on book.ISBN = order_contains.isbn where order_ID = " + str(orders[int(user) - 1][0]))
			result = cursor.fetchall()
			for i in range(len(result)):
				print("ISBN: " + str(result[i][0]) + " Title: " + result[i][1] + "Author: " + result[i][2] + " Amount: " + str(result[i][3]))
		else:
			print("Please choose a valid option")
	# Quit
	elif choice == "0":
		quit()
	
	else:
		print("Please choose a given option")

	return True, ID


try:
	conn = psycopg2.connect(
	dbname = "Project",
	user = "postgres",
	password = "7676",
	host = "localhost",
	port = "5432"
	)

	login = False
	account = None
	cur = conn.cursor()
	print("Welcome to our bookstore")
	while(True):
		menu(login)
		choice = input("Please enter your selection: ")
		if login == False:
			login, account = guest(choice, cur)
		else:
			login, account = user(choice, cur, account)

		conn.commit()


except psycopg2.OperationalError:
	print("Unable to connect\n Now exitting")
	quit()



