class Node(object):
    def __init__(self, val):
        self.__val = val;
        self.__left = None;
        self.__right = None;
    
    @property
    def val(self):
        return self.__val;
    
    @property
    def left(self):
        return self.__left;
    
    @left.setter
    def left(self, left):
        self.__left = left;
        
    @property
    def right(self):
        return self.__right;
    
    @right.setter
    def right(self, right):
        self.__right = right;
        

def initTree():
    node = Node(3);
    node.left = Node(2);
    node.right = Node(8);
    node.left.left = Node(9);
    node.left.right = Node(10);
    node.right.right = Node(4);
    return node;

def pushStack(stack, node):
    while(node):
        stack.append(node);
        if node.left:
            node = node.left;
        elif node.right:
            node = node.right;
        else:
            break;

def postPairsTree(node):
    stack = [];
    pushStack(stack, node);
    ret, preNode = [], None;
    while(stack):
        node = stack.pop();
        if preNode == node.left and node.right:
            stack.append(node);
            pushStack(stack, node.right);
            continue;
        ret.append(node.val);
        preNode = node;
    return ret;


def main():
    node = initTree();
    print(postPairsTree(node));
    pass;

if __name__ == "__main__":
    main();