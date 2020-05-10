import math;

class A(object):
    def __init__(self, val):
        self.__val = val;
    
    @property
    def val(self):
        return self.__val;
    
    @val.setter
    def val(self, val):
        self.__val = val;
    
    def f(self):
        pass;
    
    @staticmethod
    def g(self):
        pass;
    
    def __str__(self):
        return "2333333";

def changeA(a):
    a.val = 233;
    print(a.val, id(a), id(a.val));
    pass;

def changeX(x):
    x = 233;
    print(id(x));


if __name__ == "__main__":
    v = A(0);
    print(f"{v}");
    a, b = A(v), A(v);
    print("--------------------");
    print(id(a) == id(b), a is b); # False False
    print(id(a.f) == id(b.f), a.f is b.f); # True False
    print(id(a.g) == id(b.g), a.g is b.g); # True True
    print("--------------------");
    c, d = a.f, b.f;
    print(id(c) == id(d), c is d); # False False
    print(id(a.f) == id(b.f), a.f is b.f); # True False
    print("--------------------");
    e, f = a.g, b.g;
    print(id(e) == id(f), e is f); # True True
    print("--------------------");
    print(id(256) == id(256), id(1 * math.pow(10, 6)) == id(1 * math.pow(10, 6))); # True False
    print("--------------------");
    i, j = "abcd", "dbfag";
    print(id(i) == id(j), id(i[0]) == id(j[3])); # False True
    print(id("abcdef") == id("abcdef"), id("abcdef" * int(math.pow(10, 6))) == id("abcdef" * int(math.pow(10, 6)))); # True False
    print("--------------------");
    x = 1;
    print(id(x)); # 140737105978000
    changeX(x); # 140737105985424
    print(id(x)); # 140737105978000
    print("--------------------");
    print(a.val, id(a), id(a.val)); # <__main__.A object at 0x000002B83EBBC080> 3214606844088 3214606844032
    changeA(a); # 233 3214606844088 140737105985424
    