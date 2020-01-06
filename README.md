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

- Follow formatting specified in the formats section
- To implement: multiple insertion/deletion/update

### Main functions
**insert_data(table_name, data_to_insert)**
Parameters:
- table_name: JobsTable or UserLogs
- data_to_insert: command line string

**update_data(table_name, data_to_update)**
Parameters:
- table_name: JobsTable or UserLogs
- data_to_update: command line string

**delete_data(table_name, rows)**
Parameters:
- table_name: JobsTable or UserLogs
- rows: command line string 

**view_data(table_name, row)**
Parameters:
- table_name: JobsTable or UserLogs
- row: command line string 

### Formatting
#### Insertion / Update


JobsTable:
<job_id> <latitude> <longitude> 

UserLogs:
<user_id> <job_1_id> <date_success>


### View / Deletion
JobsTable:
<job_id_1> <job_id_2>....<job_id_3>

UserLogs:
<user_id_1> <user_id_2>...<user_id_3>
