import sys
import pydot
import shutil
import os

class TreeNode(object):
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1


class AVLTree(object):
    def __init__(self):
        self.root = None

    # Function to insert a node
    def insert_node(self, root, key):

        # Find the correct location and insert the node
        if not root:
            return TreeNode(key)
        elif key < root.key:
            root.left = self.insert_node(root.left, key)
        else:
            root.right = self.insert_node(root.right, key)

        root.height = 1 + max(self.getHeight(root.left),
                              self.getHeight(root.right))

        # Update the balance factor and balance the tree
        balanceFactor = self.getBalance(root)
        if balanceFactor > 1:
            if key < root.left.key:
                return self.rightRotate(root)
            else:
                root.left = self.leftRotate(root.left)
                return self.rightRotate(root)

        if balanceFactor < -1:
            if key > root.right.key:
                return self.leftRotate(root)
            else:
                root.right = self.rightRotate(root.right)
                return self.leftRotate(root)

        return root

    # Function to delete a node
    def delete_node(self, root, key):

        # Find the node to be deleted and remove it
        if not root:
            return root
        elif key < root.key:
            root.left = self.delete_node(root.left, key)
        elif key > root.key:
            root.right = self.delete_node(root.right, key)
        else:
            if root.left is None:
                temp = root.right
                root = None
                return temp
            elif root.right is None:
                temp = root.left
                root = None
                return temp
            temp = self.getMinValueNode(root.right)
            root.key = temp.key
            root.right = self.delete_node(root.right,
                                          temp.key)
        if root is None:
            return root

        # Update the balance factor of nodes
        root.height = 1 + max(self.getHeight(root.left),
                              self.getHeight(root.right))

        balanceFactor = self.getBalance(root)

        # Balance the tree
        if balanceFactor > 1:
            if self.getBalance(root.left) >= 0:
                return self.rightRotate(root)
            else:
                root.left = self.leftRotate(root.left)
                return self.rightRotate(root)
        if balanceFactor < -1:
            if self.getBalance(root.right) <= 0:
                return self.leftRotate(root)
            else:
                root.right = self.rightRotate(root.right)
                return self.leftRotate(root)
        return root

    # Function to perform left rotation
    def leftRotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self.getHeight(z.left),
                           self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left),
                           self.getHeight(y.right))
        return y

    # Function to perform right rotation
    def rightRotate(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self.getHeight(z.left),
                           self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left),
                           self.getHeight(y.right))
        return y

    # Get the height of the node
    def getHeight(self, root):
        if not root:
            return 0
        return root.height

    # Get balance factore of the node
    def getBalance(self, root):
        if not root:
            return 0
        return self.getHeight(root.left) - self.getHeight(root.right)

    def getMinValueNode(self, root):
        if root is None or root.left is None:
            return root
        return self.getMinValueNode(root.left)
   
    def getMaxValueNode(self, root):
        if root is None or root.right is None:
            return root
        return self.getMaxValueNode(root.right)
    
    def searchValueNode(self, root, key):
        if root is None or key == root.key:
           return root
        if key < root.key:
           return self.searchValueNode(root.left, key)
        else:
           return self.searchValueNode(root.right, key)

    def preOrder(self, root):
        if not root:
            return
        print "{0} ".format(root.key),
        self.preOrder(root.left)
        self.preOrder(root.right)
   
    def preOrderGraph(self, root, graph):
        if not root:
           return graph
        graph.add_node(pydot.Node(root.key, shape="circle"))
        graph = self.preOrderGraph(root.left, graph)
        if not root.left is None:
           graph.add_edge(pydot.Edge(root.key, root.left.key, color="blue"))
        graph = self.preOrderGraph(root.right, graph)
        if not root.right is None:
           graph.add_edge(pydot.Edge(root.key, root.right.key, color="blue"))
        return graph

    # Print the tree
    def printHelper(self, currPtr, indent, last):
        if currPtr != None:
            sys.stdout.write(indent)
            if last:
                sys.stdout.write("R----")
                indent += "     "
            else:
                sys.stdout.write("L----")
                indent += "|    "
            print currPtr.key
            self.printHelper(currPtr.left, indent, False)
            self.printHelper(currPtr.right, indent, True)

def main():
    shutil.rmtree('Graficos')
    os.mkdir("Graficos")
    myTree = AVLTree()
    root = None
    #nums = [33, 13, 8, 40, 35, 4, 6, 21]
    nums = [40, 20, 32, 45, 50, 25, 35, 55, 28, 30, 31, 33, 60, 65, 5, 10, 15]
    i = 1
    for num in nums:
        root = myTree.insert_node(root, num)
        graph = pydot.Dot("AVL_Tree", graph_type="graph", bgcolor="white")
        graph = myTree.preOrderGraph(root, graph)
        graph.write_png("Graficos/AVL_Tree_" + str(i) + ".png")
        print "Grafico", i, ", insertando", num, ", revisar archivo generado..."
        i = i + 1
    nums = [35, 25, 21, 10]
    for num in nums:
        root = myTree.delete_node(root, num)
        graph = pydot.Dot("AVL_Tree", graph_type="graph", bgcolor="white")
        graph = myTree.preOrderGraph(root, graph)
        graph.write_png("Graficos/AVL_Tree_" + str(i) + ".png")
        print "Grafico ", i, ", borrando", num,  ", revisar archivo generado..."
        i = i + 1
    
    print "Minimo:", myTree.getMinValueNode(root).key
    print "Maximo:", myTree.getMaxValueNode(root).key
    nums = [15, 35, 40]
    for num in nums:
        print "Buscando: ", num,
        print ", se encontro en arbol" if not myTree.searchValueNode(root, num) is None else ", no se encontro en arbol"
    '''
    myTree.printHelper(root, "", True)
    key = 13
    root = myTree.delete_node(root, key)
    print "After Deletion: "
    myTree.printHelper(root, "", True)
    print "Minimo: ",
    print myTree.getMinValueNode(root).key
    print "Maximo: ",
    print myTree.getMaxValueNode(root).key
    num = 33
    print "Valor: ", num,
    print "se encuentra en arbol" if not myTree.searchValueNode(root, num) is None else "no se encuentra en arbol"
    num = 20
    print "Valor: ", num,
    print "se encuentra en arbol" if not myTree.searchValueNode(root, num) is None else "no se encuentra en arbol"
    print "Preorder: "
    myTree.preOrder(root)
    print
    graph = pydot.Dot("AVL_Tree", graph_type="graph", bgcolor="white")
    graph = myTree.preOrderGraph(root, graph)
    graph.write_png("Graficos/AVL_Tree_" + str(i) +".png")
    print "Grafico final, revisar archivo generado..."
    '''

main()