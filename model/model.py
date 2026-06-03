import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._idMapC = {}
        pass

    def getAllYears(self):
        return DAO.getAllYears()

    def buildGraph(self, a1, a2):
        self._graph.clear()
        nodi = DAO.getAllNodes(a1, a2)
        self._graph.add_nodes_from(nodi)
        for n in nodi:
            self._idMapC[n.constructorId]= n
        archi = DAO.getAllEdges(a1, a2)
        for a in archi:
            u = self._idMapC[a[0]]
            v = self._idMapC[a[1]]
            self._graph.add_edge(u, v, weight= a[2])
    def getDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getBestArchi(self):
        archi = list(self._graph.edges(data=True))
        archi.sort(key=lambda x: x[2]["weight"], reverse=True)
        return archi[0:3]

    def getNumCompConnesse(self):
        compConn = nx.number_connected_components(self._graph)
        return compConn

    def getBestComp(self):
        return max(nx.connected_components(self._graph), key=len)

    def getBestDecresc(self):
        largest_cc = max(nx.connected_components(self._graph), key=len)
        pilTuple = []
        for n in largest_cc:
            grado = self._graph.degree(n)
            pilTuple.append((n, grado))
        pilTuple.sort(key=lambda x: x[1], reverse=True)
        return pilTuple

