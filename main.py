from fastapi import FastAPI
from fastapi import Response
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from rdflib import Graph, Namespace, Literal
from rdflib.plugins.sparql import prepareQuery

storage = "kg/emofinder_kg.nt" 

g = Graph()

g.parse(storage, format="ntriples") 

EMOFIND = Namespace("https://www.usc.gal/pcc/app/emofinder/") 

app = FastAPI()

app.mount("/web", StaticFiles(directory="web"), name="web")
app.mount("/kg", StaticFiles(directory="kg"), name="kg")

@app.get("/")
async def index():
    # Return the search page
    return FileResponse("web/search.html", media_type="text/html")

@app.get("/search.html")
async def search():
    # Return the search page
    return FileResponse("web/search.html", media_type="text/html")

@app.get("/bases.html")
async def bases():
    # Return the bases page
    return FileResponse("web/bases.html", media_type="text/html")

@app.get("/examples.html")
async def examples():
    # Return the examples page
    return FileResponse("web/examples.html", media_type="text/html")

@app.get("/consulta_base")
async def consultaBase():

    #query
    q1 = prepareQuery('''
  SELECT
        ?nombre ?articulo ?enlace (GROUP_CONCAT(distinct ?tipoanotacion; SEPARATOR = ", ") AS ?anotaciones)
      WHERE { 
        ?base rdf:type emofind:WordDatabase .
        ?base emofind:name ?nombre .
        ?base emofind:article ?articulo .
        ?base emofind:articleLink ?enlace .
        ?anotacion rdf:type ?tipoanotacion .
        ?anotacion emofind:extractedFrom ?base .
        FILTER(?tipoanotacion != emofind:Annotation)
  } 
  GROUP BY ?nombre ?articulo ?enlace
  ''',
      initNs = { "emofind": EMOFIND}
    )
    
    #obtener json
    res=g.query(q1).serialize(format="json")
    if res!= None:
        return Response(content=res.decode("utf-8"),media_type="application/json")
    else:
        return {"message": "Fallo consulta"}
  
    