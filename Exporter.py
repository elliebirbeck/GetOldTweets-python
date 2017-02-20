# -*- coding: utf-8 -*-

import sys,getopt,got3,datetime,codecs,csv,pytz

def main(argv):

	if len(argv) == 0:
		print ('You must pass some parameters. Use \"-h\" to help.')
		return
		
	if len(argv) == 1 and argv[0] == '-h':
		print ("""\nTo use this jar, you can pass the folowing attributes:
    username: Username of a specific twitter account (without @)
       since: The lower bound date (yyyy-mm-aa)
       until: The upper bound date (yyyy-mm-aa)
 querysearch: A query text to be matched
   maxtweets: The maximum number of tweets to retrieve

 \nExamples:
 # Example 1 - Get tweets by username [barackobama]
 python Exporter.py --username "barackobama" --maxtweets 1\n

 # Example 2 - Get tweets by query search [europe refugees]
 python Exporter.py --querysearch "europe refugees" --maxtweets 1\n

 # Example 3 - Get tweets by username and bound dates [barackobama, '2015-09-10', '2015-09-12']
 python Exporter.py --username "barackobama" --since 2015-09-10 --until 2015-09-12 --maxtweets 1\n
 
 # Example 4 - Get the last 10 top tweets by username
 python Exporter.py --username "barackobama" --maxtweets 10 --toptweets\n""")
		return
 
	try:
		opts, args = getopt.getopt(argv, "", ("username=", "since=", "until=", "querysearch=", "toptweets", "maxtweets=", "outputFilename="))
		
		tweetCriteria = got3.manager.TweetCriteria()
		
		outputFile = codecs.open("output_got.csv", "w+", "utf-8")

		for opt,arg in opts:
			if opt == '--username':
				tweetCriteria.username = arg
				
			elif opt == '--since':
				tweetCriteria.since = arg
				
			elif opt == '--until':
				tweetCriteria.until = arg
				
			elif opt == '--querysearch':
				tweetCriteria.querySearch = arg
				
			elif opt == '--toptweets':
				tweetCriteria.topTweets = True
				
			elif opt == '--maxtweets':
				tweetCriteria.maxTweets = int(arg)

			elif opt == '--outputFilename':
				outputFilename = codecs.open(arg, "w+", "utf-8")	
				
		
		outputFile.write('id;datetime;datetime_gmt;datetime_est;username;text;retweets;favorites;mentions;hashtags;permalink')
		
		print ('Searching...\n')

		gmt = pytz.timezone('GMT')
		est = pytz.timezone('US/Eastern')
		
		def receiveBuffer(tweets):
			for t in tweets:

				#edit to remove quotes and semicolons from tweet text content
				text = t.text
				text_noQuotes = text.replace('"','')
				text_noSemicolon = text_noQuotes.replace(';','')

				#format date and time and adjust timezones
				#datetime = t.date.strftime("%Y%m%d %H:%M %Z")
				dt = datetime.datetime.strptime(t.date.strftime("%Y%m%d %H:%M"), "%Y%m%d %H:%M")
				dt_gmt = gmt.localize(dt)
				dt_est = dt_gmt.astimezone(est)

				outputFile.write(('\n%s;%s;%s;%s;%s;"%s";%d;%d;%s;%s;%s' % (t.id, dt.strftime("%Y%m%d %H:%M"), dt_gmt.strftime("%Y%m%d %H:%M"), dt_est.strftime("%Y%m%d %H:%M"), t.username, text_noSemicolon, t.retweets, t.favorites, t.mentions, t.hashtags, t.permalink)))
			outputFile.flush();
			print ('More %d saved on file...\n' % len(tweets))
		
		got3.manager.TweetManager.getTweets(tweetCriteria, receiveBuffer)
		
	except arg:
		print ('Arguments parser error, try -h' + arg)
	finally:
		outputFile.close()
		print ('Done. Output file generated "output_got.csv".')

if __name__ == '__main__':
	main(sys.argv[1:])