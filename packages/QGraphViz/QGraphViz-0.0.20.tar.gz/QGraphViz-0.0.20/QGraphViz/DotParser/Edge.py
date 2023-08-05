#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Saifeddine ALOUI
Description:
Dot perser implementation
"""

class Edge():
    """
    Describes edges that connect nodes
    """
    def __init__(self, source, dest):
        self.source = source
        self.dest = dest

        source.out_edges.append(self)
        dest.in_edges.append(self)

    
