from pq import *

'''Inheriting the Priority Queue class and Element class as a foundation for building 
the Adaptable Priority Queue'''
class Element(Element):
    def __init__(self, key, value, index):
        super().__init__(key, value)
        self.index = index

    def __str__(self):
        outstr = "(%i, %i (%i))" % (self.key, self.value, self.index)
        return outstr
    
    def wipe(self):
        self.key = None
        self.value = None
        self.index = None

class APQ(Heap):

    def __init__(self):
        super().__init__()

    def add(self, key, value):
        self.size += 1
        self.last = self.size - 1
        element = Element(key, value, self.last)
        self.structure.append(element)
        self.root = 0
        if self.size > 1:
            self.bubbleUp(self.last)
        return element

    def remove_min(self):
        min = self.min()
        # Swapping the index values for the root and last before swapping the nodes
        # themselves to keep it balanced. Same technique used in bubbleUp and bubbleDown
        self.structure[self.root].index, self.structure[self.last].index = self.structure[self.last].index, self.structure[self.root].index 
        self.structure[self.root], self.structure[self.last] = self.structure[self.last], self.structure[self.root]
        self.structure.pop(self.last)
        self.last -= 1
        self.size -= 1
        self.bubbleDown(self.root)
        return min

    def updateKey(self, element, newKey):
        if newKey < element.key:
            element.key = newKey
            self.bubbleUp(element.index)
        else:
            element.key = newKey
            self.bubbleDown(element.index)

    def bubbleUp(self, index):
        if index != self.root:
            parent = (index-1) // 2
            if self.structure[index].key < self.structure[parent].key:
                self.structure[index].index, self.structure[parent].index = self.structure[parent].index, self.structure[index].index
                self.structure[index], self.structure[parent] = self.structure[parent], self.structure[index]
                self.bubbleUp(parent)

    def bubbleDown(self, index):
        if 2 * index + 2 <= self.last:
            lc = 2 * index + 1
            rc = 2 * index + 2
            if self.structure[lc].key < self.structure[rc].key:
                swap = 2 * index + 1
            else:
                swap = 2 * index + 2
        elif 2 * index + 1 <= self.last:
            swap = 2 * index + 1
        else:
            return None
        if self.structure[index].key > self.structure[swap].key:
            self.structure[index].index, self.structure[swap].index = self.structure[swap].index, self.structure[index].index
            self.structure[index], self.structure[swap] = self.structure[swap], self.structure[index]
            self.bubbleDown(swap)

    def remove(self, element):
        swapElt = self.structure[self.last]
        self.structure[element.index], self.structure[swapElt.index] = self.structure[swapElt.index], self.structure[element.index]
        element.index, swapElt.index = swapElt.index, element.index
        removed = self.structure.pop(self.last)
        self.last -= 1
        self.bubbleDown(swapElt.index)
        self.size -= 1
        return removed