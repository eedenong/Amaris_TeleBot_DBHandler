import sqlite3
import numpy as np
import io
from db_handler import DBHandler, print_help
import sys
import re


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except FileNotFoundError as e:
        print(e)
    
    return conn

def finish(conn):
    conn.close()

def cmd_handler(db_handler):
    cmd = input("Please enter a command: ")
    cmd = cmd.strip(' ')
    cmd = cmd.upper()
    if cmd == "CREATE":
        #table_name = input("Please enter a name for the table to be created: "
        db_handler.create_tables()
        print("Finished creating tables")
        return True
    elif cmd == "INSERT":
        table_name = input("Please enter table name: ")
         # add this line to let user exit from here
        if table_name.lower() == "exit":
            return False
        else:
            try:
                sp = table_name.split(' ')[0].lower()
                valid_name = check_valid_table_name(sp)
                if valid_name:
                    print("Enter the data components separated by a space")
                    print("Example for JobsTable, job_id, latitude, longitude: A001 1.2 1.1")
                    #data_to_insert = input("Please enter the data you wish to input: ")
                    data_to_insert = None
                    # now, the num of arguments for both tables is 3
                    data_to_insert = get_input(3)
                    # check if the data_to_insert string is empty
                    if not data_to_insert:
                        return False

                    print("Inserting the following data into {}: ".format(table_name))
                    print(data_to_insert)
                    d = re.split(' |\n', data_to_insert)
                    db_handler.insert_data(table_name, data_to_insert, int(len(d)/3))
                    
                else:
                    s = "Invalid table name. Available options:\nJobsTable\nUserLogs\njobs\nusers\nlogs"
                    raise Exception(s)
            except Exception as e:
                print(e.args[0])
                
        return True
   
    elif cmd == "UPDATE":
        while True:
            table_name = input("Please enter table name: ")
            # check if user wants to exit first 
            if table_name.lower() == "exit":
                return False
            
            # Else, check that table name is entered correctly
            try:
                sp = table_name.split(' ')[0].lower()
                valid_name = check_valid_table_name(sp)
                if valid_name:
                    print("Please input the data below. After finishing entering your data, press enter again")
                    # Get the input from the user
                    # Update functions for both tables require 3 args
                    data_to_update = get_input(3)
                    if not data_to_update:
                        return False
                    # Check the table name
                    print(data_to_update)
                    print(type(data_to_update))
                    d = re.split(' |\n', data_to_update)
                    db_handler.update_data(table_name, data_to_update, int(len(d)/3))
                    return True
                else:
                    s = "Invalid table name. Available options:\nJobsTable\nUserLogs\njobs\nusers\nlogs"
                    raise Exception(s)
            except Exception as e:
                print(e.args[0])
                continue
    
    elif cmd == "DELETE":
        table_name = input("Please enter table name: ")
        if table_name.lower() == "exit":
            return False

        use_id = input("Do you want to use row id? (Y/N): ")
        if use_id.lower() == "exit":
            return False
        use_id = use_id.upper()
        if use_id == "Y":
            use_id = True
        elif use_id == "N":
            use_id = False

        if use_id:
            row_to_delete = input("Please enter the row number to be deleted (id): ")
            if row_to_delete.lower() == "exit":
                return False
            db_handler.delete_data(table_name, row_to_delete, use_id=True)
        else:
            row_to_delete = input("Please enter the row to be deleted (job_id or user_id): ")
            if row_to_delete.lower() == "exit":
                return False
            
            db_handler.delete_data(table_name, row_to_delete)
    
    elif cmd == "VIEW":
        """ table_name = "JobsTable"
        job_id = input("Job id: ")
        print(db_handler.get_job(table_name, job_id)) """
    
        table_name = input("Please enter table name: ")
        if table_name.lower() == "exit":
            return False
        
        use_id = input("Do you want to use row id? (Y/N): ")
        if use_id.lower() == "exit":
            return False

        use_id = use_id.upper()
        if use_id == "Y":
            use_id = True
        elif use_id == "N":
            use_id = False
        
        if use_id:
            row_to_view = input("Please enter the row number to view (id): ")
            db_handler.view_data(table_name, row_to_view, use_id=True)
            return True
        else:
            row_to_view = input("Please enter the row to view (job_id or user_id): ")
            db_handler.view_data(table_name, row_to_view)
            return True
        
    elif cmd == "EXIT":
        return False
    else:
        print("Invalid command. Please try again")
        print('-----------------------------------------------------------------')

def get_input(num_args):
    # in this function, we must assert that the user gives us num of args
    # as specified by num_args
    data = []
    while True:
        line = input()
        if line:
            # check for the length here
            tmp = line.split(' ')
            num_args_given = len(tmp)
            try:
                correct_num = num_args_given == num_args
                if correct_num:
                    data.append(line)
                else:
                    raise Exception(str(num_args_given))
            except Exception as e:
                x = e.args
                
                print("Incorrect number of arguments!")
                print("Number of arguments required is: {}".format(num_args))
                
                print("Given number of arguments is: {}".format(x[0]))
                print("Please try again, or press enter again to quit")
                continue
        else:
            break
    data = '\n'.join(data)
    return data

# Takes in a string and checks if it is a valid table name
def check_valid_table_name(table_name):
    is_JobsTable = table_name == "jobstable" or table_name == "jobs"
    is_UserLogs = table_name == "userlogs" or table_name == "user" or table_name == "logs"
    return is_JobsTable or is_UserLogs

def is_jobs(table_name):
    return table_name == "jobstable" or table_name == "jobs"

def is_userlogs(table_name):
    return table_name == "userlogs" or table_name == "user" or table_name == "logs"

def main():
    # give functionality for creating table, inserting into table, deleting from table, retrieving data from table

    conn = create_connection("test_amaris.db")
    
    while True:    
        db_handler = DBHandler(conn)
        print_help("init")
        curr = cmd_handler(db_handler)
        if curr == False:
            break
    
    finish(conn)   

if __name__ == "__main__":
    main()




# def adapt_array(arr):
#     """
#     http://stackoverflow.com/a/31312102/190597 (SoulNibbler)
#     """
#     out = io.BytesIO()
#     np.save(out, arr)
#     out.seek(0)
#     return sqlite3.Binary(out.read())

# def convert_array(text):
#     out = io.BytesIO(text)
#     out.seek(0)
#     return np.load(out)


# # Converts np.array to TEXT when inserting
# sqlite3.register_adapter(np.ndarray, adapt_array)

# # Converts TEXT to np.array when selecting
# sqlite3.register_converter("arr", convert_array)
# to use, remember to add  detect_types=sqlite3.PARSE_DECLTYPES when doing sqlite.connect()