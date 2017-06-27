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

To list all services of API, type this endpoint in your web browser : "http://localhost:5000/".

## USAGE AND EXAMPLE
The example below shows how to extract entities from an English text with cURL :
```
curl http://localhost:5000/entities --data-urlencode "text=Ennio Morricone, né le 10 novembre 1928 à Rome (Italie), est un compositeur, producteur et chef d'orchestre italien." --data "language=fr"
```

The result is a list of entities in a JSON dictionary :
```
{
  "entities": [
    {
      "abstract": "Ennio Morricone (n\u00e9 le 10 novembre 1928 \u00e0 Rome) est un compositeur et chef d'orchestre italien, r\u00e9put\u00e9 notamment pour ses musiques de films, en partic...",
      "dbtype": "Person",
      "label": "Ennio Morricone",
      "photo": "http://commons.wikimedia.org/wiki/Special:FilePath/Ennio_Morricone_Cannes_2012.jpg?width=50",
      "uri": "http://fr.dbpedia.org/resource/Ennio_Morricone",
      "wiki": "http://fr.wikipedia.org/wiki/Ennio_Morricone?oldid=110641314"
    },
    {
      "abstract": "Le 10 novembre est le 314e jour de l'ann\u00e9e  du calendrier gr\u00e9gorien, le 315e en cas d'ann\u00e9e bissextile. Il reste 51 jours avant la fin de l'ann\u00e9e.C'\u00e9t...",
      "dbtype": "Entity",
      "label": "10 novembre",
      "photo": null,
      "uri": "http://fr.dbpedia.org/resource/10_novembre",
      "wiki": "http://fr.wikipedia.org/wiki/10_novembre?oldid=111009910"
    },
    {
      "abstract": "Rome (en italien Roma, prononc\u00e9 [\u02c8ro\u02d1ma\u2006]) est la capitale de l'Italie depuis 1871. Situ\u00e9e au centre-ouest de la p\u00e9ninsule italienne, sur les c\u00f4tes de...",
      "dbtype": "Place",
      "label": "Rome",
      "photo": "http://commons.wikimedia.org/wiki/Special:FilePath/Collage_Rome.jpg?width=50",
      "uri": "http://fr.dbpedia.org/resource/Rome",
      "wiki": "http://fr.wikipedia.org/wiki/Rome?oldid=110475933"
    },
    {
      "abstract": null,
      "dbtype": "Place",
      "label": "Italie",
      "photo": "http://commons.wikimedia.org/wiki/Special:FilePath/Flag_of_Italy.svg?width=50",
      "uri": "http://fr.dbpedia.org/resource/Italie",
      "wiki": "http://fr.wikipedia.org/wiki/Italie?oldid=111025098"
    },
    {
      "abstract": "Un compositeur de musique (couramment d\u00e9nomm\u00e9 compositeur) (du latin compositum, supin signifiant \u00ab pour composer \u00bb du verbe componere) est un musicie...",
      "dbtype": "Entity",
      "label": "Compositeur",
      "photo": "http://commons.wikimedia.org/wiki/Special:FilePath/Louis-Nicolas_Clerambault.jpg?width=50",
      "uri": "http://fr.dbpedia.org/resource/Compositeur",
      "wiki": "http://fr.wikipedia.org/wiki/Compositeur?oldid=107179123"
    },
    {
      "abstract": "Un chef d'orchestre est un musicien charg\u00e9 de coordonner le jeu des instrumentistes des orchestres symphoniques, de jazz, d'harmonie ou de fanfare. Sa...",
      "dbtype": "Entity",
      "label": "Chef d'orchestre",
      "photo": "http://commons.wikimedia.org/wiki/Special:FilePath/Charles_Lamoureux.png?width=50",
      "uri": "http://fr.dbpedia.org/resource/Chef_d'orchestre",
      "wiki": "http://fr.wikipedia.org/wiki/Chef_d'orchestre?oldid=109128433"
    }
  ]
}
```

## NOTE
This API works with Python2 and Python3.

## DOCKER
To build this API for Docker :
```
docker build -t <name> .
```

To run the Docker container :
```
docker run -p <port>:5000 <name>
```
