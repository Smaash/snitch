#!/usr/bin/python
# -*- coding: utf-8 -*-

# snitch v0.3.2
# github.com/Smaash

# Examples:
# snitch.py --D ext,info -U gov -S 127.0.0.1:9050
# snitch.py --url=site.com --dork=all -O /tmp/dorks -I5
# snitch.py -C "site:edu ext:bak" -P3 -v

try:
	from optparse import OptionParser
	import urllib, json, re, socket, signal, time, random, sys
except:
	print "\n[!] Some python modules are missing!"
	exit()

try:
	import socks
except:
	print "\n[!] Socks module is missing!"


# Defaults

interval  = 2  # Seconds between requests
limit 	  = 10 # Search pages limit (will notice end of results)


# Functions

def signal_handler(signal, frame):
    print '\n[!] Interrupted by user!'
    exit()


def find(dork):

	global output
	global limit
	global interval
	global verbosity

	method = 1
	clear  = []
	agents = [
	"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3",
	"Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.7) Gecko/20100809 Fedora/3.6.7-1.fc14 Firefox/3.6.7",
	"Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
	"Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)",
	"YahooSeeker/1.2 (compatible; Mozilla 4.0; MSIE 5.5; yahooseeker at yahoo-inc dot com ; http://help.yahoo.com/help/us/shop/merchant/)",
	"Mozilla/5.0 (Windows; U; Windows NT 5.1) AppleWebKit/535.38.6 (KHTML, like Gecko) Version/5.1 Safari/535.38.6",
	"Mozilla/5.0 (Macintosh; U; U; PPC Mac OS X 10_6_7 rv:6.0; en-US) AppleWebKit/532.23.3 (KHTML, like Gecko) Version/4.0.2 Safari/532.23.3",
	"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
	"Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
	"Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)",
	"Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)"
		      ]

	#1 - Google AJAX API
	if method == 1:
		try:
			if verbosity == 1: print "[~] Using Google API"
			for i in range(0, limit):

				time.sleep(interval)
				query = urllib.urlencode({'q' : dork})
 				url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s&start=%i' % (query,i)
 				urllib.URLopener.version = random.choice(agents)
 				try:
 					response = urllib.urlopen(url)
 				except:
					if verbosity == 1: print "\n[!] Timeout connecting to Google API... \n[!] Switching method\n"
					method += 1
					break

 				results  = response.read()
 				res = json.loads(results)

	 			if res['responseStatus'] == 400:
 					i += 666
 					pass

	 			elif res['responseStatus'] == 403:
					if verbosity == 1: print "\n[!] Temporary blocked on Google API.\n[!] Switching method\n"
 					method += 1
 					break

 				data = res['responseData']
  				hits = data['results']
  				for h in hits:
  					clear.append(urllib.unquote(h['url']))

  			method += 1
  			pass

		except ValueError:
			if verbosity == 1: print "\n[!] Lost connection to Google API... \n[!] Switching to next method\n"
			method += 1
			pass

	#2 - Search-Results
	if method == 2:
		try:
			if verbosity == 1: print "[~] Using Search-Results"
			for i in range(0, limit):

				time.sleep(interval)
				url = 'http://www.search-results.com/web?q=%s&hl=en&page=%i&src=hmp' % (urllib.quote(dork), i)
				urllib.URLopener.version = random.choice(agents)

				try:
					response = urllib.urlopen(url)
				except:
					if verbosity == 1: print "\n[!] Timeout connecting to Search-Results... \n[!] Switching method\n"
					method += 1
					break

				results = response.read()

				if re.search('Your search for', results) and re.search('did not match with any results', results):
					i += 666
					pass

				urls = re.findall('(?<=href=")(.*?)(?=")', results)

				for url in urls:
					if 'http' in url or 'https' in url:
						if re.search('search-results', url) or re.search('ask.com', url):
							pass
						else:
							clear.append(url)

			method += 1
			pass

		except ValueError:
			if verbosity == 1: print "\n[!] Lost connection to search-results... \n[!] Switching to next method\n"
			method += 1
			pass

	#3 - Ask
	if method == 3:
		try:
			if verbosity == 1: print "[~] Using Ask"
			for i in range(0, limit):

				time.sleep(interval)
				url = 'http://www.ask.com/web?q=%s&page=%i' % (urllib.quote(dork), i)
				urllib.URLopener.version = random.choice(agents)

				try:
					response = urllib.urlopen(url)
				except:
					if verbosity == 1: print "\n[!] Timeout connecting to Ask... \n[!] Switching method.\n"
					method += 1
					break

				results = response.read()

				if re.search('Your search for', results) and re.search('did not match with any Answers results', results):
					i += 666
					pass

				urls = re.findall('(?<=href=")(.*?)(?=")', results)

				for url in urls:
					if 'http' in url or 'https' in url:
						if re.search('ask.com', url):
							pass
						else:
							clear.append(url)

			method += 1
			pass

		except ValueError:
			if verbosity == 1: print "\n[!] Lost connection to Ask... \n[!] Switching to next method\n"
			method += 1
			pass

	#4 - MyWebSearch
	if method == 4:
		try:
			if verbosity == 1: print "[~] Using MyWebSearch"
			for i in range(0, limit):

				time.sleep(interval)
				url = 'http://int.search.mywebsearch.com/mywebsearch/GGweb.jhtml?searchfor=%s&pn=%i' % (urllib.quote(dork), i)
				urllib.URLopener.version = random.choice(agents)
				try:
					response = urllib.urlopen(url)
				except:
					if verbosity == 1: print "\n[!] Timeout connecting to MyWebSearch... \n[!] Switching method\n"
					method += 1
					break

				results = response.read()

				if re.search('Your search for', results) and re.search('did not match with any results', results):
					i += 666
					pass

				urls = re.findall('(?<=href=")(.*?)(?=")', results)

				for url in urls:
					if 'http' in url or 'https' in url:
						if re.search('mywebsearch', url) or re.search('imgfarm.com', url) or re.search('eula.mindspark.com', url):
							pass
						else:
							clear.append(url)

			method += 1
			pass

		except ValueError:
			if verbosity == 1: print "\n[!] Lost connection to MyWebSearch..."
			method += 1
			pass

	#5 - Google Interia
	if method == 5:
		try:
			if verbosity == 1: print "[~] Using Google Interia"
			for i in range(0, limit):

				time.sleep(interval)
				url = 'http://www.google.interia.pl/szukaj,q,%s,w,sw,p,%i' % (urllib.quote(dork), i)
				urllib.URLopener.version = random.choice(agents)

				try:
					response = urllib.urlopen(url)
				except:
					if verbosity == 1: print "\n[!] Timeout connecting to Google Interia..."
					method = 1

				results  = response.read()

				if re.search('Poszukiwane słowo (fraza)', results) and re.search('nie zostało odnalezione'):
					i += 666
					pass

				urls  = re.findall('(?<=href=")(.*?)(?=")', results)

				for url in urls:
					if 'http' in url or 'https' in url:
						if re.search('interia', url) or re.search("\/szukaj\/kopia,id", url):
							pass
						else:
								clear.append(url)

		except ValueError:
			if verbosity == 1: print "\n[!] Lost connection to Google Interia..."

	else:
		print "\n[!] Wrong method."
		exit()

  	for y in set(clear):
  		if re.search('facebook', y) or re.search('stackoverflow.com', y) or re.search('php.net', y) or re.search('drupal.org', y) or re.search('wordpress.org', y) or re.search('youtube.org', y):
  			pass
  		else:
			print y
			if output != 0:
				try:
					outfile = open(output, "a")
					outfile.write(y+"\n")
					outfile.close()
				except:
					print "\n[!] Error writing to output file."

	method = 1
	return

def dork(url, dork):

	dorkleak = (
	#MySQL
	'intext:"supplied argument is not a valid MySQL result resource" OR intext:"You have an error in your SQL syntax" ',
	'"Unable to jump to row" "on MySQL result index" "on line" ',
	'intext:"mysql_fetch_assoc()" OR intext:"mysql_fetch_object()" OR intext:"mysql_numrows()" ',
	'intext:"mysql_fetch_array()" OR intext:"mysql_fetch_row() OR intext:"mysql_query() ',
	'intext:"Warning: mysql_connect(): Access denied for user: \'*@*" "on line" ',
	'intext:"error in your SQL syntax" OR intext:"Error Occurred While Processing Request" ',

	#IBM
	'intext:"detected an internal error [IBM][CLI Driver][DB2/****]" ',

	#MS
	'intext:"MSSQL_OLEdb : Microsoft OLE DB Provider for SQL Server" OR intext:"MSSQL_Uqm : Unclosed quotation mark" ',
	'intext:"MS-Access_ODBC : ODBC Microsoft Access Driver" OR intext:"MS-Access_JETdb : Microsoft JET Database" ',
	'intext:"Microsoft OLE DB Provider for ODBC Drivers error" OR intext:"InvalidQuerystring" ',
	'intext:"OLE DB Provider for ODBC" OR intext:"VBScript Runtime" ',

	#Oracle
	'intext:"ORA-00936: missing expression" OR intext:"ORA-00921: unexpected end of SQL command" ',
	'intext:"ORA-00933: SQL command not properly ended" OR intitle:"error occurred" "ORA-12541: TNS:no listener" ',
	'intext:"JDBC_CFM" OR intext:"JDBC_CFM2" AND intext:"SQLServer JDBC Driver" OR intext:"Error Executing Database Query" ',

	#PgSQL
	'intext:"PostgreSQL query failed: ERROR: parser: parse error" OR intext:"supplied argument is not a valid PostgreSQL result" ',
	'intext:"Warning: pg_exec()" OR intext:"Warning: pg_numrows()" ',
	'intext:"Warning: pg_connect(): Unable to connect to PostgreSQL server: FATAL" ',

	#Generic
	'intext:"Server Error in \'/\' Application" ',
	'intitle:"Apache Tomcat" "Error Report" ',
	'ext:asp "[ODBC SQL" ',
	'intext:"ADODB.Field" OR intext:"ADODB.Command" ',
	'intext:"Input string was not in a correct format" ',
	'intext: inurl:"*.php?*=*.php" intext:"Warning: include" -inurl:.html ',
	'intext:"Warning:" "failed to open stream: HTTP request failed" "on line" ',
	'intext:"Fatal error: Class \'Red_Action\' not found in" ',
	'intext:"[function.getimagesize]: failed to open stream: No such file or directory in " ',
	'intext: "Warning: Cannot modify header information - headers already sent" ',
	'intext:"Syntax error" OR intext:"GetArray()" OR intext:"FetchRow()" '
	)

	dorkfile = (
	#Dirs
	'intitle:"Index of" OR "Index of /backup" ',
	'intitle:"Index of" .mysql_history OR intitle:index.of ws_ftp.ini OR intitle:index.of .bash_history ',
	'inurl:admin OR inurl:administrator OR intitle:admin +intitle:login ',
	'intitle:"401 Authorization required" ',

	#Files
	'inurl:admin.php OR inurl:administrator.php OR inurl:cms.php ',
	'inurl:"smb.conf" intext:"workgroup" ext:conf ',
	'inurl:server-status intext:"Apache" ',
	'intitle:phpinfo "PHP Version" ',
	'"# phpMyAdmin MySQL-Dump" "# Dumping data for table" "INSERT INTO" -"the" ext:sql ',
	'inurl:test ext:php OR ext:html ',
	'ext:url +inurl:"ftp://"  +inurl:"@" ',
	'allinurl:install.php OR upgrade.php ',
	'inurl:configuration.php-dist OR inurl:config.php.bak OR inurl:config.php.new ',
	'ext:zip OR ext:rar OR ext:gz OR ext:tar.gz OR ext:tar ',

	#Info
	'file:robots ext:txt ',
	'file:crossdomain ext:xml ',
	'inurl:sitemap ext:xml ',
	'ext:wsdl wsdl '
	)

	dorksoft = (
	#Generic
	'"index of" intext:fckeditor inurl:fckeditor ',
	'inurl:/tiny_mce/plugins/filemanager/ OR inurl:"tiny_mce/plugins/tinybrowser/" ',

	#Stats
	'intitle:"Usage Statistics for" "Generated by Webalizer" ',
	'"This summary was generated by wwwstat" ',

	#ReadMe
	'inurl:readme.html OR inurl:readme.txt OR inurl:README ',
	'inurl:changelog.txt OR inurl:CHANGELOG ',

	#HTTP
	'intitle:"Apache Status" "Apache Server Status for" ',
	'intitle:index.of "Apache" "server at" ',
	'intitle:"Apache Tomcat" "Error Report" ',
	'intitle:"Tomcat Server Administration" ',
	'"Microsoft-IIS/* server at" intitle:index.of ',
	'allinurl:"/*/_vti_pvt/" OR allinurl:"/*/_vti_cnf/" OR allinurl:/xampp ',
	'filetype:asmx inurl:(_vti_bin|api|webservice) ',
	'"XAMPP" inurl:xampp/index OR intitle:"Test Page for Apache" ',

	#Managment
	'inurl:+:2222 intext:"DirectAdmin" ',
	'Powered by WHMCompleteSolution - OR inurl:WHMCS OR announcements.php ',
	'intitle:phpMyAdmin OR intitle:phpPgAdmin ',
	'"phpMyAdmin" "running on" inurl:"main.php" ',
	'inurl:jmx-console OR inurl:JMXInvokerServlet ',
	'inurl:"/jenkins/login OR intitle:"Default PLESK Page" ',
	'inurl:8080 intitle:"Dashboard [Jenkins]" ',

	#eCommerce
	'intext:"Powered by Quick.Cms" OR intext:"Powered by Quick.Cart" OR intext:"Powered by PrestaShop" ',
	'intext:"Powered By OpenCart" -site:opencart.pl ',
	'intitle:osCommerce OR intext:"Powered by osCommerce" -site:oscommerce.com ',
	'intext:"Powered by Shopify" OR intext:"Powered by Zen Cart" ',

	#Wiki
	'inurl:wiki/MediaWiki OR inurl:MediaWiki ',
	'intext:"Powered by TWiki" OR intext:"Driven by DokuWiki" ',

	#Mails
	'intitle:"Zimbra Web Client Log In" OR intitle:"Zimbra Web Client Sign In" ',
	'intitle:"RoundCube Webmail" OR intitle:"Atmail" OR intitle:"Horde" ',
	'inurl:login.php OR inurl:index.php intext:"SquirrelMail" ',

	#CMS
	'intext:"powered by CMS Made Simple" OR intext:"Powered by CMSimple" ',
	'intext:"Powered by Drupal" OR intext:"Powered by Joomla" OR intext:"Powered by mojoPortal" ',
	'intext:"Powered by PHP-Fusion" -inurl:php-fusion OR inurl:typo3/install/index.php?mode= ',
	'"Powered by XOOPS" -site:xoops.pl OR intext:"Welcome to PHP-Nuke" ',
	'inurl:wp-login.php OR inurl:wp-admin.php AND intext:"WordPress" OR intext:"Powered by Wordpress" ',

	#Forums
	'intext:"Powered by: vBulletin" OR intext:"Powered By IP.Board" OR intext:"software by XenForo" ',
	'intext:"Powered by MyBB" OR intext:"powered by MyBulletinBoard" ',
	'intext:"Powered by phpBB" OR intext:"Powered by PunBB" OR intext:"Powered by SMF" '
	)

	dorkext = (
	'ext:bak OR ext:old OR ext:tmp OR ext:log OR ext:sql ',
	'ext:inc OR ext:conf OR ext:cfg OR ext:ini OR ext:reg '
	)

	dorkdoc = (
	'ext:cvs OR ext:xls OR ext:ppt OR ext:pptx ',
	'ext:pdf OR ext:docx OR ext:doc OR ext:rtf ',
	'ext:msg OR ext:eml '
	)

	for x in dork.split(','):
		if x in 'all,info,ext,docs,files,soft': 
			if x == 'info' or x == 'all':
				print "\n[+] Looking for information leaks" "\n"
				for y in dorkleak:
					find(y+"site:"+url)
			if x == 'ext' or x == 'all':
				print "\n[+] Looking for sensitive extensions\n"
				for y in dorkext:
					find(y+"site:"+url)
			if x == 'docs' or x == 'all':
				print "\n[+] Looking for documents and messages\n"
				for y in dorkdoc:
					find(y+"site:"+url)
			if x == 'files' or x == 'all':
				print "\n[+] Looking for files and directories\n"
				for y in dorkfile:
					find(y+"site:"+url)
			if x == 'soft' or x == 'all':
				print "\n[+] Looking for web software\n"
				for y in dorksoft:
					find(y+"site:"+url)

		else:
			print "\n[!] Wrong dork type specified!"
			exit()


def setproxy(ip, port):
	try:
		socket.inet_aton(ip)
		socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, ip, port)
		socket.socket = socks.socksocket

	except socket.error:
		print "Invalid proxy IP address / port."
		exit()

# Main

signal.signal(signal.SIGINT, signal_handler)
prs = OptionParser()

prs.add_option("-U", "--url", dest="url", type="string", help="domain(s) or domain extension(s) separated by comma*", metavar="[url]")
prs.add_option("-D", "--dork", dest="dork", type="string", help="dork type(s) separated by comma*", metavar="[type]")
prs.add_option("-C", "--custom", dest="custom", type="string", help="custom dork*", metavar="[dork]")
prs.add_option("-O", "--output", dest="output", type="string", help="output file", metavar="[file]")
prs.add_option("-S", "--socks", dest="socks", type="string", help="socks5 proxy", metavar="[ip:port]")
prs.add_option("-I", "--interval", dest="interval", type="int", help="interval between requests, %is by default" % interval, metavar="[seconds]")
prs.add_option("-P", "--pages", dest="pages", type="int", help="pages to retrieve, %i by default" % limit, metavar="[pages]")
prs.add_option("-v", dest="verb", action="store_true", help="turn on verbosity", metavar=" ")

(options, args) = prs.parse_args()

if len(sys.argv) == 1:
	print """
		               _ __       __
		   _________  (_) /______/ /_
		  / ___/ __ \/ / __/ ___/ __ \\
		 (__  ) / / / / /_/ /__/ / / /
		/____/_/ /_/_/\__/\___/_/ /_/ ~0.3
		  """
	prs.print_help()
	print """
 Dork types:
  info   Information leak & Potential web bugs
  ext    Sensitive extensions
  docs   Documents & Messages
  files  Files & Directories
  soft   Web software
  all    All
  		  """
else:

    if options.socks != None:
    	try:
    		prx = options.socks.split(":")
    		port = int(prx[1])
    		setproxy(prx[0], port)
    	except:
    		print "\n[!] Wrong SOCKS address"
    		exit()
    	try:
    		ipres = urllib.urlopen('http://bot.whatismyipaddress.com/')
    		print "[!] Using SOCKS5 (%s)" % ipres.read()
    	except:
    		print "\n[!] SOCKS connection error"
    		exit()

    if options.verb != None:
    	print "[!] Verbosity on"
    	verbosity = 1
    else:
    	verbosity = 0

    if options.interval != None:
    	print "[!] Interval set to",options.interval,"s"
    	interval = options.interval

    if options.pages != None:
    	print "[!] Pages limit set to",options.pages
    	limit = options.pages

    if options.output != None:
    	print "[!] Output set to",options.output
    	output = options.output
    else:
    	output = 0


	if options.custom != None and options.url == None:
		print "[+] Using custom search"
		find(options.custom)

    if options.url != None and options.dork != None:
    	print "[+] Target: " + options.url
    	for i in options.url.split(","):
			dork(i, options.dork)

	print "\n[+] Done!\n"
