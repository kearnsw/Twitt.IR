# Twitter

Firehose.py opens the connection with Twitter streaming API and saves tweets both to JSON and MongoDB.
The program takes as input the query and output file (optional MongoDB storage default=Virus) for storage
e.g. 
`python Firehose.py "Zika" zika.json Virus`

The shell script firehose.sh will run this script and restart the script even if there is an interruption
in the connection with the Twitter API on any level, e.g.
`path/to/file/firehose.sh "Zika" zika.json`

Load.py takes two arguments the database and collection to be searched and returns all tweets in English this
is customizable through modifying the configuration file. The collection name should be the same as the query
term out of the box.
`python Load.py Virus Zika`
