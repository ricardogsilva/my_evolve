#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Evolution experiences.
"""

import numpy as np

def first_characteristic_mutation(parentA, parentB):
    return parentA + parentB

def second_characteristic_mutation(parentA, parentB):
    return parentA - parentB

class Characteristic(object):

    def __init__(self, value):
        
        self.rank = value

    def __add__(self, otherObject):
              % (self.rank, otherObject.rank))
        self.rank += otherObject.rank


class Color(Characteristic):

    def __init__(self, color, rank):
        super(Color, self).__init__(rank)
        self.color = color

    @property
    def value(self):
        return self.color

    def __add__(self, otherObject):
        super(Color, self).__add__(otherObject)
        try:
            self.color += otherObject.color
        except TypeError:
            self.color = None

    def __repr__(self):
        return "%s(color=%r, rank=%r)" \
                % (self.__class__.__name__, self.color, self.rank)


class Length(Characteristic):

    def __init__(self, length, rank):
        super(Length, self).__init__(rank)
        self.length = length

    @property
    def value(self):
        return self.length

    def __add__(self, otherObject):
        super(Length, self).__add__(otherObject)
        try:
            self.length += otherObject.length
        except TypeError:
            self.length = None


    def __repr__(self):
        return "%s(length=%r, rank=%r)" \
                % (self.__class__.__name__, self.length, self.rank)

class BBing(object):

    matingSuccessThreshold = 0.2 # lower value means higher mating probability
    mutationThreshold = 0.2 # lower value means higher mutation probability
    deadlyMutation = 1 - ((1 - mutationThreshold) / 8)
    charMutations = [
            first_characteristic_mutation,
            #second_characteristic_mutation,
            ]
    allowedCharacteristics = [Color, Length]

    def __init__ (self, characteristics):
        self.characteristics = []
        for char in characteristics:
            if True in [isinstance(char, ac) for ac in self.allowedCharacteristics]:
                self.characteristics.append(char)
            else:
                pass # could raise an error

    def mate(self, otherParent=None):
        print("mate method called.")
        if otherParent is None:
            otherParent = self
        successProb = np.random.random()
        print("successProb: %s" % successProb)
        if successProb >= self.matingSuccessThreshold:
            print("mating successful")
            offspringChars = []
            for charMother, charFather in zip(self.characteristics,
                                              otherParent.characteristics):
                print("charMother: %s\tcharFather:%s" % (charMother, charFather))
                mutationProbability = np.random.random()
                print("mutationProbability: %s" % mutationProbability)
                if mutationProbability >= self.mutationThreshold:
                    # there will be a mutation
                    print("mutation warning!")
                    if mutationProbability > self.deadlyMutation:
                        # this mutation is deadly
                        print("deadly mutation! (ignored for the moment)")
                    else:
                        #try:
                        nChar = self._get_new_char(charMother, charFather)
                        print("nChar: %s" % nChar)
                        #except:
                        #    pass
                        offspringChars.append(nChar)
                else:
                    if charMother.rank >= charFather.rank:
                        offspringChars.append(charMother)
                    else:
                        offspringChars.append(charFather)
            newBorn = BBing(offspringChars)
        else:
            print("mating unsuccessfull...")
            newBorn = None
        return newBorn

    def _get_new_char(self, cMother, cFather):
        print("_get_new_char method called.")
        charFuncIdx = np.random.random_integers(0, len(self.charMutations) - 1)
        print("charFunction: %s" % self.charMutations[charFuncIdx])
        newChar = self.charMutations[charFuncIdx](cMother, cFather)
        print("_get_new_char method exiting.")
        return newChar

    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, self.characteristics)


