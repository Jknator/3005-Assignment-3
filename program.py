import psycopg2
from datetime import datetime

#defining global variable to ensure consistency with function defs in specs
global connection

#Retrieves and displays all records from the students table.
def getAllStudents():
    try: 
        #getting connection and cursor
        global connection
        cursor = connection.cursor()
        #using query to get the table of students
        cursor.execute(f"SELECT * From students")

        # using fetchall(), we can get the query we made before from the cursor
        rows = cursor.fetchall()

        #printing table
        print("(student_id, first_name, last_name, email, enrollment_date)")

        for row in rows:
            print(row)
        print("\nPrinting table complete.\n")

    except psycopg2.Error as e:
         print(f"Error, cannot get students: {e}\n")



#Inserts a new student record into the students 
def addStudent(first_name, last_name, email, enrollemnt_date):
    try:
        #getting connection and cursor
        global connection
        cursor = connection.cursor()

        #using query to insert a new student with given values
        cursor.execute(""" INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES (%s,%s,%s,%s)""", (first_name, last_name, email, enrollemnt_date))

        #establish changes to database
        connection.commit()

        #print for formatting
        print("\nAdding student complete. \n")
    except psycopg2.Error as e:
         print(f"Error, cannot add student: {e}\n")


#Updates the email address for a student with the specified student_id.
def updateStudentEmail(student_id, new_email):
        try:
            #getting connection and cursor
            global connection
            cursor = connection.cursor()

            #checks to see if given id is valid
            cursor.execute("SELECT EXISTS (SELECT 1 From students where student_id = %s)", (student_id,))
            if(not cursor.fetchone()[0]):
                print("Invalid student ID.\n")
                return 
            
            #using query to update a specific student 
            cursor.execute("UPDATE students SET email = %s WHERE student_id=%s", (new_email, student_id))
            #establish changes to database
            connection.commit()

            #print for formatting
            print("\nUpdating student complete.\n")

        except psycopg2.Error as e:
            print(f"Error, cannot update student: {e}\n")




#Deletes the record of the student with the specified student_id
def deleteStudent(student_id): 
        try:
            #getting connection and cursor
            global connection
            cursor = connection.cursor()

            #checks to see if given id is valid
            cursor.execute("SELECT EXISTS (SELECT 1 From students where student_id = %s)", (student_id,))
            if(not cursor.fetchone()[0]):
                print("Invalid student ID.\n")
                return 
            
            #using query to delete a specific student 
            cursor.execute("DELETE from students WHERE student_id=%s", (student_id,))
            #establish changes to database
            connection.commit()

            #print for formatting
            print("\nDeleting student complete.\n")

        except psycopg2.Error as e:
            print(f"Error, could not delete student: {e}\n")    



#executes the given filename. The return is a bool that represents if the operation was successful or not
def executeGivenFileToDatabase(filename, cursor):
    
    try: 
        #put contents of file into a string 
        with open(filename, "r") as file:
            fileContents = file.read()

        #execute file
        cursor.execute(fileContents)

        #returns true as operation was successful
        return True

    except psycopg2.Error as e:
         print(f"Error, cannot run file: {e}\n")
         return False



#if the database hasn't already ran the DDL.sql and DML.sql then this function will run them 
#DML will only run if DDL runs. So its either both run or neither runs.
def setupDatabase():
    doesTableExist = False
    try: 
        #get a cursor which is crucial for retrieving and manipulating data
        global connection
        cursor = connection.cursor()
        #query returns a bool if "Students" exists or not 
        cursor.execute("select exists(select relname from pg_class where relname= %s)", ("students",))
        # We then use fetchone()[0] to get that bool value we got from our previous query
        doesTableExist = cursor.fetchone()[0]

        #run data
        if(not doesTableExist):
            #checking if both succssesfully executed if so print the victory
            check1 = executeGivenFileToDatabase("DDL.sql", cursor)
            check2 = executeGivenFileToDatabase("DML.sql", cursor)
            if(check1 and check2):
                print("Created Students table and filled with initial data!\n")
                
            #save changes
            connection.commit()
        else:
            print("Students table already exists. Will not create table and fill with initial data!\n")

        #close cursor 
        cursor.close()

    except psycopg2.Error as e:
         print(f"Error, could not initilizae database: {e}\n")



def main():
    #values to make connection with specific postgres database
    m_user = "postgres"
    m_password = "PASSWORD"
    m_host = "localhost" 
    m_port = 5432
    m_database = "Assignment3-1"

    #establish connection with postgres database. If it can't make a connection tell user to fix variables, and try again. 
    try: 
        global connection 
        connection = psycopg2.connect(user=m_user, password=m_password, host=m_host, port=m_port, database=m_database)
    except psycopg2.Error as e:
         print("Error: cannot make connection to database. Fix values given.")
         exit()

    #if there is no Students table then make one and fill with data
    setupDatabase()

    #as long user doesn't want to end session then continue loop
    finishSession = False

    while(not finishSession):
        print("1: Get all students.")
        print("2: Add a student.")
        print("3: Update a student's email.")
        print("4: Delete a student.")
        print("5: Exit program\n")
        
        userInput = input("Input a command using associated number: ")
       
       #checking if user input is valid. If not tell user it is invalid. If it is then call function/command
        if (userInput.isnumeric()):
            userInput = int(userInput)
            cursor = connection.cursor()

            if (userInput > 0 and userInput <= 5):

                if(userInput == 1):
                    getAllStudents()

                if(userInput == 2):
                    #get information on student
                    firstName = input("Input first name: ")
                    lastName = input("Input last name: ")
                    email = input("Input email: ")
                    
                    #requires user to put 3 valid integers that form a valid date, or keep looping
                    while(True):
                        year = input("Input the year of enrollment: ")
                        month = input("Input the month of enrollment: ")
                        day = input("Input the day of enrollment: ")
                        
                        #checking if inputs are numeric
                        if(year.isnumeric() and month.isnumeric() and day.isnumeric()):
                            try:
                                #this is how we check if given date is valid
                                enrollmentDate = datetime(int(year), int(month), int(day)).strftime("%Y-%d-%m")
                                break
                            except ValueError:
                                print("Invalid date! Please provide valid date.")
                        else:
                            print("Please provide integers.")
                    addStudent(firstName, lastName, email, enrollmentDate)
                        
                if(userInput == 3):
                    while(True):
                        studentID = input("Input student ID: ")
                        if(studentID.isnumeric()):
                            break
                        else:
                            print("Invalid input. Please insert a integer.")
                    newEmail = input("Input new email for given student: ")
                    updateStudentEmail(studentID, newEmail)

                if(userInput == 4):
                    while(True):
                        studentID = input("Input student ID: ")
                        if(studentID.isnumeric()):
                            break
                        else:
                            print("Invalid input. Please insert a integer.")                    
                    deleteStudent(studentID)

                if (userInput == 5):
                    print("closing")
                    quit();
            else:
                print("Invalid number!\n")
        else:
             print("Invalid input!\n")


if __name__ == "__main__":
        main()
