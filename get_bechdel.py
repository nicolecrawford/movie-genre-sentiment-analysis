import urllib
import urllib2
import parser
import pickle

movie_map = parser.get_parsed_data()
url = 'http://bechdeltest.com/search/'

pass_count = 0
not_pass_count = 0
no_bechdel = 0
bechdel_map = {}
for key in movie_map:
	title = movie_map[key].title
	query_args = {'term': title}
	data = urllib.urlencode(query_args)

	request = urllib2.Request(url, data)
	response = urllib2.urlopen(request)

	html = response.read()
	passing = "<img src=\"/static/pass.png\""
	not_passing = "<img src=\"/static/nopass.png\""
	if passing in html:
		pass_count +=1
		bechdel_map[key] = 1
	elif not_passing in html:
		not_pass_count +=1
		bechdel_map[key] = -1
	else:
		no_bechdel +=1
		bechdel_map[key] = 0

pickle.dump(bechdel_map, open("bechdels.p", "wb"))

