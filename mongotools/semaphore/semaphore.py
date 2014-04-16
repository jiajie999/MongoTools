
class Semaphore(object):

    """docstring for Semaphore"""
    def __init__(self, db, id, counter, value, collection_name='mongotools.semaphore'):
        self._db = db
        self._name = collection_name
        self._id = id
        self._counter = counter
        self._max = value
        doc = self._db[self._name].find_and_modify(dict(_id=id), {'$setOnInsert':{counter:value}}, upsert=True, new=True)
        if counter not in doc:
            self._db[self._name].update({'_id':id, counter:{'$exists':False}}, {'$set': {counter:value}}, w=1)

    def acquire(self):
        doc = self._db[self._name].update({'_id':self._id, self._counter:{'$gt':0}}, {'$inc': {self._counter:-1} }, w=1)
        return doc['updatedExisting']

    def release(self):
        self._db[self._name].update({'_id':self._id, self._counter:{'$lt':self._max}}, {'$inc': {self._counter:1}})

