# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 22:24:09 2019

@author: NickovicD
"""
from rtamt.node.stl.temporal_node import TemporalNode



class Until(TemporalNode):
    """
    A class for storing STL Since nodes
    Inherits TemporalNode
    """
    def __init__(self, child1, child2, bound):
        """Constructor for Since node

            Parameters:
                child1 : stl.Node
                child2 : stl.Node
                bound : Interval
        """
        super(Until, self).__init__(bound)
        self.addChild(child1)
        self.addChild(child2)

