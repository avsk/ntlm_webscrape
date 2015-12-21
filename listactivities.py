from lxml import html

with open("./log/responseincident.html","r") as f:
	 detailstr = f.read()

from lxml import html
tree = html.fromstring(detailstr)

trlist = tree.xpath("//h4[center='Activities']/following::tr")
count = 0
for tr in trlist:
	
	# elecount = 0
	header  = tr.xpath("./th/text()")
	details = tr.xpath("./td/text()")
	
	# if len(header) != 0 or len(details) != 0 :
	if len(header) == 0 and len(details) == 0:
		continue
	else:
		print "tr #"+str(count)
		print "---------------------"
		print header
		print details
		count = count +1
	
	'''for ele in tr.xpath('.//text()'):
		print str(elecount) + ":"
		print ele
		elecount = elecount+1
	print "====================="
	'''
	
	'''try:
		extract = (a,b,c,d)
		extract = act.xpath('.//text()')
	except:
		pass
	'''		
	
	

	
