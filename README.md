# job_tracker

Job Tracking CLI: This commandline application is based on a course I followed in Udemy. 
I like command line tools and the Python library called "Click" to build CLI tools in Python. In this simple CLI app, you can add jobs, delete them from the database, edit later, and save the db. 
*The only aim was to practise some Python libraries like Click. Nothing special or useful but it was a good exercise for me.*

The code will guide you in the terminal, yet I can add some example terminal commands for this CLI tool.

                                                          # Examples:


# Add A New Job to the Database
	
	eg: python3 job_tracker.py  add-job --name EmreYbs --address Turkey --email emreYbs.github@gmail.com --title Pentester --jobtype Remote --salary 340000 --status Pending
	

# View Job By Title : 
*You can add the name of the job as you wish. But if you write "Nurse", then you cannot find it as "nurse" in the database. 
Later, I will update the code and write some functions to accept some alternatives and ass some Try/Catch for the possible errors.*
	
  eg:  python3 job_tracker.py view-job -t "Pentester"
	eg:	python3 job_tracker.py view-job --title "Developer"
	eg:  python3 job_tracker.py view-job -t "Data Scientist"
  eg:  python3 job_tracker.py view-job -t "Teacher"
  
# Show All Jobs 
	
	eg: python3 job_tracker.py show-all
  
  
# Search Job By Options [Name or Title or Status]

	eg:  python3 job_tracker.py search "Developer" --by="title"
  
  
 # Edit Job By Field[title/author/message] 
 
	eg. python3 job_tracker.py edit-note --field="author" --old="Emre" --new="Emre:Ybs"
  
  
 # Delete Job By Title 
 
	eg. python3 job_tracker.py delete-job --title "Developer"
  
 # Show Info About Software 
	
	eg, python3 job_tracker.py info
  
  
