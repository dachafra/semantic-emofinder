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

#query bases
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
        FILTER(?tipoanotacion != emofind:EmotionalDimention)
        FILTER(?tipoanotacion != emofind:EmotionalCategory)
        FILTER(?tipoanotacion != emofind:OtherProperties)
        FILTER(?tipoanotacion != emofind:RecognitionTime)
  } 
  GROUP BY ?nombre ?articulo ?enlace
  ''',
      initNs = { "emofind": EMOFIND}
    )

#querys ejemplos
e1 = prepareQuery('''
    SELECT 
        ?nombre ?mediav 
    WHERE { 
        ?anotacion rdf:type emofind:Valence .
        ?anotacion emofind:affects ?palabra .
        ?anotacion emofind:mean ?mediav .
        ?palabra emofind:name ?nombre
        FILTER (LANG(?nombre) = "es")
        FILTER (?mediav > 8.5)
    } 
  ''',
      initNs = { "emofind": EMOFIND}
    )
e2 = prepareQuery('''
    SELECT 
        ?nombre ?valor_tdl ?valor_naming 
        WHERE { 
        ?anotacion1 rdf:type emofind:TimeTdl .
        ?anotacion1 emofind:affects ?palabra .
        ?anotacion1 emofind:value ?valor_tdl .
        FILTER (?valor_tdl > 570) .

        ?anotacion2 rdf:type emofind:TimeNaming .
        ?anotacion2 emofind:affects ?palabra .
        ?anotacion2 emofind:value ?valor_naming .
        ?palabra emofind:name ?nombre .
        FILTER (LANG(?nombre) = "es") .
        FILTER (?valor_naming < 490)
    
    }  
  ''',
      initNs = { "emofind": EMOFIND}
    )
e3 = prepareQuery('''
    SELECT 
        ?nombre ?media ?desviacion_tipica 
        WHERE { 
        ?anotacion rdf:type emofind:Anger .
        ?anotacion emofind:affects ?palabra .
        ?anotacion emofind:mean ?media .
        ?anotacion emofind:standarDeviation ?desviacion_tipica .
        ?palabra emofind:name ?nombre .
        FILTER (LANG(?nombre) = "es") .
        FILTER (?media < 1.5) .
        FILTER (?desviacion_tipica < 0.2) .


    } 
  ''',
      initNs = { "emofind": EMOFIND}
    )
e4 = prepareQuery('''
    SELECT 
        ?nombre ?media
        WHERE { 
        ?anotacion rdf:type emofind:ContextualAvailability .
        ?anotacion emofind:affects ?palabra .
        ?anotacion emofind:mean ?media .
        ?palabra emofind:name ?nombre .
        FILTER (LANG(?nombre) = "es") .
        FILTER (?media >= 3.5 && ?media <= 4 ) 

    
    }
  ''',
      initNs = { "emofind": EMOFIND}
    )
e5 = prepareQuery('''
    SELECT
        ?nombre ?articulo ?enlace
      WHERE { 
        ?base rdf:type emofind:WordDatabase .
        ?base emofind:name ?nombre .
        ?base emofind:article ?articulo .
        ?base emofind:articleLink ?enlace .
        FILTER (?nombre="guasch_2016"^^xsd:string)

  } 
  ''',
      initNs = { "emofind": EMOFIND}
    )
e6 = prepareQuery('''
    SELECT
        ?nombre (GROUP_CONCAT(distinct ?tipoanotacion; SEPARATOR = ", ") AS ?anotaciones)
      WHERE { 
        ?base rdf:type emofind:WordDatabase .
        ?base emofind:name ?nombre .
        ?anotacion rdf:type ?tipoanotacion .
        ?anotacion emofind:extractedFrom ?base .
        FILTER(?tipoanotacion != emofind:Annotation) #eliminar las clases de la jerarquía que no son las hojas
        FILTER(?tipoanotacion != emofind:EmotionalDimention)
        FILTER(?tipoanotacion != emofind:EmotionalCategory)
        FILTER(?tipoanotacion != emofind:OtherProperties)
        FILTER(?tipoanotacion != emofind:RecognitionTime)
  } 
  GROUP BY ?nombre
  ''',
      initNs = { "emofind": EMOFIND}
    )
e7 = prepareQuery('''
    SELECT DISTINCT
        ?nombre
        WHERE { 
        ?base rdf:type emofind:WordDatabase .
        ?base emofind:name ?nombre .
        ?anotacion rdf:type emofind:Sadness .
        ?anotacion emofind:extractedFrom ?base .
    } 
  ''',
      initNs = { "emofind": EMOFIND}
    )
e8 = prepareQuery('''
    SELECT 
        ?nombre ?media
        WHERE { 
        ?anotacion rdf:type emofind:Familiarity .
        ?anotacion emofind:affects ?palabra .
        ?anotacion emofind:mean ?media .
        ?palabra emofind:name ?nombre .
        FILTER (LANG(?nombre) = "es") .
        FILTER regex ( ?nombre, "^al")

    
    } 
  ''',
      initNs = { "emofind": EMOFIND}
    )
e9 = prepareQuery('''
    SELECT 
        ?nombre ?media
        WHERE { 
        ?anotacion rdf:type emofind:Arousal .
        ?anotacion emofind:affects ?palabra .
        ?anotacion emofind:mean ?media .
        ?palabra emofind:name ?nombre .
        FILTER (LANG(?nombre) = "es") .
        FILTER (?media > 5.0)
        FILTER regex ( ?nombre, "cla")

    
    } 
  ''',
      initNs = { "emofind": EMOFIND}
    )

app = FastAPI()

app.mount("/web", StaticFiles(directory="web"), name="web")
app.mount("/kg", StaticFiles(directory="kg"), name="kg")

@app.get("/")
async def index():
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



@app.get("/consulta_caracteristica")
async def consultaCaracteristica(param: str):
    qselect= "SELECT ?palabra ?base "
    qwhere= "WHERE { "
    qfilter= ""
    list = param.split("|")
    categorias = list[1].split(";")
    umbrales = {}

    #categorias y umbrales
    for i in range(len(categorias)-1):
        cati=categorias[i].split(":")
        if cati[0] == "TimeTdl" or cati[0] == "TimeNaming":
            qselect += "?caracteristica"+str(i)+" ?valor" + str(i) + " "
            qwhere += '''values ?caracteristica'''+str(i)+''' { "'''+cati[0]+'''" }
                        ?anotacion'''+str(i)+''' rdf:type emofind:'''+cati[0]+''' . 
                        ?anotacion'''+str(i)+''' emofind:affects ?pal . 
                        ?anotacion'''+str(i)+''' emofind:extractedFrom ?bas . 
                        ?anotacion'''+str(i)+''' emofind:value ?valor'''+str(i)+''' . 
                        '''
            catumbrales=cati[1].split("-")
            if len(catumbrales[0])>0:
                qfilter +=  '''FILTER(?valor'''+str(i)+''' > ?u'''+ str(len(umbrales))+''')
                        '''
                umbrales["u"+ str(len(umbrales))] = Literal(float(catumbrales[0]))
            if len(catumbrales[1])>0:
                qfilter +=  '''FILTER(?valor'''+str(i)+''' < ?u'''+ str(len(umbrales))+''')
                        '''
                umbrales["u"+ str(len(umbrales))] = Literal(float(catumbrales[1]))
        else:
            qselect += "?caracteristica"+str(i)+" ?media" + str(i) + " ?sd" + str(i) + " "
            qwhere += '''values ?caracteristica'''+str(i)+''' { "'''+cati[0]+'''" }
                        ?anotacion'''+str(i)+''' rdf:type emofind:'''+cati[0]+''' . 
                        ?anotacion'''+str(i)+''' emofind:affects ?pal . 
                        ?anotacion'''+str(i)+''' emofind:extractedFrom ?bas . 
                        ?anotacion'''+str(i)+''' emofind:mean ?media'''+str(i)+''' . 
                        ?anotacion'''+str(i)+''' emofind:standarDeviation ?sd'''+str(i)+''' . 
                        '''
            catumbrales=cati[1].split("-")
            if len(catumbrales[0])>0:
                qfilter +=  '''FILTER(?media'''+str(i)+''' > ?u'''+ str(len(umbrales))+''')
                        '''
                umbrales["u"+ str(len(umbrales))] = Literal(float(catumbrales[0]))
            if len(catumbrales[1])>0:
                qfilter +=  '''FILTER(?media'''+str(i)+''' < ?u'''+ str(len(umbrales))+''')
                        '''
                umbrales["u"+ str(len(umbrales))] = Literal(float(catumbrales[1]))
            if len(catumbrales[2])>0:
                qfilter +=  '''FILTER(?sd'''+str(i)+''' > ?u'''+ str(len(umbrales))+''')
                        '''
                umbrales["u"+ str(len(umbrales))] = Literal(float(catumbrales[2]))
            if len(catumbrales[3])>0:
                qfilter +=  '''FILTER(?sd'''+str(i)+''' < ?u'''+ str(len(umbrales))+''')
                        '''
                umbrales["u"+ str(len(umbrales))] = Literal(float(catumbrales[3]))
            
    qwhere += '''?pal emofind:name ?palabra . 
                ?bas emofind:name ?base .
                FILTER (LANG(?palabra) = "es")
                 
            '''
    
    #bases
    bases = list[2].split(";")
    filtrobases=""
    if len(bases)>1:
        filtrobases=" FILTER ("
        for i in range(len(bases)-1):
            if i == 0:
                filtrobases+= '?base="'+bases[i]+'"^^xsd:string '
            else:
                filtrobases+= '|| ?base="'+bases[i]+'"^^xsd:string '
        filtrobases+=") "
    qfilter += filtrobases

    #palabras
    palabras = list[0]
    if len(palabras)>1:
        for i in range(len(palabras.split("-"))-1):
            qfilter += ' FILTER regex ( ?palabra, "'+ palabras.split("-")[i] + '") '
    
    query=qselect+qwhere+qfilter+"}"
    q = prepareQuery(query, initNs = { "emofind": EMOFIND})

    #debug
    #for r in g.query(q, initBindings=umbrales):
    #    print(r.palabra, r.base, r.media0, r.sd0, r.media1, r.sd1)
    
    #obtener json
    res=g.query(q, initBindings=umbrales).serialize(format="json")
    if res!= None:
        return Response(content=res.decode("utf-8"),media_type="application/json")
    else:
        return Response(content={"message": "Fallo consulta"}, status_code=500)

@app.get("/consulta_base")
async def consultaBase():

    #obtener json
    res=g.query(q1).serialize(format="json")
    if res!= None:
        return Response(content=res.decode("utf-8"),media_type="application/json")
    else:
        return Response(content={"message": "Fallo consulta"}, status_code=500)
    
@app.get("/consulta_ejemplo")
async def consultaBase(param: int):
    res=None
    match param:
        case 1:
            #obtener json
            res=g.query(e1).serialize(format="json")
        case 2:
            #obtener json
            res=g.query(e2).serialize(format="json")
        case 3:
            #obtener json
            res=g.query(e3).serialize(format="json")
        case 4:
            #obtener json
            res=g.query(e4).serialize(format="json")
        case 5:
            #obtener json
            res=g.query(e5).serialize(format="json")
        case 6:
            #obtener json
            res=g.query(e6).serialize(format="json")
        case 7:
            #obtener json
            res=g.query(e7).serialize(format="json")
        case 8:
            #obtener json
            res=g.query(e8).serialize(format="json")
        case 9:
            #obtener json
            res=g.query(e9).serialize(format="json")

    if res!= None:
        return Response(content=res.decode("utf-8"),media_type="application/json")
    else:
        return Response(content={"message": "Fallo consulta"}, status_code=500)
  
    