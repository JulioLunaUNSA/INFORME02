# Create a node
class BTreeNode:
    def __init__(self, leaf=False):
        self.leaf = leaf
        self.keys = []
        self.child = []


# Tree
class BTree:
   def __init__(self, t):
       self.root = BTreeNode(True)
       self.t = t

   # Insert node old
   def insert_old(self, k):
       root = self.root
       #if len(root.keys) == (2 * self.t) - 1:
       if len(root.keys) == (self.t - 1):
          temp = BTreeNode()
          self.root = temp
          temp.child.insert(0, root)
          self.split_child(temp, 0)
          self.insert_non_full(temp, k)
       else:
          self.insert_non_full(root, k)
   
   # Insert node
   def insert(self, k):
       root = self.root
       self.insert_non_full(root, k)
       if len(root.keys) == self.t:
          temp = BTreeNode()
          self.root = temp
          temp.child.insert(0, root)
          self.split_child(temp, 0)

   # Insert nonfull
   def insert_non_full(self, x, k):
       i = len(x.keys) - 1
       if x.leaf:
          x.keys.append(None)
          while i >= 0 and k < x.keys[i]:
             x.keys[i + 1] = x.keys[i]
             i -= 1
          x.keys[i + 1] = k
       else:
          while i >= 0 and k < x.keys[i]:
             i -= 1
          i += 1
          #if k > x.keys[i]:
          #   i += 1
          self.insert_non_full(x.child[i], k)
          if len(x.child[i].keys) == self.t:
             self.split_child(x, i)

   # Split the child
   def split_child(self, x, i):
       j = 0
       t = self.t
       y = x.child[i]
       z = BTreeNode(y.leaf)
       x.child.insert(i + 1, z)
       j = (t-1)/2
       x.keys.insert(i, y.keys[j])
       z.keys = y.keys[j + 1:]
       y.keys = y.keys[:j]
       if not y.leaf:
          z.child = y.child[j + 1:]
          y.child = y.child[: j + 1]

   def iDelete(self, x, k):
       if self.search_key(k, self.root) == None: return
       self.delete(x, k)
       return

   # Delete a node
   def delete(self, x, k):
       t = self.t
       i = 0
       j = (t-1)/2
       while i < len(x.keys) and k > x.keys[i]:#ok
           i += 1
       if x.leaf:#ok
          if i < len(x.keys) and x.keys[i] == k:
             x.keys.pop(i)
             return
          return

       if i < len(x.keys) and x.keys[i] == k:
          return self.delete_internal_node(x, k, i)
       elif len(x.child[i].keys) >= j and not x.child[i].leaf:#ok
          self.delete(x.child[i], k)
          if len(x.child[i].keys) == 0:
             x.child.append(None)
             if x.child[i + 1] != None:
                self.delete_merge(x, i, i + 1)
             else:
                self.delete_merge(x, i, i - 1)
       else:
          self.delete(x.child[i], k)
          if i != 0 and i + 1 < len(x.child):
             if len(x.child[i - 1].keys) >= (j + 1):
                self.delete_sibling(x, i, i - 1)
             elif len(x.child[i + 1].keys) >= (j + 1):
                self.delete_sibling(x, i, i + 1)
             else:
                self.delete_merge(x, i, i + 1)
          elif i == 0:
             if len(x.child[i + 1].keys) >= (j + 1):#ok
                self.delete_sibling(x, i, i + 1)
             else:
                self.delete_merge(x, i, i + 1)
          elif i + 1 == len(x.child):
             if len(x.child[i - 1].keys) >= (j + 1):
                self.delete_sibling(x, i, i - 1)
             else:#ok
                self.delete_merge(x, i, i - 1)
                #i -= 1

   # Delete internal node
   def delete_internal_node(self, x, k, i):
       t = self.t
       j = (t-1)/2
       if x.leaf:
          if x.keys[i] == k:
             x.keys.pop(i)
             return
          return

       if len(x.child[i].keys) >= (j + 1):
          x.keys[i] = self.delete_predecessor(x.child[i])
          return
       elif len(x.child[i + 1].keys) >= (j + 1):
          x.keys[i] = self.delete_successor(x.child[i + 1])
          return
       else:
          self.delete_merge(x, i, i + 1)
          self.delete_internal_node(x.child[i], k, j)

   # Delete the predecessor
   def delete_predecessor(self, x):
       j = (self.t - 1)/2
       if x.leaf:
          return x.keys.pop()
       n = len(x.keys) - 1
       if len(x.child[n].keys) >= (j + 1):
          self.delete_sibling(x, n + 1, n)
       else:
            self.delete_merge(x, n, n + 1)
       self.delete_predecessor(x.child[n])

   # Delete the successor
   def delete_successor(self, x):
       j = (self.t - 1)/2
       if x.leaf:
          return x.keys.pop(0)
       if len(x.child[1].keys) >= (j + 1):
          self.delete_sibling(x, 0, 1)
       else:
          self.delete_merge(x, 0, 1)
       self.delete_successor(x.child[0])

   # Delete resolution
   def delete_merge(self, x, i, j):
       cnode = x.child[i]

       if j > i:
          rsnode = x.child[j]
          cnode.keys.append(x.keys[i])
          for k in range(len(rsnode.keys)):
              cnode.keys.append(rsnode.keys[k])
              if len(rsnode.child) > 0:
                 cnode.child.append(rsnode.child[k])
          if len(rsnode.child) > 0:
             cnode.child.append(rsnode.child.pop())
          new = cnode
          x.keys.pop(i)
          x.child.pop(j)
       else:
          lsnode = x.child[j]
          lsnode.keys.append(x.keys[j])
          for i in range(len(cnode.keys)):
              lsnode.keys.append(cnode.keys[i])
              if len(lsnode.child) > 0:
                 lsnode.child.append(cnode.child[i])
          if len(lsnode.child) > 0:
             lsnode.child.append(cnode.child.pop())
          new = lsnode
          x.keys.pop(j)
          x.child.pop(i)

       if x == self.root and len(x.keys) == 0:
          self.root = new

   # Delete the sibling
   def delete_sibling(self, x, i, j):
       cnode = x.child[i]
       if i < j:#ok
          rsnode = x.child[j]
          cnode.keys.append(x.keys[i])
          x.keys[i] = rsnode.keys[0]
          if len(rsnode.child) > 0:
             cnode.child.append(rsnode.child[0])
             rsnode.child.pop(0)
          rsnode.keys.pop(0)
       else:
          lsnode = x.child[j]
          cnode.keys.insert(0, x.keys[i - 1])
          x.keys[i - 1] = lsnode.keys.pop()
          if len(lsnode.child) > 0:
             cnode.child.insert(0, lsnode.child.pop())

   # Print the tree
   def print_tree(self, x, l=0):
       print "Level ", l, " ", len(x.keys), ":",
       for i in x.keys:
          print i,
       print
       l += 1
       if len(x.child) > 0:
          for i in x.child:
             self.print_tree(i, l)

   # Search key in the tree
   def search_key(self, k, x=None):
       if x is not None:
          i = 0
          while i < len(x.keys) and k > x.keys[i]:
             i += 1
          if i < len(x.keys) and k == x.keys[i]:
             return (x, i)
          elif x.leaf:
             return None
          else:
             return self.search_key(k, x.child[i])
         
       else:
          return self.search_key(k, self.root)


def main():
    B = BTree(4)

    #for i in range(10):
    #    B.insert((i, 2 * i))
    #nums = [33, 13, 8, 40, 35, 46, 21, 10, 34]
    #nums = [20, 40, 10, 30, 33, 50, 60]
    nums = [5, 10, 15, 20, 25, 28, 30, 31, 32, 33, 35, 40, 45, 50, 55, 60, 65]
    for num in nums:
        B.insert(num)

    B.print_tree(B.root)
    n = 8
    print "Search: ", n,
    if B.search_key(n) is not None:
       print "Found"
    else:
       print "Not Found"
    nums = [35, 40, 21, 10]
    for num in nums:
        print "Delete: ", num
        B.iDelete(B.root, num)
        B.print_tree(B.root)
    '''
    n = 35
    print "Delete: ", n
    B.delete(B.root, n)
    B.print_tree(B.root)
    n = 13
    print "Delete: ", n
    B.delete(B.root, n)
    B.print_tree(B.root)
    n = 10
    print "Delete: ", n
    B.delete(B.root, n)
    B.print_tree(B.root)
    n = 40
    print "Delete: ", n
    B.delete(B.root, n)
    B.print_tree(B.root)
    n = 35
    print "Delete: ", n
    B.delete(B.root, n)
    B.print_tree(B.root)
    n = 40
    print "Delete: ", n
    B.delete(B.root, n)
    B.print_tree(B.root)
    n = 21
    print "Delete: ", n
    B.delete(B.root, n)
    B.print_tree(B.root)
    n = 10
    print "Delete: ", n
    B.delete(B.root, n)
    B.print_tree(B.root)
    '''
main()