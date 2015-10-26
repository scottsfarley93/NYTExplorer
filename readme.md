1.	Setup
1.1.	Get developer key – used by organizations to keep track of who is using their API interface and make sure that people don’t use too many of their resources without paying
1.1.1.	Go to http://developer.nytimes.com/
1.1.2.	Click ‘Request an API Key’
1.1.3.	Sign into your NYT account or create one now – its free.
1.1.4.	 Give your application a name – it can be anything, since you won’t be deploying you application it doesn’t matter.
1.1.5.	Click ‘Issue a new key for Article Search API’
1.1.6.	Agree to the terms of service
1.1.7.	Copy and paste your new API key – you can always find it again online
1.2.	Download materials
1.2.1.	Go to https://github.com/scottsfarley93/NYTExplorer
1.2.2.	Click download zip (lower right)
1.2.3.	Unzip the file
1.3.	Run setup script
The explorer script is fairly dependency heavy (it depends on other libraries of code for much of its functionality).  The setup script that accompanies the main script will try to install these modules for you, so you don’t have to do it manually.  These instructions require you to have administrator access to you computer and that you are running on a mac or linux system, not windows.
1.3.1.	Open a new terminal window
1.3.2.	cd to the folder you just unzipped 
1.3.3.	Run this command: >> sudo python setup.py 
1.3.4.	If you see “You’re all set!” all necessary packages were successfully installed.  Otherwise, you will have to try to install these packages manually. 
1.4.	Set your API key 
1.4.1.	Open nytExplorer.py with any text editor (notepad++)
1.4.2.	Find the class declaration Configuration
1.4.3.	Find the line that says self.apiKey = “” (line 52)
1.4.4.	Replace self.apiKey = “” with self.apiKey = {{your api key}}

At this point, the script should be correctly configured to run on your computer.

2.	Run
2.1.	Run the main script by this command: >>python nytExplorer.py
2.2.	If everything has been setup properly, the main menu should appear in your console. 
2.3.	New Run – Start a new run from scratch  (Option 1)
2.3.1.	Enter a search term, (“Syria”, “Syrian Migrants”.  This term will be used to search the New York Times for articles in which this term appears in the head or body text.
2.3.2.	Enter a start date in yyyy, mm, dd format.  Articles on or after this date will be included in the search
2.3.3.	Enter an end date in yyyy, mm, dd format.  Articles on or before this date will be included in the search
2.3.4.	The system will prompt you for a confirmation.  Review your input to make sure it is correct, if it is, enter ‘Y’ otherwise enter ‘N’ and try again.
2.3.5.	Go get a beer and wait patiently.  The program will first search for all articles that contain your search term, and then try to obtain the text for every one of these articles.  The amount of time this process takes depends on your search term and the duration of your date range.  Expect large searches (popular term and 10-12 months range) to take 2-4 hours.  Expect smaller searcher (popular terms with <1 month range) to take around 10-15 minutes. 
2.3.6.	Your results are saved by default to a .dat file (json with encoded text) so you won’t have to wait if you want to do this same search again sometime.
2.4.	Load a file
2.4.1.	Previous runs are saved by default to /users/[Your Username]/documents/nytExplorer/explorer_[startString]_[endString].dat
2.4.2.	If you have one of these files, select option 2 of the main menu.  When prompted, enter you .dat file path.
2.4.3.	If it is correctly formatted, it should be successfully imported into the program.
3.	Analysis Menu – Analysis choices are grouped into aggregate analysis (statistics over all text within your time range) and term change analysis (daily statistics for each day in your time range). 
3.1.	Aggregate mode – Analyze all text to get aggregate statistics
3.1.1.	Interactive Mode
3.1.1.1.	Interactive mode allows you to query search terms one at a time.  This will take some time on larger datasets.  This searches all the text within your date range and returns the number of occurrences of this term.
3.1.1.2.	Enter a query. Wait for response.  Repeat as desired.
3.1.1.3.	Press Q to quit.
3.1.2.	Query builtin lists – Several lists have been precompiled for analysis.
3.1.2.1.	Built-in lists can be modified by opening the nytExplorer script with a text editor, going to the NYT Parser Class Declaration, Finding the __init__ function (at the top of the declaration), and then adding words to the lists as desired.
3.1.2.2.	Results will not be written to disk, only written to the console.
3.1.2.3.	Built-in lists:
 
3.1.2.3.1.	European Countries (and other regionally important countries): 
"RUSSIA", 
"UKRAINE", 
"FRANCE", 
"SPAIN", 
"SWEDEN", 
'GERMANY', 
"FINLAND", 
"NORWAY", 
"POLAND", 
"ITALY",
"UK", 
"ROMANIA", 
"BELARUS", 
"KAZAKHSTAN", 
"GREECE", 
"BULGARIA", 
"ICELAND", 
"HUNGARY", 
"PORTUGAL",
"AZERBAIJAN",
“AUSTRIA",
 "CZECH", 
"SERBIA",
 "IRELAND", 
"GEORGIA", 
"LITHUANIA", 
"LATVIA",
 "CROATIA", 
"BOSNIA",
"HERZEGOVINA", 
"SLOVAKIA", 
"ESTONIA",
 "DENMARK", 
"NETHERLANDS", 
"SWITZERLAND", 
"MOLDOVA", 
"BELGIUM",
"ARMENIA", 
"ALBANIA", 
"MACEDONIA", 
"TURKEY",
 "SLOVENIA", 
"MONTENEGRO", 
"CYPRUS", 
"LUXEMBOURG",
"ANDORRA", 
"MALTA",
"LIECHTENSTEIN" 
"MONACO", 
"VATICAN", 
"SYRIA", 
"LEBANON", 
"JORDAN", 
"IRAQ",
"IRAN", 
"EGYPT", 
"UNITED", 
"STATES", 
"AFGHANISTAN", 
"LIBYA",
"MOROCCO"
3.1.2.3.2.	Culturally important queries
"MUSLIM", 
"ARAB", 
"CHRISTIANITY", 
"JEW", 
"JEWISH", 
"CHRISTIAN",
"KURD", 
"ISLAM", 
"QURAN", 
"BIBLE", 
"ISIS", 
"ISLAMIC"
3.1.2.3.3.	Other Queries:
"SYRIAN", 
"EUROPEAN", 
"RUSSIAN", 
"AFGHAN", 
"IRAQI", 
"HUNGARIAN", 
"MIGRANT", 
"REFUGEE", 
"WAR",
"CIVIL", 
“BOMB", 
"TERRORIST", 
"TERROR",
 "SHOOTING", 
"SHOT", 
"KILLED", 
"DEAD",
"SOLDIER",
 "ARMED", 
"GUNMEN", 
"MILITANT", 
"SECURITY", 
"FORCES",
 "PEACE", 
"TENSION", 
"EAST",
 "WEST",
"WESTERN", 
"EASTERN", 
"CLASH", 
"BATTLE", 
"CONTESTED",
"AGENCY”
 
3.1.3 Print aggregate statistics – print the number of articles analyzed, number of days in the analysis, the number of total words in the analysis and the number of unique words.
3.1.4 Find common phrases – search the text data for common phrases of 2- and 3- words.  (Works, but under development).
3.1.5 Quit Aggregate mode with ‘Q’ 
3.2.	Term Change / Time series analysis
3.2.1.	Change points – Possible points of interest based in the data.  Change points will be automatically calculated for each field you search for (i.e., “Russia” may have 2 change points, “Syria”4 change points, etc). 
3.2.2.	Single Term – Interactive mode like in aggregate analysis mode.  Search for a single term.  The results will include graphs of occurrence over your time period, possible change points, and a csv of the results. The csv is automatically saved to disk at: /Users/[Your Username]/Documents/NYTExplorer/term_change_analysis_[startString]_[endString].csv
3.2.2.1.	Graphics and Change points are in development, but work marginally well for now.
3.2.3.	List of Terms – Interactive mode to add terms to a list, and then see how those changes happen in relation to one another (i.e., put “Syria”, “Russia”, and “Hungary” all on a single graph and look at their relative rates of change.  
3.2.4.	Terms of built-in Europe Query – Query the European countries list (see above) and write the results to a csv.  Graphics are surpressed. Change points are analyzed.
3.2.5.	Terms of built-in Other Query – Query the Other query list (see above) and write the results to a csv.  Graphics are surpressed.  Change points are analyzed.
3.2.6.	Press Q to quit time series analysis.
4.	Implementation Strategies
4.1.	Coming soon.


5.	Menu Design


##Main Menu
	##New Run
	##Load Run
##Analysis Menu
	##Aggregate mode
		##Interactive Mode
		##Built-in Lists
		##Aggregate Statistics
		##Common Phrases
	##Time Series / Term Change
		##Single Term (interactive)
		##List of Terms (interactive)
		##Query Europe List
		##Query ‘Other’ List

		






