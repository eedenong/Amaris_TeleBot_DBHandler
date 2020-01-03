import sqlite3
import numpy as np
import io
from db_handler import DBHandler, print_help


def create_connection(db_file):
    conn = None

    try:
        conn = sqlite3.connect(db_file)
    except FileNotFoundError as e:
        print(e)
    
    return conn

def finish(conn):
    conn.commit()
    conn.close()

def cmd_line_helper_test(handler):
    cmd = input("Please enter a command: ")
    cmd = cmd.strip(' ')
    cmd = cmd.upper()
    if cmd == "CREATE":
        #table_name = input("Please enter a name for the table to be created: "
        handler.create_tables()
        print("Finished creating tables")
        return True
    elif cmd == "INSERT":
        table_name = input("Please enter table name: ")
        print("Enter the data components separated by a space")
        print("Example for JobsTable, job_id, latitude, longitude: A001 1.2 1.1")
        data_to_insert = input("Please enter the data you wish to input: ")
        print("Inserting the following data into {}: ".format(table_name))
        print(data_to_insert)
        handler.insert_data(table_name, data_to_insert)
        print("Finished inserting data")
        return True
    elif cmd == "UPDATE":
        table_name = input("Please enter table name: ")
        data_to_update = input("Please input the data: ")
        handler.update_data(table_name, data_to_update)
        return True
    elif cmd == "DELETE":
        table_name = input("Please enter table name: ")
        use_id = input("Do you want to use row id? (Y/N):")
        use_id = use_id.upper()
        if use_id == "Y":
            use_id = True
        elif use_id == "N":
            use_id = False

        if use_id:
            row_to_delete = input("Please enter the row number to be deleted (id): ")
            handler.delete_data(table_name, row_to_delete, use_id=True)
        else:
            row_to_delete = input("Please enter the row to be deleted (job_id or user_id): ")
            handler.delete_data(table_name, row_to_delete)
    elif cmd == "VIEW":
        table_name = input("Please enter table name: ")
        use_id = input("Do you want to use row id? (Y/N): ")
        use_id = use_id.upper()
        if use_id == "Y":
            use_id = True
        elif use_id == "N":
            use_id = False
        if use_id:
            row_to_view = input("Please enter the row number to view (id): ")
            handler.view_data(table_name, row_to_view, use_id=True)
            return True
        else:
            row_to_view = input("Please enter the row to view (job_id or user_id): ")
            handler.view_data(table_name, row_to_view)
            return True
    elif cmd == "EXIT":
        return False


def main():
    # give functionality for creating table, inserting into table, deleting from table, retrieving data from table
    
    conn = create_connection("test_tele.db")
    
    while True:    
        handler = DBHandler(conn)
        print_help("init")
        curr = cmd_line_helper_test(handler)
        if curr == False:
            break
    
    finish(conn)
    #create the tables in the database
    #handler.create_tables()

    #finish(conn)
    




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