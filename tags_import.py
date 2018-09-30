import json
from app.models import Tags
from app import db

tags_file = open('tags.json', 'r')
tag_file = json.load(tags_file)


for tag in tag_file:
	data = Tags(symbol=tag['symbol'],
		name=tag['name'],
		example=tag['example'])
	db.session.add(data)
	db.session.commit()