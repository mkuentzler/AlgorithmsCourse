class Node:
    """
    Implements a linked list. Cargo is the first entry of the list,
    nextelem is a linked list.
    """
    def __init__(self, cargo=None, nextelem=None):
        self.car = cargo
        self.nxt = nextelem

    def __str__(self):
        return str(self.car)

    def display(self):
        if self.car:
            print str(self)
        if self.nxt:
            self.nxt.display()

    def next(self):
        return self.nxt

    def value(self):
        return self.car


def reverse(unrev, rev=None):
    """
    Reverses a linked list.
    """
    if unrev:
        return reverse(unrev.next(), Node(unrev.value(), rev))
    else:
        return rev

B = Node(3)
C = Node(2, B)
A = Node(1, C)

A.display()
print

D = reverse(A)
D.display()