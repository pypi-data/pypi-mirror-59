# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 20:32:57 2019

@author: NickovicD
"""

import logging
from rtamt.spec.stl.specification import STLSpecification
from rtamt.spec.stl.io_type import IOType
from rtamt.spec.io_stl.evaluator import STLIOEvaluator


class STLIOSpecification(STLSpecification):
    """A class used as a container for IO-Aware STL specifications
       Inherits STLSpecification

    Attributes:
        iosem : String

        in_vars : set(String) - set of input variable names
        out_vars : set(String) - set of out variable names
    """
    def __init__(self):
        """Constructor for STL Specification"""
        super(STLIOSpecification, self).__init__()
        self.iosem = 'standard'
        self.in_vars = set()
        self.out_vars = set()


    def parse(self):
        super(STLIOSpecification, self).parse()
        # Initialize the evaluator
        self.evaluator = STLIOEvaluator(self.var_object_dict, self)
        self.top.accept(self.evaluator)

    @property
    def iosem(self):
        return self.__iosem

    @iosem.setter
    def iosem(self, iosem):
        self.__iosem = iosem

    @property
    def in_vars(self):
        return self.__in_vars

    @in_vars.setter
    def in_vars(self, in_vars):
        self.__in_vars = in_vars

    @property
    def out_vars(self):
        return self.__out_vars

    @out_vars.setter
    def out_vars(self, out_vars):
        self.__out_vars = out_vars

    def visitVariableDeclaration(self, ctx):
        super(STLIOSpecification, self).visitVariableDeclaration(ctx)
        var_name = ctx.identifier().getText()
        var_iotype = IOType.UNDEFINED
        # If 'var' is input, add to the set of input vars
        # If 'var' is output, add to the set of output vars
        if (not ctx.ioType() is None):
            if (not ctx.ioType().Input() is None):
                var_iotype = IOType.INPUT
            elif (not ctx.ioType().Output() is None):
                var_iotype = IOType.OUTPUT
        self.set_var_io_type(var_name, var_iotype)

    def set_var_io_type(self, var_name, var_iotype):
        if not var_name in self.vars:
            logging.warning('The variable {} does not exist'.format(var_name))
        else:
            if var_iotype == IOType.INPUT:
                self.add_input_var(var_name)
                self.remove_output_var(var_name)
            elif var_iotype == IOType.OUTPUT:
                self.add_output_var(var_name)
                self.remove_input_var(var_name)
            else:
                self.remove_input_var(var_name)
                self.remove_output_var(var_name)

    def add_input_var(self, input_var):
        self.in_vars.add(input_var)

    def remove_input_var(self, var):
        self.in_vars.discard(var)

    def add_output_var(self, output_var):
        self.out_vars.add(output_var)

    def remove_output_var(self, var):
        self.out_vars.discard(var)





