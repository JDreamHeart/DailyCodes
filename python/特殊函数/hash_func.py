class Mylist(list):
    def __hash__(self):
        print("hash(self(0)) = ",hash(self[0]))
        print("hash running.")
        return hash(self[0])

    def __eq__(self,other):
        print("eq running.")
        return self[0] == other

def test1():
    l = Mylist([1,2])
    d = {}
    d[l] = l
    print(d)
    d[1] = 1
    print(d)
    # 输出：
    # hash(self(0)) =  1
    # hash running.
    # {[1, 2]: [1, 2]}
    # eq running.
    # {[1, 2]: 1}

def test2():
    l = Mylist([1,2])
    d = {}
    d[1] = 1
    print(d)
    d[l] = l
    print(d)
    # 输出：
    # {1: 1}
    # hash(self(0)) =  1
    # hash running.
    # eq running.
    # {1: [1, 2]}

if __name__ == "__main__":
    test1();
    print("-------------------------------")
    test2();