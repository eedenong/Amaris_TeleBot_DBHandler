import sqlite3
import numpy as np
import io
import ast
import json
# Python class to handle the database
# The class has one attribute, which is the connection to the database
class DBHandler():
    def __init__(self, conn):
        self.conn = conn

        
    def create_tables(self):
        print("creating tables")
    # Name is a string of the table name
    # Params is a tuple indicating the column names of the table to be created, and their respective data types
        cur = self.conn.cursor()
        #params = self.__get_params__()
        #cur.execute("CREATE TABLE IF NOT EXISTS ? ?", (name, params))
        create_job_table_cmd = """
        CREATE TABLE IF NOT EXISTS JobsTable (
            id INTEGER PRIMARY KEY,
            job_id TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL
        );
        """
        cur.executescript(create_job_table_cmd)
        print("Created JobsTable table")
        # log is an dict that of 
        # format: KEY job_id, VALUE array of results
        create_logging_table_cmd = """
        CREATE TABLE IF NOT EXISTS UserLogs (
            id INTEGER PRIMARY KEY,
            user_id TEXT NOT NULL,
            log BLOB NOT NULL
        );
        """
        cur.executescript(create_logging_table_cmd)
        print("Created UserLogs table")
    # Insert new data into either JobsTable or UserLogs
    # data_to_insert is a tuple with the format:
    # if table_name is JobsTable, data_to_insert = (job_id, latitude, longitude)
    # if table_name is UserLogs, data_to_insert = (user_id, log)
    def insert_data(self, table_name, data_to_insert):
        cur = self.conn.cursor()
        #cur.execte('INSERT INTO {} ({}) VALUES ?'.format(table_name, rows_col), (data_to_insert, ))
        #print(cur.fetchone())
        
        # Inserting data into JobsTable
        # Tuple will be of the format (job_id, latitude, longitude)
        if table_name == "JobsTable":
            data = data_to_insert.split(' ')
            print("Inserting into JobsTable: {}".format(data_to_insert))
            job_id = data[0]
            lat = data[1]
            lon = data[2]
            print(job_id)
            print(lat)
            print(lon)
            cur.execute('INSERT INTO JobsTable (job_id, latitude, longitude) VALUES (?, ?, ?)', (job_id, lat, lon))
            self.conn.commit()
        elif table_name == "UserLogs":
            #John {"A010": ["020220_Y"], "A002":["121119_N", "010220_Y"]} -> does not work
            #John {'A010': ['020220_Y'], 'A002':['121119_N', '010220_Y']}
            user_id = data_to_insert.split(' ')[0]
            logs_dict = data_to_insert[len(user_id)+1:]
            logs_dict = ast.literal_eval(logs_dict)
            print(type(logs_dict))
            # convert to bytes
            logs_dict_bytes = json.dumps(logs_dict).encode('utf-8')
            print(type(logs_dict_bytes))
            print("Inserting into UserLogs: {}".format(data_to_insert))
            #print(user_id)
            #print(log)
            cur.execute('INSERT INTO UserLogs (user_id, log) VALUES (?, ?)', (user_id, logs_dict_bytes))
            self.conn.commit()
        print("Data successfully inserted")
        #cur.fetchall()
    # update_data enables the changing of data in the specified table_name
    # data_to_update is in the format:
    # JobsTable: (latitude, longitude, job_id) -> updates a new value for latitude and longitude for the specified job_id
    # UserLogs: (log, user_id)
    def update_data(self, table_name, data_to_update):
        cur = self.conn.cursor()
        data = data_to_update.split(' ')
        if table_name == "JobsTable":
            print("Updating JobsTable data at job {} with lat {} and long {}".format(data[0], data[1], data_to_update[2]))
            cur.execute('UPDATE JobsTable SET latitude = ?, longitude = ? WHERE job_id = ?', (data[0], data[1]))
            self.conn.commit()
        elif table_name == "UserLogs":
            print("Updating JobsTable data at user {} with log {}".format(data[0], data[1]))
            cur.execute('UPDATE UserLogs SET log = ? WHERE user_id = ?', (data[0], data[1]))
            self.conn.commit()
        print("Table updated")
        cur.fetchall()
    # deletes the specified row(s) from the table_name
    # for JobsTable, use job_id to reference row to be deleted
    # for UserLgs, use user_id to reference row to be deleted
    # supports the deletion of multiple rows
    def delete_data(self, table_name, rows, use_id=False):
        #cur = self.conn.cursor()
        rows = rows.split(' ')
        if not use_id:
            if len(rows) > 1:
                self.__delete_mult__(table_name, rows)
            else:
                self.__delete_single__(table_name, rows[0])
        else:
            if len(rows) > 1:
                self.__delete_mult__(table_name, rows, use_id=True)
            else:
                self.__delete_single__(table_name, rows[0], use_id=True)
        self.conn.commit()
        print("Data successfully deleted")


    def __delete_single__(self, table_name, row, use_id=False):
        cur = self.conn.cursor()
        if table_name == "JobsTable":
            if not use_id:
                print("Deleting data from JobsTable at job {}".format(row))
                cur.execute('DELETE FROM JobsTable WHERE job_id = ?', (row, ))
            else:
                print("Deleting data from JobsTable at row {}".format(row))
                cur.execute('DELETE FROM JobsTable WHERE id = ?', (row, ))
        elif table_name == "UserLogs":
            if not use_id:
                print("Deleting data from UserLogs at user_id {}".format(row))
                cur.execute('DELETE FROM UserLogs WHERE user_id = ?', (row, ))
            else:
                print("Deleting data from UserLogs at row {}".format(row))
                cur.execute('DELETE FROM UserLogs WHERE id = ?', (row, )) 
        self.conn.commit()

    def __delete_mult__(self, table_name, rows, use_id=False):
        cur = self.conn.cursor()
        for i in range(len(rows)):
            self.__delete_single__(table_name, rows[i], use_id)
        
    # returns the specified row in the table_name
    def view_data(self, table_name, row, use_id=False):
        cur = self.conn.cursor()
        if table_name == "JobsTable":
            if not use_id:
                cur.execute('SELECT * FROM JobsTable WHERE job_id = ?', (row, ))
                self.__print_view_data__(cur, ["job_id", "latitude", "longitude"])
            else:
                cur.execute('SELECT * FROM JobsTable WHERE id = ?', (row, ))
                self.__print_view_data__(cur, ["job_id", "latitude", "longitude"])
        elif table_name == "UserLogs":
            if not use_id:
                cur.execute('SELECT * FROM UserLogs WHERE user_id = ?', (row, ))
                self.__print_view_data__(cur, ["user_id", "log"])
            else:
                cur.execute('SELECT * FROM UserLogs WHERE id = ?', (row, ))
                self.__print_view_data__(cur, ["user_id", "log"])

    def __print_view_data__(self, cursor, param_list):
        data = cursor.fetchone()
        #print(type(data))
        print("--------- REQUESTED DATA ---------")
        count = 0
        for i in range(len(param_list)):
            print("{}: {}".format(param_list[i], data[i+1]))
        print("----------------------------------")

    def __get_params__(self):
        col_names_arr = []
        col_types_arr = []
        # While loop to add names
        while True:
            num_names = input("Please enter the number (positive integer) of columns for the table: ")
            if num_names.isdigit():
                # Make sure that the number that is entered is a valid value
                if int(num_names) > 0:
                    x = int(num_names)
                    for i in range(x):
                        name = input("Enter the name of column number {}: ".format(i+1))
                        col_names_arr.append(name)
                    # Done appending names 
                    break
                else:
                    print("Invalid input. Please enter a POSTIVE integer")
                    continue
            else:
                print("Invalid input. Please input a valid integer")
                continue
        
        i = 0
        
        #print_help("initial data input")
        while i < len(col_names_arr):
            data_type = input("Please input data type for column number {}:".format(i+1))
            data_type = data_type.upper()
            correct_input = check_valid_datatype(data_type)
            if correct_input:
                col_types_arr.append(data_type)
                i += 1
            else:
                print_help("invalid data input")
                continue
        param_string = self.__generate_param_string__(col_names_arr, col_types_arr)
        return param_string

    # Given an array of names and types for the database columns, create a string
    # names, types are all in string
    def __generate_param_string__(self, names_arr, types_arr):
        #"(logs BLOB NOT NULL, worker_name TEXT NOT NULL)"
        param_list = []
        for i in range(len(names_arr)):
            name = names_arr[i]
            data_type = types_arr[i]
            new_string = name + ' ' + data_type
            param_list.append(new_string)
            #print(param_list)
        
        output_string = ', '.join(param_list)
        return output_string


####################
# HELPER FUNCTIONS #
####################
def dict_to_binary(the_dict):
    str = json.dumps(the_dict)
    binary = ' '.join(format(ord(letter), 'b') for letter in str)
    return binary


def binary_to_dict(the_binary):
    jsn = ''.join(chr(int(x, 2)) for x in the_binary.split())
    d = json.loads(jsn)  
    return d

def convert_to_bin_data(filename):
    with open(filename, 'rb') as file:
        blob = file.read()
    return blob

def check_valid_datatype(datatype_string):
    is_null = datatype_string == "NULL" 
    is_integer = datatype_string == "INTEGER"
    is_float = datatype_string == "REAL"
    is_string = datatype_string == "TEXT"
    is_blob = datatype_string == "BLOB"
    if is_null or is_integer or is_float or is_string or is_blob:
        return True
    else:
        return False

def print_help(option):
    if option == "init":
        print("Running Amaris.ai Manhole Detection Database Manager")
        print('-----------------------------------------------------------------')
        print("List of commands: ")
        print("CREATE: create new table in database")
        print("INSERT: insert new entry into existing table in database")
        print("DELETE: delete an entry from existing table in database")
        print("VIEW: view an entry in an existing table in the database")
        print('-----------------------------------------------------------------')
    elif option == "initial data input":
        print('-----------------------------------------------------------------')
        print("Please input the data types for each of your respective columns.")
        print("Supported data types are as listed (in all caps): ")
        print("NULL: null value")
        print("INTEGER: signed integer")
        print("REAL: floating point value")
        print("TEXT: string")
        print("BLOB: blob of data (in bytes)")
        print("")
        print("If you wish to ensure that new data input to the table will not be empty, please append 'NOT NULL' to the back of the input data type.")
        print("For example: INTEGER NOT NULL")
        print('-----------------------------------------------------------------')
    elif option == "invalid data input":
        print('-----------------------------------------------------------------')
        print("Invalid data type. Please enter a valid data type from the following: ")
        print("NULL: null value")
        print("INTEGER: signed integer")
        print("REAL: floating point value")
        print("TEXT: string")
        print("BLOB: blob of data (in bytes)")
        print('-----------------------------------------------------------------')