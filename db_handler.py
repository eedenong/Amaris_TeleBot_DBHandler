import re
import sys
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
            job_id TEXT NOT NULL UNIQUE,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL
        );
        """
        cur.executescript(create_job_table_cmd)
        self.conn.commit()
        print("Created JobsTable table")
        # log is an dict that of 
        # format: KEY job_id, VALUE array of results
        create_logging_table_cmd = """
        CREATE TABLE IF NOT EXISTS UserLogs (
            id INTEGER PRIMARY KEY,
            user_id TEXT NOT NULL UNIQUE,
            log BLOB NOT NULL
        );
        """
        cur.executescript(create_logging_table_cmd)
        self.conn.commit()
        print("Created UserLogs table")
    # Insert new data into either JobsTable or UserLogs
    # data_to_insert is a tuple with the format:
    # if table_name is JobsTable, data_to_insert = (job_id, latitude, longitude)
    # if table_name is UserLogs, data_to_insert = (user_id, log)
    def insert_data(self, table_name, data_to_insert, num_insert):
        # Empty data will resolve to true if data_to_insert is just whitespace
        empty_data = not bool(data_to_insert.strip())
        if empty_data:
            print("Cannot insert empty data")
            return None

        if num_insert > 1:
            self.__insert_mult__(table_name, data_to_insert, num_insert)
        else:
            self.__insert_single__(table_name, data_to_insert)
    
    def __insert_single__(self, table_name, data_to_insert):
        cur = self.conn.cursor()
        # Split the data_to_insert
        data = re.split(' |\n', data_to_insert)

        # Inserting data into JobsTable
        if is_jobs(table_name):
            try:
                print("Inserting into JobsTable:\n{}".format(data_to_insert))
                job_id = data[0]
                lat = data[1]
                lon = data[2]
                print(job_id)
                print(lat)
                print(lon)
                cur.execute('INSERT INTO JobsTable (job_id, latitude, longitude) VALUES (?, ?, ?)', (job_id, lat, lon))
                self.conn.commit()
                print("Data successfully inserted")
                print("Finished inserting data")
            except sqlite3.Error as e:
                print("job_id {} already exists in JobsTable. Failed to insert data {}.".format(job_id, data_to_insert))
                print("Try the UPDATE command instead.")
                print(e.args[0])
        elif is_userlogs(table_name):
            try:
                # create a dict 
                # format of dict will be:
                #{job_id:[date_success1, date_success2]}
                logs_dict = {}
                # get the user_id
                user_id = data[0]
                # get job_id
                job_id = data[1]
                # create empty array at job_id
                logs_dict[job_id] = []
                # get date_success
                date_success = data[2]
                # append to the array
                logs_dict[job_id].append(date_success)
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
                print("Finished inserting data")
            except sqlite3.Error as e:
                print("user_id {} already exists in UserLogs. Failed to insert data {}.")
                print("Try the UPDATE command instead.")
                print(e.args[0])
        

    def __insert_mult__(self, table_name, data_to_insert, num_insert):

        cur = self.conn.cursor()
        # Split the data string accordingly
        data = re.split(' |\n', data_to_insert)
        for n in range(1,num_insert+1):
            # to get the idx to reference from data_to_update
            curr = (n-1) * 3
            #print("curr is {}".format(curr))
            grp = " "
            # get a list containing the arguments to be used to join
            lis = []
            lis.append(data[curr])
            #print("curr list is {}".format(lis))
            lis.append(data[curr+1])
            #print("curr list is {}".format(lis))
            lis.append(data[curr+2])
            #print("curr list is {}".format(lis))
            # join it back into a string as __update_single__ requires a string arg
            grp = grp.join(lis)
            print(grp)
            #print("running update_single")
            self.__insert_single__(table_name, grp)
    # update_data enables the changing of data in the specified table_name
    # data_to_update is a string 
    # num_update is the number of items to be updated
    # For jobs table: job_id latitude longitude
    # For userlogs : user_id job_id date_success
    def update_data(self, table_name, data_to_update, num_update):
        empty_data = bool(data_to_update.strip())
        if empty_data:
            print("Cannot update with empty data")
            return None
        if num_update > 1:
            self.__update_mult__(table_name, data_to_update, num_update)
        else:
            self.__update_single__(table_name, data_to_update)
    
    def __update_single__(self, table_name, data_to_update):
        cur = self.conn.cursor()
        # Split the data string accordingly
        data = re.split(' |\n', data_to_update)
        print(data)
        if is_jobs(table_name):
            job_id = data[0]
            lat = data[1]
            lon = data[2]
            try:
                cur.execute("SELECT id FROM JobsTable WHERE job_id = ?", (job_id, ))
                data = cur.fetchone()
                if data is None:
                    raise Exception("job_id {} does not exist in table JobsTable".format(job_id))
                else:
                    print("Updating JobsTable data at job {} with lat {} and long {}".format(job_id, lat, lon))
                    cur.execute('UPDATE JobsTable SET latitude = ?, longitude = ? WHERE job_id = ?', (lat, lon, job_id))
            except Exception as e:
                print(e.args[0])
        elif is_userlogs(table_name):
            # check if the job exists in the user's log dict
            user_id = data[0]
            job_id = data[1]
            job_date = data[2]
            try:
                cur.execute('SELECT id FROM UserLogs where user_id = ?', (user_id, ))
                # Check if the user_id exists in the table
                data = cur.fetchone()
                if data is None:
                    # data is None means that user_id does not exist in the table
                    raise Exception("user_id {} does not exist in table UserLogs".format(user_id))
                else:
                    # else, the user_id exists in the table. check the logs dict
                    # get the dictionary in bytes at the user_id
                    # no need to check if the log exists as there will always be a log
                    cur.execute('SELECT log FROM UserLogs where user_id = ?', (user_id, ))
                    user_log_dict = cur.fetchone()[0]
                    # convert the bytes to dictionary
                    user_log_dict = json.loads(user_log_dict)
                    print(type(user_log_dict))
                    print(user_log_dict)
                    try:
                        user_log_dict[job_id].append(job_date)
                    except:
                        # if the job_id is not found in the log_dict, create the KV pair
                        # then append the date of job 
                        user_log_dict[job_id] = []
                        user_log_dict[job_id].append(job_date)
                    # update has finished, insert the dictionary back into the database
                    logs_dict_bytes = json.dumps(user_log_dict).encode('utf-8')
                    print(logs_dict_bytes)

                    print("Updating JobsTable data at user {} with log {}".format(user_id, user_log_dict))
                    cur.execute('UPDATE UserLogs SET log = ? WHERE user_id = ?', (logs_dict_bytes, user_id))
            except Exception as e:
                print(e.args[0])
        self.conn.commit()

    # handles multiple arg updates by making use of the update single function
    def __update_mult__(self, table_name, data_to_update, num_update):
        # data_to_update is a string containing all the arguments
        cur = self.conn.cursor()
        # Split the data string accordingly
        data = re.split(' |\n', data_to_update)
        for n in range(1,num_update+1):
            # to get the idx to reference from data_to_update
            curr = (n-1) * 3
            #print("curr is {}".format(curr))
            grp = " "
            # get a list containing the arguments to be used to join
            lis = []
            lis.append(data[curr])
            #print("curr list is {}".format(lis))
            lis.append(data[curr+1])
            #print("curr list is {}".format(lis))
            lis.append(data[curr+2])
            #print("curr list is {}".format(lis))
            # join it back into a string as __update_single__ requires a string arg
            grp = grp.join(lis)
            print(grp)
            #print("running update_single")
            self.__update_single__(table_name, grp)

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
        


    def __delete_single__(self, table_name, row, use_id=False):
        cur = self.conn.cursor()
        if is_jobs(table_name):
            if not use_id:
                try:
                    cur.execute("SELECT id FROM JobsTable WHERE job_id = ?",(row, ))
                    data = cur.fetchone()
                    if data is None:
                        raise Exception("job_id {} does not exist in table JobsTable".format(row))
                    else:
                        print("Deleting data from JobsTable at job {}".format(row))
                        cur.execute('DELETE FROM JobsTable WHERE job_id = ?', (row, ))
                        print("Data successfully deleted")
                except Exception as e:
                    print(e.args[0])
            else:
                try:
                    cur.execute("SELECT id FROM JobsTable WHERE id = ?",(row, ))
                    data = cur.fetchone()
                    if data is None:
                        raise Exception("id {} does not exist in table JobsTable".format(row))
                    else:
                        print("Deleting data from JobsTable at row {}".format(row))
                        cur.execute('DELETE FROM JobsTable WHERE id = ?', (row, ))
                        print("Data successfully deleted")
                except Exception as e:
                    print(e.args[0])
        elif is_userlogs(table_name):
            if not use_id:
                try:
                    cur.execute("SELECT id FROM UserLogs WHERE user_id = ?", (row, ))
                    data = cur.fetchone()
                    if data is None:
                        raise Exception("user_id {} does not exist in table UserLogs".format(row))
                    else:
                        print("Deleting data from UserLogs at user_id {}".format(row))
                        cur.execute('DELETE FROM UserLogs WHERE user_id = ?', (row, ))
                        print("Data successfully deleted")
                except Exception as e:
                    print(e.args[0])
            else:
                try:
                    cur.execute("SELECT id from UserLogs where id = ?", (row, ))
                    data = cur.fetchone()
                    if data is None:
                        raise Exception("id {} does not exist in table UserLogs".format(row))
                    else:
                        print("Deleting data from UserLogs at row {}".format(row))
                        cur.execute('DELETE FROM UserLogs WHERE id = ?', (row, ))
                        print("Data successfully deleted")
                except Exception as e:
                    print(e.args[0]) 
        self.conn.commit()
        

    def __delete_mult__(self, table_name, rows, use_id=False):
        cur = self.conn.cursor()
        for i in range(len(rows)):
            self.__delete_single__(table_name, rows[i], use_id)

    # if the job_id exists in the JobsTable, return its lat and long
    # else return None
    def get_job(self, table_name, job_id):
        cur = self.conn.cursor()
        out_string = " "
        cur.execute("SELECT * FROM JobsTable WHERE job_id = ?", (job_id, ))
        data = cur.fetchone()
        print(data)
        if len(data) == 0:
            out_string = "Job not found!"
        else:
            # get the latitude and longitude
            lat = data[2]
            lon = data[3]
            lat_str = "Latitude: {}".format(lat)
            lon_str = "Longitude: {}".format(lon)
            out_string = out_string.join([lat_str, lon_str])
        
        return out_string

        

    ### bug in view data code   
    '''
    def view_data(self, table_name, rows, use_id=False):
        rows = rows.split(' ')
        print("--------- REQUESTED DATA ---------")
        if not use_id:
            if len(rows) > 1:
                self.__view_data_mult__(table_name, rows)
            else:
                self.__view_data_single__(table_name, rows[0])
        else:
            if len(rows) > 1:
                self.__view_data_mult__(table_name, rows, use_id=True)
            else:
                self.__view_data_single__(table_name, rows[0], use_id=True)
        print("----------------------------------")
   
   
    # returns the specified row in the table_name
    def __view_data_single__(self, table_name, row, use_id=False):
        cur = self.conn.cursor()
        if is_jobs(table_name):
            if not use_id:
                try:
                    cur.execute('SELECT * FROM JobsTable WHERE job_id = ?', (row, ))
                    data = cur.fetchone()
                    print("data type in view data single is {}".format(type(data)))
                    if data is None:
                        raise Exception("job_id {} does not exist in table JobsTable".format(row))
                    else:
                        self.__print_view_data__(cur, ["job_id", "latitude", "longitude"])
                except Exception as e:
                    print(e.args[0])
            else:
                try:
                    cur.execute('SELECT * FROM JobsTable WHERE id = ?', (row, ))
                    data = cur.fetchone()
                    if data is None:
                        raise Exception("id {} does not exist in table JobsTable".format(row))
                    else:
                        self.__print_view_data__(cur, ["job_id", "latitude", "longitude"])
                except Exception as e:
                    print(e.args[0])
        elif is_userlogs(table_name):
            if not use_id:
                try:
                    cur.execute('SELECT * FROM UserLogs WHERE user_id = ?', (row, ))
                    data = cur.fetchone()
                    if data is None:
                        raise Exception("user_id {} does not exist in table UserLogs".format(row))
                    else:
                        self.__print_view_data__(cur, ["user_id", "log"])
                except Exception as e:
                    print(e.args[0])
            else:
                try:
                    cur.execute('SELECT * FROM UserLogs WHERE id = ?', (row, ))
                    data = cur.fetchone()
                    if data is None:
                        raise Exception("id {} does not exist in table UserLogs".format(row))
                    else:
                        self.__print_view_data__(cur, ["user_id", "log"])
                except Exception as e:
                    print(e.args[0])

    def __view_data_mult__(self, table_name, rows, use_id=False):
        cur = self.conn.cursor()
        for i in range(len(rows)):
            self.__view_data_single__(table_name, rows[i], use_id)

    def __print_view_data__(self, cursor, param_list):
        data = cursor.fetchone()
        print("data type in print view data is {}".format(type(data)))
        out_string = " "
        st_arr = []
        count = 0
        for i in range(len(param_list)):
            if isinstance(data[i+1], bytes):
                # Means that the data is in the form of a dictionary, in bytes
                # Decode it. d is of type dict
                d = json.loads(data[i+1].decode('utf-8'))
                st_arr.append(param_list[i])
                #print("{}:".format(param_list[i]))
                # gets a list of tuples of the log items
                # in the form of (job_id, date)
                d_items = d.items()
                for data in d_items:
                    # for each tuple in the d_items list
                    st_arr.append("job_id: {}".format(data[0]))
                    #print("job_id: {}".format(data[0]))
                    st_arr.append("Date of attempt_success: {}".format(data[1][0]))
                    #print("Date of attempt_success: {}".format(data[1][0])) 
                #print("{}: {}".format(param_list[i], json.loads(data[i+1].decode('utf-8'))))
            else:
                print("{}: {}".format(param_list[i], data[i+1]))
        print()
    '''

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

# Takes in a string and checks if it is a valid table name
def check_valid_table_name(table_name):
    is_JobsTable = table_name == "jobstable" or table_name == "jobs"
    is_UserLogs = table_name == "userlogs" or table_name == "user" or table_name == "logs"
    return is_JobsTable or is_UserLogs
def is_jobs(table_name):
    return table_name == "jobstable" or table_name == "jobs"

def is_userlogs(table_name):
    return table_name == "userlogs" or table_name == "user" or table_name == "logs"