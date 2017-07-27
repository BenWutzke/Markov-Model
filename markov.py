# -*- coding: utf-8 -*-

import random
import numpy as np
import itertools
from functools import reduce
from operator import mul
from graph_utils import draw_graph, NchooseK

class Markov(object):
   """
   Graph based Markov model.  Instead of encoding transition probabilities
   in a matrix, we encode them in a hash to save space.
   """
   def __init__(self, nodes = None,
                node_emissions = None,
                sequences = [],
                sequence_probs = [],
                node_cnx = None,
                edge_labels = None
                ):
      self.nodes = nodes
      self.node_emissions = node_emissions
      self.sequences = sequences
      self.sequence_probs = sequence_probs
      self.node_cnx = node_cnx
      self.edge_labels = edge_labels
      
   def get_node_cnx(self):
      """
      Returns node connections hash if it exists.
      Creates random node connection if it does not exist
      To set node_connection yourself, use instance assignment for node_cnx
      instance.node_cnx = {N1:[(Nm,Pn1->nm),()],N2:[(),()],...}
      """
      if self.nodes:
         k = len(self.nodes)/2
         if not self.node_cnx:
            self.node_cnx = {node:[map(None,NchooseK(self.nodes,random.randint(1,k)),
                                       np.random.dirichlet(np.ones(k),size=1)[0].tolist())] for node in self.nodes}
            for key in self.node_cnx:
               if sum([v[1] for v in self.node_cnx[key]]) < 1:
                  self.node_cnx[key].append((key,1-sum([v[1] for v in self.node_cnx[key]])))
                  
         return self.node_cnx
      
      print("Please create nodes or generate random model.")
      
   def get_node_emissions(self,emission_range=[0,10],emission_ceiling=1):
      """
      Returns node emission hash if it exists.
      Creates random node emission hash if it does not exist.
      To set node_emission yourself, use instance assignment for node_emissions.
      instance.node_emissions = {N1:[E1,E2,...],N2:[En,..Em],...}
      """
      if self.nodes:
         if not self.node_emissions:
            self.node_emissions = {node:[random.randint(emission_range[0],emission_range[1]) for _ in range(emission_ceiling)] for node in self.nodes}
            
         return self.node_emissions
      print("Please create nodes or generate random model")
      
   def get_sequenceprob(self,seq):
      """
      Returns the probability of observing a sequence "seq"
      """
      seq_prob = []
      for i in range(len(seq)-1):
         if not self.node_cnx[seq[i]]:
            return 0
         body = self.node_cnx[seq[i]]
         seq_prob += [f[1] for f in body if f[0] == seq[i+1]]
         
      return (seq,reduce(mul,seq_prob,1))
   
   def get_all_sequence_prob(self):
      """
      Returns all sequences in the sequences attribute, zipped with their probabilities.
      Ordered from lowest prop to highest prob.
      """
      temp = []
      for s in self.sequences:
         temp.append(self.get_sequenceprob(s))
      self.sequence_probs = sorted(temp,key=lambda tup: tup[1])
      return sorted(self.sequence_probs,reverse = True)
   
   def get_sequences(self,start_node,seq_len,current_sequence = []):
      """
      Returns all possible sequences that begin at 'start_node' and
      are of length 'seq_len'.
      """
      if seq_len < 1:
         return
      current_sequence +=[start_node]
      if seq_len == 1:
         self.sequences.append(current_sequence)
         return
      if seq_len > 1:
         for k in [f[0] for f in self.node_cnx[start_node]]:
            temp_sequence = [f for f in current_sequence]
            self.get_sequences(k,seq_len-1,temp_sequence)
            
            
   def random_model_init(self,cnx):
      """
      Initializes a markov model with random node connections and
      node emissions.
      """
      k = min(cnx,len(self.nodes))
      if not self.node_emissions:
         self.node_emissions = {node:random.randint(0,10) for node in self.nodes}
      if not self.node_cnx:
         self.node_cnx = {node: list(zip(NchooseK(self.nodes,random.randint(1,k)),
                                    np.random.dirichlet(np.ones(k),size=1)[0].tolist())) for node in self.nodes}
         
   
   def show(self,export=False):
      """
      Display a graph of the Markov Model.
      """
      graph = [(node,val[0]) for node in self.node_cnx for val in self.node_cnx[node]]
      edge_labels = [round(val[1],2) for node in self.node_cnx for val in self.node_cnx[node]]
      draw_graph(graph,labels=edge_labels,export=export)
      
def main():
   a=Markov()
   a.nodes = ['a','b','c','d','e','f','g']
   a.random_model_init(3)
   a.show()
   for node in a.node_cnx.keys():
      print(node,":  ",a.node_cnx[node])
      
   print('\n')
   a.get_sequences(list(a.node_cnx.keys())[0],5)
   print(a.sequences)
   a.get_all_sequence_prob()
   print('\n')
   print(a.sequence_probs)
   
   return a
   
if __name__=='__main__':
   a=main()
   
      
   
      
   
