from linked_list import LinkedList


class HashTable:

    def __init__(self, size, hash_func, attribute_func=lambda el: el):
        self.hash_func = hash_func
        self.attribute_func = attribute_func
        self.size = size
        self.table = [LinkedList() for x in range(size)]

    def insert(self, x, key):
        hash = self.hash_func(key)
        self.table[hash].insert(x)

    def search(self, key):
        hash = self.hash_func(key)
        return self.table[hash].search(key, self.attribute_func)

    def delete(self, key):
        hash = self.hash_func(key)
        self.table[hash].delete(key, self.attribute_func)


def hash(x):
    return sum([ord(n) for n in x]) % 11


names = ['Mia', 'Tim', 'Bea', 'Zoe', 'Sue', 'Len', 'Moe', 'Lou', 'Rae', 'Max', 'Tod']
hash_table = HashTable(11, hash)

for name in names:
    hash_table.insert(name, name)

print(name)
