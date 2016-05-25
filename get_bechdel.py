import urllib
import urllib2
import parser

movie_map = parser.get_parsed_data()
url = 'http://bechdeltest.com/search/'

for key in movie_map:
	title = movie_map[key].title
	query_args = {'term': title}
	data = urllib.urlencode(query_args)

	request = urllib2.Request(url, data)
	response = urllib2.urlopen(request)

	html = response.read()
	passing = "<img src=\"/static/pass.png\""
	print title, (passing in html)
