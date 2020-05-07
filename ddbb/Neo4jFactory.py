from py2neo import Graph, Node, Relationship, NodeMatcher


class Neo4jFactory(object):
    def __init__(self):
        self.graph = Graph(password="300699")

    def close(self):
        self._driver.close()

    def insertarParaula(self, noticia, paraula, frequencia):
        matcher = NodeMatcher(self.graph)
        noticiarel = matcher.match("Noticia", title=noticia).first()
        paraulaInDB = matcher.match("Palabra", paraula=paraula).first()
        paraularel = Node("Palabra", paraula=paraula)

        tx = self.graph.begin()
        if paraulaInDB is None:
            tx.create(paraularel)
            ConteParaula = Relationship(paraularel, "ContienePalabra", noticiarel, frequencia=frequencia)
            tx.create(ConteParaula)
        else:
            ConteParaula = Relationship.type("ContienePalabra")
            tx.merge(ConteParaula(paraulaInDB, noticiarel, frequencia=frequencia))


        tx.commit()
        # tx.run("CREATE ($palabra:Palabra {name:'Noticia', content:'content'})", palabra=palabra)

    def insertarNoticia(self, noticia, retweets, propietari,plataforma):
        a = Node("Noticia", title=noticia, retweets=retweets)
        tx = self.graph.begin()
        tx.create(a)
        matcher = NodeMatcher(self.graph)
        redactorInDB = matcher.match("Redactor", redactor=propietari).first()
        redactorRel = Node("Redactor", redactor=propietari)

        plataformaInDB = matcher.match("Plataforma", plataforma=plataforma).first()
        plataformaRel = Node("Plataforma", plataforma=plataforma)

        if redactorInDB is None:
            redactadaPor = Relationship(a, "redactadaPor", redactorRel)
            tx.create(redactadaPor)
        else:
            redactadaPor = Relationship.type("redactadaPor")
            tx.merge(redactadaPor(a, redactorInDB))

        if plataformaInDB is None:
            disponibleEn = Relationship(a, "disponibleEn", plataformaRel)
            tx.create(disponibleEn)
        else:
            disponibleEn = Relationship.type("disponibleEn")
            tx.merge(disponibleEn(a, plataformaInDB))

        tx.commit()

    def insertarData(self, noticia, data):
        matcher = NodeMatcher(self.graph)
        noticiarel = matcher.match("Noticia", title=noticia).first()
        dataInDB = matcher.match("Fecha", data="{}-{}-{}".format(data.year, data.month, data.day)).first()
        dataRel = Node("Fecha", data="{}-{}-{}".format(data.year, data.month, data.day))
        tx = self.graph.begin()
        if dataInDB is None:
            tx.create(dataRel)
            publicadaEl = Relationship(dataRel, "publicadaEl", noticiarel)
            tx.create(publicadaEl)

            mesos = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Setiembre', 'Octubre',
                     'Noviembre', 'Diciembre']
            mesInDB = matcher.match("Anio", data="{} {}".format(mesos[data.month - 1], data.year)).first()
            mesRel = Node("MesAnio", data="{} {}".format(mesos[data.month - 1], data.year))
            if mesInDB is None:
                contiene = Relationship(mesRel, "contiene", dataRel)
                tx.create(contiene)
            else:
                contiene = Relationship.type("contiene")
                tx.merge(contiene(mesInDB, dataRel))
        else:
            publicadaEl = Relationship.type("publicadaEl")
            tx.merge(publicadaEl(dataInDB, noticiarel))
        tx.commit()

    def insertarComentari(self, noticia, comentari):
        matcher = NodeMatcher(self.graph)
        noticiarel = matcher.match("Noticia", title=noticia).first()
        tx = self.graph.begin()
        matcher = NodeMatcher(self.graph)
        comentariInDB = matcher.match("Comentario", comentario=comentari).first()
        comentariRel = Node("Comentario", comentario=comentari)
        if comentariInDB is None:
            tieneComoRespuesta = Relationship(noticiarel, "tieneComoRespuesta", comentariRel)
            tx.create(tieneComoRespuesta)
        else:
            tieneComoRespuesta = Relationship.type("tieneComoRespuesta")
            tx.merge(tieneComoRespuesta(noticiarel, comentariInDB))
        tx.commit()
