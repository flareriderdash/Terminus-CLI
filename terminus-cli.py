#!/usr/env/python3
import terminusdb_client
import sys
import copy
ARG_LIMIT=-1
REQUIRED_ARG=-2
def get_errstr_from_errint(errorint):

    if errorint == ARG_LIMIT:
	return "You cannot have more than one {}"
    elif errorint == REQUIRED_ARG:
	return "{} requires an argument"
    #fi
#fed
def arg_parse_err(error,str_var,usage):
	format_str = get_errstr_from_errint(error)
	print(format_str.format(str_var))
	print(usage)
	exit(error)
#fed        
def add_database_terminus_execute(kwargs):

	# Functional Programming stuffs
	kwargs = copy.copy(kwargs)

	# Query Database and Add New Database
	client=terminusdb_client.WOQLClient(server_url = kwargs['url'])
	client.connect(
		account = kwargs['accountid'],
		key     = kwargs['pass'],
		user    = kwargs['accountid'])

	client.account(kwargs['accountid'])
	print(kwargs)
	client.create_database(
		kwargs['dbid'],
		kwargs['accountid'],
		label          = kwargs['label'],
		description    = kwargs['desc'],
		prefixes       = None,
		include_schema = kwargs['schema'])
	return 0

#fed
def add_database_action(cmdline):
	# Expectations:
	# cmdline, sys.argv list

    usage = \
	    """
Action: add-database user database_id [options]

--help, -h              display this help 
			message

-d, --description       description to add
			to created database

-p, --password          password to login with

-l, --label             label for the database

-n,--no-schema          make database without
			schema
"""

    # If asking for help, politly exit

    if (("--help" in cmdline or "-h" in cmdline)
	or len(cmdline) < 5):
	    print(usage)
	    exit(0)
	#fi

    kwargs = {
	    "url":sys.argv[1],
	    "action":sys.argv[2],
	    'accountid':sys.argv[3],
	    "dbid":sys.argv[4],
	    "desc":None,
	    "pass":None,
	    "label":None,
	    "schema":True
    } 


    # Parse Arguments

    for index in range(len(cmdline)):

	# Description Parse
	if (cmdline[index] in ("-d", "--description")
	    and kwargs['desc'] == None and (index +1) < len(cmdline)):
		kwargs['desc'] = cmdline[index+1]

	elif (kwargs['desc'] != None) and (cmdline[index] in ("-d", "--description")):
		arg_parse_err(ARG_LIMIT,"description",usage)
	elif (index + 1) > len(cmdline):
		arg_parse_err(REQUIRED_ARG,"description",usage)
	#fi

	# Password Parse
	if (cmdline[index] in ("-p" ,"--password")
	    and kwargs['pass'] == None and (index + 1) < len(cmdline)):
		kwargs['pass'] = cmdline[index+1]

	elif (kwargs['pass'] != None) and (cmdline[index] in ("-p", "--password")):
		arg_parse_err(ARG_LIMIT,"password",usage)
	elif (index + 1) > len(cmdline):
		arg_parse_err(REQUIRED_ARG,"password",usage)

	#fi

	# Label Parse
	if (cmdline[index] in ("-l","--label")
	    and kwargs['label'] == None and (index + 1) < len(cmdline)):
		kwargs['label'] = cmdline[index+1]

	elif (kwargs['label'] != None) and (cmdline[index] in ("-l", "--label")):
		arg_parse_err(ARG_LIMIT,"label",usage)
	elif (index + 1) > len(cmdline):
		arg_parse_err(REQUIRED_ARG,"label",usage)

	#fi

	# Schema Parse
	if (cmdline[index] in ("-n","--no-schema")
	    and kwargs['schema'] == True):
		schema == False
	elif (kwargs['schema'] != True) and (cmdline[index] in ("-n","--no-schema")):
		arg_parse_err(ARG_LIMIT,"schema flag",usage)
	elif (index + 1) > len(cmdline):
		arg_parse_err(REQUIRED_ARG,"schema",usage)

	#fi
    #rof

    # Call stateful function for execution 
    add_database_terminus_execute(kwargs)

    return 0
#fed
def print_gen_usage():
	usage = \
"""
PLACEHOLDER
"""
	print(usage)
	#fed
def main():
    if len(sys.argv) < 3:
	print_gen_usage()
	exit(REQUIRED_ARG)
    if sys.argv[2] == "add-database":
        add_database_action(sys.argv)
    return 0
#fed

if __name__ == "__main__":
    main()
#fi
