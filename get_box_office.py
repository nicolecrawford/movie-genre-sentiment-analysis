import re
import urllib
import urllib2

import parser


movie_map = parser.get_parsed_data()
url = 'http://www.boxofficemojo.com/search/q.php'

total = len(movie_map.keys())
counter = 0
for key in movie_map:
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
		n = None
		if m is not None:
			m = m.group(0)
			n = re.search('>\$([\d,]+)<', m)
		print title, n.group(1)if n is not None else None
		if n is not None: counter += 1

print counter, total
# 456/617 movies have results for this; that's 74%
# get budget data? it's a lot more complicated 