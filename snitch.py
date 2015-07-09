#!/usr/bin/python

# snitch v0.1
# smash [at] devilteam [dot] pl
# github.com/Smaash

try:
	from optparse import OptionParser
	import urllib, json
	import socks, socket
	import sys, signal
	import time
	import random
except:
	print "\n[!] Some python modules might be missing!"
	sys.exit(0)


# Defaults

interval  = 2 # Seconds between requests
limit 	  = 3 # Search pages limit


# Functions

def signal_handler(signal, frame):
    print '\n[!] Interrupted by user!'
    sys.exit(0)


def find(dork):

	global output
	global limit

	sites  = []
	agents = [
	"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3",
	"Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.7) Gecko/20100809 Fedora/3.6.7-1.fc14 Firefox/3.6.7",
	"Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
	"Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)",
	"YahooSeeker/1.2 (compatible; Mozilla 4.0; MSIE 5.5; yahooseeker at yahoo-inc dot com ; http://help.yahoo.com/help/us/shop/merchant/)",
	"Mozilla/5.0 (Windows; U; Windows NT 5.1) AppleWebKit/535.38.6 (KHTML, like Gecko) Version/5.1 Safari/535.38.6",
	"Mozilla/5.0 (Macintosh; U; U; PPC Mac OS X 10_6_7 rv:6.0; en-US) AppleWebKit/532.23.3 (KHTML, like Gecko) Version/4.0.2 Safari/532.23.3"
		      ]
	
	# Google AJAX API
	try:
		for i in range(0, limit):
			time.sleep(interval)
			query = urllib.urlencode({'q' : dork})
 			url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s&start=%i' % (query,i)
 			urllib.URLopener.version = random.choice(agents)
 			response = urllib.urlopen(url)
 			results = response.read()
 			res = json.loads(results) 
 			data = res['responseData']
  			hits = data['results']
  			for h in hits: sites.append(urllib.unquote(h['url']))
  		x = set(sites)
  		for y in x:
  			print y
			if output != 0:
				outfile = open(output, "a")
				outfile.write(y+"\n")
				outfile.close()
	except:
		print "[!] Temporary blocked by google... "
		sys.exit(0)


def dork(url, dork):

	dorkleak = (
	'intext:"supplied argument is not a valid MySQL result resource" OR intext:"supplied argument is not a valid PostgreSQL result" ',
	'intext:"mysql_fetch_assoc() OR intext:"mysql_fetch_object() OR intext:"mysql_numrows() " ',
	'intext: inurl:"*.php?*=*.php" intext:"Warning: include" -inurl:.html -site:"php.net" -site:"stackoverflow.com" -inurl:"*forums*" ', 
	'intext:"PostgreSQL query failed: ERROR: parser: parse error" ',
	'intext:"detected an internal error [IBM][CLI Driver][DB2/6000]" ',
	'intext:"MSSQL_OLEdb : Microsoft OLE DB Provider for SQL Server" OR intext:"MSSQL_Uqm : Unclosed quotation mark" ',
	'intext:"MS-Access_ODBC : ODBC Microsoft Access Driver" OR intext:"MS-Access_JETdb : Microsoft JET Database" ',
	'intext:"error in your SQL syntax" OR intext:"Error Occurred While Processing Request" ',
	'intext:"mysql_num_rows()" OR intext:"mysql_fetch_array()" ',
	'intext:"Server Error in \'/\' Application" ',
	'intext:"Microsoft OLE DB Provider for ODBC Drivers error" ',
	'intext:"InvalidQuerystring" ',
	'intext:"OLE DB Provider for ODBC" ',
	'intext:"VBScript Runtime" ',
	'intext:"ADODB.Field" OR intext:"ADODB.Command" ',
	'intext:"mysql_fetch_row()" ',
	'intext:"Syntax error" OR intext:"GetArray()" OR intext:"FetchRow()" ',
	'intext:"Input string was not in a correct format" ',
	'intext:"Fatal error: Class \'Red_Action\' not found in" ',
	'inurl:/id= intext:"You have an error in your SQL syntax" ',
	'intitle:"Apache Tomcat" "Error Report" ',
	'intext:"ORA-00936: missing expression" OR intext:"ORA-00921: unexpected end of SQL command" OR intext:"ORA-00933: SQL command not properly ended" ',
	'ext:asp  "[ODBC SQL" ',
	'intext:"Warning: pg_exec()" OR intext:"Warning: pg_numrows()" ',
	'intext:"Warning: pg_connect(): Unable to connect to PostgreSQL server: FATAL" ',
	'intext:"Warning:" "failed to open stream: HTTP request failed" "on line" ',
	'intext:"Warning: mysql_connect(): Access denied for user: \'*@*" "on line" -help -forum ',
	'inurl:wp-includes/rss-functions.php intext:/home/ ',
	'intext:JSESSIONID OR intext:PHPSESSID ext:log ext:txt ext:bak '
	)

	dorkext = (
	'ext:bak OR ext:old OR ext:tmp OR ext:inc OR ext:sql ',
	'ext:log OR ext:conf OR ext:cfg OR ext:ini ',
	'ext:inc OR ext:bak OR ext:old OR ext:conf OR ext:cfg OR ext:ini intext:mysql_connect OR intext:mysql_pconnect ',
	'intext:"# phpMyAdmin MySQL-Dump" OR intext:"PostgreSQL database dump" ext:txt OR ext:sql '
	)

	dorkdoc = (
	'ext:cvs OR ext:xls OR ext:ppt OR ext:pptx ',
	'ext:pdf OR ext:docx OR ext:doc OR ext:rtf '
	)

	dorkfile = (
	'inurl:"smb.conf" intext:"workgroup" ext:conf ',
	'intitle:"Index of" .mysql_history OR intitle:index.of ws_ftp.ini OR intitle:index.of .bash_history ',
	'"Index of /backup" ',
	'intitle:"Index of ',
	'inurl:server-status intext:"Apache" ',
	'intitle:phpinfo "PHP Version" ',
	'file:robots ext:txt ',
	'"# phpMyAdmin MySQL-Dump"  "INSERT INTO" -"the" ext:sql ',
	'intext:"# Dumping data for table" ',
	'ext:url +inurl:"ftp://"  +inurl:"@" ',
	'inurl:admin OR intitle:admin +intitle:login ',
	'allinurl:install.php OR upgrade.php ',
	'inurl:admin.php OR inurl:administrator.php OR inurl:cms.php ',
	'ext:wsdl wsdl ',
	'allinurl:"/*/_vti_pvt/" OR allinurl:"/*/_vti_cnf/" ',
	'inurl:configuration.php-dist OR inurl:config.php.bak OR inurl:config.php.new ',
	'ext:xml inurl:sitemap ',
	'ext:zip OR ext:rar OR ext:gz OR ext:tar.gz '
	)

	dorksoft = (
	'"phpMyAdmin" "running on" inurl:"main.php" ',
	'inurl:jmx-console OR inurl:JMXInvokerServlet ',
	'"Microsoft-IIS/* server at" intitle:index.of ',
	'filetype:asmx inurl:(_vti_bin|api|webservice) ',
	'intitle:"Apache Status" "Apache Server Status for" ',
	'"Microsoft-IIS/* server at" intitle:index.of ',
	'intitle:phpMyAdmin OR intitle:phpPgAdmin ',
	'intitle:index.of "Apache" "server at" ',
	'intitle:"Test Page for Apache" OR  inurl:"/jenkins/login" ',
	'intitle:osCommerce OR intext:"Powered by osCommerce" -site:oscommerce.com ',
	'"Welcome to PHP-Nuke" congratulations ',
	'inurl:phpSysInfo/ "created by  phpsysinfo" ',
	'intitle:"Usage Statistics for" "Generated by Webalizer" ',
	'"This summary was generated by  wwwstat" ',
	'intext:"Powered by: vBulletin" ',
	'inurl:wp-login.php OR inurl:wp-admin.php OR inurl:readme.html AND intext:"WordPress" OR intext:"Powered by Wordpress" ',
	'inurl:login.php OR inurl:index.php intext:"SquirrelMail" ',
	'inurl:wiki/MediaWiki OR inurl:typo3/install/index.php?mode= ',
	'XAMPP "inurl:xampp/index" ',
	'intitle:"osTicket :: Support Ticket System" ',
	'intext:"powered by MyBB" OR intext:"powered by MyBulletinBoard" ',
	'"Powered by XOOPS" -site:xoops.pl ',
	'"index of" intext:fckeditor inurl:fckeditor ',
	'intext:"Powered by PHP-Fusion" -inurl:php-fusion ',
	'inurl:+:8443/login.php3 ',
	'intext:"Powered by Quick.Cms" OR intext:"Powered by Quick.Cart" ',
	'intext:"Powered By IP.Board" ',
	'Powered by WHMCompleteSolution - OR inurl:WHMCS OR announcements.php ',
	'inurl:/tiny_mce/plugins/filemanager/ OR inurl:"tiny_mce/plugins/tinybrowser/" ',
	'intext:"powered by CMS Made Simple" OR intext:"Powered by CMSimple" ',
	'intext:"Powered By OpenCart" -site:opencart.pl ',
	'intext:"Driven by DokuWiki" OR intext:"Powered by mojoPortal" ',
	'inurl:+:2222 intext:"DirectAdmin" ',
	'intitle:"Zimbra Web Client Log In" OR intitle:"Zimbra Web Client Sign In" ',
	'intitle:"RoundCube Webmail" OR intitle:"Atmail" OR intitle:"Horde" ',
	'intext:"Powered by Drupal" OR intext:"Powered by Joomla" OR intext:"Powered by PrestaShop" ',
	'intext:"Powered by phpBB" OR intext:"Powered by PunBB" OR intext:"Powered by SMF" ',
	)

	for x in dork.split(','):
		if x == 'info' or x == 'all': 
			print "\n[+] Looking for information leaks\n"
			for y in dorkleak: 
				find(y+"site:"+url)
		elif x == 'ext' or x == 'all': 
			print "\n[+] Looking for interesting extensions\n"
			for y in dorkext: 
				find(y+"site:"+url)
		elif x == 'docs' or x == 'all': 
			print "\n[+] Looking for documents\n"
			for y in dorkdoc: 
				find(y+"site:"+url)
		elif x == 'files' or x == 'all': 
			print "\n[+] Looking for files and directories\n"
			for y in dorkfile: 
				find(y+"site:"+url)
		elif x == 'soft' or x == 'all': 
			print "\n[+] Looking for web software\n"
			for y in dorksoft: 
				find(y+"site:"+url)
		else:
			print "\n[!] Wrong dork type specified!"
			sys.exit(0)


def setproxy(ip, port):
	try:
		socket.inet_aton(ip)
		socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, ip, port)
		socket.socket = socks.socksocket

	except socket.error:
		print "Invalid proxy IP address / port."
		sys.exit(0)


# Main

signal.signal(signal.SIGINT, signal_handler)
prs = OptionParser()

prs.add_option("-U", "--url", dest="url", type="string", help="url address *", metavar="[url]")
prs.add_option("-D", "--dork", dest="dork", type="string", help="dork types separated by comma *", metavar="[type]")
prs.add_option("-O", "--output", dest="output", type="string", help="save results to file", metavar="[file]")
prs.add_option("-S", "--socks5", dest="socks", type="string", help="socks5 proxy", metavar="[ip:port]")
prs.add_option("-I", "--interval", dest="interval", type="int", help="interval between requests, %is by default" % interval, metavar="[seconds]")
prs.add_option("-P", "--pages", dest="pages", type="int", help="pages to retrieve, %i by default" % limit, metavar="[pages]")

(options, args)=prs.parse_args()

if options.url == None or options.dork == None:
	print """
		               _ __       __  
		   _________  (_) /______/ /_ 
		  / ___/ __ \/ / __/ ___/ __ \ 
		 (__  ) / / / / /_/ /__/ / / /
		/____/_/ /_/_/\__/\___/_/ /_/ ~0.1   
		  """
	prs.print_help()
	print """
Dork types:
  info  | Information leak / Potential web bugs
  ext   | Interesting extensions
  docs  | Documents
  files | Files and directories
  soft  | Web software
  all   | All

Examples:
  """+__file__+""" -I5 -P3 --dork=ext,info -U gov -S 127.0.0.1:9050
  """+__file__+""" --url=site.com -D all -O /tmp/dorks
  """
else:

    print("[+] Target: "+options.url)

    if options.socks != None:
    	prx = options.socks.split(":")
    	port = int(prx[1])
    	setproxy(prx[0], port)

    	try:
    		ipres = urllib.urlopen('http://bot.whatismyipaddress.com/')
    		print "[!] Using SOCKS5 (IP - %s)" % ipres.read()
    	except:
    		print "[!] SOCKS connection error"
    		sys.exit(0)


    if options.interval != None:
    	print "[!] Interval set to",options.interval,"s"
    	interval = options.interval    	

    if options.pages != None:
    	print "[!] Pages limit set to",options.pages
    	limit = options.pages  

    if options.output != None:
    	print "[!] Output saved to",options.output
    	output = options.output
    else:
    	output = 0   	

    if options.url != None and options.dork != None:	
		dork(options.url, options.dork)
		print "\n[+] Done!"

