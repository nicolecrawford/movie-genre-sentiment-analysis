########################################################################
#####################not in use, use file in ./script ##################
########################################################################




import re
import urllib
import urllib2

import parser


movie_map = parser.get_parsed_data()
url = 'http://www.boxofficemojo.com/search/q.php'
movie_success = {}
total = len(movie_map.keys())
counter = 0
for key in movie_map:
	box_office = 0
	budget = 0
	movie_page = ""
	title = movie_map[key].title
	query_args = {'q': title}
	data = urllib.urlencode(query_args)

	request = urllib2.Request(url, data)

	try:
		response = urllib2.urlopen(request)
	except urllib2.HTTPError as e:
		print title, e # this only seems to fail on "the world is not enough"
	else:
		html = response.read()
		# searching for highlighted entry; it's the most likely to be correct
		m = re.search('<tr bgcolor=#FFFF99>(.+)</tr>', html, re.DOTALL)
		box_office = 0
		if m is not None:
			m = m.group(0)
			box_office = re.search('>\$([\d,]+)<', m)
			if box_office is not None:
				box_office = int(box_office.group(1).replace(",", ""))
			else:
				box_office = 0


			movie_page = "http://www.boxofficemojo.com" + re.search('<a href="(/movies/\?id=\w+.htm)">', m).group(1)
			# get the budget
			response = urllib2.urlopen(movie_page)
			html = response.read()
			budget = re.search('Production Budget: <b>\$(\d+) million</b>', html)
			if budget is not None:
				budget = budget.group(1)			
				budget = int(budget.replace(",", "") + ("0" * 6))
			else:
				budget = 0

		print "------------------"
		print title, box_office
		print movie_page
		print "budget:", budget
		if box_office is not None: counter += 1

		if budget < movie_success:
			movie_success[key] = 1
		elif budget > movie_success:
			movie_success[key] = -1
		else:
			movie_success[key] = 0



print counter, total
# 456/617 movies have results for this; that's 74%
# get budget data? it's a lot more complicated 
