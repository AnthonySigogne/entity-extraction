# entity-extraction
API to extract entities from a text.

The goal is to identify the most important "concepts" of a text : companies, brands, people, places...
Each concept, or entity, is associated with additional data like the link to the Wikipedia page, an abstract or a photo.

This API uses the library DBPedia Spotlight : https://github.com/dbpedia-spotlight/dbpedia-spotlight.

## INSTALL
```
pip install -r requirements.txt
FLASK_APP=index.py flask run
```

To launch in debug mode :
```
FLASK_APP=index.py FLASK_DEBUG=1 flask run
```

## USAGE
To list all services of API, type this endpoint in your web browser : "http://localhost:5000/"
