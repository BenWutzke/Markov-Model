# -*- coding: utf-8 -*-
"""
Created on Wed Jul 26 18:37:04 2017

@author: voodo
"""

import networkx as nx
import matplotlib.pyplot as plt
import datetime
import copy
import random

def NchooseK(A,k):
   ot = []
   n = copy.deepcopy(A)
   for _ in range(k):
      q = random.choice(n)
      ot = ot+[q]
      n.remove(q)
   return ot
def draw_graph(graph,export=None,labels=None,graph_layout='random',
               node_size = 1800,node_color = 'blue',node_alpha=0.3,
               node_text_size = 14,
               edge_color = 'blue',edge_alpha = 0.3,edgethickness = 1,
               edge_text_pos = 0.5,text_font='sans=serif'):
   
   G = nx.DiGraph()
   for edge in graph:
      G.add_edge(edge[0],edge[1])
      
   if graph_layout == 'spring':
      graph_pos = nx.spring_layout(G)
   elif graph_layout == 'spectral':
      graph_pos = nx.spectral_layout(G)
   elif graph_layout == 'random':
      graph_pos = nx.random_layout(G)
   else:
      graph_pos=nx.shell_layout(G)
      
   nx.draw_networkx_nodes(G,graph_pos,node_size=node_size,
                          alpha=node_alpha,node_color=node_color)
   nx.draw_networkx_edges(G,graph_pos,width=edgethickness,
                          alpha = edge_alpha,color = edge_color,arrows = True)
   nx.draw_networkx_labels(G,graph_pos,font_size=node_text_size,font_family=text_font)
   
   if labels is None:
      labels = range(len(graph))
      
   edge_labels = dict(zip(graph,labels))
   nx.draw_networkx_edge_labels(G,graph_pos,edge_labels=edge_labels,
                                label_pos=edge_text_pos)
   
   plt.show()
   
   if export:
      plt.savefig(''+datetime.datetime.strftime(datetime.datetime.now(),'%m-%d-%Y') + '.png')