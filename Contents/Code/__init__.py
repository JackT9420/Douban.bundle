DOUBAN_API_KEY = "0b2bdeda43b5688921839c8ecb20399b"

DOUBAN_API_URL = "http://api.douban.com/v2/"

DOUBAN_MOVIE_URL = DOUBAN_API_URL + "movie/"
DOUBAN_TV_Shows_URL = ""

#DOUBAN_MOVIE_SEARCH = DOUBAN_MOVIE_URL + 'search?q=%s&apikey=' + DOUBAN_API_KEY
DOUBAN_MOVIE_SEARCH = "https://movie.douban.com/j/subject_suggest?q=%s"
DOUBAN_MOVIE_SUBJECT = DOUBAN_MOVIE_URL + 'subject/%s?apikey=' + DOUBAN_API_KEY
#DOUBAN_MOVIE_BASE = 'http://movie.douban.com/subject/%s/'

def Start():
	HTTP.CacheTime = CACHE_1WEEK

class DoubanAgent(Agent.Movies):
	name = 'Douban'
	languages = [Locale.Language.Chinese, Locale.Language.English]
	primary_provider = True
	accepts_from = ['com.plexapp.agents.localmedia']
	contributes_to = ['com.plexapp.agents.imdb']

	def search(self, results, media, lang):

		search_str = String.Quote(media.name)
		rt = JSON.ObjectFromURL(DOUBAN_MOVIE_SEARCH % search_str, sleep=2.0, cacheTime=CACHE_1HOUR * 3)

		if len(rt)==0:
			pass
		else:
			for i, movie in enumerate(rt):
				if movie["type"] != "movie":
					continue

				score = 90

				dist = String.LevenshteinDistance(movie["title"].lower(), media.name.lower())
				dist = abs(dist)

				if "sub_title" in movie:
					dist_sub = String.LevenshteinDistance(movie["sub_title"].lower(), media.name.lower())
					dist_sub = abs(dist_sub)
					if dist_sub<dist:
						dist = dist_sub

				score = score - dist

				# Adjust score slightly for 'popularity' (helpful for similar or identical titles when no media.year is present)
				score = score - (5 * i)

				release_year = None
				if "year" in movie and movie["year"]:
						try:
							release_year = int(movie['year'])
						except:
							pass

				media_year = None
				try:
					media_year = int(media.year)
				except:
					pass

				if media.year and media_year > 1900 and release_year:
						year_diff = abs(media_year - release_year)
						if year_diff <= 1:
								score = score + 10
						else:
								score = score - (5 * year_diff)

				if score <= 0:
					continue
				else:
					# All parameters MUST be filled in order for Plex find these result.
					results.Append(MetadataSearchResult(id=movie["id"], name=movie["title"], year=movie["year"], lang=lang, score=score))

	def update(self, metadata, media, lang):
		m = JSON.ObjectFromURL(DOUBAN_MOVIE_SUBJECT % metadata.id, sleep=2.0)

		metadata.rating = float(m['rating']['average'])
		metadata.title = m['title']
		metadata.original_title = m['original_title']
		metadata.summary = m['summary']

		# Genres
		metadata.genres.clear()
		for genre in m['genres']:
			metadata.genres.add(genre)

		# Countries
		metadata.countries.clear()
		for country in m['countries']:
			metadata.countries.add(country)

		# Writers
		metadata.writers.clear()
		for writer in m["writers"]:
			meta_writer = metadata.writers.new()
			meta_writer.name = writer["name"]
			meta_writer.photo = writer["avatars"]["large"]

		# Directors
		metadata.directors.clear()
		for director in m['directors']:
			meta_director = metadata.directors.new()
			meta_director.name = director["name"]
			meta_director.photo = director["avatars"]["large"]

		# Roles 
		metadata.roles.clear()
		for cast in m['casts']:
			meta_role = metadata.roles.new()
			meta_role.name = cast["name"]
			meta_role.photo = cast["avatars"]["large"]

		# Poster
		if len(metadata.posters.keys()) == 0:
			poster_url = m['images']['large']
			thumb_url = m['images']['small']
			metadata.posters[poster_url] = Proxy.Preview(HTTP.Request(thumb_url), sort_order=1)

class DoubanAgent(Agent.TV_Shows):
	name = 'Douban'
	languages = [Locale.Language.Chinese, Locale.Language.English]
	primary_provider = True
	accepts_from = ['com.plexapp.agents.localmedia', 'com.plexapp.agents.thetvdb']
	contributes_to = ['com.plexapp.agents.thetvdb']

	def search(self, results, media, lang):

		search_str = String.Quote(media.name)
		rt = JSON.ObjectFromURL(DOUBAN_MOVIE_SEARCH % search_str, sleep=2.0, cacheTime=CACHE_1HOUR * 3)

		if len(rt)==0:
			pass
		else:
			for i, movie in enumerate(rt):
				if movie["type"] != "movie":
					continue

				score = 90

				dist = String.LevenshteinDistance(movie["title"].lower(), media.name.lower())
				dist = abs(dist)

				if "sub_title" in movie:
					dist_sub = String.LevenshteinDistance(movie["sub_title"].lower(), media.name.lower())
					dist_sub = abs(dist_sub)
					if dist_sub<dist:
						dist = dist_sub

				score = score - dist

				# Adjust score slightly for 'popularity' (helpful for similar or identical titles when no media.year is present)
				score = score - (5 * i)

				release_year = None
				if "year" in movie and movie["year"]:
						try:
							release_year = int(movie['year'])
						except:
							pass

				media_year = None
				try:
					media_year = int(media.year)
				except:
					pass

				if media.year and media_year > 1900 and release_year:
						year_diff = abs(media_year - release_year)
						if year_diff <= 1:
								score = score + 10
						else:
								score = score - (5 * year_diff)

				if score <= 0:
					continue
				else:
					# All parameters MUST be filled in order for Plex find these result.
					results.Append(MetadataSearchResult(id=movie["id"], name=movie["title"], year=movie["year"], lang=lang, score=score))

	def update(self, metadata, media, lang):
		m = JSON.ObjectFromURL(DOUBAN_MOVIE_SUBJECT % metadata.id, sleep=2.0)

		metadata.rating = float(m['rating']['average'])
		metadata.title = m['title']
		metadata.original_title = m['original_title']
		metadata.summary = m['summary']

		# Genres
		metadata.genres.clear()
		for genre in m['genres']:
			metadata.genres.add(genre)

		# Countries
		metadata.countries.clear()
		for country in m['countries']:
			metadata.countries.add(country)

		# Writers
		metadata.writers.clear()
		for writer in m["writers"]:
			meta_writer = metadata.writers.new()
			meta_writer.name = writer["name"]
			meta_writer.photo = writer["avatars"]["large"]

		# Directors
		metadata.directors.clear()
		for director in m['directors']:
			meta_director = metadata.directors.new()
			meta_director.name = director["name"]
			meta_director.photo = director["avatars"]["large"]

		# Roles 
		metadata.roles.clear()
		for cast in m['casts']:
			meta_role = metadata.roles.new()
			meta_role.name = cast["name"]
			meta_role.photo = cast["avatars"]["large"]

		# Poster
		if len(metadata.posters.keys()) == 0:
			poster_url = m['images']['large']
			thumb_url = m['images']['small']
			metadata.posters[poster_url] = Proxy.Preview(HTTP.Request(thumb_url), sort_order=1)