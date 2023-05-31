"""
File: linkedbst.py
Author: Ken Lambert
"""

from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
# from linkedqueue import LinkedQueue
from math import log
import time


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            string = ""
            if node is not None:
                string += recurse(node.right, level + 1)
                string += "| " * level
                string += str(node.data) + "\n"
                string += recurse(node.left, level + 1)
            return string

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right is not None:
                    stack.push(node.right)
                if node.left is not None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node is not None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) is not None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left is None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right is None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def alter_add(self, item):
        if self.isEmpty():
            self._root = BSTNode(item)
            self._size += 1
            return None
        my_que = [self._root]
        while True:
            node = my_que.pop(0)
            if item < node.data:
                if node.left is None:
                    node.left = BSTNode(item)
                    break
                my_que.append(node.left)
            elif item > node.data:
                if node.right is None:
                    node.right = BSTNode(item)
                    break
                my_que.append(node.right)
        self._size += 1


    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")
        return item

    def replace(self, item, new_item):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe is not None:
            if probe.data == item:
                old_data = probe.data
                probe.data = new_item
                return old_data
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''
        def height1(top):
            '''
            Helper function
            :param top:
            :return:
            '''
            if top is None:
                return 0
            else:
                return 1 + max(height1(top.left), height1(top.right))
        return height1(self._root)-1 if height1(self._root) > 0 else 0

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        if self.height() < (2*log(self._size + 1, 2)) - 1:
            return True
        return False

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        res = list(self.inorder())
        return res[res.index(low):res.index(high)+1]

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        roots_lst = []
        for i in self.inorder():
            roots_lst.append(i)
        for i in roots_lst:
            self.remove(i)
        for i in roots_lst:
            self.add(i)
        return self

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        res = None
        for i in self.inorder():
            if i > item:
                if res is None:
                    res = i
                elif res > i:
                    res = i
        return res


    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        res = None
        for i in self.inorder():
            if i < item:
                if res is None:
                    res = i
                elif res < i:
                    res = i
        return res

    def alter_find(self, item):
        if self._root is None:
            return None
        my_que = [self._root]
        while True:
            node = my_que.pop(0)
            if node.data == item:
                break
            elif node.data < item:
                my_que.append(node.right)
            elif node.data > item:
                my_que.append(node.left)
    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        with open(path, "r") as file:
            words = file.read().splitlines()
        print("Час пошуку 10000 випадкових слів у впорядкованому за абеткою словнику:")
        start_time = time.time()
        for i in range(10000):
            result = words[i] in words
        end_time = time.time()
        print(f"Час: {end_time - start_time} секунд")

        print("Час пошуку 10000 випадкових слів у словнику, який представлений у вигляді \
бінарного дерева пошуку (впорядкований за абеткою):")
        sorted_list = words.copy()
        sorted_list = sorted(sorted_list)[:1000]
        ordered_list = LinkedBST()
        for i in sorted_list:
            ordered_list.alter_add(i)
        start_time = time.time()
        for i in range(1000):
            ordered_list.alter_find(sorted_list[i])
        end_time = time.time()
        print(f"Час: {end_time - start_time} секунд")

        print("Час пошуку 10000 випадкових слів у словнику, який представлений у вигляді \
бінарного дерева пошуку. (слова у дерево додаються випадковим чином).")
        unord_tree = LinkedBST()
        for i in range(1000):
            unord_tree.add(words[i])
        start_time = time.time()
        for i in range(1000):
            unord_tree.alter_find(words[i])
        end_time = time.time()
        print(f"Час: {end_time - start_time} секунд")

        print("Час пошуку 10000 випадкових слів у словнику, який представлений у вигляді \
бінарного дерева пошуку після його балансування.")
        balanced_tree = unord_tree.rebalance()
        start_time = time.time()
        for i in range(1000):
            balanced_tree.alter_find(words[i])
        end_time = time.time()
        print(f"Час: {end_time - start_time} секунд")