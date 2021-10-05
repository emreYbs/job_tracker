
import click
from click_didyoumean import DYMGroup
from click_plugins import with_plugins
import click_config_file
from click_help_colors import HelpColorsGroup,HelpColorsCommand
from pkg_resources import iter_entry_points
import sqlite3

# DataBase
conn = sqlite3.connect('data.db')
c = conn.cursor()

def create_table():
	c.execute('CREATE TABLE IF NOT EXISTS jobstable(name TEXT,address TEXT,email TEXT,title TEXT,jobtype TEXT,salary INTEGER,status TEXT)')


def add_data(name,address,email,title,jobtype,salary,status):
	c.execute('INSERT INTO jobstable(name,address,email,title,jobtype,salary,status) VALUES (?,?,?,?,?,?,?)',(name,address,email,title,jobtype,salary,status))
	conn.commit()


def view_all_jobs():
	c.execute('SELECT * FROM jobstable')
	data = c.fetchall()
	# for row in data:
	# 	print(row)
	return data

def get_single_job(title):
	c.execute('SELECT * FROM jobstable WHERE title="{}"'.format(title))
	data = c.fetchall()
	return data

def get_job_by_title(title):
	c.execute('SELECT * FROM jobstable WHERE title="{}"'.format(title))
	data = c.fetchall()
	return data

def get_job_by_name(name):
	c.execute('SELECT * FROM jobstable WHERE name="{}"'.format(name))
	data = c.fetchall()
	return data
 

def get_job_by_address(address):
	c.execute("SELECT * FROM jobstable WHERE address like '%{}%'".format(address))
	data = c.fetchall()
	return data

def get_job_by_status(status):
	c.execute("SELECT * FROM jobstable WHERE status like '%{}%'".format(status))
	data = c.fetchall()
	return data

def edit_job_name(name,new_name):
	c.execute('UPDATE jobstable SET name ="{}" WHERE name="{}"'.format(new_name,name))
	conn.commit()
	data = c.fetchall()
	return data

def edit_job_title(title,new_title):
	c.execute('UPDATE jobstable SET title ="{}" WHERE title="{}"'.format(new_title,title))
	conn.commit()
	data = c.fetchall()
	return data


def edit_job_status(status,new_status):
	c.execute('UPDATE jobstable SET status ="{}" WHERE status="{}"'.format(new_status,status))
	conn.commit()
	data = c.fetchall()
	return data

def delete_data(title):
	c.execute('DELETE FROM jobstable WHERE title="{}"'.format(title))
	conn.commit()


# Main CLI
@with_plugins(iter_entry_points('click_command_tree'))
@click.group(cls=DYMGroup)
@click.version_option('0.01',prog_name='jobtracker')
def main():
	""" Job Tracking CLI """
	pass

@main.command(cls=HelpColorsCommand,help_headers_color='yellow',help_options_color='green')
@click.option('--name','-n',help='Name of Company',type=str,prompt=True)
@click.option('--address','-a',help='Address of Company',type=str,prompt=True)
@click.option('--email','-e',help='Email of Company',type=str,prompt=True)
@click.option('--title','-t',help='Job Title',type=str,prompt=True)
@click.option('--jobtype','-jt',help='Job Type',type=click.Choice(['Full-Time','Part-Time','Remote','Contract']),prompt=True)
@click.option('--salary','-s',help='Annual Salary',type=int,prompt=True)
@click.option('--status','-st',help='Job Status',type=click.Choice(['Pending','Cancelled','Success']),prompt=True)
@click_config_file.configuration_option()
def add_job(name,address,email,title,jobtype,salary,status):
	"""Add A New Job
	
	eg. python3 job_tracker.py  add-job --name EmreYbs --address Turkey --email emreYbs.github@gmail.com --title Pentester --jobtype Remote --salary 340000 --status Pending
	
	"""
	click.echo("Add A New Job")
	click.secho("Added {} to Database".format(title),fg='blue')
	click.echo("========Summary===============")
	from terminaltables import AsciiTable
	user_notes = [
		['Jobs Info','Details'],
		['Company Name:',name],
		['Company Address:',address],
		['Company Email:',email],
		['Job Title:',title],
		['Job Type:',jobtype],
		['Job Salary:',salary],
		['Status:',status]
	
	
	]
	create_table()
	add_data(name,address,email,title,jobtype,salary,status)
	table1 = AsciiTable(user_notes)

	click.echo(table1.table)
	click.secho('Saved Job To DataBase',fg='blue')

@main.command(cls=HelpColorsCommand,help_headers_color='yellow',help_options_color='magenta')
@click.option('--title','-t',prompt=True)
def view_job(title):
	""" View Job By Title 
	
	eg.	python3 job_tracker.py view-job --title "Developer"
	eg.  python3 job_tracker.py view-job -t "Data Scientist"
	"""
	click.secho("Searched For {}".format(title),bg='blue')
	from terminaltables import AsciiTable
	result = get_single_job(title)
	table1 = AsciiTable(result)
	click.echo(table1.table)

@main.command(cls=HelpColorsCommand,help_headers_color='yellow',help_options_color='magenta')
def show_all():
	""" Show All Jobs 
	
	eg. python3 job_tracker.py show-all
	"""
	click.secho("Showing All Jobs",bg='blue')
	click.echo("==============================")
	from terminaltables import AsciiTable
	result = view_all_jobs()
	new_result = ['Company Name','Address','Email','Title','JobType','Salary','Status']
	click.secho('{}'.format(new_result),bg='blue')
	table1 = AsciiTable(result)
	click.echo(table1.table)

@main.command(cls=HelpColorsCommand,help_headers_color='yellow',help_options_color='magenta')
@click.argument('text')
@click.option('--by','-b',default='title',type=click.Choice(['name','title','status']))
def search(text,by):
	""" Search Job By Options [Name or Title or Status]
	eg  python3 job_tracker.py search "Developer" --by="title"
	 """
	click.secho("Searched For :: {}".format(text),bg='blue')
	from terminaltables import AsciiTable
	if by == 'title':
		result = get_job_by_title(text)
		table1 = AsciiTable(result)
		click.echo(table1.table)
	elif by == 'name':
		result = get_job_by_name(text)
		table1 = AsciiTable(result)
		click.echo(table1.table)
	elif by == 'status':
		result = get_job_by_status(text)
		table1 = AsciiTable(result)
		click.echo(table1.table)
	else:
		click.secho("{} Not a Choice ,Pls Try either of these [name/title/status]".format(by),bg='red')




@main.command(cls=HelpColorsCommand,help_headers_color='yellow',help_options_color='magenta')
@click.option('--old')
@click.option('--new')
@click.option('--field')
def edit_job(field,old,new):
	""" Edit Job By Field[title/author/message] 
	eg. python3 job_tracker.py edit-note --field="author" --old="Emre" --new="Emre:Ybs" 
	"""
	click.secho('Editing Field:: {} with {} and Updating to {}'.format(field,old,new),fg='yellow')
	from terminaltables import AsciiTable

	click.echo("===========Previous==============")
	result2 = view_all_notes()
	new_result = ['Company Name','Address','Email','Title','JobType','Salary','Status']
	click.secho('{}'.format(new_result),bg='blue')
	table2 = AsciiTable(result2)
	click.echo(table2.table)


	if field == 'title':
		result = edit_job_title(old,new)
		table1 = AsciiTable(result)
		click.echo(table1.table)
	if field == 'name':
		result = edit_job_name(old,new)
		table1 = AsciiTable(result)
		click.echo(table1.table)
	if field == 'status':
		result = edit_job_status(old,new)
		table1 = AsciiTable(result)
		click.echo(table1.table)


	click.echo("==========Updated===============")
	result3 = view_all_notes()
	new_result2 = ['Company Name','Address','Email','Title','JobType','Salary','Status']
	click.secho('{}'.format(new_result2),bg='blue')
	table3 = AsciiTable(result3)
	click.echo(table3.table)


@main.command(cls=HelpColorsCommand,help_headers_color='yellow',help_options_color='magenta')
@click.option('--title')
def delete_job(title):
	""" Delete Job By Title 
	eg. python3 job_tracker.py delete-job --title "Developer"
	"""
	click.secho('Deleting :: {} '.format(title),fg='yellow')
	from terminaltables import AsciiTable

	click.echo("===========Previous==============")
	result2 = view_all_notes()
	new_result =  ['Company Name','Address','Email','Title','JobType','Salary','Status']
	click.secho('{}'.format(new_result),bg='blue')
	table2 = AsciiTable(result2)
	click.echo(table2.table)

	result = delete_data(title)
	click.echo("Deleted From DataBase")

@main.command()
def info():
	""" Show Info About Software 
	
	eg, python3 job_tracker.py info
	"""


	click.secho('Name:: {}'.format('JobTracker'),bg='red')
	click.secho('Version:: {}'.format('0.01'),bg='green')
	click.secho('Author:: {}'.format('EmreYbs'),bg='blue')

if __name__ == '__main__':
	main()

