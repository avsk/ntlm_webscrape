import sys,getopt
import urllib2
import mechanize
import mechanize
from ntlm import HTTPNtlmAuthHandler
import re

##Configuration

incident = ''

user = 'nttda259'
password = 'welcome4'
baseurl = 'https://tfs.bcbsnc.com/CAisd/pdmweb.exe'

# password manager
passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
passman.add_password(None, baseurl, user, password)

auth_NTLM = HTTPNtlmAuthHandler.HTTPNtlmAuthHandler(passman)

# create browser instance and set handles

browser = mechanize.Browser()
browser.set_handle_refresh(False)  # can sometimes hang without this

# enable debugging information :

browser.set_debug_http(True)
browser.set_debug_redirects(True)
browser.set_debug_responses(True)

# add user agent headers
# Chrome 

browser.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36')]

# Internet Explorer
'''
browser.addheaders = [('User-agent', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3; .NET4.0E)')]
'''
# prepare handlers to use

handlersToKeep = []

for handler in browser.handlers:
	if not isinstance(handler,(mechanize._http.HTTPRobotRulesProcessor)):
		handlersToKeep.append(handler)
		
# set handlers 
browser.handlers = handlersToKeep
# add ntlm authorization handler
browser.add_handler(auth_NTLM)


'''Get incident number'''
def getArg(argv):     
	
	try:
		opts,args= getopt.getopt(argv,"hi:",["help","incident="])
	except getopt.GetoptError:
		print "Usage : argtest.py -i <incident>"
		sys.exit(2)

	for opt,arg in opts:
		if opt in ("-h","--help"):
			print "Usage : argtest.py -i <incident>"
		elif opt in ("-i","--incident"):
			return arg
			


# username , pasword, base url details

'''
	user name , password should be provided as argument and encrypted : TODO 
	
'''

def connectUrl():
	response = browser.open(baseurl)
	resdata = response.read()

	#Log Response : 
	with open('./log/responsebaseurl.html','w') as f :
		f.write(resdata)
	
# get target url from returned page 
# for now inspect returned url session id and use (Need to work on logic to capture this)
# url = url + session_id
# example : 

	'''
	<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
	<html lang="en"><HEAD>

	</HEAD>
	<BODY>
	<SCRIPT LANGUAGE="JavaScript">
	var url = "/CAisd/pdmweb.exe?SID=940509109+FID=552358377+OP=REPLACE_LOGIN+HTMPL=post_menu.htmpl";
	window.location.replace(url);
	</SCRIPT>
	</BODY>
	</HTML>
	'''

	# url = url + "/CAisd/pdmweb.exe?SID=940509109+FID=552358377+OP=REPLACE_LOGIN+HTMPL=post_menu.htmpl"

	session_id = re.findall('url = "?\'?([^"\'>]*)',resdata).pop()
	url = baseurl + session_id

	browser.open(url)
	browser.select_form('post_menu')
	browser.method = "POST"

	response = browser.submit()


	#Log Response : 
	with open('./log/responsesessionid.html','w') as f :
		f.write(response.read())

	browser.select_form(nr=0)
	print incident
	browser['PERSID'] = incident
	response = browser.submit()

	#Log Response : 
	with open('./log/responseincident.html','w') as f :
		f.write(response.read())

	
if __name__ == "__main__":
		incident = getArg(sys.argv[1:])
		connectUrl()
