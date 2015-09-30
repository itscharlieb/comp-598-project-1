----------
Structure:
----------
	- hacker.py:
		This file is used to call the HackerNews API (https://github.com/HackerNews/API)
		and to grab 2 types of data: stories and users. It creates json files in a folder called "data".
	- datahacker.py:
		This file is used to parse the json result we got from the HackerNews API, and extract features from each story.
		In this file, we also create the final CSV file with the new data and all the features.
	- urlhacker.py:
		This is where we tried to parse URLs and get more features from the HTML content,
		but our Alchemy API account wasn't sufficient to do 21,000 queries.
	- learner.py:
		This is where we implemented the regression algorithms.
		First, we have a function that reads the data from a given CSV file and create an array of tupple (each tuple being information regarding one example).
		We then have functions for closed-form regression, k-fold cross validation, and gradient descent.
	- project1.py:
		This is the file to run in order to test and see our algorithms in action.


-------------
Requirements:
-------------

Python
	csv
	json
	numpy
	nltk
	gensim

-------------------------------------
To install required python libraries:
-------------------------------------
>> sudo pip install csv, json, numpy

-------------------
To run the program:
-------------------
>> python project1.py


