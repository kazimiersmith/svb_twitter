#!/bin/zsh
#
set -e
set -x

twitter_data=~/Dropbox/sivb/data/in/twitter
cd $twitter_data

start_date=2023-02-28
end_date=2023-03-11

for tag in SVB SBNY FRC
do
	#snscrape --jsonl --since $start_date twitter-hashtag $tag > hashtag_$tag.json
	#snscrape --jsonl --since $start_date twitter-cashtag $tag > cashtag_$tag.json
	snscrape --jsonl twitter-search "(#$tag) since:$start_date until:$end_date" > search_$tag.json
done
