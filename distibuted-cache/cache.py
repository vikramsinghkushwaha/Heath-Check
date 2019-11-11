import datetime
import random
import os
import json



class MyCache:
    def __init__(self):
        self.cache = {}

    def compute_hash(self,key):
        if isinstance(key,str):
            s = sum([ord(i) for i in key])
            return s%10
        elif isinstance(key,int):
            return key%10
        else:
            return key

    def contains(self, key):
        cache = {}
        hash_val  = self.compute_hash(key)
        node_path = os.path.join('cache','general')
        if not hash_val//10:
            node_path = os.path.join('cache',str(hash_val))
        if os.path.isfile(node_path):
            cache = json.load(open(node_path,'r'))
        if key in cache:
            return True
        else:
            return False

    def update(self, key, value):
        hash_val  = self.compute_hash(key)
        self.cache[key] = {'date_accessed': datetime.datetime.now().strftime("%B"),'value': value}
        cache = {}
        node_path = os.path.join('cache','general')
        if not hash_val//10:
            node_path = os.path.join('cache',str(hash_val))
        if os.path.isfile(node_path):
            cache = json.load(open(node_path,'r'))
        cache[key] = {'date_accessed': datetime.datetime.now().strftime("%B"),'value': value}
        json.dump(cache,open(node_path,'w'))


    def remove_oldest(self):
        oldest_entry = None
        for key in self.cache:
            if oldest_entry == None:
                oldest_entry = key
            elif self.cache[key]['date_accessed'] < self.cache[oldest_entry]['date_accessed']:
                oldest_entry = key
        self.cache.pop(oldest_entry)

    


if __name__ == '__main__':
    keys = ['test', 'the', 'program', 'check', 'if', 'it', 'stores', 'all' ,'red',
             'fox', 'fence', 'junk', 'other', 'alpha', 'bravo', 'cal', 'devo', 
            'ele']

    cache = MyCache()
    for i, key in enumerate(keys):
        if cache.contains(key):
            continue
        else:
            value = key
            cache.update(key, value)
        print("%s iterations, Stored %s in  cache" % (i+1, key))