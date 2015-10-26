##This is the New York Times Data Explorer
##This is version 0.0.5
##Run setup.py before attempting to run this script

print "Welcome to the New York Times Data Explorer."
print "Getting set up.  Please Wait."
##Import all modules
try:
    import progressbar
    import nltk
    import urllib2
    import json
    import time
    from bs4 import BeautifulSoup
    import requests
    import collections
    import operator
    import os
    import matplotlib.pyplot as plt
    import pandas
    import ast
except ImportError:
    print "You do not have the necessary modules properly configured.  Try running the setup script."
    exit()



class Day():
    """Holds attributes for a single day of news.  Holds number of articles, words, etc"""
    def __init__(self):
        self.numAnalyzed = 0 ##number that are news articles and that were available online
        self.numHits = 0 ##overall pieces of content
        self.numNotNews = 0 ##articles not meeting news article requirements
        self.numNotAccessed = 0 ##Articles that were not available online
        self.numWords = 0  ##number of total words for the day
        self.numUniqueWords = 0  ##Number of unique words for this day
        self.date = "" ##date string for this day
        self.urls = [] ##urls of all articles (news and non-news, online and not online)
        self.text = "" ##the raw text aggregated for the day
        self.savedLocation = "" ##file location for this text dump

class Configuration():
    """Holds configurations for this execution of the script and holds default file names"""
    def __init__(self):
        ##Program options
        self.doProgress = False
        self.changeThreshold = 1 ##percent
        docsFolder = os.environ['HOME'] + "/documents"
        if not os.path.exists(docsFolder + "/NYTExplorer"):
            os.mkdir(docsFolder + "/NYTExplorer")
        self.defaultFolder = docsFolder + "/NYTExplorer"
        self.apiKey = ""


class NYTParser():
    """Class to implement a web scraper of new york times articles using their search api v2 and html parsing"""
    def __init__(self, searchTerm, startDate, endDate):
        ##Dates are tuples (year, month, day)
        self.startDate = startDate
        self.endDate = endDate
        ##Validate dates --> end must be after start and months, days, years, should be valid(ish)
        try:
            assert(len(str(startDate[0])) == 4)
            assert(len(str(endDate[0])) == 4)
            assert(startDate[1] < 13)
            assert(startDate[1] > 0)
            assert(startDate[2] > 0)
            assert(startDate[2] < 32)
            assert(endDate[1] > 0)
            assert(endDate[1] < 13)
            assert(endDate[2] > 0)
            assert(endDate[2] < 32)
        except AssertionError:
            print "Start date was: ", startDate
            print "End date was: ", endDate
            print "Failed to validate input dates.  Aborting script."
            exit()
        ##formatv dates for api
        self.startString = self.assembleDateString(self.startDate)
        self.endString = self.assembleDateString(self.endDate)
        d = pandas.Timestamp(self.endString) - pandas.Timestamp(self.startString)
        self.numDays = d.days
        try:
            assert(int(self.startString) <= int(self.endString))
        except AssertionError:
            print "End date must be greater than start date.  Aborting script."
            exit()
        self.searchTerm = searchTerm
        self.sections_to_ignore =["Advertisement", None] ##gets rid of these sections, because it is hard to really accurately pin down where the article is in the page
        self.characters_to_replace = [",", ".", "!", "/", "?", ">", "<", '"', "'"] ##characters to get rid of so they don't throw off analysis
        self.occurrenceTerms = []
        self.alltext = "" ##big-ass string
        ##Get configuration options
        self.config = Configuration()
        ##Lists of hardcoded queries that can be calculated within interactive mode
        self.europeQuery = ["RUSSIA", "UKRAINE", "FRANCE", "SPAIN", "SWEDEN", 'GERMANY', "FINLAND", "NORWAY", "POLAND", "ITALY",
                          "UK", "ROMANIA", "BELARUS", "KAZAKHSTAN", "GREECE", "BULGARIA", "ICELAND", "HUNGARY", "PORTUGAL","AZERBAIJAN",
                          "AUSTRIA", "CZECH", "SERBIA", "IRELAND", "GEORGIA", "LITHUANIA", "LATVIA", "CROATIA", "BOSNIA",
                          "HERZEGOVINA", "SLOVAKIA", "ESTONIA", "DENMARK", "NETHERLANDS", "SWITZERLAND", "MOLDOVA", "BELGIUM",
                          "ARMENIA", "ALBANIA", "MACEDONIA", "TURKEY", "SLOVENIA", "MONTENEGRO", "CYPRUS", "LUXEMBOURG",
                          "ANDORRA", "MALTA", "LIECHTENSTEIN", "MONACO", "VATICAN", "SYRIA", "LEBANON", "JORDAN", "IRAQ",
                          "IRAN", "EGYPT", "UNITED", "STATES", "AFGHANISTAN", "LIBYA", "MOROCCO"] ##MUST BE IN ALL CAPS

        self.cultureQuery = ["MUSLIM", "ARAB", "CHRISTIANITY", "JEW", "JEWISH", "CHRISTIAN", "KURD", "ISLAM", "QURAN", "BIBLE", "ISIS", "ISLAMIC"]

        self.other_query = ["SYRIAN", "EUROPEAN", "RUSSIAN", "AFGHAN", "IRAQI", "HUNGARIAN", "MIGRANT", "REFUGEE", "WAR",
                            "CIVIL", "SLAUGHTER", "BOMB", "TERRORIST", "TERROR", "SHOOTING", "SHOT", "KILLED", "DEAD",
                            "SOLDIER", "ARMED", "GUNMEN", "MILITANT", "SECURITY", "FORCES", "PEACE", "TENSION", "EAST", "WEST",
                            "WESTERN", "EASTERN", "CLASH", "BATTLE", "CONTESTED", "AGENCY"]
        self.builtinLists = [self.europeQuery, self.cultureQuery, self.other_query]
        ##Stopwords == words that are not interesting for analysis (the, on, with, of, ...)
        from nltk.corpus import stopwords
        sw = stopwords.words('english')
        sw_list = ["ON", "'S", "FOR", '-', '?']
        i = 0
        while i < len(sw):
            w = sw[i].upper()
            sw_list.append(w)
            i +=1
        self.words_to_ignore = sw_list
        self.days = [] ##list of day objects to keep references of the time series
        return

    def getDay(self, day):
        """Querys the database for a specific day yyyymmdd (string) and saves the aggregated text to disk"""
                ##Query elements
        baseURL = "http://api.nytimes.com/svc/search/v2/articlesearch.json"
        api_key = self.config.apiKey ##Scott Farley, scottsfarley@gmail.com
        q = self.searchTerm ##term to search Nyt database for, eg "Syria"
        ##url encode the search term if it is multiple words long
        if " " in q:
            q = q.replace(" ", "%20")
        if self.validateDateString(day):
            begin_date = day ##already in string format
            end_date = day ##already in string format
        else:
            print "Not valid date"
            exit()
        sort = "newest"
        ##Get total number of articles expected to be returned
        URL = baseURL + "?sort=" + sort + '&fq=' + q + '&begin_date=' + str(begin_date) + "&end_date=" + str(end_date) + "&api-key=" + api_key
        response = urllib2.urlopen(URL)
        response = json.load(response)
        numHits = response['response']['meta']['hits']
        self.numArticles = numHits
        ##will fail if there are 0 hits, so quit preemptively if nothing is returned
        if numHits == 0:
            print "Didn't find any articles at all for ", self.searchTerm, "between", self.startDate, "and", self.endDate
            return [] ##return an empty list instead of quiting so we can continue with interactive mode if we want
        ##Now loop through and get data on all articles
        articleURLS = []
        period_start = int(begin_date)
        period_end = int(begin_date)
        total_end = int(end_date)
        numRead = 0
        numNotRead = 0
        overallCounter = 0
        articlesNotNews=0
        ##Get the number of 10 page increments needed to extract all data
        numPages = numHits / 10
        #numPages = 1
        i = 0
        day_text = "" ##Keeps track of all text for the day
        while i < numPages:
            ##Query the database
            URL = baseURL + "?sort=" + sort + '&fq=' + q + '&begin_date=' + str(period_start) + "&end_date=" + str(period_end) + "&page=" + str(i) + "&api-key=" + api_key
            ##parse the response
            response = urllib2.urlopen(URL)
            data = json.load(response)
            offset = data['response']['meta']['offset']
            #loop through the items in the page
            j = 0
            ##article URLS are found in the json like this json['response']['docs']['web_url']
            articles = data['response']['docs']
            while j < len(articles):
                ##only get news articles
                article = articles[j]
                url = article['web_url']
                t = article['type_of_material']
                dtype = article['document_type']
                source = article['source']
                if dtype == 'article' and t == "News" and url != None and url not in articleURLS:
                    text = self.getHTMLOfArticle(url)
                    if text.strip() != "Go to Home Page" and text != "":
                        day_text += text ##aggregate all text for the day
                    else:
                        numNotRead += 1
                    articleURLS.append(url)
                else:
                    articlesNotNews += 1
                j += 1
                overallCounter += 1
            time.sleep(0.1) ##Limits on api calls
            i += 1
        ##get text stats
        ##create an object to hold these properties
        thisDay = Day()
        thisDay.numNotNews = articlesNotNews
        thisDay.numHits = numHits
        thisDay.numNotAccessed = numNotRead
        thisDay.numAnalyzed = numHits - articlesNotNews - numNotRead
        thisDay.text = day_text
        thisDay.date = day
        thisDay.urls = articleURLS
        return thisDay



    def getDateRange(self, start, end, saveRawText=False, verbose=False):
        """Run the getday function for each day in a range --> effectively aggregates and stores text found for each day in the range"""
        period_start = int(self.assembleDateString(start))
        period_end = int(self.assembleDateString((end)))
        running_date = period_start
        daysInRange = [] ##list of Day objects that represent each day of news
        while running_date <= period_end:
            day = str(running_date) ##must be fed to getDay as string
            print "Day is: ", day
            d = self.getDay(day) ##returns Day Object
            if saveRawText:
                self.writeDayToFile(d) ##saves text to disk in default location
            ##tokenize the text for summary of words
            text = d.text
            words = nltk.word_tokenize(text)
            totalWords = len(words)
            uniqueWords = len(set(words))
            d.numWords = totalWords
            d.numUniqueWords = uniqueWords
            self.days.append(d)
            if verbose:
                self.getDaySummary(d)
            running_date = int(self.getNextDate(day)) ##advance loop
        return



    def validateDateString(self, s):
        """Validates a yyyymmmdd date string"""
        try:
            assert isinstance(s, str)
            assert(len(s) == 8)
        except AssertionError:
            print "Incorrectly formatted date string"
            return False
        try:
            int(s)
        except:
            print "Not a valid date."
            return False
        return True

    def assembleDateString(self, tup):
        """Converts from a (yyyy, mm, dd) tuple to a yyyymmdd string"""
        year = tup[0]
        month = tup[1]
        day = tup[2]
        if month < 10:
            monthStr = "0" + str(month)
        else:
            monthStr = str(month)

        if day<10:
            dayString = "0" + str(day)
        else:
            dayString = str(day)
        return str(year) + monthStr + dayString

    def getNextDate(self, dateString):
        """Returns the string of the next day in the calendar --> deals with month and year changes"""
        dateString = str(dateString)
        year = dateString[0:4]
        month = dateString[4:6]
        day = dateString[6:8]

        daysInMonths = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]##doesnt deal with leap years
        monthNumber = int(month)
        dayNumber = int(day)
        yearNumber = int(year)
        daysInThisMonth = daysInMonths[monthNumber - 1] ##correct for index
        ##year changes
        if monthNumber == 12 and dayNumber >= 31:
            yearNumber += 1
            monthNumber = 1
            dayNumber = 1
        else:
            ##month changes
            if dayNumber >= daysInThisMonth:
                monthNumber += 1
                dayNumber = 1
            else:
                dayNumber +=1
        yearString = str(yearNumber)
        ##format with zeros
        if monthNumber < 10:
            monthString = "0" + str(monthNumber)
        else:
            monthString = str(monthNumber)
        if dayNumber < 10:
            dayString = "0" + str(dayNumber)
        else:
            dayString = str(dayNumber)
        return yearString + monthString + dayString

    def getHTMLOfArticle(self, url, tag='p'):
        """Scrape the body text of an article at url, returns a text string.
        tag is the html tag to search for."""
        r = requests.get(url)
        data = r.text
        soup = BeautifulSoup(data)
        body = soup.html.body
        story = soup.select(tag)
        article_text = ""
        i = 0
        while i < len(story):
            ##Story might be split into multiple html elements
            s = story[i].string ##gives the value inside of the tagged element

            if s not in self.sections_to_ignore:
                value = "".join([x if ord(x) < 128 else '?' for x in s])
                value = value.replace("?", " ")
                if value != "Go to Home Page": ##This is the text if the article is no longer online at nyt.com
                    article_text += value + " "
            i += 1
        return article_text

    def writeDayToFile(self, D, loc="default"):
        """Accepts a Day object and writes the text to file"""
        text = D.text
        date = D.date
        if loc == "default":
            loc = self.config.defaultFolder + "/articleText_" + date + ".txt"
        f = open(loc, 'w')
        f.write(text)
        f.close()
        D.savedLocation = loc

    def getDaySummary(self, D):
        """Reads a day object and prints out a summary of the number of words and articles"""
        date = D.date
        print "-----Day:", date, "---------"
        print "Total Content Found: ", D.numHits
        print "Content not News Articles: ", D.numNotNews
        print "Articles Not Read: ", D.numNotAccessed
        print "Analyzed: ", D.numAnalyzed
        print "Total Words: ", D.numWords
        print "Unique Words: ", D.numUniqueWords
        print "Saved to: ", D.savedLocation


    def aggregateDateRange(self):
        """Aggregates the text over all of the dates in the date range requested so you can do overall analysis"""
        self.aggregatedText = ""
        for d in self.days:
            t = d.text
            self.aggregatedText += t
        return self.aggregatedText


    def findCollocations(self, text, verbose=True):
        """Find common phrases for a piece of text"""
        print "Searching..."
        words = self.tokenize(text)
        bigram_measures = nltk.collocations.BigramAssocMeasures
        finder = nltk.collocations.BigramCollocationFinder.from_words(words)
        finder.apply_freq_filter(3)
        two_word_collocations = finder.nbest(bigram_measures.pmi, 10)
        trigram_measures = nltk.collocations.TrigramAssocMeasures()
        finder3 = nltk.collocations.TrigramCollocationFinder.from_words(words)
        finder3.apply_freq_filter(3)
        three_words = finder3.nbest(trigram_measures.pmi, 3)
        if verbose:
            print "-----Common Phrases-----"
            print "1.  Two-Word Phrases:"
            i = 0
            while i < len(two_word_collocations):
                p = two_word_collocations[i]
                print p[0], p[1]
                i +=1
            print "\n\n"
            print "2.  Three-word Phrases:"
            i =0
            while i < len(three_words):
                p = three_words[i]
                print p[0], p[1], p[2]
                i +=1
        return [two_word_collocations, three_words]


    def countOccurrencesOfTerm(self, text, term, verbose=False):
        """Counts and returns the number of times a term appears in a text string
            Returns tuple of form (term, count)"""
        ##only do analysis in uppercase
        words = self.tokenize(text)
        term = term.upper()
        c = words.count(term)
        if verbose:
            print 'Found', c, "occurrences of term", term
        return (term, c)

    def countOccurrencesOfTermsInList(self, text, termList, verbose=False):
        """Counts the number of times each term in a list appears in a text string
            Returns the result as a list of tuples (term, occurrences)"""
        results = []
        i = 0
        while i < len(termList):
            ##iterate through all terms
            term = termList[i]
            occ = self.countOccurrencesOfTerm(text, term, verbose=False)
            results.append(occ)
            i +=1
        ##sort by frequency
        s = sorted(results, key=lambda tup: tup[1]) ##list of tuples sorted by frequency
        s.reverse() ##highest to lowest
        if verbose:
             ##print the results
            j = 0
            while j < len(s):
                t = s[j]
                print t[0], t[1] ##term, value
                j += 1
        return s


    def dateStringtoTuple(self, dateString):
        """Convert a date string to a date tuple"""
        year = dateString[0:4]
        print year
        month = dateString[4:6]
        print month
        day = dateString[6:8]
        print day
        try:
            year = int(year)
            month = int(month)
            day = int(month)
        except:
            print "Improperly formatted date string."
            return (0, 0, 0)
        return (year, month, day)

    def tokenize(self, text):
        """Convert to upper case, tokenize via nltk, and remove stopwords"""
        words = nltk.word_tokenize(text)
        return_words = []
        i = 0
        while i < len(words):
            word = words[i]
            word = word.upper()
            if word not in self.words_to_ignore and word not in self.characters_to_replace:
                return_words.append(word)
            i +=1
        return return_words

    def analyzeChange(self, termsList, plot=True, normalize=False, save=True, saveLocation='default', resampleInterval='default', resampleRule='sum'):
        """Find change points for the terms in termsList within the text argument"""
        ##turn off graphing if more than 5 fields
        if len(termsList) > 5:
            plot = False
        ##build pandas data frame
        results = []
        headers = ["Date", "NumArticles"] + termsList
        dates = []
        ##iterate through date range
        ##progressbar to show long operation
        if self.numDays != 0:
            w = ["Reading: ", progressbar.Percentage(), " ", progressbar.Bar(), " ", progressbar.FileTransferSpeed()]
            bar = progressbar.ProgressBar(maxval=self.numDays + 1, widgets=w).start()

                ##resample
        if resampleInterval == 'default':
            ##if longer than 2 months -> resample to weeks
            if self.numDays > 60:
                resampleInterval = '1W'
            ##if longer than 12 months -> resample to months
            if self.numDays > 365:
                resampleInterval = '1M'
        

        i = 0
        while i < len(self.days):
            day = self.days[i]
            dateString = day.date
            termOccurrences = [] ##putting into a dataframe, so we just want occurrence value
            ts = pandas.Timestamp(dateString)
            termOccurrences.append(ts)
            text = day.text
            occ = self.countOccurrencesOfTermsInList(text, termsList)
            dates.append(str(ts.year) + "-" + str(ts.month) + "-" + str(ts.day))
            ##normalization
            numArticles = day.numAnalyzed
            termOccurrences += [numArticles]
            j = 0
            while j < len(occ):
                if normalize:
                    if numArticles != 0: ##Div!/0 error prevention
                        val = (occ[j][1] / numArticles)
                    else:
                        val = 0
                    termOccurrences += [val]
                else:
                    val = (occ[j][1])
                    termOccurrences += [val]
                j +=1
            results.append(termOccurrences)
            i +=1
            if self.numDays !=0 :
                bar.update(i)
        df = pandas.DataFrame(results, columns=headers, index=dates)
        if self.numDays!= 0:
            bar.finish()

        ##plot the results
        if plot:
            ##plot the whole df
            plt.figure()
            df.plot(title="Term List # per Day")
            plt.xlabel("Day")
            plt.ylabel("Raw Number of Mentions")
            for column in df:
                ##plot rate of change plots
                col = df[column]
                if column != 'Date':
                    pct = col.pct_change(periods=2)
                    plt.figure()
                    if normalize:
                        title = column + " Percent Change in Mentions/Article"
                    else:
                        title = column + " Percent Change in Number of Mentions"
                    if column == 'NumArticles':
                        title = "Number of Articles"
                    pct.plot(kind='bar', title=title)
                    col.plot()
                    plt.xlabel("Day")
                    plt.ylabel("Percent Change")
            ##finish
            plt.show()

        ##try to find change points
        print "________POSSIBLE CHANGE POINTS________"
        changePoints = {}
        for column in df:
            col = df[column] ##pandas series
            if column != 'Date':
                pct_change = col.pct_change(periods = 2)
                possible_changepoints = []
                i = 0
                while i < len(pct_change):
                    item = pct_change[i]
                    if item > 0: ##we only want positive change
                        if i > 0: ## can't do this on the first record
                            previous = pct_change[i-1]
                            if item > self.config.changeThreshold and item > previous:
                                row = df.ix[i,]
                                date = row['Date']
                                possible_changepoints.append(date)
                    i +=1
                changePoints[column] = possible_changepoints
        for item in changePoints:
            print "--------", item, "---------"
            i = 0
            while i < len(changePoints[item]):
                print changePoints[item][i]
                i +=1

        ##save the file, if requested
        if save:
            if saveLocation == 'default':
                saveLocation = self.config.defaultFolder + "/term_change_analysis_" + self.startString + "_" + self.endString + ".csv"
            ##write the data frame
            df.to_csv(saveLocation)
            print "Saved analysis to csv"
        return df

    def getCalculatedDays(self):
        i = 0
        while i < len(self.days):
            print self.days[i].date
            i +=1

    def saveRangeAsJSON(self, outfile='default'):
        """Save a date range of days as json"""
        out = {}
        out['searchTerm'] = self.searchTerm

        startDate = self.days[0].date
        numdays = len(self.days)
        endDate = self.days[numdays - 1].date
        out['startDate'] = startDate
        out['endDate'] = endDate
        out['data'] = []

        i = 0
        while i < len(self.days):
            day = self.days[i]
            date = day.date
            d = str(day.__dict__)
            d = d
            out['data'].append(d)
            i +=1
        out = json.dumps(out)
        if outfile == 'default':
            outfile = self.config.defaultFolder + "/explorer_" + startDate + "_" + endDate + ".dat"
        f = open(outfile, 'w')
        f.write(out)
        f.close()
        print "Wrote data to disk"

    def printDateRangeStatistics(self):
        numArticles = 0
        numWords = 0
        numUniqueWords = 0
        i = 0
        while i < len(self.days):
            d = self.days[i]
            numArticles += d.numAnalyzed
            numWords += d.numWords
            numUniqueWords += d.numUniqueWords
            i +=1
        print "------Date Range Aggregation------"
        print "Start Date: ", self.startDate
        print "End Date: ", self.endDate
        print "Articles Analyzed: ", numArticles
        print "Total words analyzed: ", numWords
        print "Unique words analyzed: ", numUniqueWords



def loadRangeFromDisk(filename):
    """Load a date range data file from the disk
        parse the values into attributes
        return the corresponding parser object"""
    try:
        f = open(filename, 'r')
        data = json.load(f)
        days = data['data']
        searchTerm = data['searchTerm']
        startDate = data['startDate']
        endDate = data['endDate']
        startDateTup = dateStringtoTuple(startDate)
        endDateTup = dateStringtoTuple(endDate)
        ##number of days in period
        delta = pandas.Timestamp(endDate) - pandas.Timestamp(startDate)
        tsd = int(delta.days) ##days between start and end
        print "Found data file object with", tsd, "days. Importing..."
        ##make new parser object
        parser = NYTParser(searchTerm, startDateTup, endDateTup)
        ##show a progress bar to indicate the loading progress
        w = ["Loading: ", progressbar.Percentage(), " ", progressbar.Bar(), " ", progressbar.ETA()]
        bar = progressbar.ProgressBar(maxval=tsd+1, widgets=w).start()
        ##add the days to the parser's day list
        #parser.numDays = tsd
        i = 0
        counter = 0
        for i in days:
            try:
                jsonData = ast.literal_eval(json.loads(i))  ##make a dictionary from a unicode string --> not sure why this is necessary but it works.
            except:
                try:
                    jsonData = ast.literal_eval(i)
                except:
                    print "Could not import data file.  Super sorry.  Peaceout!"
                    exit()
            D = Day() ##new Day instance
            D.numWords = jsonData['numWords']
            D.numNotAccessed = jsonData['numNotAccessed']
            D.numUniqueWords = jsonData['numUniqueWords']
            D.text = jsonData['text']
            D.numHits = jsonData['numHits']
            D.numNotNews = jsonData['numNotNews']
            D.urls = jsonData['urls']
            D.savedLocation = jsonData['savedLocation']
            D.date = jsonData['date']
            D.numAnalyzed = D.numHits - D.numNotAccessed - D.numNotNews
            parser.days.append(D)
            counter +=1
            bar.update(counter)
        f.close()
        bar.finish()
        return parser
    except Exception as e:
        print "Failed to import requested file."
        print "File was:", filename
        print "Error was:", str(e)
        print "Super sorry.  Goodbye."




def dateStringtoTuple(dateString):
    """Convert a date string to a date tuple"""
    year = dateString[0:4]
    month = dateString[4:6]
    day = dateString[6:8]
    try:
        year = int(year)
        month = int(month)
        day = int(day)
    except:
        print "Improperly formatted date string."
        return (0, 0, 0)
    tup = (year, month, day)
    return tup



#s = NYTParser("Syria", (2015, 10, 1), (2015, 10, 23))
#s.getHTMLOfArticle("http://www.nytimes.com/2015/10/24/world/middleeast/us-and-russia-find-common-goals-on-syria-if-not-on-assad.html?_r=0")
#s.getDateRange((2015, 10, 1), (2015, 10, 23))
#text = s.aggregateDateRange()
#s.findCollocations(text)
#s.countOccurrencesOfTerm(text, "Syria", verbose=True)
#s.analyzeChange(['Russia', "Syria", "States", "ISIS", "Turkey", "Hungary"])
#s.saveRangeAsJSON()
#loadRangeFromDisk("/Users/Scottsfarley/Documents/NYTExplorer/explorer_20150101_20150102.dat")
#s = loadRangeFromDisk("/Users/Scottsfarley/Documents/NYTExplorer/explorer_20151001_20151023.dat")
#text = s.aggregateDateRange()
#print text
#s.countOccurrencesOfTerm(text, "Syria", verbose=True)
#s.countOccurrencesOfTerm(text, "Russia", verbose=True)
#s.getCalculatedDays()
#s.analyzeChange(["Syria", "Russia", 'States'], plot=True)
#s.analyzeChange(s.europeQuery, plot=False, save=True)


def InteractiveRun():
    ##Main Menu
    ##1. New Run
    ##2. Load From Disk
    ##Q. Quit
    mainMenu = True
    conf = Configuration()
    if conf.apiKey == "":
        ##Abort if user does not have their own api key
        print "You must enter your api key before continuing."
        exit()
    while mainMenu:
        try:
            mainMenuChoices = ['1', '2', 'Q', 'q']
            mainChoice = raw_input("----New York Times Explorer Main Menu----\n"
                               "\t(1)New Run\n"
                               "\t(2)Load from disk\n"
                               "\t(Q)uit program\n"
                               "Choice:::")
            if mainChoice not in mainMenuChoices:
                raise ValueError
            elif mainChoice == '1':
                ##Run New Run --> download, etc from website
                ##create new parser
                confirm  = True
                while confirm:
                    ##make sure the user has the desired settings
                    try:
                        term = raw_input("Please enter a search term: ")
                        startDate = input("Enter a search start date in format yyyy,mm,dd:")
                        endDate = input("Enter a search end date in format yyyy,mm,dd:")
                        userConfirm = raw_input("The following analysis will run:\n"
                                                "\tSearch Term: " + str(term) + "\n"
                                                "\tStart Date: " + str(startDate) + "\n"
                                                "\tEnd Date: " + str(endDate) + "\n"
                                                "Is this Correct? (Y/N)")
                        if userConfirm == 'Y' or userConfirm == 'y':
                            confirm = False
                        else:
                            raise ValueError
                    except ValueError:
                        print "Okay, let's try again."
                ##validate
                assert isinstance(term, str)
                assert isinstance(startDate, tuple)
                assert isinstance(endDate, tuple)
                parser = NYTParser(term, startDate, endDate)
                parser.getDateRange(startDate, endDate)
                parser.saveRangeAsJSON() ##write to disk
                mainMenu = False
            elif mainChoice == '2':
                load = True
                while load:
                    try:
                        ##load a .dat file from disk
                        fName = raw_input("Enter a .dat file to import or (Q)uit: ")
                        if fName == 'Q' or fName=='q':
                            load = False
                        elif not os.path.exists(fName) or fName[-4:] != ".dat": ##make sure its a legit file
                            raise ValueError
                        else:
                            parser = loadRangeFromDisk(fName)
                            load = False
                            mainMenu = False
                    except ValueError:
                        print "That was not a valid file name."
            elif mainChoice == "q" or mainChoice == 'Q':
                print "Okay goodbye!"
                exit()
        except ValueError:
            print "Not an option, try again."
    ########ANALYSIS --> parser object has been successfully loaded
    print "Explorer Object Loaded Successfully."
    analysisMenu = True
    while analysisMenu:
        try:
            analysisChoices = ['1', '2', 'q', 'Q']
            analysisChoice = raw_input("----Analysis Menu----\n"
                                   "\t(1)Aggregate Analysis\n"
                                   "\t(2)Term Change Analysis\n"
                                   "\t(Q)uit\n"
                                   "Choice:::")
            if analysisChoice not in analysisChoices:
                raise ValueError
            elif analysisChoice == '1':
                ##aggregate the text and analyze
                aggMode = True
                ##do the text aggregation
                aggText = parser.aggregateDateRange()
                while aggMode:
                    try:
                        aggOptions = ['1', '2', '3', '4', 'Q', 'q']
                        aggChoice = raw_input("\t----Aggregate Data Options----\n"
                                          "\t\t(1)Interactive Mode\n"
                                          "\t\t(2)Query Built-in Lists\n"
                                          "\t\t(3)Print aggregate statistics\n"
                                          "\t\t(4)Find Common Phrases\n"
                                          "\t\t(Q)uit aggregate mode\n"
                                          "\tChoice:::")
                        if aggChoice not in aggOptions:
                            raise ValueError
                        elif aggChoice == '1' :
                            ##interactive mode
                            interactive = True
                            while interactive:
                                try:
                                    term = raw_input("Enter a term to query or (Q)uit interactive mode:")
                                    if term == 'Q' or term == 'q':
                                        ##quit interactive mode
                                        interactive = False
                                    else:
                                        print "Querying text..."
                                        ##do the query
                                        parser.countOccurrencesOfTerm(aggText, term, verbose=True)
                                except:
                                    pass ##keep the loop running
                        elif aggChoice == '2':
                            ##Query the built in lists of the parser
                            i = 0
                            while i < len(parser.builtinLists):
                                queryList = parser.builtinLists[i]
                                parser.countOccurrencesOfTermsInList(aggText, queryList, verbose=True)
                                i += 1
                            raise ValueError ##return to menu
                        elif aggChoice == '3':
                            parser.printDateRangeStatistics()
                            raise ValueError
                        elif aggChoice == '4':
                            parser.findCollocations(aggText)
                        elif aggChoice == 'Q' or aggChoice =='q':
                            ##Quit aggregation mode
                            aggMode = False
                    except ValueError:
                        pass

            elif analysisChoice == '2':
                ##time series analysis
                changeMode = True
                while changeMode:
                    try:
                        changeOptions = ['1', '2', '3', '4',  'q', 'Q']
                        changeChoice = raw_input("\t----Time Series/Change Analysis Menu----\n"
                                       "\t\t(1)Single Term\n"
                                       "\t\t(2)List of Terms\n"
                                       "\t\t(3)Terms in Built-in Europe Query\n"
                                       "\t\t(4)Terms in Built-in Other Query\n"
                                       "\t\t(Q)uit\n"
                                       "\tChoice::::")
                        if changeChoice not in changeOptions:
                            raise ValueError
                        if changeChoice == 'Q' or changeChoice =='q':
                            changeMode = False ##Quit change mode
                        elif changeChoice == '1':
                            interactive = True
                            while interactive:
                                try:
                                    term = raw_input("Enter a search term or (Q)uit interactive mode:")
                                    if term == 'Q' or term=='q':
                                        interactive = False
                                    else:
                                        if " " in term.strip():
                                            print "Term must be only one word."
                                            raise ValueError
                                        parser.analyzeChange([term])
                                except:
                                    pass
                        elif changeChoice == '2':
                            buildList = True
                            builtList = False
                            termList = []
                            while buildList:
                                try:
                                    print "Current list is: ", termList
                                    term = raw_input("Add a search term to the list, (D)one, (Q)uit:")
                                    if term == 'Q' or term == 'q':
                                        buildList = False
                                    if term == 'D' or term =='d':
                                        builtList = True
                                        print "List is: ", termList
                                        buildList = False
                                    else:
                                        if " " in term.strip():
                                            print "Terms must be only one word."
                                            raise ValueError
                                        else:
                                            termList.append(term)
                                except ValueError:
                                    pass
                            ##if the user built the list, then do the query
                            if builtList:
                                if len(termList) != 0:
                                    parser.analyzeChange(termList)
                                else:
                                    print "You must enter at least one search term."
                        elif changeChoice == '3':
                            ##query europe query
                            print "Analyzing europe query list."
                            parser.analyzeChange(parser.europeQuery)
                        elif changeChoice == 4:
                            print "Analyzing other query list."
                            parser.analyzeChange(parser.other_query)
                    except:
                        pass ##continue with loop
                raise ValueError
            elif analysisChoice == 'q' or analysisChoice == 'Q':
                print "Okay Goodbye!"
                exit()
        except ValueError:
            print "Not an option, try again."

InteractiveRun()