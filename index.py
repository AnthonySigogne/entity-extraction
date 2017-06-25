#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
API to extract entities from a text.
The goal is to identify the most important "concepts" of a text : companies, brands, people, places...
Each concept, or entity, is associated with additional data like the link to the Wikipedia page, an abstract or a photo.
This API uses the library DBPedia Spotlight : https://github.com/dbpedia-spotlight/dbpedia-spotlight.
"""

__author__ = "Anthony Sigogne"
__copyright__ = "Copyright 2017, Byprog"
__email__ = "anthony@byprog.com"
__license__ = "MIT"
__version__ = "1.0"

# libraries of tool
import subprocess
import json
from SPARQLWrapper import SPARQLWrapper, JSON
from collections import Counter
from flask import Flask, request, jsonify, url_for, render_template
app = Flask(__name__)


@app.route("/entities", methods=['POST'])
def entity_extraction():
    """
    URL : /entities
    Extract entities (Company, Place,...) from a text.
    Method : POST
    Form data :
        - text : the text to analyze
        - lang : language of text ("fr" or "en")
    Return a JSON dictionary with one key : {"entities":[list of entities]}
    """
    def query_dbpedia(entity, lang) :
        """
        Query DBPedia to get more data about entity.
        """
        # compute entity type from dbpedia types
        dbtype = u"Entity"
        if "Schema:Place" in entity["@types"] :
            dbtype = u"Place"
        elif "Schema:Person" in entity["@types"] :
            dbtype = u"Person"
        elif "DBpedia:Company" in entity["@types"] :
            dbtype = u"Company"

        # create a new entity structure
        entity = {"uri":entity["@URI"], "dbtype":dbtype}

        # query dbpedia for more information about entity
        sparql = SPARQLWrapper("http://%sdbpedia.org/sparql"%("fr." if lang == "fr" else ""))
        sparql.setQuery(u"""
            prefix db-owl: <http://dbpedia.org/ontology/>
            select * where
            {
             ?uri <http://dbpedia.org/ontology/wikiPageID> ?id.
             FILTER (?uri = <%s>)
             OPTIONAL {?uri db-owl:thumbnail ?photo}
             ?uri <http://www.w3.org/ns/prov#wasDerivedFrom> ?wiki.
             ?uri rdfs:label ?label.
             OPTIONAL{?uri db-owl:abstract ?abstract.
             FILTER (LANG(?abstract) = "%s").}
             FILTER (LANG(?label) = "%s")
            }
        """%(entity["uri"],lang,lang))
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        res = results["results"]["bindings"][0]
        entity.update({
            "label":res["label"]["value"],
            "wiki":res["wiki"]["value"],
            "photo":res["photo"]["value"].replace("width=300","width=50") if "photo" in res else None,
            "abstract":res["abstract"]["value"][:150]+"..." if "abstract" in res else None
        })

        return entity

    # get POST data
    data = dict((key, request.form.get(key)) for key in request.form.keys())
    data["content"] = data["content"][:7000] # limit text content to 7000 characters

    # get entities with dbpedia spotlight tool
    port = 2225 if data["language"] == "fr" else 2222
    confidence = 0.3 if data["language"] == "fr" else 0.5
    res = subprocess.check_output(["curl","http://spotlight.sztaki.hu:%d/rest/annotate"%port,'--data-urlencode',"text=%s"%data["content"].encode("utf8"),'--data',"confidence=%f"%confidence,'-H',"Accept: application/json"])

    # browse entities and get dbpedia data
    entities = []
    for entity in json.loads(res.decode("utf8")).get("Resources",[]) :
        if float(entity["@similarityScore"]) > 0.92 : # only entities with high similarity score
            entities.append(query_dbpedia(entity, data["language"]))

    return jsonify(entities=entities)

@app.route("/")
def helper():
    """
    URL : /
    Helper that list all methods of tool.
    Return a simple text.
    """
    # print module docstring
    output = [__doc__.replace("\n","<br/>"),]

    # then, get and print docstring of each rule
    for rule in app.url_map.iter_rules():
        if rule.endpoint == "static" : # skip static endpoint
            continue
        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)
        methods = ','.join(rule.methods)
        output.append(app.view_functions[rule.endpoint].__doc__.replace("\n","<br/>"))

    return "<br/>".join(output)
