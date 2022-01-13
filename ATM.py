import MySQLdb
myConnection = MySQLdb.connect( host='localhost', user='root', passwd='auth', db='atm')


'''def doQuery( conn ) :
    cur = conn.cursor()

    cur.execute( "SELECT RollNo, Name FROM student" )

    for firstname, lastname in cur.fetchall() :
        print( firstname, lastname )
doQuery(myConnection)
'''

cur = myConnection.cursor()                                               # IMPORTANT reuse code
cur.execute( "SELECT * FROM records" )
list_of_rec = cur.fetchall()
data = cur.rowcount                                                       # IMPORTANT reuse code
cur.execute( "SELECT * FROM records" )
list_of_rec_1 = cur.fetchall()



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




#acc_1 = Account("Kellen", 1001, 5000, input("Enter Password: "))




print("================================================================================")

print("                            WELCOME TO OUR ATM  ")

print("================================================================================")

print("1.To Create Account")
print("2.To Login")
print("3.Exit")
print("================================================================================")

op = int(input("Enter your Choice : "))
print("================================================================================")

login = False

if op == 1:

    length = len(list_of_rec_1)
    acc_plus = list_of_rec_1[length - 1][1]

    password = 0
    con_password = 1
    while password != con_password:
        name = str(1)
        while name.isdigit():
            name = str(input("Enter your Name: "))
            if name.isdigit():
                print("Please enter a string.\n")
        password = str(input("Enter your Password: "))
        con_password = str(input("Confirm your Password: "))

    acc_create = Account(name, acc_plus+1, con_password)

    list_acc = acc_create.list_maker()

    cur.execute('insert into records(name, acc_no, acc_balance, password) values("{}", {}, {}, "{}")'.format(str(list_acc[0]), list_acc[1], list_acc[2], str(list_acc[3])))
    myConnection.commit()

if op == 2:
    while not login:
        acc_no_check = int(input("Enter Account Number: "))
        password_check = str(input("Enter Password: "))
        for i in list_of_rec:
            if i[1] == acc_no_check:
                if i[3] == password_check:
                    login = True
                else:
                    print("Incorrect Password\n")


elif op == 3:
    print("BYE BYE")