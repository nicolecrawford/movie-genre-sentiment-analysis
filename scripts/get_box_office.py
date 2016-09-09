import re
import urllib
import urllib2
import httplib # for partial read
import pickle
import parser


# do only once
# movie_map = parser.get_parsed_data()
# pickle.dump(movie_map, open("pickles/movie_map.p", "wb"))

# load
movie_map = pickle.load(open("pickles/movie_map.p", "r"))
print "finished loading movie_map"

url = 'http://www.boxofficemojo.com/search/q.php'
movie_success = {}
total = len(movie_map.keys())
hits = 0
flops = 0
no_data = 0
mid_range = 0
for key in movie_map:
	movie_success[key] = 0
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
		try:
			html = response.read()
		except httplib.IncompleteRead as e:
			html = e.partial
		
		# searching for highlighted entry; it's the most likely to be correct
		m = re.search('<tr bgcolor=#FFFF99>(.+)</tr>', html, re.DOTALL)
		
		# searching if there's only one movie found
		one_movie = re.search('>1 Movie Matches:(.*?)</table>', html, re.DOTALL)

		if m is None and one_movie is not None:
			m = one_movie.group(0)
		elif m is not None:
			m = m.group(0)

		box_office = 0
		budget = 0
		movie_page = ""

		# if either a highlighted match or only 1 match was found
		if m is not None:

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

				# 16 million
				budget = re.search('Production Budget: <b>\$(\d+) million</b>', html)
				if budget is None: # 16.5 million
					budget = re.search('Production Budget: <b>\$(\d+)\.\d\d? million</b>', html)

				if budget is not None:
					budget = budget.group(1)			
					budget = int(budget.replace(",", "") + ("0" * 6))
				else:
					budget = 0
		
		print title
		print "box_office", box_office
		print movie_page
		print "budget:", budget

		if budget == 0 or box_office == 0: # no info
			no_data += 1
			movie_success[key] = 0
			print "box office n/a"
		elif (budget * 1.5) < box_office: # success
			hits += 1
			movie_success[key] = 1
			print "box office success"
		elif budget > box_office: # failure
			flops += 1
			movie_success[key] = -1
			print "box office flop"
		else: # nothing
			mid_range += 1
			movie_success[key] = 0
			print "box office dead gap"


print "hits", hits
print "flops", flops
print "no_data", no_data
print "mid_range", mid_range

pickle.dump(movie_success, open("pickles/movie_success_point_five.p", "wb"))


print total
# 456/617 movies have results for this; that's 74%
# get budget data? it's a lot more complicated 
