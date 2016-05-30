import re
import urllib
import urllib2
import pickle
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

	print "------------------"
	print title

	request = urllib2.Request(url, data)

	try:
		response = urllib2.urlopen(request)
	except urllib2.HTTPError as e:
		print title, e # this only seems to fail on "the world is not enough"
	else:
		html = response.read()
		
		# searching for highlighted entry; it's the most likely to be correct
		m = re.search('<tr bgcolor=#FFFF99>(.+)</tr>', html, re.DOTALL)
		
		# searching if there's only one movie found
		one_movie = re.search('1 Movie Matches:', html)

		box_office = 0

		# if either a highlighted match or only 1 match was found
		if m is not None or one_movie is not None:
			
			m = m.group(0) if m is not None else html

			box_office = re.search('>\$([\d,]+)<', m)
			if box_office is not None:
				box_office = int(box_office.group(1).replace(",", ""))
			else:
				box_office = 0

			movie_page = "http://www.boxofficemojo.com" + re.search('<a href="(/movies/\?id=[\w\.-]+.htm)">', m).group(1)
			
			# get the budget
			try:
				response = urllib2.urlopen(movie_page)
			except urllib2.HTTPError as e:
				print title, e # this only seems to fail on "the world is not enough"
			else:
				try:
					html = response.read()
				except httplib.IncompleteRead as e:
					html = e.partial
				budget = re.search('Production Budget: <b>\$(\d+) million</b>', html)
				if budget is not None:
					budget = budget.group(1)			
					budget = int(budget.replace(",", "") + ("0" * 6))
				else:
					budget = 0

		print "box_office", box_office
		print movie_page
		print "budget:", budget
		if box_office is not None: counter += 1

		if budget < movie_success:
			movie_success[key] = 1
		elif budget > movie_success:
			movie_success[key] = -1
		else:
			movie_success[key] = 0


pickle.dump(vocab, open("pickles/movie_success.p", "wb"))


print counter, total
# 456/617 movies have results for this; that's 74%
# get budget data? it's a lot more complicated 
