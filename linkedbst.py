"""
File: linkedbst.py
Author: Ken Lambert
"""

from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
from linkedqueue import LinkedQueue
from math import log, ceil
from tqdm import tqdm
from random import choice, shuffle

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
            s = ""
            if node != None:
                s += recurse(node.right, level + 1)
                s += "| " * level
                s += str(node.data) + "\n"
                s += recurse(node.left, level + 1)
            return s

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def inorder_iter(self):
     
        current = self._root
        tree = []
        stack = []
        
        while True:
            
            if current is not None:
                stack.append(current)
                current = current.left
    
            elif(stack):
                current = stack.pop()
                tree.append(current.data)

                current = current.right
    
            else:
                break
        
        return tree

    def add_iter(self, item):
        if self.isEmpty():
            self._root=BSTNode(item)
            self._size+=1
        current = self._root
        if current.data!= item:
            while True:
                if current.data > item:
                    if current.left:
                        current = current.left
                    else:
                        current.left = BSTNode(item)
                        self._size+=1
                        break
                if current.data <= item:
                    if current.right:
                        current = current.right
                    else:
                        current.right = BSTNode(item)
                        self._size+=1
                        break

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return list(iter(self))

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return list(iter(lyst))

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                recurse(node.right)
                lyst.append(node.data)
        recurse(self._root)
        return list(iter(lyst))

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

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
    
    def find_iter(self, item):
        current = self._root
        while current:
            if current.data == item:
                return current.data
            if current.data > item:
                current = current.left
            else:
                current = current.right
        return None

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
                if node.left == None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right == None:
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

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def liftMaxInLeftSubtreeToTop(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            currentNode = top.left
            while not currentNode.right == None:
                parent = currentNode
                currentNode = currentNode.right
            top.data = currentNode.data
            if parent == top:
                top.left = currentNode.left
            else:
                parent.right = currentNode.left

        # Begin main part of the method
        if self.isEmpty():
            return None

        # Attempt to locate the node containing the item
        itemRemoved = None
        preRoot = BSTNode(None)
        preRoot.left = self._root
        parent = preRoot
        direction = 'L'
        currentNode = self._root
        while not currentNode == None:
            if currentNode.data == item:
                itemRemoved = currentNode.data
                break
            parent = currentNode
            if currentNode.data > item:
                direction = 'L'
                currentNode = currentNode.left
            else:
                direction = 'R'
                currentNode = currentNode.right

        # Return None if the item is absent
        if itemRemoved == None:
            return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not currentNode.left == None \
                and not currentNode.right == None:
            liftMaxInLeftSubtreeToTop(currentNode)
        else:

            # Case 2: The node has no left child
            if currentNode.left == None:
                newChild = currentNode.right

                # Case 3: The node has no right child
            else:
                newChild = currentNode.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = newChild
            else:
                parent.right = newChild

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = preRoot.left
        return itemRemoved

    def replace(self, item, newItem):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                oldData = probe.data
                probe.data = newItem
                return oldData
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
        def is_leaf(node):
            return True if not node.left and not node.right else False

        def children(node):
            children = []
            if node.left:
                children.append(node.left)
            if node.right:
                children.append(node.right)
            return children

        def height1(top):
            '''
            Helper function
            :param top:
            :return:
            '''
            if is_leaf(top):
                return 0
            else:
                return 1+max(height1(child) for child in children(top))

        return height1(self._root)

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        return self.height() < 2* log(self._size+1) -1 

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        order = self.inorder()
        return [i for i in order if i>= low and i<= high]

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        order = self.inorder_iter()
        def recurs(lst):
            if len(lst) == 0:
                return None
            half  = len(lst)//2
            node = BSTNode(lst[half])
            node.left = recurs(lst[:half])
            node.right = recurs(lst[half+1:])
            return node
        self._root = recurs(order)


    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        order = self.inorder()
        for elem in order:
            if elem > item:
                return elem
        return None

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        
        order = self.inorder()[::-1]
        for elem in order:
            if elem < item:
                return elem
        return None

        
    @staticmethod
    def demo_bst(path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        wordstofind=[]
        with open(path, mode = 'r', encoding='utf-8')as f:
            words=f.readlines()
        for i in range(1000):
            wordstofind.append(choice(words))
        for i in tqdm(range(len(wordstofind))):
            for j in range(len(words)):
                if wordstofind[i]==words[j]:
                    break
        tree = LinkedBST()
        for word in words:
            tree.add_iter(word)
        for i in tqdm(range(len(wordstofind))):
            tree.find_iter(wordstofind[i])
        shuffle(words)
        treer= LinkedBST()
        for word in words:
            treer.add_iter(word)
        for i in tqdm(range(len(wordstofind))):
            treer.find_iter(wordstofind[i])
        tree.rebalance()
        for i in tqdm(range(len(wordstofind))):
            tree.find_iter(wordstofind[i])


if __name__ == "__main__":
    LinkedBST.demo_bst('test.txt')
