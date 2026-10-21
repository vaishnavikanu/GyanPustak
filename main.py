import mysql.connector
from mysql.connector import Error
import os
import time

# DATABASE
class DB:
    def __init__(self):
        self.conn = None

    def connect(self):
        try:
            self.conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='PASSWORD',
                database='gyan_pustak'
            )
            print(" Database connected\n")
            return True
        except Error as e:
            print("Error:", e)
            return False

    def query(self, sql, params=None, fetch=None):
        cursor = self.conn.cursor(dictionary=True)
        try:
            cursor.execute(sql, params or ())
            if fetch == 'one':
                return cursor.fetchone()
            elif fetch == 'all':
                return cursor.fetchall()
            else:
                self.conn.commit()
                return cursor.lastrowid
        except Error as e:
            print("Error:", e)
            return None
        finally:
            cursor.close()

class UI:
    def __init__(self):
        self.db = DB()
        self.user = None
        self.user_type = None

    def clear(self):
        os.system('clear' if os.name != 'nt' else 'cls')

    def header(self, title):
        print("\n" + "="*60)
        print(f"  {title.center(56)}")
        print("="*60 + "\n")

    # MAIN
    def main_menu(self):
        while True:
            self.clear()
            self.header("GyanPustak - Textbook Platform")
            print("1. Student Login")
            print("2. Employee Login")
            print("3. Register Student")
            print("4. View Universities")
            print("5. Exit")
            
            ch = int(input("\nChoice (1-5): "))

            if ch == 1:
                self.student_login()
            elif ch == 2:
                self.employee_login()
            elif ch == 3:
                self.register()
            elif ch == 4:
                self.view_universities()
            elif ch == 5:
                break

    # STUDENT
    def student_login(self):
        self.header("Student Login")
        sid = int(input("Student ID: "))
        user = self.db.query("SELECT * FROM Student WHERE studentID=%s",(sid,), 'one')

        if user:
            self.user = user
            self.user_type = 'student'
            print(f" Welcome {user['firstName']}!")
            input("Press Enter...")
            self.student_menu()
        else:
            print(" Invalid ID")
            input("Press Enter...")

    def student_menu(self):
        while True:
            self.clear()
            self.header(f"Student - {self.user['firstName']}")
            print("1. View Profile")
            print("2. View All Books")
            print("3. Search Books by Title")
            print("4. Search Books by Author")
            print("5. Search Books by Keyword")
            print("6. Add to Cart")
            print("7. View Cart")
            print("8. Place Order")
            print("9. View Orders")
            print("10. Write Review")
            print("11. Raise Ticket")
            print("12. View Universities & Courses")
            print("13. Logout")
            
            ch = int(input("\nChoice (1-13): "))

            if ch == 1:
                self.view_profile()
            elif ch == 2:
                self.view_books()
            elif ch == 3:
                self.search_books_by_title()
            elif ch == 4:
                self.search_books_by_author()
            elif ch == 5:
                self.search_books_by_keyword()
            elif ch == 6:
                self.add_to_cart()
            elif ch == 7:
                self.view_cart()
            elif ch == 8:
                self.place_order()
            elif ch == 9:
                self.view_orders()
            elif ch == 10:
                self.write_review()
            elif ch == 11:
                self.raise_ticket()
            elif ch == 12:
                self.view_universities()
            elif ch == 13:
                break

    def view_profile(self):
        self.header("My Profile")
        s = self.user
        print(f"Name: {s['firstName']} {s['lastName']}")
        print(f"Email: {s['email']}")
        print(f"Phone: {s['phone']}")
        print(f"Gender: {s['gender']}")
        print(f"Current Year: {s['currentYear']}")
        print(f"Status: {s['status']}")
        input("\nPress Enter...")

    def register(self):
        self.header("Register Student")
        fname = input("First name: ")
        lname = input("Last name: ")
        email = input("Email: ")
        phone = input("Phone: ")
        dob = input("DOB (YYYY-MM-DD): ")
        gender = input("Gender (M/F/Other): ")
        address = input("Address: ")
        major = input("Major: ")

        print("\nAvailable Universities:")
        unis = self.db.query("SELECT * FROM University", fetch='all')

        if unis:
            for u in unis:
                print(f"{u['universityID']}. {u['name']}")
        else:
            print("No universities found")
            input("Press Enter...")
            return

        university_id = int(input("Select University ID: "))

        depts = self.db.query(
            "SELECT * FROM Department WHERE universityID=%s",
            (university_id,), 'all'
        )

        if depts:
            print("\nAvailable Departments:")
            for d in depts:
                print(f"{d['departmentID']}. {d['name']}")
            department_id = int(input("Select Department ID: "))
        else:
            department_id = None

        enrollment_year = int(input("Enrollment Year (YYYY): "))
        current_year = int(input("Current Year of Study (1/2/3/4): "))

        sid = self.db.query(
            """INSERT INTO Student(firstName,lastName,email,phone,dob,gender,address,
            departmentID,major,enrollmentYear,currentYear,status)
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'active')""",
            (fname, lname, email, phone, dob, gender, address,
            department_id, major, enrollment_year, current_year)
        )

        print(f" Registered! Student ID: {sid}")
        input("Press Enter...")

    def view_books(self):
        self.header("All Books")
        books = self.db.query("""
            SELECT b.*, 
                   GROUP_CONCAT(DISTINCT a.authorName SEPARATOR ', ') as authors,
                   GROUP_CONCAT(DISTINCT c.name SEPARATOR ', ') as categories
            FROM Book b
            LEFT JOIN BookAuthor ba ON b.bookID = ba.bookID
            LEFT JOIN Author a ON ba.authorID = a.authorID
            LEFT JOIN BookCategory bc ON b.bookID = bc.bookID
            LEFT JOIN Category c ON bc.categoryID = c.categoryID
            GROUP BY b.bookID
        """, fetch='all')
        
        if books:
            for b in books:
                print(f"\n{b['bookID']}. {b['title']}")
                print(f"   Authors: {b['authors'] or 'N/A'}")
                print(f"   Price: ₹{b['price']} | Rental: ₹{b['rentalPrice'] or 'N/A'} | Stock: {b['quantity']}")
                print(f"   Rating: {b['rating']}/5 | Type: {b['type']}")
                print(f"   Format: {b['format']} | Language: {b['language']}")
                if b['categories']:
                    print(f"   Categories: {b['categories']}")
                print("-"*55)
        else:
            print("No books found")
        input("\nPress Enter...")

    def search_books_by_author(self):
        self.header("Search Books by Author")
        author_name = input("Enter Author Name (partial match ok): ")
        
        books = self.db.query("""
            SELECT DISTINCT b.* 
            FROM Book b
            JOIN BookAuthor ba ON b.bookID = ba.bookID
            JOIN Author a ON ba.authorID = a.authorID
            WHERE a.authorName LIKE %s
        """, (f"%{author_name}%",), 'all')
        
        if books:
            print(f"\n Found {len(books)} book(s):\n")
            for b in books:
                # Get authors for this book
                authors = self.db.query("""
                    SELECT GROUP_CONCAT(a.authorName SEPARATOR ', ') as authors
                    FROM BookAuthor ba
                    JOIN Author a ON ba.authorID = a.authorID
                    WHERE ba.bookID=%s
                """, (b['bookID'],), 'one')
                
                print(f"{b['bookID']}. {b['title']}")
                print(f"   Authors: {authors['authors']}")
                print(f"   Price: ₹{b['price']} | Rental: ₹{b['rentalPrice'] or 'N/A'} | Stock: {b['quantity']}")
                print(f"   Rating: {b['rating']}/5 | Type: {b['type']}")
                print(f"   Format: {b['format']} | ISBN: {b['isbn']}")
                print("-"*55)
        else:
            print(f" No books found by author '{author_name}'")
        
        input("\nPress Enter...")

    def search_books_by_keyword(self):
        self.header("Search Books by Keyword")
        keyword = input("Enter Keyword: ")
        
        books = self.db.query("""
            SELECT DISTINCT b.* 
            FROM Book b
            JOIN BookKeyword bk ON b.bookID = bk.bookID
            JOIN Keyword k ON bk.keywordID = k.keywordID
            WHERE k.keyword LIKE %s
        """, (f"%{keyword}%",), 'all')
        
        if books:
            print(f"\n Found {len(books)} book(s):\n")
            for b in books:
                # Get authors for this book
                authors = self.db.query("""
                    SELECT GROUP_CONCAT(a.authorName SEPARATOR ', ') as authors
                    FROM BookAuthor ba
                    JOIN Author a ON ba.authorID = a.authorID
                    WHERE ba.bookID=%s
                """, (b['bookID'],), 'one')
                
                # Get keywords for this book
                keywords = self.db.query("""
                    SELECT GROUP_CONCAT(k.keyword SEPARATOR ', ') as keywords
                    FROM BookKeyword bk
                    JOIN Keyword k ON bk.keywordID = k.keywordID
                    WHERE bk.bookID=%s
                """, (b['bookID'],), 'one')
                
                print(f"{b['bookID']}. {b['title']}")
                print(f"   Authors: {authors['authors'] or 'Unknown'}")
                print(f"   Price: ₹{b['price']} | Rental: ₹{b['rentalPrice'] or 'N/A'} | Stock: {b['quantity']}")
                print(f"   Rating: {b['rating']}/5 | Type: {b['type']}")
                print(f"   Format: {b['format']} | ISBN: {b['isbn']}")
                if keywords['keywords']:
                    print(f"   Keywords: {keywords['keywords']}")
                print("-"*55)
        else:
            print(f" No books found with keyword '{keyword}'")
        
        input("\nPress Enter...")

    def search_books_by_title(self):
        self.header("Search Books by Title")
        title = input("Enter Book Title (partial match ok): ")
        
        books = self.db.query("""
            SELECT * FROM Book 
            WHERE title LIKE %s
        """, (f"%{title}%",), 'all')
        
        if books:
            print(f"\n Found {len(books)} book(s):\n")
            for b in books:
                # Get authors for this book
                authors = self.db.query("""
                    SELECT GROUP_CONCAT(a.authorName SEPARATOR ', ') as authors
                    FROM BookAuthor ba
                    JOIN Author a ON ba.authorID = a.authorID
                    WHERE ba.bookID=%s
                """, (b['bookID'],), 'one')
                
                print(f"{b['bookID']}. {b['title']}")
                print(f"   Authors: {authors['authors'] or 'Unknown'}")
                print(f"   Price: ₹{b['price']} | Rental: ₹{b['rentalPrice'] or 'N/A'} | Stock: {b['quantity']}")
                print(f"   Rating: {b['rating']}/5 | Type: {b['type']}")
                print(f"   Format: {b['format']} | ISBN: {b['isbn']}")
                print("-"*55)
        else:
            print(f" No books found with title '{title}'")
        
        input("\nPress Enter...")

    def add_to_cart(self):
        self.header("Add to Cart")
        bid = int(input("Book ID: "))
        qty = int(input("Quantity: "))
        ptype = input("Purchase Type (rent/buy): ")

        # Check if book exists
        book = self.db.query("SELECT * FROM Book WHERE bookID=%s", (bid,), 'one')
        
        if not book:
            print(" Book not found")
            input("Press Enter...")
            return

        # Check stock
        if qty > book['quantity']:
            print(f" Not enough stock! Available: {book['quantity']}")
            input("Press Enter...")
            return

        # Check if cart exists
        cart = self.db.query(
            "SELECT * FROM Cart WHERE studentID=%s",
            (self.user['studentID'],), 'one'
        )

        # Create cart if not exists
        if not cart:
            cart_id = self.db.query(
                "INSERT INTO Cart(studentID) VALUES(%s)",
                (self.user['studentID'],)
            )
        else:
            cart_id = cart['cartID']

        # Check if book already in cart
        existing = self.db.query("""
            SELECT * FROM CartItem 
            WHERE cartID=%s AND bookID=%s
        """, (cart_id, bid), 'one')

        if existing:
            # Update quantity
            self.db.query("""
                UPDATE CartItem 
                SET quantity = quantity + %s
                WHERE cartID=%s AND bookID=%s
            """, (qty, cart_id, bid))
        else:
            # Insert new item
            self.db.query("""
                INSERT INTO CartItem(cartID, bookID, quantity, purchaseType)
                VALUES(%s, %s, %s, %s)
            """, (cart_id, bid, qty, ptype))

        print(" Added to cart")
        input("Press Enter...")

    def view_cart(self):
        self.header("My Cart")

        # Get cart
        cart = self.db.query(
            "SELECT * FROM Cart WHERE studentID=%s",
            (self.user['studentID'],), 'one'
        )

        if not cart:
            print(" Cart is empty")
            input("Press Enter...")
            return

        # Get all items in cart
        items = self.db.query("""
            SELECT ci.*, b.title, b.price
            FROM CartItem ci
            JOIN Book b ON ci.bookID = b.bookID
            WHERE ci.cartID=%s
        """, (cart['cartID'],), 'all')

        if not items:
            print(" Cart is empty")
            input("Press Enter...")
            return

        # Display items
        total = 0
        for item in items:
            subtotal = item['price'] * item['quantity']
            total += subtotal

            print(f"\nBook: {item['title']}")
            print(f"Price: ₹{item['price']}")
            print(f"Quantity: {item['quantity']}")
            print(f"Type: {item['purchaseType']}")
            print(f"Subtotal: ₹{subtotal}")
            print("-"*40)

        # Show total
        print(f"\nTotal Amount: ₹{total}")

        input("\nPress Enter...")

    def place_order(self):
        self.header("Place Order")

        # Get cart
        cart = self.db.query(
            "SELECT * FROM Cart WHERE studentID=%s",
            (self.user['studentID'],), 'one'
        )

        if not cart:
            print(" No cart found. Please add items first.")
            input("Press Enter...")
            return

        # Get all cart items + stock
        items = self.db.query("""
            SELECT ci.*, b.price, b.quantity AS stock
            FROM CartItem ci
            JOIN Book b ON ci.bookID = b.bookID
            WHERE ci.cartID=%s
        """, (cart['cartID'],), 'all')

        if not items:
            print(" Cart has no items. Add books before placing order.")
            input("Press Enter...")
            return

        # Check stock availability
        for item in items:
            if item['quantity'] > item['stock']:
                print(f" Not enough stock for Book ID {item['bookID']}")
                input("Press Enter...")
                return

        # Calculate total
        total = sum(item['price'] * item['quantity'] for item in items)

        # Get user input
        shipping = input("Shipping Type (standard/2-day/1-day/express) [standard]: ") or "standard"

        while True:
            card_num = input("Card Number (16 digits): ")
            if len(card_num) == 16 and card_num.isdigit():
                break
            print(" Invalid card number")

        while True:
            card_exp = input("Card Expiry (MM/YY): ")
            if len(card_exp) == 5 and card_exp[2] == '/':
                break
            print(" Invalid format")

        card_name = input("Card Holder Name: ")

        while True:
            card_type = input("Card Type (visa/mastercard/amex/debit): ").lower()
            if card_type in ['visa', 'mastercard', 'amex', 'debit']:
                break
            print(" Invalid card type")

        addr = input("Shipping Address: ")

        # Create order
        order_num = f"ORD{int(self.user['studentID'])}{int(time.time())}"
        order_id = self.db.query("""
            INSERT INTO `Order`(studentID,orderNumber,shippingType,shippingAddress,orderStatus,totalAmount,finalAmount)
            VALUES(%s,%s,%s,%s,'pending',%s,%s)
        """, (self.user['studentID'], order_num, shipping, addr, total, total))

        # Insert all items into OrderBook
        for item in items:
            subtotal = item['price'] * item['quantity']

            self.db.query("""
                INSERT INTO OrderBook(orderID,bookID,quantity,purchaseType,pricePerUnit,subtotal)
                VALUES(%s,%s,%s,%s,%s,%s)
            """, (
                order_id,
                item['bookID'],
                item['quantity'],
                item['purchaseType'],
                item['price'],
                subtotal
            ))

        # REDUCE BOOK STOCK
        for item in items:
            self.db.query("""
                UPDATE Book 
                SET quantity = quantity - %s 
                WHERE bookID=%s
            """, (item['quantity'], item['bookID']))

        # Payment
        self.db.query("""
            INSERT INTO Payment(orderID,amount,paymentMethod,cardNumber,cardExpiry,cardHolderName,cardType,paymentStatus,transactionID)
            VALUES(%s,%s,'card',%s,%s,%s,%s,'successful',%s)
        """, (order_id, total, card_num, card_exp, card_name, card_type, f"TXN{order_id}"))

        # Clear cart
        self.db.query("DELETE FROM CartItem WHERE cartID=%s", (cart['cartID'],))
        self.db.query("DELETE FROM Cart WHERE cartID=%s", (cart['cartID'],))

        print(f" Order placed successfully! Order ID: {order_id}")
        input("Press Enter...")

    def view_orders(self):
        self.header("My Orders")

        orders = self.db.query(
            "SELECT * FROM `Order` WHERE studentID=%s",
            (self.user['studentID'],),
            'all'
        )

        if not orders:
            print(" No orders found")
            input("\nPress Enter...")
            return

        for o in orders:
            print(f"\nOrder #{o['orderID']} ({o['orderNumber']})")
            print(f"Amount: ₹{o['finalAmount']}")
            print(f"Status: {o['orderStatus']}")
            print(f"Shipping: {o['shippingType']}")
            print(f"Date: {o['dateCreated']}")
            
            items = self.db.query("""
                SELECT ob.*, b.title
                FROM OrderBook ob
                JOIN Book b ON ob.bookID = b.bookID
                WHERE ob.orderID=%s
            """, (o['orderID'],), 'all')

            if items:
                print("Items:")
                for item in items:
                    print(f"  - {item['title']} x{item['quantity']} (₹{item['subtotal']})")

            print("-"*40)

        input("\nPress Enter...")

    def write_review(self):
        self.header("Write Review")
        bid = int(input("Book ID: "))
        book = self.db.query("SELECT * FROM Book WHERE bookID=%s",(bid,),'one')
        
        if not book:
            print(" Book not found")
            input("Press Enter...")
            return

        rating = int(input("Rating (1-5): "))
        review_text = input("Review Text: ")

        # Check if verified purchase
        verified = self.db.query("""
            SELECT COUNT(*) as count FROM OrderBook ob
            JOIN `Order` o ON ob.orderID = o.orderID
            WHERE o.studentID=%s AND ob.bookID=%s
        """, (self.user['studentID'], bid), 'one')

        is_verified = verified['count'] > 0 if verified else False

        self.db.query("""
        INSERT INTO Review(studentID,bookID,rating,reviewText,isVerifiedPurchase)
        VALUES(%s,%s,%s,%s,%s)
        """, (self.user['studentID'], bid, rating, review_text, is_verified))

        print(" Review added")
        input("Press Enter...")

    def raise_ticket(self):
        self.header("Raise Support Ticket")
        
        categories = self.db.query("SELECT * FROM TicketCategory", fetch='all')
        
        if categories:
            for i, cat in enumerate(categories, 1):
                print(f"{i}. {cat['categoryName']}")
            
            cat_choice = int(input("Category (number): ")) - 1
            
            if 0 <= cat_choice < len(categories):
                category_id = categories[cat_choice]['categoryID']
            else:
                print(" Invalid category")
                input("Press Enter...")
                return
        else:
            print("No categories available")
            input("Press Enter...")
            return

        title = input("Title: ")
        desc = input("Description: ")

        self.db.query("""
        INSERT INTO Ticket(studentID, employeeID, categoryID, title, description, status)
        VALUES(%s, NULL, %s, %s, %s, 'new')
        """, (self.user['studentID'], category_id, title, desc))

        print(" Ticket created")
        input("Press Enter...")

    def view_universities(self):
        self.header("Universities & Departments")
        unis = self.db.query("SELECT * FROM University", fetch='all')
        
        uni_num = 1
        for u in unis:
            print(f"\n{uni_num}. {u['name']}")
            print(f"   Address: {u['address']}, {u['city']}")
            
            depts = self.db.query("SELECT * FROM Department WHERE universityID=%s",(u['universityID'],),'all')
            
            if depts:
                dept_num = 1
                for d in depts:
                    print(f"\n   {dept_num}. {d['name']}")
                    
                    # Get instructors in this department
                    instructors = self.db.query("""
                    SELECT DISTINCT i.* FROM Instructor i
                    WHERE i.departmentID=%s
                    """, (d['departmentID'],), 'all')
                    
                    if instructors:
                        print(f"      Instructors:")
                        for instr in instructors:
                            print(f"        • {instr['firstName']} {instr['lastName']} ({instr['specialization']})")
                    
                    # Get courses in this department
                    courses = self.db.query("""
                    SELECT c.* FROM Course c
                    JOIN DepartmentCourse dc ON c.courseID = dc.courseID
                    WHERE dc.departmentID=%s
                    """, (d['departmentID'],), 'all')
                    
                    if courses:
                        print(f"\n      Courses:")
                        course_num = 1
                        for c in courses:
                            # Get instructors for this course
                            course_instructors = self.db.query("""
                            SELECT i.firstName, i.lastName FROM Instructor i
                            JOIN CourseInstructor ci ON i.instructorID = ci.instructorID
                            WHERE ci.courseID=%s
                            """, (c['courseID'],), 'all')
                            
                            instr_names = ", ".join([f"{i['firstName']} {i['lastName']}" for i in course_instructors])
                            if instr_names:
                                print(f"        {course_num}. {c['courseCode']} - {c['courseName']} (Year {c['year']}, Sem {c['semester']}) | Instructor: {instr_names}")
                            else:
                                print(f"        {course_num}. {c['courseCode']} - {c['courseName']} (Year {c['year']}, Sem {c['semester']}) | Instructor: Not Assigned")
                            course_num += 1
                    
                    dept_num += 1
            
            uni_num += 1
        
        input("\nPress Enter...")

    # EMPLOYEE
    def employee_login(self):
        self.header("Employee Login")
        eid = int(input("Employee ID: "))
        emp = self.db.query("SELECT * FROM Employee WHERE employeeID=%s",(eid,), 'one')

        if emp:
            self.user = emp
            self.user_type = emp['empType']
            print(f" Welcome {emp['firstName']}!")
            input("Press Enter...")
            
            if emp['empType'] == 'support':
                self.support_menu()
            else:
                admin = self.db.query("SELECT * FROM Admin WHERE employeeID=%s",(eid,), 'one')
                
                if admin and admin['isSuperAdmin']:
                    self.user_type = 'superadmin'
                else:
                    self.user_type = 'admin'

                self.admin_menu()
        else:
            print(" Invalid employee ID")
            input("Press Enter...")

    # SUPPORT AGENT MENU
    def support_menu(self):
        """Support Agent can VIEW ALL, ASSIGN NEW tickets, and CREATE tickets"""
        while True:
            self.clear()
            self.header(f"Support Agent - {self.user['firstName']}")
            print("1. View All Tickets")
            print("2. Assign NEW Ticket to Administrator")
            print("3. Create New Ticket")
            print("4. Logout")
            
            ch = int(input("\nChoice (1-4): "))

            if ch == 1:
                self.view_all_tickets_support()
            elif ch == 2:
                self.assign_to_admin()
            elif ch == 3:
                self.support_create_ticket()
            elif ch == 4:
                break

    def view_all_tickets_support(self):
        """Support Agent can VIEW all tickets but READ ONLY"""
        self.header("All Tickets (View Only)")
        tickets = self.db.query("""
            SELECT t.*, tc.categoryName FROM Ticket t
            LEFT JOIN TicketCategory tc ON t.categoryID = tc.categoryID
        """, fetch='all')
        
        if tickets:
            for t in tickets:
                admin_name = "Unassigned"
                if t['adminEmployeeID']:
                    admin = self.db.query("SELECT firstName, lastName FROM Employee WHERE employeeID=%s", (t['adminEmployeeID'],), 'one')
                    if admin:
                        admin_name = f"{admin['firstName']} {admin['lastName']}"
                
                print(f"\n#{t['ticketID']} - {t['title']}")
                print(f"Category: {t['categoryName']}")
                print(f"Status: {t['status']} | Admin: {admin_name}")
                print(f"Created At: {t['dateLogged']}")
                if t['studentID']:
                    print(f"Student ID: {t['studentID']}")
                elif t['employeeID']:
                    print(f"Employee ID: {t['employeeID']}")
                print("-"*50)
        else:
            print("No tickets found")
        
        input("\nPress Enter...")

    def assign_to_admin(self):
        """Support Agent can ONLY assign NEW tickets to Admin"""
        self.header("Assign NEW Ticket to Administrator")
        tid = int(input("Ticket ID: "))
        ticket = self.db.query("SELECT * FROM Ticket WHERE ticketID=%s",(tid,), 'one')

        if not ticket:
            print(" Ticket not found")
            input("Press Enter...")
            return
        
        if ticket['status'] != 'new':
            print(f" Cannot assign ticket! Current status: {ticket['status']}")
            print("   You can only assign NEW tickets")
            input("Press Enter...")
            return

        admins = self.db.query("SELECT e.* FROM Employee e JOIN Admin a ON e.employeeID=a.employeeID WHERE e.status='active'", fetch='all')
        
        if admins:
            print("\nAvailable Administrators:")
            for i, admin in enumerate(admins, 1):
                print(f"{i}. {admin['firstName']} {admin['lastName']}")
            
            choice = int(input("Select Admin (number): ")) - 1
            
            if 0 <= choice < len(admins):
                admin_id = admins[choice]['employeeID']
                
                self.db.query("""
                UPDATE Ticket SET status='assigned', adminEmployeeID=%s WHERE ticketID=%s
                """, (admin_id, tid))
                
                self.db.query("""
                INSERT INTO TicketHistory(ticketID,previousStatus,newStatus,changedByEmployeeID)
                VALUES(%s,'new','assigned',%s)
                """, (tid, self.user['employeeID']))
                
                print(f" Ticket #{tid} assigned to admin")
            else:
                print(" Invalid selection")
        else:
            print(" No available administrators")
        
        input("Press Enter...")

    def support_create_ticket(self):
        self.header("Create Ticket")

        categories = self.db.query("SELECT * FROM TicketCategory", fetch='all')

        if categories:
            print("\nCategories:")
            for i, cat in enumerate(categories, 1):
                print(f"{i}. {cat['categoryName']}")

            cat_choice = int(input("Category (number): ")) - 1
            
            if 0 <= cat_choice < len(categories):
                category_id = categories[cat_choice]['categoryID']
            else:
                print(" Invalid category")
                input("Press Enter...")
                return
        else:
            print("No categories available")
            input("Press Enter...")
            return

        title = input("Title: ")
        desc = input("Description: ")
        
        self.db.query("""
        INSERT INTO Ticket(studentID, employeeID, categoryID, title, description, status)
        VALUES(NULL, %s, %s, %s, %s, 'new')
        """, (self.user['employeeID'], category_id, title, desc))

        print(" Ticket created successfully")
        input("Press Enter...")

    # ADMIN MENU
    def admin_menu(self):
        """Regular Admin can handle assigned, in-progress, and closed tickets"""
        while True:
            self.clear()
            self.header(f"Administrator - {self.user['firstName']}")
            print("1. View All Students")
            print("2. View Books")
            print("3. View Assigned Tickets (My Queue)")
            print("4. View In-Progress Tickets")
            print("5. View Closed Tickets")
            print("6. Add New Books")
            print("7. Start Working on Ticket (Assigned → In-Progress)")
            print("8. Resolve Ticket (In-Progress → Completed)")
            print("9. Close Completed Ticket (Completed → Closed)")
            if self.user_type == 'superadmin':
                print("10. Add Employee")
                print("11. View All Employees")
                print("12. Logout")
            else:
                print("10. Logout")
            
            ch = int(input("\nChoice : "))

            if ch == 1:
                self.view_all_students()
            elif ch == 2:
                self.view_books_admin()
            elif ch == 3:
                self.view_assigned_tickets_admin()
            elif ch == 4:
                self.view_inprogress_tickets()
            elif ch == 5:
                self.view_closed_tickets()
            elif ch == 6:
                self.admin_add_book_to_course()
            elif ch == 7:
                self.start_ticket()
            elif ch == 8:
                self.admin_resolve_ticket()
            elif ch == 9:
                self.close_resolved_ticket()
            elif self.user_type == 'admin' and ch == 10:
                break
            elif self.user_type == 'superadmin' and ch == 10:
                self.add_employee()
            elif self.user_type == 'superadmin' and ch == 11:
                self.view_all_employees()
            elif (self.user_type == 'superadmin' and ch == 12) or (self.user_type != 'superadmin' and ch == 10):
                break

    def view_books_admin(self):
        """Admin can view books"""
        self.header("Books")
        books = self.db.query("""
            SELECT b.*, 
                   GROUP_CONCAT(DISTINCT a.authorName SEPARATOR ', ') as authors
            FROM Book b
            LEFT JOIN BookAuthor ba ON b.bookID = ba.bookID
            LEFT JOIN Author a ON ba.authorID = a.authorID
            GROUP BY b.bookID
        """, fetch='all')
        
        if books:
            for b in books:
                print(f"{b['bookID']}. {b['title']} by {b['authors'] or 'Unknown'}")
                print(f"   Price: ₹{b['price']} | Stock: {b['quantity']}")
        else:
            print("No books found")
        
        input("\nPress Enter...")

    def view_assigned_tickets_admin(self):
        """Admin views ONLY assigned tickets"""
        self.header("My Assigned Tickets")
        tickets = self.db.query("""
        SELECT t.*, tc.categoryName FROM Ticket t
        LEFT JOIN TicketCategory tc ON t.categoryID = tc.categoryID
        WHERE t.adminEmployeeID=%s AND t.status='assigned'
        """, (self.user['employeeID'],), 'all')
        
        if tickets:
            for t in tickets:
                print(f"\n#{t['ticketID']} - {t['title']}")
                print(f"Category: {t['categoryName']}")
                if t['studentID']:
                    print(f"Student ID: {t['studentID']}")
                elif t['employeeID']:
                    print(f"Employee ID: {t['employeeID']}")
                print(f"Status: ASSIGNED")
                print(f"Created At: {t['dateLogged']}")
                print("-"*40)
        else:
            print("No assigned tickets")
        
        input("\nPress Enter...")

    def view_inprogress_tickets(self):
        """Admin views ONLY in-progress tickets"""
        self.header("In-Progress Tickets")
        tickets = self.db.query("""
        SELECT t.*, tc.categoryName FROM Ticket t
        LEFT JOIN TicketCategory tc ON t.categoryID = tc.categoryID
        WHERE t.adminEmployeeID=%s AND t.status='in-progress'
        """, (self.user['employeeID'],), 'all')
        
        if tickets:
            for t in tickets:
                print(f"\n#{t['ticketID']} - {t['title']}")
                print(f"Category: {t['categoryName']}")
                print(f"Status: IN-PROGRESS")
                print(f"Created At: {t['dateLogged']}")
                print("-"*40)
        else:
            print("No in-progress tickets")
        
        input("\nPress Enter...")

    def view_closed_tickets(self):
        """Admin can view CLOSED tickets (read-only)"""
        self.header("Closed Tickets")
        tickets = self.db.query("""
        SELECT t.*, tc.categoryName FROM Ticket t
        LEFT JOIN TicketCategory tc ON t.categoryID = tc.categoryID
        WHERE t.adminEmployeeID=%s AND t.status='closed'
        """, (self.user['employeeID'],), 'all')
        
        if tickets:
            for t in tickets:
                print(f"\n#{t['ticketID']} - {t['title']}")
                print(f"Category: {t['categoryName']}")
                print(f"Status: CLOSED")
                print(f"Solution: {t['solution']}")
                print(f"Created At: {t['dateLogged']}")
                print("-"*40)
        else:
            print("No closed tickets")
        
        input("\nPress Enter...")

    def admin_add_book_to_course(self):
        self.header("Add New Book for Course")

        # Enter NEW Book Details
        title = input("Book Title: ")
        isbn = input("ISBN: ")
        publisher = input("Publisher: ")
        pub_date = input("Publication Date (YYYY-MM-DD): ")
        edition = int(input("Edition: "))
        language = input("Language: ")
        btype = input("Type (new/used): ")
        purchase_option = "buy"
        format_type = input("Format (hardcover/softcover/electronic): ")
        price = float(input("Price: "))
        rental_price = input("Rental Price (or leave blank): ")
        quantity = int(input("Stock Quantity: "))

        # Insert new book
        book_id = self.db.query("""
        INSERT INTO Book(title, isbn, publisher, publicationDate, edition, language, type, purchaseOption, format, price, rentalPrice, quantity)
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (title, isbn, publisher, pub_date, edition, language, btype, purchase_option, format_type, price, rental_price if rental_price else None, quantity))

        print(f" Book added with ID: {book_id}")

        # Add Authors
        add_authors = input("Add authors? (y/n): ").lower() == 'y'
        
        if add_authors:
            while True:
                author_name = input("Author name (or 'done' to finish): ")
                if author_name.lower() == 'done':
                    break
                
                # Check if author exists
                author = self.db.query("SELECT authorID FROM Author WHERE authorName=%s", (author_name,), 'one')
                
                if author:
                    author_id = author['authorID']
                else:
                    author_id = self.db.query("INSERT INTO Author(authorName) VALUES(%s)", (author_name,))
                
                self.db.query("INSERT INTO BookAuthor(bookID, authorID) VALUES(%s, %s)", (book_id, author_id))

        # Add Keywords
        add_keywords = input("Add keywords? (y/n): ").lower() == 'y'
        
        if add_keywords:
            while True:
                keyword = input("Keyword (or 'done' to finish): ")
                if keyword.lower() == 'done':
                    break
                
                # Check if keyword exists
                kw = self.db.query("SELECT keywordID FROM Keyword WHERE keyword=%s", (keyword,), 'one')
                
                if kw:
                    keyword_id = kw['keywordID']
                else:
                    keyword_id = self.db.query("INSERT INTO Keyword(keyword) VALUES(%s)", (keyword,))
                
                self.db.query("INSERT INTO BookKeyword(bookID, keywordID) VALUES(%s, %s)", (book_id, keyword_id))

        # Add Categories
        categories = self.db.query("SELECT * FROM Category WHERE parentCategoryID IS NULL", fetch='all')
        
        if categories:
            print("\nAvailable Categories:")
            for i, cat in enumerate(categories, 1):
                print(f"{i}. {cat['name']}")
            
            cat_choice = int(input("Select category (number): ")) - 1
            
            if 0 <= cat_choice < len(categories):
                category_id = categories[cat_choice]['categoryID']
                self.db.query("INSERT INTO BookCategory(bookID, categoryID) VALUES(%s, %s)", (book_id, category_id))

        # Link Book to Course
        link_course = input("Link to course? (y/n): ").lower() == 'y'
        
        if link_course:
            cid = int(input("Course ID: "))
            course = self.db.query("SELECT * FROM Course WHERE courseID=%s", (cid,), 'one')

            if not course:
                print(" Course not found")
                input("Press Enter...")
                return

            iid = int(input("Instructor ID: "))
            instructor = self.db.query("SELECT * FROM Instructor WHERE instructorID=%s", (iid,), 'one')

            if not instructor:
                print(" Instructor not found")
                input("Press Enter...")
                return

            book_type = input("Book Type (required/recommended/reference): ")

            # Link to course
            self.db.query("""
            INSERT INTO CourseBook(courseID,bookID,instructorID,year,semester,bookType)
            VALUES(%s,%s,%s,%s,%s,%s)
            """, (cid, book_id, iid, course['year'], course['semester'], book_type))

        print(" Book added successfully!")
        input("Press Enter...")
        
    def start_ticket(self):
        """Admin changes assigned ticket to in-progress"""
        self.header("Start Working on Ticket")
        tid = int(input("Ticket ID: "))
        ticket = self.db.query("SELECT * FROM Ticket WHERE ticketID=%s",(tid,), 'one')
        
        if not ticket:
            print(" Ticket not found")
            input("Press Enter...")
            return
        
        if ticket['adminEmployeeID'] != self.user['employeeID']:
            print(" This ticket is not assigned to you")
            input("Press Enter...")
            return
        
        if ticket['status'] != 'assigned':
            print(f" Cannot change status! Current status: {ticket['status']}")
            print("   You can only work on ASSIGNED tickets")
            input("Press Enter...")
            return
        
        self.db.query("""
        UPDATE Ticket SET status='in-progress' WHERE ticketID=%s
        """, (tid,))
        
        self.db.query("""
        INSERT INTO TicketHistory(ticketID,previousStatus,newStatus,changedByEmployeeID)
        VALUES(%s,'assigned','in-progress',%s)
        """, (tid, self.user['employeeID']))
        
        print(f" Ticket #{tid} marked as In-Progress")
        input("Press Enter...")

    def admin_resolve_ticket(self):
        """Admin can ONLY resolve in-progress tickets"""
        self.header("Resolve Ticket")
        tid = int(input("Ticket ID: "))
        solution = input("Solution: ")
        
        ticket = self.db.query("SELECT * FROM Ticket WHERE ticketID=%s",(tid,), 'one')
        
        if not ticket:
            print(" Ticket not found")
            input("Press Enter...")
            return
        
        if ticket['adminEmployeeID'] != self.user['employeeID']:
            print(" This ticket is not assigned to you")
            input("Press Enter...")
            return
        
        if ticket['status'] != 'in-progress':
            print(f" Cannot resolve! Current status: {ticket['status']}")
            print("   You can only resolve IN-PROGRESS tickets")
            input("Press Enter...")
            return
        
        self.db.query("""
        UPDATE Ticket SET status='completed', solution=%s, completionDate=NOW() WHERE ticketID=%s
        """, (solution, tid))
        
        self.db.query("""
        INSERT INTO TicketHistory(ticketID,previousStatus,newStatus,changedByEmployeeID)
        VALUES(%s,'in-progress','completed',%s)
        """, (tid, self.user['employeeID']))
        
        print(f" Ticket #{tid} resolved successfully")
        input("Press Enter...")

    def close_resolved_ticket(self):
        """Admin can close completed tickets"""
        self.header("Close Ticket")
        tid = int(input("Ticket ID: "))
        ticket = self.db.query("SELECT * FROM Ticket WHERE ticketID=%s",(tid,), 'one')
        
        if not ticket:
            print(" Ticket not found")
            input("Press Enter...")
            return
        
        if ticket['adminEmployeeID'] != self.user['employeeID']:
            print(" This ticket is not assigned to you")
            input("Press Enter...")
            return
        
        if ticket['status'] != 'completed':
            print(f" Cannot close! Current status: {ticket['status']}")
            print("   You can only close COMPLETED tickets")
            input("Press Enter...")
            return
        
        self.db.query("""
        UPDATE Ticket SET status='closed' WHERE ticketID=%s
        """, (tid,))
        
        self.db.query("""
        INSERT INTO TicketHistory(ticketID,previousStatus,newStatus,changedByEmployeeID)
        VALUES(%s,'completed','closed',%s)
        """, (tid, self.user['employeeID']))
        
        print(f" Ticket #{tid} closed successfully")
        input("Press Enter...")

    # SUPER ADMIN MENU

    def view_all_students(self):
        self.header("All Students")
        students = self.db.query("SELECT * FROM Student", fetch='all')
        
        if students:
            for s in students:
                dept_name = "N/A"
                if s['departmentID']:
                    dept = self.db.query("SELECT name FROM Department WHERE departmentID=%s", (s['departmentID'],), 'one')
                    if dept:
                        dept_name = dept['name']
                
                print(f"{s['studentID']}. {s['firstName']} {s['lastName']} - {s['email']} ({dept_name})")
        else:
            print("No students found")
        
        input("\nPress Enter...")

    def view_all_employees(self):
        self.header("All Employees")
        employees = self.db.query("SELECT * FROM Employee", fetch='all')
        
        if employees:
            for e in employees:
                print(f"{e['employeeID']}. {e['firstName']} {e['lastName']} - {e['empType'].upper()}")
        else:
            print("No employees found")
        
        input("\nPress Enter...")

    def add_employee(self):
        self.header("Add New Employee")
        fname = input("First Name: ")
        lname = input("Last Name: ")
        email = input("Email: ")
        phone = input("Phone: ")
        gender = input("Gender (M/F/Other): ")
        aadhaar = input("Aadhaar Number: ")
        address = input("Address: ")
        emp_type = input("Employee Type (admin/support): ").lower()
        salary = float(input("Salary: "))
        join_date = input("Join Date (YYYY-MM-DD): ")
        
        eid = self.db.query("""
        INSERT INTO Employee(firstName,lastName,email,phone,gender,aadhaar,address,empType,salary,joinDate,status)
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'active')
        """, (fname, lname, email, phone, gender, aadhaar, address, emp_type, salary, join_date))
        
        if emp_type == 'admin':
            self.db.query("""
            INSERT INTO Admin(employeeID, isSuperAdmin)
            VALUES(%s, FALSE)
            """, (eid,))
        elif emp_type == 'support':
            self.db.query("""
            INSERT INTO CustomerSupport(employeeID)
            VALUES(%s)
            """, (eid,))
        
        print(f" Employee added! ID: {eid}")
        input("Press Enter...")

    # RUN
    def run(self):
        if self.db.connect():
            self.main_menu()
        else:
            print("Failed to connect to database")

if __name__ == "__main__":
    UI().run()