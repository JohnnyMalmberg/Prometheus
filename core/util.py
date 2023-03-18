def find(l, predicate):
    return next((x for x in l if predicate(x)), None)