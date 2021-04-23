from django.db.models import Q
import operator


def get_queryset_descendants(nodes, include_self=False):
    if not nodes:
        return Node.tree.none()
    filters = []
    for n in nodes:
        lft, rght = n.lft, n.rght
        if include_self:
            lft -= 1
            rght += 1
        filters.append(Q(tree_id=n.tree_id, lft__gt=lft, rght__lt=rght))
    q = reduce(operator.or_, filters)
    return Node.tree.filter(q)

