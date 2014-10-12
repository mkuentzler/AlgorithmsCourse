"""
unionfind.py

Union-find data structure. Based on Josiah Carlson's code,
http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/215912
with additional changes by D. Eppstein and M. Kuentzler.
"""


class UnionFind:
    """Union-find data structure.

    Each unionFind instance X maintains a family of disjoint sets of
    hashable objects, supporting the following two methods:

    - X[item] returns a name for the set containing the given item.
      Each set is named by an arbitrarily-chosen one of its members; as
      long as the set remains unchanged it will keep the same name. If
      the item is not yet part of a set in X, a new singleton set is
      created for it.

    - X.union(item1, item2, ...) merges the sets containing each item
      into a single larger set.  If any item is not yet part of a set
      in X, it is added to X as one of the members of the merged set.
    """

    def __init__(self):
        """Create a new empty union-find structure."""
        self._ranks = {}
        self._parents = {}

    def __getitem__(self, obj):
        """Find and return the name of the set containing the object."""

        # check for previously unknown object
        if obj not in self._parents:
            self._parents[obj] = obj
            self._ranks[obj] = 1
            return obj

        # find path of objects leading to the root
        path = [obj]
        root = self._parents[obj]
        while root != path[-1]:
            path.append(root)
            root = self._parents[root]

        # compress the path and return
        for ancestor in path:
            self._parents[ancestor] = root
        return root
        
    def __iter__(self):
        """Iterate through all items ever found or unioned by this structure."""
        return iter(self._parents)

    def union(self, *objects):
        """Find the sets containing the objects and merge them all."""
        roots = [self[x] for x in objects]
        # Use union-by-rank to determine the new root, and to update the ranks.
        heaviest = max([(self._ranks[r], r) for r in roots])[1]
        for r in roots:
            self._parents[r] = heaviest
        for r in roots:
            if r != heaviest and self._ranks[r] == self._ranks[heaviest]:
                self._ranks[heaviest] += 1
                break