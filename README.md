## Amaris.AI Telegram Bot Database Script for Singtel Manhole Duct Detection 

### Overview
Database handler script for Amaris AI Singtel Manhole Duct Detection
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
Parameters:
- table_name: String. Taken as command line argument.
- data_to_insert: String. Taken as command line argument.
General format: row data1 data2
If data_to_insert contains multiple lines, num_insert should correspond to the number of lines to be inserted.
- num_insert: Integer. Number of rows to insert into database.

Function:
Inserts data contained in __data_to_insert__ into the database. Alerts the user when user tries to insert a row that already exists in the database. Insertion of multiple data is allowed.


**update_data(table_name, data_to_update, num_insert)**
Parameters:
- table_name: String. Taken as command line argument.
- data_to_update: String. Taken as command line argument.
General format: row data1 data2
If data_to_update contains multiple lines, num_update should correspond to the number of lines to be updated.
- num_insert: Integer. Number of rows to update in the database

Function:
Updates the specified row (read from data_to_update) to the contained data (also read from data_to_update). Update of multiple data is allowed.
Alerts the user when user tries to update an entry that does not exist in the database, or with an empty entry.

**delete_data(table_name, rows, use_id)**
Parameters:
- table_name: String. Taken as command line argument.
- rows: String. Taken as command line argument.
- use_id: Boolean. Flags whether the specified __rows__ indicates the specific row number (Int String), or is a user_id/job_id (String). If use_id is set to __True__, then __rows__ should be the specific row number.

Function:
Deletes the specified row(s) at the row number(s) if use_id=True, else at specified job_id(s)/user_id(s). 
If __rows__ contains multiple numbers or job_id(s)/user_id(s), multiple rows of data will be deleted.
Alerts the user if user tries to delete an entry that does not exist in the database.

**view_data(table_name, rows, use_id)**
Parameters:
- table_name: String. Taken as command line argument.
- rows: String. Taken as command line argument.
- use_id: Boolean. Flags whether the specified __rows__ indicates the specific row number (Int String), or is a user_id/job_id (String). If use_id is set to __True__, then __rows__ should be the specific row number.

Function:


### Formatting 
#### Insertion / Update


JobsTable:
<job_id1> <latitude1> <longitude1> /r/n
<job_id2> <latitude2> <longitude2> /r/n
.
.
.
<job_idN> <latitudeN> <longitudeN> /r/n
/r/n

UserLogs:
<user_id1> <job_id1> <date_success> /r/n
<user_id2> <job_id2> <date_success> /r/n
.
.
.
<user_idN> <job_idN> <date_success> /r/n
/r/n

### View / Deletion
JobsTable:
<job_id_1> <job_id_2>....<job_id_3>

UserLogs:
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