# guardian-content
A simple web scraper for querying articles from The Guardian using their API

Requests for articles containing keywords, passed by the command line, are made using the content endpoint. 
Article information returned is formatted and saved to an excel file.


To use you must first register for an API key from The Guardian [here](https://open-platform.theguardian.com/access/)

Once you have an API key, to run the script you will need to save your API key to a file named 'key.txt' at the same level as the script 
Run the script from the console using `python GuardianContent.py <Your query content>` for example to get information on articles about Italy and pasta: `python GuardianContent.py Italy AND pasta`

You can find more information on how to format your query string [here](https://open-platform.theguardian.com/documentation/search)
