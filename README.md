# snitch

Snitch is a tool which automate dorking process for specified domain. Using build-in dork categories, this tool helps gather informations about domain which can be found using search engines. It can be quite useful in early phases of pentest.


###Examples

```
devil@hell:~/snitch$ python snitch.py

		               _ __       __  
		   _________  (_) /______/ /_ 
		  / ___/ __ \/ / __/ ___/ __ \ 
		 (__  ) / / / / /_/ /__/ / / /
		/____/_/ /_/_/\__/\___/_/ /_/ ~0.1   
		  
Usage: snitch.py [options]

Options:
  -h, --help            show this help message and exit
  -U [url], --url=[url]
                        url address *
  -D [type], --dork=[type]
                        dork types separated by comma *
  -O [file], --output=[file]
                        save results to file
  -S [ip:port], --socks5=[ip:port]
                        socks5 proxy
  -I [seconds], --interval=[seconds]
                        interval between requests, 2s by default
  -P [pages], --pages=[pages]
                        pages to retrieve, 3 by default

Dork types:
  info  | Information leak / Potential web bugs
  ext   | Interesting extensions
  docs  | Documents
  files | Files and directories
  soft  | Web software
  all   | All

Examples:
  snitch.py -I5 -P3 --dork=ext,info -U gov -S 127.0.0.1:9050
  snitch.py --url=site.com -D all -O /tmp/dorks
```

```
devil@hell:~/Desktop/Python$ python snitch.py -I5 -P5 -D ext --url=gov -S 127.0.0.1:9050
[+] Target: gov
[!] Using SOCKS5 (IP - XX.XX.XX.XX)
[!] Interval set to 5 s
[!] Pages limit set to 5

[+] Looking for interesting extensions

http://www.seismic.ca.gov/pub/CSSC_1998-01_COG.pdf.OLD
http://oceancitymd.gov/Risk/top.inc
http://www.swrcb.ca.gov/losangeles/board_decisions/adopted_orders/index.shtml.old
ftp://ftp.fec.gov/FEC/new_f1nm.inc
http://oceancitymd.gov/Risk/footer.inc
ftp://ftp.fec.gov/FEC/new_f1tp.inc
http://www.erh.noaa.gov/gsp/office/office.bak
http://taunton-ma.gov/Pages/TauntonMA_WebDocs/wheretogo.old
https://www.health.ny.gov/health_care/medicaid/nyserrcd.ini
http://maine.gov/REVENUE/netfile/WS_FTP.LOG
http://www-esh.fnal.gov/pls/default/itna.log
http://www.dss.virginia.gov/tst.log
http://appliedresearch.cancer.gov/nhanes_pam/create.pam_perday.log
http://www.glerl.noaa.gov/metdata/2check_all.log
http://appliedresearch.cancer.gov/nhanes_pam/create.pam_perminute.log
https://security.fnal.gov/krb5.conf
http://okdrs.gov/php.ini
https://aglearn.usda.gov/customcontent/OCIO/USDA-CUI-FOIA/server/config_tpl/php.ini
http://okcommerce.gov/assets/php/simplepie.inc

[+] Done!

```


###Todo
 * More search engines
