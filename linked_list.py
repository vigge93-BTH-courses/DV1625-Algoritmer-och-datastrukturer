class LinkedList:

    def __init__(self):
        self.key = []
        self.prev = []
        self.next = []
        self.head = None

    def search(self, key, attribute_func=lambda el: el):
        x = self.head
        while x is not None and key != attribute_func(self.key[x]):
            x = self.next[x]
        if x is not None:
            return self.key[x]
        else:
            return None

    def _search_idx(self, key, attribute_func=lambda el: el):
        x = self.head
        while x is not None and key != attribute_func(self.key[x]):
            x = self.next[x]
        return x

    def insert(self, key):
        self.key.append(key)
        idx = len(self.key) - 1
        self.next.append(self.head)
        if self.head is not None:
            self.prev[self.head] = idx
        self.head = idx
        self.prev.append(None)

    def delete(self, key, attribute_func: lambda el: el):
        idx = self._search_idx(key, attribute_func)
        if self.prev[idx] is not None:
            self.next[self.prev[idx]] = self.next[idx]
        else:
            self.head = self.next[idx]
        if self.next[idx] is not None:
            self.next[self.prev[idx]] = self.prev[idx]
