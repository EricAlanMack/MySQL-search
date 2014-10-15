"""Enter a database and a table index to get record details.
Enter a particular column (attribute) in order to retrieve its 
metadata."""


import MySQLdb
import sys 
import string 


mydb = MySQLdb.connect(host = 'localhost',
						user = 'root',
						db = 'bank')

cur = mydb.cursor()

statement1 = """Show tables"""
command = cur.execute(statement1)
results = cur.fetchall()

print "Which table would you like to use?"

for i in range(0, len(results)):
	print i + 1, results[i][0]

while True:
	choice = raw_input("Input Number: ")
	choice_string = str(choice) 
	confirm = input("You chose %s? Type 1 or 0: " % choice_string[0])
	if confirm == 1: 	
		if choice.isdigit() is True:
			if (int(choice_string[0])>0) and (int(choice_string[0])<=len(results)):
				break #need to do something to allow for double digit indices. 
			else: 
				print "We'll need another number in range."
		else: 
			print "We'll need a digit."  
	else: 
		pass

real_choice = int(choice_string[0]) - 1

table_statement = """DESCRIBE %s""" % results[real_choice][0]

cur.execute(table_statement) 

table_result = cur.fetchall() 

print "The records in the %s table are %d-tuples:" % (results[real_choice][0],
														len(table_result))
for i in range(len(table_result)):
	print i+1, table_result[i][0]

col_option = raw_input("Would you like to use a particular column? Enter y or n: ")
if col_option == 'y':
	col_choice = raw_input("Which one? Enter its index: ")
	try: 
		print "Field:", table_result[int(col_choice) - 1][0]
		print "Type:", table_result[int(col_choice) - 1][1]
		print "Null:", table_result[int(col_choice) - 1][2]
		print "Key:", table_result[int(col_choice) - 1][3]
		print "Default:", table_result[int(col_choice) - 1][4]
		print "Extra:", table_result[int(col_choice) - 1][5]
	except: print "Oops, something went wrong."

mydb.close() 