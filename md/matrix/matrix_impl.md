# 通过代码实现矩阵类

----
[矩阵与空间坐标系变换](./matrix.md)一文介绍了矩阵的概念。  

然而概念性的东西总是较难理解的，所以就想到了通过代码来实现一个矩阵类（该类包含矩阵创建，及基本运算功能），来加深对矩阵的理解。

## 设计思路
  * 确定矩阵的初始化参数，并进行参数校验；
  * 实现矩阵的转置、行列式、逆矩阵；
  * 实现矩阵的等于、加、减、乘法功能；

## 参数及校验
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

## 矩阵的转置
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

## 矩阵的行列式
