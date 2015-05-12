import BTrees

from zope import component
from zope.app.intid.interfaces import IIntIds

from zc.relation.catalog import Catalog
from zc.relation.interfaces import ICatalog

from z3c.relationfield.interfaces import IRelationValue

def dump(obj, catalog, cache):
    intids = cache.get('intids')
    if intids is None:
        intids = cache['intids'] = component.getUtility(IIntIds)
    return intids.getId(obj)
    
def load(token, catalog, cache):
    intids = cache.get('intids')
    if intids is None:
        intids = cache['intids'] = component.getUtility(IIntIds)
    return intids.getObject(token)
    
class RelationCatalog(Catalog):

    def __init__(self):
        Catalog.__init__(self, dump, load)
        self.addValueIndex(IRelationValue['from_id'])
        self.addValueIndex(IRelationValue['to_id'])
        self.addValueIndex(IRelationValue['from_attribute'],
                           btree=BTrees.family32.OI)
        self.addValueIndex(IRelationValue['from_interfaces_flattened'],
                           multiple=True,
                           btree=BTrees.family32.OI)
        self.addValueIndex(IRelationValue['to_interfaces_flattened'],
                           multiple=True,
                           btree=BTrees.family32.OI)

