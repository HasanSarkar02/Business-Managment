import mysql.connector


#--------------------------Database Connection Class Start here----------------
class Database:
    def __init__(self, host, user, password, database):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor()

    def execute_query(self, query, data=None):
        self.cursor.execute(query, data)
        self.connection.commit()

    def fetch_all(self, query, data=None):
        self.cursor.execute(query, data)
        return self.cursor.fetchall()
#-----------------------------Database Connection Class End here------------------
#------------------------------Hotel Class Start here-----------------------------
class hotel:
    def __init__(self, db,customer_info):
        self.db=db  
        self.customer_manager=customer_info
    def list_hotels(self):    
        query ="SELECT * FROM hotel"
        hotel=self.db.fetch_all(query)
        print("\n---Hotel List---")
        
        for hot in hotel:
            print(f"{hot[0]}. {hot[1]}")
        print("3. Exit")    
    def list_hotel(self,hotel_id): 
          
        query ="SELECT * FROM hotel WHERE hotel_id= %s"
        hotel=self.db.fetch_all(query,(hotel_id,))
        
        for hot in hotel:
            print(f"\n---Welcome to {hot[1]}----")
            print("----------------------------")
            print(f"-------{hot[1]}-----------")
            print("----------------------------")
            print(f"Type:{hot[2]}   Location:{hot[3]}\n \nPer Day Cost: {hot[4]}   Status: {hot[5]}\n \nCheck-In: 2:00PM   Check-Out:12:00PM")        
            print("\n\n1. BOOK NOW")


    def hotel_booking(self):
         hotel_id = int(input("Enter Your Choice: "))
         query="SELECT * FROM hotel WHERE hotel_id = %s"
         hotel = self.db.fetch_all(query, (hotel_id,))
         if not hotel:
            print("Invalid hotel ID. Please try again.")
         fname = input("Enter your first name: ")
         lname = input("Enter your last name: ")
         country = input("Enter your country: ")
         email = input("Enter your email: ")
         days_ = int(input("Enter the number of days: "))
         self.customer_manager.customer_booking(hotel_id,fname, lname, country, email, days_)
         
#------------------------------Hotel Class End here-----------------------------         
            



#-----------------------------Customer Booking Class Start here------------------
class customer:
    def __init__ (self,db):
        self.db=db  
    def customer_booking(self,hotel_id,fname,lname,country, email,days_):
      try:
          query = "INSERT INTO customer_booking_info (hotel_id,fname,lname,country, email,days_) VALUES (%s,%s, %s, %s, %s,%s)"
          self.db.execute_query(query, (hotel_id,fname,lname,country,email,days_))
          print("Thank You! Your Booking is successful!")   
      except mysql.connector.Error as err:
         print(f"Error: {err}")
#-----------------------------Customer Booking Class End here------------------


#-----------------------------------ADMIN CLASS START HERE---------------------
class Admin:
    def __init__(self, db):
        self.db = db
        self.property_manager = Property(db)
        self.customer_manager = customer(db)

    def admin_dashboard(self):
        while True:
            print("\n--- Admin Dashboard ---")
            print("1. Add Property")
            print("2. Update Property Availability")
            print("3. View Customer Bookings")
            print("4. Post Job Circular")
            print("5. Logout")
            choice = input("Enter your choice: ")

            if choice == "1":
                # Add a new property
                property_type = input("Enter property type (e.g., Apartment, House,Land): ")
                location = input("Enter property location: ")
                price = float(input("Enter property price: "))
                self.property_manager.add_property(property_type, location, price)

            elif choice == "2":
                # Update property availability
                property_id = int(input("Enter property ID to update: "))
                status = input("Enter new availability status (Available/Not Available): ")
                query = "UPDATE properties SET status = %s WHERE id = %s"
                self.db.execute_query(query, (status, property_id))
                print("Property availability updated successfully!")

            elif choice == "3":
                # View customer bookings
                query = "SELECT * FROM customer_booking_info"
                bookings = self.db.fetch_all(query)
                print("\n--- Customer List ---")
                for booking in bookings:
                    print(f"\nID: {booking[0]}, Name: {booking[2]} {booking[3]}, Country: {booking[4]} Email: {booking[5]}, Days: {booking[6]}")

            elif choice == "4":
                # Post job circular
                job_title = input("Enter job title: ")
                description = input("Enter job description: ")
                query = "INSERT INTO manpower_jobs (title, description) VALUES (%s, %s)"
                self.db.execute_query(query, (job_title, description))
                print("Job circular posted successfully!")

            elif choice == "5":
                print("Logging out...")
                break

            else:
                print("Invalid choice. Please try again.")
#-----------------------------------ADMIN CLASS END HERE---------------------
#-----------------------------------Man Power CLASS START HERE---------------
class Man_power:
    def __init__ (self,db):
        self.db=db

    def job_list(self):
        query= "SELECT * FROM  manpower_jobs"
        manpower_jobs= self.db.fetch_all(query)
        print("---Available Circulars---")
        for man in manpower_jobs:
            print(f"Job ID: {man[0]}, Job Title: {man[1]}, Description: {man[2]}, Posted at: {man[3]}")
#-----------------------------------Man Power CLASS END HERE---------------

#----------------------------------Property Class START HERE---------------
class Property:
    def __init__(self, db):
        self.db = db

    def add_property(self, property_type, location, price):
        query = "INSERT INTO properties (type, location, price) VALUES (%s, %s, %s)"
        self.db.execute_query(query, (property_type, location, price))
        print("Property added successfully!")

    def list_properties(self):
        query = "SELECT * FROM properties"
        properties = self.db.fetch_all(query)
        print("\n--- Available Properties ---")
        for prop in properties:
            print(f"ID: {prop[0]}, Type: {prop[1]}, Location: {prop[2]}, Price: {prop[3]}, Status: {prop[4]}")
#----------------------------------Property Class END HERE---------------

#---------------------------------User Class START HERE------------------
class User():
    def __init__(self, db, hotel_manager, customer_manager,customer_info):
        self.db = db
        self.hotel_manager = hotel_manager
        self.customer_manager = customer_manager
        self.customer_info=customer_info
        
    def register_user(self, name, email, password, role="Customer"):
        query = "INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)"
        self.db.execute_query(query, (name, email, password, role))
        print("User registered successfully!")

    def login_user(self, email, password):
        query = "SELECT * FROM users where email = %s AND password = %s"
        user = self.db.fetch_all(query, (email, password))
        if user:
            role = user[0][4]
            print(f"Welcome, {user[0][1]}! You are logged in as {user[0][4]}.")
            return role
        else:
            print("Invalid login credentials!")
    def user_dashboard(self):
        while True:
            print("\n--- User Dashboard ---")
            print("1. View Hotels")
            print("2. Book a Hotel")
            print("3. View Properties")
            print("4. Logout")
            choice = input("Enter your choice: ")

            if choice == "1":
                # List hotels
                while True:
                    self.hotel_manager.list_hotels()
                    hotel_choice = input("Enter Your Choice: ")

                    if hotel_choice == '3':
                      break
                    elif hotel_choice.isdigit():
                      self.hotel_manager.list_hotel(int(hotel_choice))
                      self.hotel_manager.hotel_booking()
                      break  
            elif choice == "2":
                # Book a hotel
                self.hotel_manager.list_hotels()
                self.hotel_manager.hotel_booking()

            elif choice == "3":
                # View properties
                property_manager = Property(self.db)
                property_manager.list_properties()

            elif choice == "4":
                print("Logging out...")
                break

            else:
                print("Invalid choice. Please try again.")        
#---------------------------------User Class END HERE------------------

#------------------------------Main Application START HERE-------------
def main():
    # Connect to the database
    db = Database(host="localhost", user="root", password="", database="realestatedb")

    # Initialize Property and User objects
    property_manager = Property(db)
    customer_info=customer(db)
    hotel_manager=hotel(db,customer_info)
    job_list=Man_power(db)
    user_manager = User(db, hotel_manager,customer_info,customer_info)
    admin_manager=Admin(db)
    

    while True:
        print("\n--- WELCOME TO UNIQUE GROUP (PLC)---")
        print("1. USER REGISTRATION")
        print("2. LOGIN")
        print("3. HOSPITAL")
        print("4. PROPERTIES LIST")
        print("5. HOTEL")
        print("6. MAN POWER")
        print("7. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            # Register a new user
            name = input("Enter your name: ")
            email = input("Enter your email: ")
            password = input("Enter your password: ")
            user_manager.register_user(name, email, password)

        elif choice == "2":
            # User login
            email = input("Enter your email: ")
            password = input("Enter your password: ")
            role= user_manager.login_user(email, password)
            if role == "Admin":
                admin_manager.admin_dashboard()
            elif role == "Customer":
                user_manager.user_dashboard()
            else:
                print("Login failed! Please try again.")
        elif choice=="3":
            print("---WELCOME TO GULSHAN CLINIC---")
        elif choice == "4":
            # List all properties
            property_manager.list_properties()
        elif choice == "5":
         while True:
           hotel_manager.list_hotels()
           hotel_choice = input("Enter Your Choice: ")

           if hotel_choice == '3':
             break
           elif hotel_choice.isdigit():
              hotel_manager.list_hotel(int(hotel_choice))
              while True:
                 customer_choice= input("Enter Your Choice: ")
                 if customer_choice == '3':
                     break
                 elif customer_choice.isdigit():
                     fname=input("Enter Your First Name:")
                     lname=input("Enter Your Last Name:")
                     country=input("Enter your country name:")
                     email=input("Enter Your Email:")
                     days_=int(input("How many days:"))
                     customer_info.customer_booking(customer_choice,fname, lname, country, email, days_)
                     break
                 else:
                     print("Invalid")
                  
           else:
              print("Invalid choice. Please try again.")
        elif choice=="6":
            job_list.job_list()

        elif choice == "7":
            print("Exiting the system. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")
#------------------------------Main Application END HERE-------------

#---------------------------PROGRAM START FROM HERE-----------------
if __name__ == "__main__":
    main()