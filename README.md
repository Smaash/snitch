# snitch

Snitch is a tool which automate dorking process for specified domain. Using build-in dork categories, this tool helps gather informations about domain which can be found using search engines. It can be quite useful in early phases of pentest.


####Examples

```
devil@hell:~/snitch/$ python snitch.py

		               _ __       __  
		   _________  (_) /______/ /_ 
		  / ___/ __ \/ / __/ ___/ __ \ 
		 (__  ) / / / / /_/ /__/ / / /
		/____/_/ /_/_/\__/\___/_/ /_/ ~0.2   
		  
Usage: snitch.py [options]

Options:
  -h, --help            show this help message and exit
  -U [url], --url=[url]
                        domain(s) or domain extension(s) separated by comma *
  -D [type], --dork=[type]
                        dork type(s) separated by comma *
  -O [file], --output=[file]
                        output file
  -S [ip:port], --socks=[ip:port]
                        socks5 proxy
  -I [seconds], --interval=[seconds]
                        interval between requests, 2s by default
  -P [pages], --pages=[pages]
                        pages to retrieve, 10 by default
  -v                    turn on verbosity

Dork types:
  info  | Information leak & Potential web bugs
  ext   | Sensitive extensions
  docs  | Documents & Messages
  files | Files & Directories
  soft  | Web software
  all   | All

Examples:
  snitch.py -I5 -P3 --dork=ext,info -U gov -S 127.0.0.1:9050
  snitch.py --url=site.com -D all -O /tmp/dorks

```

```
devil@hell:~/snitch/$ python dork.py -U gov -D ext -P20 -S 127.0.0.1:9050
[+] Target: gov
[!] Using SOCKS5 (IP - XX.XX.XX.XX)
[!] Pages limit set to 20

[+] Looking for sensitive extensions

http://www.seismic.ca.gov/pub/CSSC_1998-01_COG.pdf.OLD
http://greengenes.lbl.gov/Download/Sequence_Data/Fasta_data_files/CoreSet_2010/formatdb.log
http://www.uspto.gov/web/patents/pdx/permitting_access.pdf_2010may17.bak
http://www.dss.virginia.gov/tst.log
http://appliedresearch.cancer.gov/nhanes_pam/create.pam_perday.log
ftp://ftp.eia.doe.gov/pub/oil_gas/natural_gas/feature_articles/2006/ngshock/ngshock.pdf.bak
http://appliedresearch.cancer.gov/nhanes_pam/create.pam_perminute.log
https://igscb.jpl.nasa.gov/igscb/station/mgexlog/nya2_20130905.log
http://www.swrcb.ca.gov/losangeles/board_decisions/adopted_orders/index.shtml.old
https://trac.mcs.anl.gov/projects/mpich2/attachment/ticket/83/config.log
https://tcga-data.nci.nih.gov/docs/index.html.bak
https://software.sandia.gov/trac/canary/attachment/ticket/3917/Pike_Hach%26SCAN_Oracle.edsx_convert.log
http://www.glerl.noaa.gov/metdata/2check_all.log
http://ft.ornl.gov/eavl/regression/configure.log
http://airsar.jpl.nasa.gov/airdata/PRECISION_LOG/hd1883.log
http://www.antd.nist.gov/pubs/Sriram_BGP_IEEE_JSAC.pdf.old
http://www-esh.fnal.gov/pls/default/itna.log
http://www.lanl.gov/wrtout/projects/tscattering/nano/Output//Defaults/ellipsoid.log
http://maine.gov/REVENUE/netfile/WS_FTP.LOG
http://mls.jpl.nasa.gov/lay/UARS_MLS.LOG
http://airsar.jpl.nasa.gov/airdata/PRECISION_LOG/hd1469.log
http://www.modot.mo.gov/_baks/indexalt.htm.0001.b041.bak
ftp://ftp.hrsa.gov/ruralhealth/FY04RAEDGuidance.pdf.bak
https://www.health.ny.gov/health_care/medicaid/nyserrcd.ini
http://www.thruway.ny.gov/business/contractors/expedite/bid.ini
http://www.star.bnl.gov/~pjakl/documents/configuration.cfg
http://www.wpc.ncep.noaa.gov/html/ecmwf0012loop500_ak.cfg
https://fermilinux.fnal.gov/documentation/security/krb5.conf
http://mirror.pnl.gov/macports/release/ports/security/fail2ban/files/pf-icefloor.conf
https://svn.mcs.anl.gov/repos/ZeptoOS/trunk/BGP/ramdisk/CN/tree/etc/syslog.conf
http://cmip-pcmdi.llnl.gov/cmip5/docs/esg.ini
https://security.fnal.gov/krb5.conf
http://collaborate2.nws.noaa.gov/canned_data/data_files/pqact.conf

[+] Done!

```


####Changelog
######0.2
 	- more dorks & search engines
 	- misc
