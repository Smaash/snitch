# snitch

Snitch is a tool which automate information gathering process for specified domain. Using build-in dork categories, this tool helps gather specified informations domain which can be found using web search engines. It can be quite useful in early phases of pentest.

####Examples

```
devil@hell:~/snitch$ python snitch.py
		               _ __       __  
		   _________  (_) /______/ /_ 
		  / ___/ __ \/ / __/ ___/ __ \ 
		 (__  ) / / / / /_/ /__/ / / /
		/____/_/ /_/_/\__/\___/_/ /_/ ~0.3   
		  
Usage: snitch.py [options]

Options:
  -h, --help            show this help message and exit
  -U [url], --url=[url]
                        domain(s) or domain extension(s) separated by comma*
  -D [type], --dork=[type]
                        dork type(s) separated by comma*
  -C [dork], --custom=[dork]
                        custom dork*
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
  info   Information leak & Potential web bugs
  ext    Sensitive extensions
  docs   Documents & Messages
  files  Files & Directories
  soft   Web software
  all    All


```

```
devil@hell:~/snitch$ python snitch.py -D ext -U gov -P15
[!] Pages limit set to 15
[+] Target: gov

[+] Looking for sensitive extensions

http://www.seismic.ca.gov/pub/CSSC_1998-01_COG.pdf.OLD
http://greengenes.lbl.gov/Download/Sequence_Data/Fasta_data_files/CoreSet_2010/formatdb.log
http://www.uspto.gov/web/patents/pdx/permitting_access.pdf_2010may17.bak
https://software.sandia.gov/trac/canary/attachment/ticket/3917/Pike_Hach%26SCAN_Oracle.edsx_convert.log
http://www.dss.virginia.gov/tst.log
http://appliedresearch.cancer.gov/nhanes_pam/create.pam_perday.log
https://igscb.jpl.nasa.gov/igscb/station/log/abmf_20150428.log
http://sun.ars-grin.gov:8080/dbf.sql
http://cci.lbl.gov/~phzwart/Betty_data/latest_data/acorn/14_molrep.log
http://appliedresearch.cancer.gov/nhanes_pam/create.pam_perminute.log
https://software.sandia.gov/trac/dakota/attachment/ticket/4166/hopperConf.log
https://igscb.jpl.nasa.gov/igscb/station/mgexlog/nya2_20130905.log
http://www.swrcb.ca.gov/losangeles/board_decisions/adopted_orders/index.shtml.old
http://web.epa.ohio.gov/phpMyAdmin.2.11.5/scripts/create_tables_mysql_4_1_2+.sql
https://trac.mcs.anl.gov/projects/mpich2/attachment/ticket/83/config.log
https://tcga-data.nci.nih.gov/docs/index.html.bak
http://spec.jpl.nasa.gov/ftp/pub/catalog/c098001.log
http://www.glerl.noaa.gov/metdata/2check_all.log
http://www.maine.gov/dep/ftp/MAIRIS/5.2.3_Installation/mairis_5_2_3_seq_mgmt.sql
http://ft.ornl.gov/eavl/regression/configure.log
http://airsar.jpl.nasa.gov/airdata/PRECISION_LOG/hd1883.log
http://www.uspto.gov/main/homepagenews/pprwrk_rdctn_act.htm_2009sep29a.bak
http://eula.mindspark.com/cookies/
http://www.antd.nist.gov/pubs/Sriram_BGP_IEEE_JSAC.pdf.old
http://www-esh.fnal.gov/pls/default/itna.log
http://web.epa.ohio.gov/phpMyAdmin.2.11.5/scripts/upgrade_tables_mysql_4_1_2+.sql
http://www.modot.mo.gov/newsandinfo/documents/_baks/Whathappenstoyourbenefitswhenyouterminatestateemployment.pdf.0001.c487.bak
http://maine.gov/REVENUE/netfile/WS_FTP.LOG
http://mls.jpl.nasa.gov/lay/UARS_MLS.LOG
http://airsar.jpl.nasa.gov/airdata/PRECISION_LOG/hd1469.log
http://www.iowa.gov/boee/handbook.pdf.old
http://yuri.lbl.gov/ontologies/obo-all/uberon_prerelease/uberon_prerelease.obo_xml.OLD
https://igscb.jpl.nasa.gov/igscb/station/general/blank.log
http://yuri.lbl.gov/ontologies/obo-all/disease_ontology/disease_ontology.owl2.OLD
https://www.health.ny.gov/health_care/medicaid/nyserrcd.ini
http://www.thruway.ny.gov/business/contractors/expedite/bid.ini
http://www.wpc.ncep.noaa.gov/html/ecmwf0012loop500_ak.cfg
https://fermilinux.fnal.gov/documentation/security/krb5.conf
http://spartatools.dnsops.gov/wiki/index.php/Dnsval.conf
http://w3.pppl.gov/~hammett/comp/MSWindows/teraterm/TERATERM.INI
http://usgcb.nist.gov/usgcb/content/configuration/workstation-ks.cfg
https://ics-web.sns.ornl.gov/kasemir/CSS/Training/DLS/Config/settings.ini
http://cmip-pcmdi.llnl.gov/cmip5/docs/esg.ini
http://spartatools.dnsops.gov/wiki/index.php/Dnssec-tools.conf
http://www.usatlas.bnl.gov/~caballer/files/cvmfs/etc/httpd/welcome.conf
https://security.fnal.gov/krb5.conf
http://collaborate2.nws.noaa.gov/canned_data/data_files/pqact.conf
http://archives1.dags.hawaii.gov/gsdl/collect/vitalsta/etc/oai.cfg
http://lambda.gsfc.nasa.gov/data/suborbital/BICEP2/B2_3yr_camb_planck_withB_params_20140314.ini

[+] Done!

```


####Changelog
######0.3.2
	- Fixed: 'socks' import error, logo printing on win, loop using 'all' dork types
######0.3.1
	- Fixed 'dork type' iteration with the 'all' value
######0.3
	- more search engines
	- custom dorks / multiple targets
	- misc fixes
######0.2
 	- more dorks & search engines
 	- misc
 
