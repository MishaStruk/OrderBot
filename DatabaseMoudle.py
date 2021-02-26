import mysql.connector

FOODTYPE = ("pizza", "toast", "falafel")

def create_connection():
    mydb = mysql.connector.connect(
        host="<Enter Host>",
        user="<Enter user>",
        passwd="<Enter password>",
        database ="<Enter database>"
    )
    return mydb

class userDatabase():

    def __init__(self):
        """ Connects to the database"""
        self.db = create_connection()
        self.cursor_db = self.db.cursor()
        print(self.db)
    def CheckIfUserIdExist(self, username):
        """Function to check if a userid is in use"""
        """param: username : string : the user id of the username"""
        """:return : boolean"""
        cmd = "SELECT * FROM Users WHERE userid = '" + username + "'"
        self.cursor_db.execute(cmd)
        items = self.cursor_db.fetchall()
        if not items:
            return False
        return  True
    def addUser(self, username, password):
        """Function to add a use to the database"""
        """param: username : string : the user id of the username"""
        """param: password : string : password"""
        """:return : None"""
        if(self.CheckIfUserIdExist(username)):
            print("Username in use")
            return
        cmd = "INSERT INTO Users VALUES ('{0}','{1}',0)".format(username, password)
        self.cursor_db.execute(cmd)
        self.db.commit()
        print("Added")

    def fetchUserInfo(self, username):
        """Function to get a user information"""
        """param: username : string : the user id of the username"""
        """:return : List of the instances"""
        cmd = "SELECT * FROM Users WHERE userid = '" + username + "'"
        self.cursor_db.execute(cmd)
        items = self.cursor_db.fetchall()
        print(items)
        return items

    def checkIfOrderExist(self,username,date):
        """Function to check if there was an order that date"""
        """param: username : string : the user id of the username"""
        """param: date : int : date of the order"""
        """:return : boolean"""
        cmd = "SELECT * FROM Orders WHERE userid = '" + username + "' AND date='"+date+"'"
        self.cursor_db.execute(cmd)
        items = self.cursor_db.fetchall()
        if not items:
            return False
        return True
    def addOrder(self, username, foodType_str, date):
        """Function to add an order to a database"""
        """param: username : string : the user id of the username"""
        """param: foodType : string : type of food 0-pizza , 1 - toast, 2 - falafel"""
        """param: date : int : date of the order"""
        """:return : List of the instances"""

        """TODO: Add Cheking"""
        if not self.CheckIfUserIdExist(username):
            print("Username does not exist")
            return
        foodType= FOODTYPE.index(foodType_str)
        if foodType < 0 or foodType>2:
            print("Food does not exist")
            return
        if self.checkIfOrderExist(username, date):
            print ("You have already ordered today, Try tomorrow")
            return
        cmd = "INSERT INTO Orders VALUES ('{0}','{1}','{2}')".format(username, foodType,date)
        print(cmd)
        self.cursor_db.execute(cmd)
        self.db.commit()
        print("Added")

    def fetchOrders(self, username):
        """Function fetch order by username from the database """
        """param: username : string : the user id of the username"""
        """:return : List of the instances"""
        cmd = "SELECT * FROM Orders WHERE userid = '" + username + "'"
        print(cmd)
        self.cursor_db.execute(cmd)
        items = self.cursor_db.fetchall()
        return items

    def ShowAllOrders(self,username):
        list = self.fetchOrders(username)
        print("All orders of userid: "+username)
        print("Order  | Date")
        for item in list:
            print(FOODTYPE[item[1]]+"  "+item[2])

    def __del__(self):
        self.db.close()

if __name__ == '__main__':
    pass
# connection closing
# user_db.close()
# order_db.close()
