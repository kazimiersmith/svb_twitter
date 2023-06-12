#!/bin/zsh
#
set -e
set -x

twitter_data=~/Dropbox/sivb/data/in/twitter
cd $twitter_data

start_date=2023-02-28

for tag in SVB SBNY FRC
do
	snscrape --jsonl --since $start_date twitter-hashtag $tag > hashtag_$tag.json
	snscrape --jsonl --since $start_date twitter-cashtag $tag > cashtag_$tag.json
done
