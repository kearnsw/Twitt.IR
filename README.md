# Twitt.IR an Information Retreival tool for Twitter API using MongoDB and Instaparser API

This is an alpha release of Twitt.IR a package that queries the Twitter firehose and stores the selected tweets into MongoDB. Twitt.IR then provides functions for sampling from Mongo and extracting contextual information from the tweets using Instaparser API. 

#Firehose
Firehose.py opens the connection with Twitter streaming API and saves tweets both to JSON and MongoDB.
The program takes as input the query and output file (optional MongoDB storage default=Virus) for storage
e.g. 
`python Firehose.py "search_term" "output_file" "db_name"`
By default the start time of the stream is appended to the file name to reduce risk of data loss and for
identification purposes. OAuth information required by twitter should be stored in config file.

The shell script firehose.sh will run this script and restart the script even if there is an interruption
in the connection with the Twitter API on any level, e.g.
`path/to/Twitt.IR/firehose.sh "search_term" "output_file"`

#Sample
createSample.py is used to create samples for annotation and testing. Given a database and collection, this program returns a filtered collection of tweets from a given day which removes duplicates. 
`python createSample.py "db_name" "collection_name" "Apr 12"`

For convenience this can be called from the top level directory:
`path/to/Twitt.IR/sample.sh "db_name" "collection_name" "date"`

#Classify
Classify.py trains four classifiers, i.e. Humor, Mistrust, Relief, and Concern from the data within the /data/train/ directory. The program then applies these classifiers to a given dataset in the /data/ directory.
`path/to/Twitt.IR/classify.sh "data_to_be_classified"`

#Visualization Interface
The visual interface for contextualizing the data can be accessed at http://localhost:2112/ by running:
`python path/to/Twitt.IR/src/server.py`



