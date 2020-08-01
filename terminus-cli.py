#!/usr/env/python3
import terminusdb_client
import sys
import copy
import argparse
def add_database_notify_user(string):
        print(string)
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
        client.create_database(
                kwargs['dbid'],
                kwargs['accountid'],
                label          = kwargs['label'],
                description    = kwargs['desc'],
                prefixes       = kwargs['prefix'],
                include_schema = kwargs['schema'])
        return 0

#fed
def add_database_parse_args(options):

        #// Oh how I love my curly braces,
        #// and C syntax
        kwargs = \
                {
                        "url":options.url,
                        'accountid':options.account,
                        "dbid":options.dbid,
                        "desc":None,
                        "pass":options.password,
                        "prefix":None,
                        "label":options.label,
                        "schema":options.no_schema
                }

        # Allow the user to spread their description over multiple
        # options.
        if options.description != None:
                kwargs['desc'] = " ".join(options.description);


        # this is placeholder until I figure out how prefixes work
        if options.prefix != None:
                kwargs['prefix'] = " ".join(options.prefix);

        return kwargs;
#fed
def add_database_action(options):
        kwargs = add_database_parse_args(options);
        add_database_terminus_execute(kwargs);
        return 0
#fed
def main():
        parser=argparse.ArgumentParser();
        subparsers = parser.add_subparsers();
        add_database_parser=subparsers.add_parser('add-database', help="Action to create database within specified TerminusDB instance");
        
        add_database_parser.add_argument("url",help="The base url for the TerminusDB instance");
        add_database_parser.add_argument("dbid",help="The ID for the new databaase");
        add_database_parser.add_argument("-u","--account",help="The username/account to login with",
                                         required=True);
        add_database_parser.add_argument("-d","--description",
                                         help="The description for the new database",
                                         action="append");
        add_database_parser.add_argument("-j","--prefix",
                                         help="The prefixes for the new database",
                                         action="append");
        add_database_parser.add_argument("-p","--password",
                                         help="Password to login with",
                                         required=True);
        add_database_parser.add_argument("-l","--label",
                                         help="The label for the database(no spaces allowed)",
                                         required=True);
        add_database_parser.add_argument("-n","--no-schema",
                                         help="Disable schema for the new database");
        add_database_parser.set_defaults(func=add_database_action);
        
        options = parser.parse_args();
        options.func(options);

        return 0;
#fed

if __name__ == "__main__":
    main()
#fi
