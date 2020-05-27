class Element:

    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __str__(self):
        outstr = "(%i, %i)" % (self.key, self.value)
        return outstr

    def __eq__(self, other):
        return self.key == other.key

    def __lt__(self, other):
        return self.key < other.key

class Heap:

    def __init__(self):
        self.structure = []
        self.root = None
        self.size = 0
        self.last = None

    def __str__(self):
        outstr = "["
        for i in self.structure:
            outstr += str(i)
        outstr += "]"
        return outstr

    def min(self):
        return self.structure[self.root]

    def length(self):
        return self.size

    def is_empty(self):
        return self.length == 0

    def add(self, key, value):
        element = Element(key, value)
        self.structure.append(element)
        self.root = 0
        self.size += 1
        self.last = self.size - 1
        if self.size > 1:
            self.bubbleUp(self.last)
        return element
            

    def bubbleUp(self, index):
        if index != self.root:
            parent = (index-1) // 2
            if self.structure[index].key < self.structure[parent].key:
                self.structure[index], self.structure[parent] = self.structure[parent], self.structure[index]
                self.bubbleUp(parent)

    def remove_min(self):
        min = self.min()
        self.structure[self.root], self.structure[self.last] = self.structure[self.last], self.structure[self.root]
        self.structure.pop(self.last)
        self.last -= 1
        self.size -= 1
        self.bubbleDown(self.root)
        return min

    def bubbleDown(self, index):
        if 2 * index + 2 <= self.last:
            lc = 2 * index + 1
            rc = 2 * index + 2
            if self.structure[lc].key < self.structure[rc].key:
                swap = lc
            else:
                swap = rc
        elif 2 * index + 1 <= self.last:
            swap = 2 * index + 1
        else:
            return None
        if self.structure[index].key > self.structure[swap].key:
            self.structure[index], self.structure[swap] = self.structure[swap], self.structure[index]
            self.bubbleDown(swap)