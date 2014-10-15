"""A command line search utility. Command line options are flagged as '-t' for table, 
'-f' for format, '-o-' for output, and '-q' for query. Enter these as arguments and 
the program will output a plain text file with the relevant data."""

import MySQLdb 
import optparse 

opt = optparse.OptionParser()

opt.add_option("-d", "--database", 
				action = "store",
				type = "string", 
				dest = "database")

opt.add_option("-c", "--column", 
				action = "store", 
				type = "string", 
				dest = "column")

opt.add_option("-q", "--query",
				action = "store",
				type = "string",
				dest = "term")
				
opt.add_option("-t", "--table",
				action = "store",
				type = "string",
				dest = "table")
				
opt.add_option("-f", "--format",
				action="store_true",
				dest="format")

opt.add_option("-o", "--output", 
				action = "store", 
				type = "string", 
				dest = "outfile")

opt, args = opt.parse_args()

database = opt.database 

try:
	mydb = MySQLdb.connect(host='localhost',
							user='root',
							db=database)
except: print "That database doesn't exist here."
	
cur = mydb.cursor()

format = opt.format
table = opt.table
column = opt.column
term = opt.term 
statement = """SELECT * FROM %s WHERE %s like '%s'""" %(table, column, term)


try: 
	command = cur.execute(statement)
	results = cur.fetchall() 
except: print "Something's wrong with the db/table/col combo...it doesn't exist." 

column_list = []
for record in results:
	column_list.append(record[0:])

if format is True: 
	columns_query = """DESCRIBE %s""" %(table)
	columns_command = cur.execute(columns_query)
	headers = cur.fetchall()
	column_list = []
	for record in headers:	
		column_list.append(record[0]) 
	
	output=""
	for record in results:
		output = output + "<><<>><><<>><><<>><><<>><><<>><><<>>\n\n"		
		for field_no in range(0, len(column_list)):
			output = output + column_list[field_no]+": " + str(record[field_no]) + "\n"
		output = output + "\n"
		
else: 
	output=[]
	for record in range(0, len(results)):
		output.append(results[record])
	output = ''.join(output)
	
if opt.outfile:
	outfile = opt.outfile
	out = open(outfile, 'w')
	out.write(output)
	out.close()

else:
	print output 

mydb.close() 
