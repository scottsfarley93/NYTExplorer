<h1>New York Times Explorer</h1>
<h6> Author Scott Farley</h6>
<i>UW Madison Cartography</i><br/>
<i>October 2015</i>
<h4>Setup</h4>
<ol>
<li>	Get developer key – used by organizations to keep track of who is using their API interface and make sure that people don’t use too many of their resources without paying</li>
	<ol>
			<li>	Go to http://developer.nytimes.com/</li>
			<li>	Click ‘Request an API Key’</li>
			<li>	Sign into your NYT account or create one now – its free.</li>
			<li>	 Give your application a name – it can be anything, since you won’t be deploying you application it doesn’t matter.</li>
			<li>	Click ‘Issue a new key for Article Search API’</li>
			<li> Agree to the terms of service</li>
			<li>	Copy and paste your new API key – you can always find it again online</li>
	</ol>
<li>	Download materials</li>
<ol>
<li>	Go to https://github.com/scottsfarley93/NYTExplorer </li>
<li>	Click download zip (lower right)</li>
<li>	Unzip the file</li>
</ol>
<li>	Run setup script</li>
<i>The explorer script is fairly dependency heavy (it depends on other libraries of code for much of its functionality).  The setup script that accompanies the main script will try to install these modules for you, so you don’t have to do it manually.  These instructions require you to have administrator access to you computer and that you are running on a mac or linux system, not windows.</i>
<ol>
<li>	Open a new terminal window </li>
<li>	cd to the folder you just unzipped </li>
<li>	Run this command:<code> >> sudo python setup.py </code> </li>
<li>	If you see “You’re all set!” all necessary packages were successfully installed.  Otherwise, you will have to try to install these packages manually. </li>
</ol>
<li>	Set your API key </li>
<ol>
</li>	Open nytExplorer.py with any text editor (notepad++)</li>
</li>	Find the class declaration <code>Configuration</code></li>
</li>	Find the line that says <code>self.apiKey = “” (line 52)</code></li>
</li>	Replace <code>self.apiKey = “” with self.apiKey = {{your api key}} </code></li></ol>
</ol>

<b>At this point, the script should be correctly configured to run on your computer.</b>

<h4>Run</h4>
<ol>
</li>	Run the main script by this command: <code>>>python nytExplorer.py</code></li>
<i>	If everything has been setup properly, the main menu should appear in your console. </i>
<li>	New Run – Start a new run from scratch  (Option 1) </li>
<ol>
<li>	Enter a search term, (“Syria”, “Syrian Migrants”.  This term will be used to search the New York Times for articles in which this term appears in the head or body text.</li>
<li>	Enter a start date in yyyy, mm, dd format.  Articles on or after this date will be included in the search</li>
<li>	Enter an end date in yyyy, mm, dd format.  Articles on or before this date will be included in the search</li>
<li>	The system will prompt you for a confirmation.  Review your input to make sure it is correct, if it is, enter ‘Y’ otherwise enter ‘N’ and try again.</li>
<li>	Go get a beer and wait patiently.  The program will first search for all articles that contain your search term, and then try to obtain the text for every one of these articles.  The amount of time this process takes depends on your search term and the duration of your date range.  Expect large searches (popular term and 10-12 months range) to take <b>2-4 hours</b>.  Expect smaller searcher (popular terms with <1 month range) to take around 10-15 minutes. </li>
<li>	Your results are saved by default to a .dat file (json with encoded text) so you won’t have to wait if you want to do this same search again sometime.</li>
</ol>
<li>	Load a file
	<ol>
<li>	Previous runs are saved by default to <code>/users/[Your Username]/documents/nytExplorer/explorer_[startString]_[endString].dat</code></li>
<li>	If you have one of these files, select option 2 of the main menu.  When prompted, enter you .dat file path.</li>
<li>	If it is correctly formatted, it should be successfully imported into the program.</li>
</ol>

<li>Analysis Menu – Analysis choices are grouped into aggregate analysis (statistics over all text within your time range) and term change analysis (daily statistics for each day in your time range).</li>
<ol> 
<li>	Aggregate mode – Analyze all text to get aggregate statistics</li>
	<ol>
<li>	Interactive Mode -- allows you to query search terms one at a time.  This will take some time on larger datasets.  This searches all the text within your date range and returns the number of occurrences of this term.</li>
<li>	Enter a query. Wait for response.  Repeat as desired.</li>
<li>	Press Q to quit.</li>
</ol>
<ol>
<li>	Query builtin lists – Several lists have been precompiled for analysis.</li>
<li>	Built-in lists can be modified by opening the nytExplorer script with a text editor, going to the <code>NYT Parser</code> Class Declaration, Finding the <code>__init__</code> function (at the top of the declaration), and then adding words to the lists as desired.</li>
<li>	Results will not be written to disk, only written to the console.</li>
</ol>
<li> Print aggregate statistics – print the number of articles analyzed, number of days in the analysis, the number of total words in the analysis and the number of unique words.</li>
<li> Find common phrases – search the text data for common phrases of 2- and 3- words.  (Works, but under development).</li>
<li> Quit Aggregate mode with ‘Q’ </li>
<li>	Term Change / Time series analysis</li>
<ol>
<li>	Change points – Possible points of interest based in the data.  Change points will be automatically calculated for each field you search for (i.e., “Russia” may have 2 change points, “Syria”4 change points, etc). </li>
<li>	Single Term – Interactive mode like in aggregate analysis mode.  Search for a single term.  The results will include graphs of occurrence over your time period, possible change points, and a csv of the results. The csv is automatically saved to disk at: <code>/Users/[Your Username]/Documents/NYTExplorer/term_change_analysis_[startString]_[endString].csv</code></li>
<li>	Graphics and Change points are in development, but work marginally well for now.</li>
<li>	List of Terms – Interactive mode to add terms to a list, and then see how those changes happen in relation to one another (i.e., put “Syria”, “Russia”, and “Hungary” all on a single graph and look at their relative rates of change.  </li>
<li>	Terms of built-in Europe Query – Query the European countries list (see above) and write the results to a csv.  Graphics are surpressed. Change points are analyzed.</li>
<li>	Terms of built-in Other Query – Query the Other query list (see above) and write the results to a csv.  Graphics are surpressed.  Change points are analyzed.</li>
<li>	Press Q to quit time series analysis.</li>
</ol>

<i>Implementation Strategies</i>
<i>Coming soon.<i>

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



##Built-in lists:

##European Countries (and other regionally important countries): 
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

##Culturally important queries
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

##Other Queries:
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
		






