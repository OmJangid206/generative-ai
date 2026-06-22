Python - FastAPI
React
VectorDB
Sqlite3 
GenAI, Opoen-router
Langchain
----------------------------------------------------------------------
Login, Logout, Sign-Up (JWT Authentication, Password Hashing (bcrypt))
----------------------------------------------------------------------
- If we give PDF ask questions related to PDF should give answer related to PDF
- if not then should replied from the Company Specific data
- Convert simple human language to SQL fetch data from the DB then summarise the resule using the GenAI also display in the form of Table also should display What all queries has been used.
- How would be convert it into the SQL Queries?
- First When User enter query then search from the vector DB top match data and get the KPI 
- Then from KPIs create the SQL Query 
- Also should handle column What all column should be selected and what all data should be return
- it Should store the history data in the table when is long history data then it make the full summerize data and store and use that for historics data
- Add user infomration in the other db login, logout and signup details
- Integrate Cloudinary to store the docs
----------------------------------------------------------------------
tables
users - contains user informations
Upload - contains docuemnts url 
documents - documents metadata
----------------------------------------------------------------------