# Amaris.AI Telegram Bot Database Script for Singtel Manhole Duct Detection 

## Overview
Database handler and manager script for Amaris AI Singtel Manhole Duct Detection.
Database consists of 2 premade tables:
1. JobsTable : Table containing the Job ID, and the location of the job represented
as it's latitude and longitude
2. UserLogs : Table containing the User ID and a log history of the jobs that the corresponding user has attempted before
    - log history is a dictionary of the format:
        - { job_id_1: [date_success1, date_success2],
            job_id_2: [date_success1, date_success2],
            .
            .
            .
            }
To use these scripts in command line, refer to [Manager](#Manager)
If you wish to simply import and use the db_handler.py script, refer to [Handler](#Handler) 

### Manager
_This assumes that you wish to run the script and its functions from the command line, and you don't already have an existing database_
**Make sure that tele_bot_db_manager.py and db_handler.py are in the same directory**

* You can rename your created database by editing the string in the create_connection function in tele_bot_db_manager.py (inside the main() function).

From the command line, enter: 
```
python tele_bot_db_manager.py
```
Then, follow the printed prompts.

### Handler
*This assumes that you wish to import the db_handler script, and that your main script already creates a connection to an existing database*
At the top of your script, write: 
```
from db_handler import DBHandler
```
Create a DBHandler object. Assume that the connection to your database is called *conn*.
```
handler = DBHandler(conn)
```

Then, you can use the DBHandler object to call the various [functions](#Main functions) specified in the db_handler script.
Example: Creating tables using the create_tables() function in the db_handler script
```
handler.create_tables()
```

#### Supported functions:
1. Insertion of _NEW_ data into JobsTable and UserLogs
2. Update of _EXISTING_ data in JobsTable and UserLogs
    - For UserLogs, update only works if the user exists in the database
3. Deletion of data from JobsTable and UserLogs
- All of the above functionality should only be done by **authorised personnel**
4. Viewing of job or user logs from JobsTable and UserLogs
- This can be done by **any** user of the bot

* For all functions, follow the formatting specified in the [Formatting](#Formatting) section

### Main functions
**insert_data(table_name, data_to_insert, num_insert)**
_Parameters_:
- table_name: String. Taken as command line argument.
- data_to_insert: String. Taken as command line argument.
General format: row data1 data2
If data_to_insert contains multiple lines, num_insert should correspond to the number of lines to be inserted.
- num_insert: Integer. Number of rows to insert into database.

_Function_:
Inserts data contained in __data_to_insert__ into the database. Alerts the user when user tries to insert a row that already exists in the database. Insertion of multiple data is allowed.

_Returns_:
N.A.


**update_data(table_name, data_to_update, num_insert)**
_Parameters_:
- table_name: String. Taken as command line argument.
- data_to_update: String. Taken as command line argument.
General format: row data1 data2
If data_to_update contains multiple lines, num_update should correspond to the number of lines to be updated.
- num_insert: Integer. Number of rows to update in the database

_Function_:
Updates the specified row (read from data_to_update) to the contained data (also read from data_to_update). Update of multiple data is allowed.
Alerts the user when user tries to update an entry that does not exist in the database, or with an empty entry.

_Returns_:
N.A.

**delete_data(table_name, rows, use_id)**
_Parameters_:
- table_name: String. Taken as command line argument.
- rows: String. Taken as command line argument.
- use_id: Boolean. Flags whether the specified __rows__ indicates the specific row number (Int String), or is a user_id/job_id (String). If use_id is set to __True__, then __rows__ should be the specific row number.

_Function_:
Deletes the specified row(s) at the row number(s) if use_id is set to **True**, else at specified job_id(s)/user_id(s). 
If __rows__ contains multiple numbers or job_id(s)/user_id(s), multiple rows of data will be deleted.
Alerts the user if user tries to delete an entry that does not exist in the database.

_Returns_:
N.A.

**view_data(table_name, rows, use_id)**
_Parameters_:
- table_name: String. Taken as command line argument.
- rows: String. Taken as command line argument.
- use_id: Boolean. Flags whether the specified __rows__ indicates the specific row number (Int String), or is a user_id/job_id (String). If use_id is set to __True__, then __rows__ should be the specific row number.

_Function_:
Views the specified row(s) at the row number(s) if use_id is set to **True**, else at specified job_id(s)/user_id(s). 
If __rows__ contains multiple numbers or job_id(s)/user_id(s), multiple rows of data will be viewed.
The row(s) that are view are **returned** as a **String**.
Alerts the user if user tries to view an entry that does not exist in the database.

_Returns_:
A **single string** representing the specified row(s).

### Formatting 
#### Insertion / Update


_JobsTable_:
<job_id1> <latitude1> <longitude1> <kbd>Enter<kbd>
<job_id2> <latitude2> <longitude2> <kbd>Enter<kbd>
.
.
.
<job_idN> <latitudeN> <longitudeN> <kbd>Enter<kbd>
<kbd>Enter<kbd>

_UserLogs_:
<user_id1> <job_id1> <date_success> <kbd>Enter<kbd>
<user_id2> <job_id2> <date_success> <kbd>Enter<kbd>
.
.
.
<user_idN> <job_idN> <date_success> <kbd>Enter<kbd>
<kbd>Enter<kbd>

### View / Deletion
_JobsTable_:
<job_id_1> <job_id_2>....<job_id_3>

_UserLogs_:
<user_id_1> <user_id_2>...<user_id_3>

### To be implemented
- [X] Updated attributes of job_id and user_id to be UNIQUE
- [X] Add functionality to exit at any point
- [ ] Exception handling: Correct argument formatting for update and insertion

#### Update function
- [X] Single argument entry for JobsTable
- [X] Single argument entry for UserLogs
- [X] Multiple argument entry for JobsTable
- [X] Multiple argument entry for UserLogs
- [X] Exception handling: Only update EXISTING
- [X] Exception handling: Assert correct number of arguments for multiple argument

#### Delete function
- [X] Single argument entry for JobsTable
- [X] Single argument entry for UserLogs
- [X] Multiple argument entry for JobsTable
- [X] Multiple argument entry for UserLogs
- [X] Exception handling: Only delete existing
* For delete only, multiple arguments are handled in the same line

#### Insertion function
- [X] Single argument entry for JobsTable
- [X] Single argument entry for UserLogs
- [X] Multiple argument entry for JobsTable
- [X] Multiple argument entry for UserLogs
- [X] Exception handling: Cannot insert existing
- [X] Exception handling: Cannot insert empty

#### View function
- [X] Single argument entry for JobsTable
- [X] Single argument entry for UserLogs
- [X] Multiple argument entry for JobsTable
- [X] Multiple argument entry for UserLogs
- [X] Exception handling: Cannot view non existent