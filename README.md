## Amaris.AI Telegram Bot Database Script for Singtel Manhole Duct Detection 

### Overview
Database handler script for Amaris AI Singtel Manhole Duct Detection
Database consists of 2 premade tables:
1. JobsTable : Table containing the Job ID, and the location of the job represented
as it's latitude and longitude
2. UserLogs : Table containing the User ID and a log history of the jobs that the corresponding user has attempted before

#### Supported functions:
1. Insertion of _NEW_ data into JobsTable and UserLogs
2. Update of _EXISTING_ data in JobsTable and UserLogs
    - Allow single update and multiple update
3. Deletion of data from JobsTable and UserLogs
    - Allow deletion using either the row number or the job/user id
    - Allow single and multiple argument deletion
- All of the above functionality should only be done by **authorised personnel**
4. Viewing of job or user logs from JobsTable and UserLogs
- This can be done by **any** user of the bot

- Follow formatting specified in the formats section

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
<job_id> <latitude> <longitude> /r/n
- repeat until there are no more jobs to input

UserLogs:
<user_id> /r/n
<job_1_id> <date_success>
...
<job_final_id> <data_success>
/r/n
- repeat if there are more users to input, otherwise press enter

### View / Deletion
JobsTable:
<job_id_1> <job_id_2>....<job_id_3>

UserLogs:
<user_id_1> <user_id_2>...<user_id_3>