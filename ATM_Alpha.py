"""********************************************************************************"""
#  Welcome to Our ATM ::: 2021~2022                                                  #
#                                                                                    # 
#  This project was created for our 12th Grade Computer Science class.               #
#                                                                                    #
#  The project features various functions, simulating a real Atm to our utmost       #
#  best. The class feature of python was used to a minimum due to syllabus           #
#  limitations.                                                                      # 
#                                                                                    #
#  The program requires multiple modules to work, they are listed below and we       #
#  reccomend that users pip install them at the command line,                        #
#                                                                                    #
#  -> mysqlclient                                                                    #
#  -> mysql-connector-python                                                         #
#  -> pymysql                                                                        #
#  Other modules used are built-in python modules, hence there is no cause for       #  
#  concern.                                                                          #
#                                                                                    #
#  The program features a connection to a MySQL database - that has to be            #
#  pre-initialized - which logs in all of the information to reuse in the next       #
#  run of the code.                                                                  #
#                                                                                    #
#  We thank our parents, teachers and all elders for the support provided            #
#  during the construction of this program.                                          #
#                                                                                    #
#  WE SINCERELY PRESENT - :::ATM_Alpha:::                                            #
#                                                                                    #
#          |  @  |                   {Warning : Program to be run only on CMD.exe}   # 
#       |Drea.office|                {          for best results.                }   #
#          |     |                   {Use : -->python 'filename'.py              }   #
#         \-------/                                                                  #
#          \ _ _ /                   Created and Updated by : Naghul, Kellen, Saran  #
# Email: Dreaserous2.0@gmail.com     ATM_Alpha™ subsidary of - Dreaserous Holdings®  #
#                                    Dreaserous™              © All Rights Reserved  #
"""********************************************************************************"""

# CODE BEGINS ########################################################################

# Module Imports

import MySQLdb
from os import system
from time import sleep

# PseudoCLass-'Account' Definition

class Account():
    def __init__(self, name, acc_no, password, acc_balance = 1000):
        self.name = name
        self.acc_no = acc_no
        self.acc_balance = acc_balance
        self.password = password

    def __str__(self):
        return str(self.acc_no)

    def __len__(self):
        return self.acc_balance

    def withdraw(self, with_amt):
        self.acc_balance -= with_amt

    def deposit(self, depo_amt):
        self.acc_balance += depo_amt

    def acc_change(self, new_num):
        self.acc_no = new_num

    def list_maker(self):
        return [self.name, self.acc_no, self.acc_balance, self.password]

# Initiating connection with the pre-initialized MySQL database - 'atm'

myConnection = MySQLdb.connect( host='localhost', user='root', passwd='auth', db='atm')
cur = myConnection.cursor()


# MAIN PROGRAM ##################################################################################


if __name__ == "__main__":

    # ATM Running Condition
    choice = 'y'

    # Main Menu Loop
    while choice in 'yY':

        # ATM Display Screen
        print("================================================================================")

        print("                            WELCOME TO OUR ATM  ")

        print("================================================================================")

        print("1.To Create Account")
        print("2.To Login")
        print("3.Exit")
        print("================================================================================")

        # Choice of User
        op = int(input("Enter your Choice : "))
        print("================================================================================")

        # Account Status
        login = False

        # Cache of all present Records
        cur.execute("SELECT * FROM records")
        list_of_rec_1 = cur.fetchall()

        cur.execute("SELECT * FROM acc_records")
        list_of_rec = cur.fetchall()

        # User Driven Operations

        # Option 1 - Account Creation
        if op == 1:
            system('cls')
            length = len(list_of_rec)                       # To ensure no primary key duplicates the program
            acc_plus = int(list_of_rec[length - 1][0]) + 1  # assigns the account numbers.

            password = 0                                    # Password Variable
            con_password = 1                                # Password Confirmation Variable

            # User Input Loop
            while password != con_password: 
                name = str(1)
                while name.isdigit():
                    name = str(input("Enter your Name: "))                     # Account Name

                    # To make sure the name contains not digit characters
                    if name.isdigit():          
                        print("Please enter a string.\n")

                password = str(input("Enter your Password: "))                 # Password Entry   
                con_password = str(input("Confirm your Password: "))           # Confirmation

            acc_create = Account(name, acc_plus, con_password)

            list_acc = acc_create.list_maker()

            # Writing all data to the MySQL database
            cur.execute('INSERT INTO records(name, acc_no, acc_balance, password) values("{}", {}, {}, "{}")'.format(str(list_acc[0]), list_acc[1], list_acc[2], str(list_acc[3])))
            myConnection.commit()

            cur.execute('INSERT INTO acc_records(acc_rec) values({})'.format(acc_plus))
            myConnection.commit()

            # User Display/Choice
            print("Your Account Number is: ", list_acc[1])
            choice = input("Do you want to continue? (y/n)")


        # Option 2 - Login
        elif op == 2:

            # Login Condition
            acc_logged = 0

            # Login Loop
            while not login:
                acc_no_check = int(input("Enter Account Number: "))      # Login Account Number
                password_check = str(input("Enter Password: "))          # Account Password

                # Password Authentication
                for i in list_of_rec_1:
                    if i[1] == acc_no_check:
                        if i[3] == password_check:
                            login = True
                            print("Successful\n")
                            acc_logged = acc_no_check
                            continue
                        else:
                            print("Incorrect Password\n")

            # Fetching Acccount Details from MySQL Database
            cur.execute('select * from records where acc_no = {}'.format(acc_logged))
            list_log = list(cur.fetchall())

            # Creation of Temporary Account Object
            acc_create_log = Account(list_log[0][0], list_log[0][1], list_log[0][3], list_log[0][2])

            # Logged In Condition
            choice_1 = 'n'

            # Login Menu Loop
            while login and choice_1 in 'nN':
                    print("\n1.Depositng Money")            # ATM Features for users
                    print("2.Withdrawing Money")
                    print("3.Transfering Money")
                    print("4.Checking Balance")
                    print("5.Changing Account Number")
                    print("6.Account Details")
                    print("7.Transfer Account Details")
                    print("8.Delete Account\n")

                    list_logged = acc_create_log.list_maker()              # Account Details in List format
                    fields = ["Name", "Acc_No", "Balance", "Password"]

                    # User Option Selection
                    op_1 = int(input("Enter your Choice: "))

                    # Relevent Code
                    if op_1 == 1:
                        acc_create_log.deposit(int(input("Enter deposit amount: ")))  # Depositing using Class Function

                        # Updating records in the Database
                        cur.execute('UPDATE records SET acc_balance = {} WHERE acc_no = {}'.format(len(acc_create_log), list_logged[1]))
                        myConnection.commit()

                        # User Information
                        print("New Balance : {}".format(len(acc_create_log)))
                        choice_1 = input("Do you want to log off? (y/n)")

                    elif op_1 == 2:
                        acc_create_log.withdraw(int(input("Enter withdraw amount: ")))  # Withdrawing using Class Function

                        # Updating records in the Database
                        cur.execute('UPDATE records SET acc_balance = {} WHERE acc_no = {}'.format(len(acc_create_log), list_logged[1]))
                        myConnection.commit()

                        # User Information
                        print("New Balance : {}".format(len(acc_create_log)))
                        choice_1 = input("Do you want to log off? (y/n)")

                    elif op_1 == 3:
                        trans_amt = int(input("Enter amount to be Transferred: "))   # Amount to be Transferred
                        trans_acc = int(input("Enter receiving account: "))          # Account to be Transferred to
                        acc_create_log.withdraw(trans_amt)                           # Withdarwing Amount

                        # Updating records in the Database
                        cur.execute('UPDATE records SET acc_balance = {} WHERE acc_no = {}'.format(len(acc_create_log), list_logged[1]))
                        myConnection.commit()

                        # Fetching Tranfer Account
                        cur.execute('SELECT * FROM records WHERE acc_no = {}'.format(trans_acc))
                        list_transfer = cur.fetchall()

                        # Tranfering the amount
                        amt_transed = int(list_transfer[0][2]) + trans_amt
                        cur.execute('UPDATE records SET acc_balance = {} WHERE acc_no = {}'.format(amt_transed, trans_acc))
                        myConnection.commit()

                        # User Information
                        print("Your Balance : {}".format(len(acc_create_log)))
                        choice_1 = input("Do you want to log off? (y/n)")

                    elif op_1 == 4:
                        print("Current Balance : {}".format(len(acc_create_log)))  # Fetching and Displaying Current Balance
                        choice_1 = input("Do you want to log off? (y/n)")

                    elif op_1 == 5:
                        acc_no_new = int(input("Enter New Account Number: ")) # New Account Number
                        acc_create_log.acc_change(acc_no_new)                 # Locally Changing Account Number

                        # Updating records in the Database
                        cur.execute('update records set acc_no = {} where acc_no = {}'.format(acc_no_new, list_logged[1]))
                        myConnection.commit()

                        # User Information
                        print("New Account Number :", end =" ")
                        print(acc_create_log)
                        choice_1 = input("Do you want to log off? (y/n)")

                    elif op_1 == 6:
                        # Fetching Logged Account Details
                        print("Account Holder details are as follows,\n" + str(fields) + '\n' + str(list_logged)) 
                        choice_1 = input("Do you want to log off? (y/n)")

                    elif op_1 == 7:
                        # Fetching all Accounts
                        for i in list_of_rec_1: 
                            if i[1] != list_logged[1] and i[1] != 1000:                   # Condition to exclude logged account and Setter Account
                                print("Account Name:", i[0], "---","Account No:", i[1])   # Displaying Account Names and Numbers

                    elif op_1 == 8:
                        # Confirmation of Important Choice
                        ch = (input("Do you want to delete your Account? (y/n)"))

                        # Deleting Stored Records
                        if ch in 'yY':
                            cur.execute("DELETE FROM records WHERE acc_no = {}".format(list_logged[1]))
                            myConnection.commit()

                        # User Information
                        print("\nThank You for working with ATM_Alpha!")

                        # Terminate the Program
                        choice = 'n'
                        break

                    else:
                        print("Invalid Entry") # User Display in case of Wrong Entry
                        choice_1 = input("Do you want to log off? (y/n)")

        elif op == 3:
            print("BYE BYE") # User Display in case of Exit
            choice = 'n'

        else:
            print("Invalid Entry") # User Display in case of Wrong Entry
            choice = input("Do you want to continue? (y/n)")
