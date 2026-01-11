import networkx as nx
from database.dao import DAO
import numpy as np

class Model:
    def __init__(self):
        self.G = nx.DiGraph()
        self._nodes = []
        self._edges = []

        self.id_map = {}
        self.soluzione_best = []

        self._lista_cromosomi = []
        self._lista_geni = []
        self._lista_geni_connessi = []

        self.load_geni()
        self.load_cromosomi()
        self.load_geni_connessi()

    def load_cromosomi(self):
        self._lista_cromosomi = DAO.get_cromosomi()

    def load_geni(self):
        self._lista_geni = DAO.get_geni()
        self.id_map = {}
        for g in self._lista_geni:
            self.id_map[g.id] = g.cromosoma

    def load_geni_connessi(self):
        self._lista_geni_connessi = DAO.get_geni_connessi()

    def build_graph(self):
        self.G.clear()

        self._nodes = []
        self._edges = []

        for c in self._lista_cromosomi:
            self._nodes.append(c)
        self.G.add_nodes_from(self._nodes)

        edges = {}
        for g1, g2, corr in self._lista_geni_connessi:
            if (self.id_map[g1], self.id_map[g2]) not in edges:
                edges[(self.id_map[g1], self.id_map[g2])] = float(corr)
            else:
                edges[(self.id_map[g1], self.id_map[g2])] += float(corr)
        for k, v in edges.items():
            self._edges.append((k[0], k[1], v))
        self.G.add_weighted_edges_from(self._edges)

    def ricerca_cammino(self, t):
        self.soluzione_best.clear()

        for n in self.get_nodes():
            partial = []
            partial_edges = []

            partial.append(n)
            self.ricorsione(partial, partial_edges, t)

        print("final", len(self.soluzione_best), [i[2]["weight"] for i in self.soluzione_best])

    def ricorsione(self, partial_nodes, partial_edges, t):
        n_last = partial_nodes[-1]
        neigh = self._get_admissible_neighbors(n_last, partial_edges, t)

        # stop
        if len(neigh) == 0:
            weight_path = self.compute_weight_path(partial_edges)
            weight_path_best = self.compute_weight_path(self.soluzione_best)
            if weight_path > weight_path_best:
                self.soluzione_best = partial_edges[:]
            return

        for n in neigh:
            print("...")
            partial_nodes.append(n)
            partial_edges.append((n_last, n, self.G.get_edge_data(n_last, n)))
            self.ricorsione(partial_nodes, partial_edges, t)
            partial_nodes.pop()
            partial_edges.pop()

    def _get_admissible_neighbors(self, node, partial_edges, soglia):
        result = []
        for u, v, data in self.G.out_edges(node, data=True):
            if data["weight"] > soglia:
                # controllo SOLO l'arco diretto
                if (u, v) not in [(x[0], x[1]) for x in partial_edges]:
                    result.append(v)
        return result

    def compute_weight_path(self, mylist):
        weight = 0
        for e in mylist:
            weight += e[2]['weight']
        return weight

    def count_edges(self, t):
        count_bigger = 0
        count_smaller = 0
        for x in self.get_edges():
            if x[2]['weight'] > t:
                count_bigger += 1
            elif x[2]['weight'] < t:
                count_smaller += 1
        return count_bigger, count_smaller

    def get_nodes(self):
        return self.G.nodes()

    def get_edges(self):
        return list(self.G.edges(data=True))

    def get_num_of_nodes(self):
        return self.G.number_of_nodes()

    def get_num_of_edges(self):
        return self.G.number_of_edges()

    def get_min_weight(self):
        return min([x[2]['weight'] for x in self.get_edges()])

    def get_max_weight(self):
        return max([x[2]['weight'] for x in self.get_edges()])