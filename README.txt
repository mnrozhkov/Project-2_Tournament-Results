2015.03.28
Athor: Mikhail Rozhkov

This is a Project 2 - Tournament Results under the Udacity Nanodegree program "Full Stack Web Developer"

There are three files there: 
1. tournament.sql: SQL database and table definitions in a file
2. tournament.py:  Python functions filling out a template of an API 
3. tournament_test.py: a test suite to verify tournament.py

How to run the program:
1. Install Vagrant and VirtualBox
2. Store all files in ".../vagrant/tournament" folder
3. Launch the Vagrant VM
4. Change current directory to ".../vagrant/tournament"
5. Run PostgreSQL from command line terminal (> psql)
6. Create database  "tournament"  abd all required tables from "tournament.sql" file (> \i tournament.sql)
7. Change current directory to ".../vagrant/tournament"
8. Run "tournament_test.py" file (> python tournament_test.py)
