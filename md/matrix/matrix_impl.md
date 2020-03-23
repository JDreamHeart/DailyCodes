# 通过代码实现矩阵类

----
之前发过一篇[矩阵与空间坐标系变换](./matrix.md)的文章，介绍了矩阵的相关概念。  

不过由于概念性的东西相对来说较难理解，于是就想到了通过代码来实现一个矩阵类（该类包含矩阵创建，及基本运算功能），来加深对矩阵的理解。

## 设计思路
  * 确定矩阵的初始化参数，并进行参数校验；
  * 实现矩阵的转置、行列式、逆矩阵；
  * 实现矩阵的等于、加、减、乘法功能；

## 1. 参数及校验
  * 参数包含矩阵数据、行列数即可；
  * 参数校验主要进行判断行列数的乘积是否与矩阵数据个数相同。
  * 同时需对传入的数据进行拷贝，以免因为引用问题，而导致矩阵数据异常。

```py
class Matrix(object):
    def __init__(self, data = [], row = 0, col = 0):
        self.__data, self.__row, self.__col = self.verify(data, row, col);
    
    # verify data
    def verify(self, data, row, col):
        count = len(data);
        if row <= 0:
            row = (count > 0) and 1 or 0;
            col = count;
        elif col <= 0:
            col = math.ceil(count / row);
        # verify data length
        if count != row * col:
            raise Exception(f"failed to create matrix by invalid data count[{count}], row[{row}] and col[{col}]");
        return [float(d) for d in data], row, col; # copy data
```

## 2. 矩阵的转置
  * 只需要将矩阵的行数据换成对应列的数据，然后返回新的矩阵。

```py
    # transpose matrix
    @property
    def trans(self):
        if not self.__trans:
            data = [];
            for i in range(self.__col):
                for j in range(self.__row):
                    data.append(self.__data[j * self.__col + i]);
            self.__trans = Matrix(data, self.__col, self.__row);
        return self.__trans;
```

## 3. 矩阵的行列式
  * 首先通过`__getDetParams__`函数，获取数据元素的排列，以及对应排列的逆序数；
  * 将以上得到的数据，传入`__getDetVal__`函数，该函数根据行列式的定义，得到行列式的值。

```py
    # matrix determinant
    @property
    def det(self):
        if self.__det == None:
            groups, ionList = self.__getDetParams__();
            if groups and ionList:
                self.__det = self.__getDetVal__(groups, ionList);
        return self.__det;

    # get params of matrix determinant
    def __getDetParams__(self):
        groups, ionList = [], [];
        if self.__row != self.__col:
            return [], [];
        def reverseOrdinal(group):
            ion = 0;
            for i in range(len(group)-1, -1, -1):
                for j in range(i-1, -1, -1):
                    if group[j] > group[i]:
                        ion += 1;
            ionList.append(ion);
        def fullArrange(group = []):
            for i in range(self.__row):
                if i not in group:
                    group.append(i);
                    if len(group) == self.__row:
                        groups.append([g for g in group]);
                        reverseOrdinal(group);
                    else:
                        fullArrange(group);
                    group.pop();
            pass;
        fullArrange();
        return groups, ionList;
    
    # get value of matrix determinant by params
    def __getDetVal__(self, groups, ionList, excludeRow = -1, excludeCol = -1):
        det = 0;
        for i, group in enumerate(groups):
            ion = ionList[i];
            adjustCnt, val = 0, 1;
            for k,v in enumerate(group):
                if k == excludeRow or v == excludeCol:
                    ion = self.__adjustIon__(ion, group, k);
                    adjustCnt += 1;
                else:
                    val *= self.__data[k * self.__col + v];
            if adjustCnt <= 1 and adjustCnt != len(group):
                det += math.pow(-1, ion) * val;
        return det;

    # adjust inverse ordinal mumber
    def __adjustIon__(self, ion, group, idx):
        for v in group[:idx]:
            if v > group[idx]:
                ion -= 1;
        for v in group[idx+1:]:
            if v < group[idx]:
                ion -= 1;
        return ion;
```

## 4. 矩阵的逆矩阵
  * 首先根据数据元素的排列和逆序数，得到矩阵的行列式、对应各个元素的余子式；
  * 接着根据对应各个元素的余子式，得到新的矩阵，然后将矩阵进行转置，再除以源矩阵的行列式的值，即可得到源矩阵的逆矩阵。

```py
    # inverse matrix
    @property
    def inv(self):
        if not self.__inv:
            groups, ionList = self.__getDetParams__();
            if groups and ionList:
                det = self.__getDetVal__(groups, ionList);
                if det == 0:
                    return None;
                data = [];
                for i in range(self.__col):
                    for j in range(self.__row):
                        mdet = math.pow(-1, i+j) * self.__getDetVal__(groups, ionList, excludeRow = i, excludeCol = j);
                        data.append(mdet);
                self.__inv = Matrix(data, self.__col, self.__row).trans * (1/det);
        return self.__inv;
```

## 5. 矩阵的等于、加、减、乘法功能
  * 通过魔法方法，实现对象的等于（`__eq__`）、加（`__add__`）、减（`__sub__`）、乘（`__mul__`）法功能;
  * 其中乘法考虑了矩阵与数相乘，和矩阵与矩阵相乘的情况。

```py
    def __eq__(self, other):
        if not isinstance(other, Matrix):
            raise TypeError("Matrix cannot campare to other instance");
        if self.__row == other.row and self.__col == other.col:
            for i,v in enumerate(self.__data):
                if v != other.get(index = i):
                    return False;
        return True;
    
    def __ne__(self, other):
        return not self.__eq__(other);
    
    def __add__(self, other):
        if not isinstance(other, Matrix):
            raise TypeError("Matrix cannot add to other instance");
        if self.__row != other.row or self.__col != other.col:
            raise TypeError("Matrix cannot add Matrix with different size");
        data = [];
        for i,v in enumerate(self.__data):
            data.append(v + other.get(index = i));
        return Matrix(data, self.__row, self.__col);
    
    def __sub__(self, other):
        if not isinstance(other, Matrix):
            raise TypeError("Matrix cannot sub to other instance");
        if self.__row != other.row or self.__col != other.col:
            raise TypeError("Matrix cannot sub Matrix with different size");
        data = [];
        for i,v in enumerate(self.__data):
            data.append(v - other.get(index = i));
        return Matrix(data, self.__row, self.__col);

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            data = [];
            for i,v in enumerate(self.__data):
                data.append(v * other);
            return Matrix(data, self.__row, self.__col);
        if not isinstance(other, Matrix):
            raise TypeError("Matrix cannot mul to other instance[not int, float, Matrix]");
        if self.__col != other.row:
            raise TypeError("Matrix cannot mul Matrix with unqualified size");
        data = [];
        for i in range(self.__row):
            for j in range(other.col):
                val = 0;
                for k in range(self.__col):
                    val += self.get(i, k) * other.get(k, j);
                data.append(val);
        return Matrix(data, self.__row, other.col);
```

## 完整代码
GitHub地址：
[https://github.com/JDreamHeart/DailyCodes/python/article/matrix.py](https://github.com/JDreamHeart/DailyCodes/blob/master/python/article/matrix.py)

