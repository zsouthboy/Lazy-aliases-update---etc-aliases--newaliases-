#!/usr/bin/python

import os, sys, datetime, subprocess

NAME = "Update Aliases 0.1 - 2011-03-11"
ALIAS_FILE = "/etc/aliases"
UPDATE_COMMAND = "newaliases"

def main(new_alias, aliased_email, explanation=""):

	today = str(datetime.date.today())
	print today

	try:
		with open(ALIAS_FILE, "a") as aliases: #open in append mode
			print "Writing date / explanation..."
			aliases.write("\n#%s %s\n" % (today, explanation))
			print "Done\nWriting alias / aliased_email..."
			aliases.write(new_alias + ": " + aliased_email)
			print "Done"
	except EnvironmentError:
		print "ERROR: couldn't open %s for writing. Bailing!" % ALIAS_FILE
		exit(-1)

	try:
		print "Running %s to update aliases in memory..." % UPDATE_COMMAND
		subprocess.Popen(UPDATE_COMMAND)
		print "Done"
	except EnvironmentError:
		print "ERROR: couldn't invoke `%s`. Bailing!" % UPDATE_COMMAND
		exit(-1)
	
	#success
	print "Successfully updated your aliases file."

if __name__ == "__main__":
    if os.getuid() != 0: #check for root UID
        print "ERROR: needs root. Bailing!"
        exit(-1)

    if len(sys.argv) < 3:
        print "\n",NAME
        print '''
Usage(as root): smtp_alias.py new_alias aliased_email explanation


Appends the specified alias to aliased_email mapping to /etc/aliases.
Optionally an explanation may be specified (a timestamped comment will
be added regardless).

Afterwards, `newaliases` is invoked to update the list in memory.

Example:
 smtp_alias.py purple.com myemail signed up for purple.com membership
Would append these two lines:
 #2011-03-11 signed up for purple.com membership
 purple.com: myemail
to /etc/aliases
'''
    elif len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
    else:
        main(sys.argv[1], sys.argv[2], ' '.join(sys.argv[3:]))