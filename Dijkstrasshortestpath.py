#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
from csv import reader
from csv import DictReader


# In[2]:


source = input("enter source: ")
destination =input("enter destination: ")


# In[3]:


from collections import defaultdict

class Graph():
    def __init__(self):
        self.edges = defaultdict(list)
        self.weights = {}
    
    def add_edge(self, from_node, to_node, weight):
        # Note: assumes edges are bi-directional
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)
        self.weights[(from_node, to_node)] = weight
        self.weights[(to_node, from_node)] = weight


# In[4]:


graph = Graph()


# In[5]:


with open('data.csv', 'r') as read_obj:
    csv_dict_reader = DictReader(read_obj)
    Average = 60
    for row in csv_dict_reader:
        Distance = int(row['distance'])
        Percentage = int(row['traffic percentage'])
        Decreased_speed = Average * (Percentage/100)
        Actual_speed = Average - Decreased_speed
        Total_time = Distance / Actual_speed
        Total_time = int(Total_time * 60)
        print("Source         Destination        Distance     Average Speed    Reduced speed    Actual speed    time")
        print("{}      {}       {}           {}             {}             {}             {}".format(row['from'], row['to'],Distance,Average,Decreased_speed,Actual_speed,Total_time))
        graph.add_edge(row['from'], row['to'], Total_time)


# In[6]:


def dijsktra(graph, initial, end):
    # shortest paths is a dict of nodes
    # whose value is a tuple of (previous node, weight)
    shortest_paths = {initial: (None, 0)}
    current_node = initial
    visited = set()
    
    while current_node != end:
        visited.add(current_node)
        destinations = graph.edges[current_node]
        weight_to_current_node = shortest_paths[current_node][1]

        for next_node in destinations:
            weight = graph.weights[(current_node, next_node)] + weight_to_current_node
            if next_node not in shortest_paths:
                shortest_paths[next_node] = (current_node, weight)
            else:
                current_shortest_weight = shortest_paths[next_node][1]
                if current_shortest_weight > weight:
                    shortest_paths[next_node] = (current_node, weight)
        
        next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}
        if not next_destinations:
            return "Route Not Possible"
        # next node is the destination with the lowest weight
        current_node = min(next_destinations, key=lambda k: next_destinations[k][1])
    
    # Work back through destinations in shortest path
    path = []
    total=0
    while current_node is not None:
        path.append(current_node)
        #print(current_node)
        next_node = shortest_paths[current_node][0]
        if next_node is not None:
            print("from : {} , to : {} , Time : {} minutes".format(next_node,current_node,graph.weights[(next_node, current_node)]))
            total = total+graph.weights[(next_node, current_node)]
        current_node = next_node
    # Reverse path
    print("Total Time = {} minutes".format(total))
    path = path[::-1]
    return path


# In[7]:


dijsktra(graph, source, destination)


# In[8]:


path1=dijsktra(graph, source, destination)


# In[9]:


print('Source : '+path1[0])
for x in range(len(path1)): 
    if x != 0 and x != len(path1)-1:
        print(path1[x])
print('Destination : '+path1[len(path1)-1])




