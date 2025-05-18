# fluteDAO.py
# Data access layer for the flute database table.
# Author: E. Qejvani
# Based on lectures by A. Beatty

import mysql.connector
import dbconfig as cfg

class FluteDAO:
    connection = ""  # Will hold the database connection
    cursor = ""      # Will hold the cursor object for executing queries
    host = ''         # DB host
    user = ''         # DB user
    password = ''     # DB password
    database = ''     # DB name

    # Initializing DB connection details from config
    def __init__(self):
        self.host = cfg.mysql['host']
        self.user = cfg.mysql['user']
        self.password = cfg.mysql['password']
        self.database = cfg.mysql['database']

    # Creating and connecting cursor for queries
    def getcursor(self):
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
        )
        self.cursor = self.connection.cursor()
        return self.cursor

    # Close cursor and connection
    def closeAll(self):
        self.connection.close()
        self.cursor.close()

    # Retrieve all flute records from the database
    def getAll(self):
        cursor = self.getcursor()
        sql = "SELECT * FROM flute"
        cursor.execute(sql)
        results = cursor.fetchall()
        returnArray = []
        for result in results:
            returnArray.append(self.convertToDictionary(result))
        self.closeAll()
        return returnArray

    # Find a flute by ID
    def findByID(self, id):
        cursor = self.getcursor()
        sql = "SELECT * FROM flute WHERE fluteID = %s"
        values = (id,)
        cursor.execute(sql, values)
        result = cursor.fetchone()
        returnValue = self.convertToDictionary(result)
        self.closeAll()
        return returnValue

    # Insert a new flute into the database
    def create(self, flute):
        cursor = self.getcursor()
        sql = """INSERT INTO flute (fluteMaker, fluteModel, fluteLevel, fluteHead,
                 fluteBody, fluteMechanism, priceRange) VALUES (%s,%s,%s,%s,%s,%s,%s)"""
        values = (
            flute.get("fluteMaker"),
            flute.get("fluteModel"),
            flute.get("fluteLevel"),
            flute.get("fluteHead"),
            flute.get("fluteBody"),
            flute.get("fluteMechanism"),
            flute.get("priceRange"),
        )
        cursor.execute(sql, values)
        self.connection.commit()
        newid = cursor.lastrowid
        flute["fluteID"] = newid
        self.closeAll()
        return flute

    # Update an existing flute record
    def update(self, id, flute):
        cursor = self.getcursor()
        sql = """UPDATE flute SET fluteMaker=%s, fluteModel=%s, fluteLevel=%s,
                 fluteHead=%s, fluteBody=%s, fluteMechanism=%s, priceRange=%s WHERE fluteID = %s"""
        values = (
            flute.get("fluteMaker"),
            flute.get("fluteModel"),
            flute.get("fluteLevel"),
            flute.get("fluteHead"),
            flute.get("fluteBody"),
            flute.get("fluteMechanism"),
            flute.get("priceRange"),
            id
        )
        cursor.execute(sql, values)
        self.connection.commit()
        self.closeAll()

    # Delete a flute by ID
    def delete(self, id):
        cursor = self.getcursor()
        sql = "DELETE FROM flute WHERE fluteID = %s"
        values = (id,)
        cursor.execute(sql, values)
        self.connection.commit()
        self.closeAll()
        print("delete done")

    # Convert a database result tuple into a dictionary
    def convertToDictionary(self, resultLine):
        keys = ['fluteID', 'fluteMaker', 'fluteModel', 'fluteLevel',
                'fluteHead', 'fluteBody', 'fluteMechanism', 'priceRange']
        flute = {}
        if resultLine:
            for i, value in enumerate(resultLine):
                flute[keys[i]] = value
        return flute


# Create an instance of FluteDAO to use for database operations
fluteDAO = FluteDAO()
