import mysql.connector
from mysql.connector import Error

somethingWrong = True
while somethingWrong:
    try:
        uname = input("Please input database username >>> ")
        pword = input("Please input database password >>> ")
        db = mysql.connector.connect(host="localhost", user=uname, password=pword)
        if (db):
            print("Connection successful")
            somethingWrong = False
    except Error:
        print("Connection unsuccessful")
        continue


cursor = db.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS vehicleStock")
cursor.execute("CREATE TABLE IF NOT EXISTS vehicleStock.vehicles("
                 "make VARCHAR(255) NOT NULL,"
                 "model VARCHAR(255) NOT NULL,"
                 "registration VARCHAR(255) NOT NULL,"
                 "price INTEGER(10),"
                 "PRIMARY KEY (registration))")


def readRangeInteger(prompt, minRange, maxRange):
    somethingIsWrong = True
    while somethingIsWrong:
        try:
            number = int(input(prompt))
            if minRange <= number <= maxRange:
                somethingIsWrong = False
            else:
                print(f"Please enter a number between {minRange} and {maxRange}.")
        except:
            print("Must be numeric.")
    return number


def readPositiveInteger(prompt):
    somethingIsWrong = True
    while somethingIsWrong:
        try:
            number = int(input(prompt))
            somethingIsWrong = number <= 0
            if number <= 0:
                print("Number must be positive.")
        except:
            print("Must be numeric.")
    return number


def readNonemptyString(prompt):
    while True:
        s = input(prompt)
        noSpaces = s.replace(' ', '')
        if len(noSpaces) > 0:
            break
        else:
            print("Please type into the user input box.")
    return s.capitalize()


def readNonemptyAlphabeticalString(prompt):
    somethingIsWrong = True
    while somethingIsWrong:
        s = input(prompt)
        copyNoSpace = s.replace(" ", "")
        if len(s) > 0 and copyNoSpace.isalpha():
            somethingIsWrong = False
        else:
            print("Letters only please.")
    return s.capitalize()


def mainMenu():  # Primary Menu.
    print(f"\nMain Menu"
          f"\n------------------------------"
          f"\n1: Edit the Table. "
          f"\n2. Select From Table. "
          f"\n3. Quit.")
    menuChoice = readRangeInteger("Please enter the corresponding number. >>> ", 1, 3)
    return menuChoice


def editMenu():
    print(f"\n Alter Table Menu"
          f"\n------------------------------"
          f"\n1: Insert. "
          f"\n2. Update. "
          f"\n3. Delete. "
          f"\n4. Back to menu")
    editChoice = readRangeInteger("Please enter the corresponding number. >>> ", 1, 4)
    return editChoice


def selectMenu():
    print(f"\n Search Menu"
          f"\n------------------------------"
          f"\n1: Search by make. "
          f"\n2. Search by model. "
          f"\n3. Search by make & model."
          f"\n4. Search by registration."
          f"\n5. Search by price."
          f"\n6. Search by price between."
          f"\n7. Show all vehicles.   "
          f"\n8. Back to menu.")

    selectChoice = readRangeInteger("Please enter the corresponding number. >>> ", 1, 8)
    return selectChoice


def insert():
    try:
        make = readNonemptyAlphabeticalString("Please enter the vehicle make. >>> ").capitalize()
        model = readNonemptyString("Please enter the vehicle model. >>> ").capitalize()
        reg = readNonemptyString("Please enter the vehicle registration. >>> ").upper()
        price = readPositiveInteger("Please enter the vehicle price. >>> ")

        sqlFormula = "INSERT INTO vehicleStock.vehicles (make, model, registration, price) VALUES (%s, %s, %s, %s)"
        newVehicle = (make, model, reg, price)
        cursor.execute(sqlFormula, newVehicle)

        sqlNCT = "INSERT INTO vehicleStock.nct (registration, nctDate) VALUES (%s, %s, %s, %s)"
        newVehicle = (make, model, reg, price)
        cursor.execute(sqlFormula, newVehicle)

        print(cursor.rowcount, "vehicle successfully added.")
        db.commit()
    except Error:
        print("Vehicle is already registered.")

def update():
    selectAllData()
    regToChange = readNonemptyString("Please enter the registration of the vehicle you would like to change. >>> ")
    print(f"\n Alter Menu"
          f"\n------------------------------"
          f"\n1: Change make. "
          f"\n2. Change model. "
          f"\n3. Change registration."
          f"\n4. Change price."
          f"\n5. Back to menu.")
    toBeChanged = readRangeInteger("Enter the corresponding number. >>> ", 1, 5)
    if toBeChanged == 1:
        alterMake(regToChange)
    if toBeChanged == 2:
        alterModel(regToChange)
    if toBeChanged == 3:
        alterReg(regToChange)
    if toBeChanged == 4:
        alterPrice(regToChange)
    if toBeChanged == 5:
        main()


def delete():
    try:
        if selectAllData() == True:
            sql = "DELETE FROM vehicleStock.vehicles WHERE registration = %s"
            regToDelete = readNonemptyString("Please enter the registration of the vehicle you would like to delete. >>> ")
            cursor.execute(sql, (regToDelete,))
            print(cursor.rowcount, "record(s) affected")
            db.commit()

    except Error:
        print("\nYou don't have the sufficient permissions to do that or that registration does not exist.")


def alterMake(regToChange):
    sql = "UPDATE vehicleStock.vehicles SET make = %s WHERE registration = %s"
    input = readNonemptyString(f"What would you like to change the make to? >>> ").capitalize()
    val = (input, regToChange)
    cursor.execute(sql, val)
    db.commit()
    print(cursor.rowcount, "record(s) affected")



def alterModel(regToChange):
    sql = "UPDATE vehicleStock.vehicles SET model = %s WHERE registration = %s"
    input = readNonemptyString(f"What would you like to change the model to? >>> ").capitalize()
    val = (input, regToChange)
    cursor.execute(sql, val)
    db.commit()
    print(cursor.rowcount, "record(s) affected")


def alterReg(regToChange):
    sql = "UPDATE vehicleStock.vehicles SET registration = %s WHERE registration = %s"
    input = readNonemptyString(f"What would you like to change the registration to? >>> ").upper()
    val = (input, regToChange)
    cursor.execute(sql, val)
    db.commit()
    print(cursor.rowcount, "record(s) affected")


def alterPrice(regToChange):
    sql = "UPDATE vehicleStock.vehicles SET price = %s WHERE registration = %s"
    input = readPositiveInteger(f"What would you like to change the price to? >>> ")
    val = (input, regToChange)
    cursor.execute(sql, val)
    db.commit()
    print(cursor.rowcount, "record(s) affected")


def selectAllData():
    cursor.execute("SELECT * FROM vehicleStock.vehicles")
    data = cursor.fetchall()
    if not cursor.rowcount:
        print("There are currently no vehicles stored in the database.")
        return False
    else:
        print(" Make   Model    Registration    Price")
        for row in data:
            print(row)
        return True


def selectDataByMake():
    input = readNonemptyAlphabeticalString(f"Please enter the make of vehicle you would like to search. >>> ")
    sqlSelectQuery = "select * from vehicleStock.vehicles where make = %s"
    cursor.execute(sqlSelectQuery, (input,))
    data = cursor.fetchall()
    if not cursor.rowcount:
        print("No results found")
    else:
        print(" Make   Model    Registration    Price")
        for row in data:
            print(row)


def selectDataByModel():
    input = readNonemptyAlphabeticalString(f"Please enter the model of vehicle you would like to search. >>> ")
    sqlSelectQuery = "select * from vehicleStock.vehicles where model = %s"
    cursor.execute(sqlSelectQuery, (input,))
    data = cursor.fetchall()
    if not cursor.rowcount:
        print("No results found")
    else:
        print(" Make   Model    Registration    Price")
        for row in data:
            print(row)


def selectDataByMakeAndModel():
    inputMake = readNonemptyAlphabeticalString(f"Please enter the make of vehicle you would like to search. >>> ")
    inputModel = readNonemptyAlphabeticalString(f"Please enter the model of vehicle you would like to search. >>> ")
    sqlSelectQuery = "select * from vehicleStock.vehicles where make = %s and model = %s"
    cursor.execute(sqlSelectQuery, (inputMake, inputModel,))
    data = cursor.fetchall()
    if not cursor.rowcount:
        print("No results found")
    else:
        print(" Make   Model    Registration    Price")
        for row in data:
            print(row)


def selectDataByRegistration():
    input = readNonemptyString(f"Please enter the registration of the vehicle you would like to search. >>> ")
    sqlSelectQuery = "select * from vehicleStock.vehicles where registration = %s"
    cursor.execute(sqlSelectQuery, (input,))
    data = cursor.fetchall()
    if not cursor.rowcount:
        print("No results found")
    else:
        print(" Make   Model    Registration    Price")
        for row in data:
            print(row)


def selectDataByPrice():
    input = readPositiveInteger("Please enter the price of vehicle you would like to search? >>> ")
    sqlSelectQuery = "select * from vehicleStock.vehicles where price = %s"
    cursor.execute(sqlSelectQuery, (input,))
    data = cursor.fetchall()
    if not cursor.rowcount:
        print("No results found")
    else:
        print(" Make   Model    Registration    Price")
        for row in data:
            print(row)


def selectDataByPriceBetween():
    inputMin = readPositiveInteger("Please enter the minimum price of vehicle you would like to search? >>> ")
    inputMax = readPositiveInteger("Please enter the maximum price of vehicle you would like to search? >>> ")
    sqlSelectQuery = "SELECT * FROM vehicleStock.vehicles WHERE price BETWEEN %s AND %s"
    cursor.execute(sqlSelectQuery, (inputMin, inputMax,))
    data = cursor.fetchall()
    if not cursor.rowcount:
        print("No results found")
    else:
        print(" Make     Model  Registration  Price")
        for row in data:
            print(row)


def main():
    while True:
        menuChoice = mainMenu()

        if menuChoice == 1:  # option edit table
            editChoice = editMenu()

            if editChoice == 1:  # option insert new vehicle
                howMany = readRangeInteger("Please enter the number of vehicles would you like to insert >>> ", 1, 99)  # how many vehicles to insert
                i = 1
                while i <= howMany:
                    insert()
                    i += 1

            if editChoice == 2:  # option to update table
                update()

            if editChoice == 3:  # option to update table
                delete()

            if editChoice == 4:  # option to return to menu
                main()

        if menuChoice == 2:  # option select
            selectChoice = selectMenu()

            if selectChoice == 1:  # search by make
                selectDataByMake()

            if selectChoice == 2:  # search by model
                selectDataByModel()

            if selectChoice == 3:  # search by make & model
                selectDataByMakeAndModel()

            if selectChoice == 4:  # search by reg
                selectDataByRegistration()

            if selectChoice == 5:  # search by price
                selectDataByPrice()

            if selectChoice == 6:  # search by price between
                selectDataByPriceBetween()

            if selectChoice == 7:  # show all vehicles
                selectAllData()

            if selectChoice == 8:  # return to menu
                main()

        if menuChoice == 3:  # option quit
            print("\nGoodbye.")
            cursor.close()
            db.close()
            quit()


main()
