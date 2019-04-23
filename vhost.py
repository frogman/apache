#! /usr/bin/python

from sys import argv
from os.path import exists
from os import makedirs
from os import symlink
from os import system
import getopt

#
#   Show Usage, Output to STDERR
#
def show_usage():
	print """
	Create a new vHost in Ubuntu Server
	Assumes /etc/apache2/sites-available and /etc/apache2/sites-enabled setup used
	    -d    DocumentRoot - i.e. /var/www/yoursite
	    -h    Help - Show this menu.
	    -s    ServerName - i.e. example.com or sub.example.com
	"""
	exit(1)

#
#   Output vHost skeleton, fill with userinput
#   To be outputted into new file
#
def create_vhost(documentroot, servername):
	out = """<VirtualHost *:80>
    ServerAdmin webmaster@localhost
    ServerName %s
    DocumentRoot %s
    <Directory %s>
        Options -Indexes +FollowSymLinks +MultiViews
        AllowOverride All
        Order allow,deny
        Allow from all
        Require all granted
    </Directory>
    ErrorLog ${APACHE_LOG_DIR}/%s-error.log
    # Possible values include: debug, info, notice, warn, error, crit,
    # alert, emerg.
    LogLevel warn
    CustomLog ${APACHE_LOG_DIR}/%s-access.log combined
</VirtualHost>""" % (servername, documentroot, documentroot, servername, servername)
	return out

#Parse flags, fancy python way. Long options also!
try:		
	opts, args = getopt.getopt(argv[1:], "hd:s:", ["help", "document-root=", 'server-name='])
except getopt.GetoptError, err:
	print str(err)
	show_usage()

#Sanity check - make sure there are arguments
if opts.__len__() == 0:
	show_usage()

documentRoot = None
serverName = None

#Get values from flags
for option, value in opts:
	if option in ('-h', '--help'):
		show_usage()
	elif option in ('-d', '--document-root'):
		documentRoot = value
	elif option in ('-s', '--server-name'):
		serverName = value
	else:
		print "Unknown parameter used"
		show_usage()

if exists(documentRoot) == False:
	makedirs(documentRoot, 0755)
	#chown USER:USER $DocumentRoot #POSSIBLE IMPLEMENTATION, new flag -u ?
	#from pwd import getpwnam  -> inspect: getpwnam('someuser')

if exists('%s/%s.conf' % (documentRoot, serverName)):
	print 'vHost already exists. Aborting'
   	show_usage()
else:
	target = open('/etc/apache2/sites-available/%s.conf' % serverName, 'w')
	target.write(create_vhost(documentRoot, serverName))
	target.close()
	
	srcLink = '/etc/apache2/sites-available/%s.conf' % serverName
	destLink = '/etc/apache2/sites-enabled/%s.conf' % serverName
	symlink(srcLink, destLink)
	
system('service apache2 reload')
