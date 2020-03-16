import math;

class Matrix(object):
    def __init__(self, data = [], row = 0, col = 0):
        self.__data, self.__row, self.__col = self.verify(data, row, col);
        self.__trans, self.__det, self.__inv = None, None, None;
        pass;
    
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

    def __div__(self, other):
        if not isinstance(other, int) and not isinstance(other, float):
            raise TypeError("Matrix cannot div to other instance[not int, float]");
        if other == 0:
            raise TypeError("Matrix cannot div zero");
        data = [];
        for i,v in enumerate(self.__data):
            data.append(v / other);
        return Matrix(data, self.__row, self.__col);
    
    def __str__(self):
        mt = [];
        for i in range(self.__row):
            m = [];
            for j in range(self.__col):
                m.append(self.get(i, j));
            mt.append(m);
        return f"Matrix({self.__row},{self.__col}){mt}";
    
    def __call__(self, row = -1, col = -1, index = -1):
        return self.get(row = row, col = col, index = index);
    
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
        return [float(d) for d in data], row, col;
    
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

    def __adjustIon__(self, ion, group, idx):
        for v in group[:idx]:
            if v > group[idx]:
                ion -= 1;
        for v in group[idx+1:]:
            if v < group[idx]:
                ion -= 1;
        return ion;
    
    def copy(self):
        return Matrix(self.__data, self.__row, self.__col);
    
    # get data
    def get(self, row = -1, col = -1, index = -1):
        if 0 <= index < len(self.__data):
            return self.__data[index];
        if row >= 0 and col >= 0:
            idx = row * self.__col + col;
            if idx < len(self.__data):
                return self.__data[idx];
            return None;
        elif row >= 0 and col < 0:
            ret = [];
            if row < self.__row:
                for i in range(self.__col):
                    ret.append(self.__data[row * self.__col + i]);
            return ret;
        elif row < 0 and col >= 0:
            ret = [];
            if col < self.__col:
                for i in range(self.__row):
                    ret.append(self.__data[i * self.__col + col]);
            return ret;
        return [d for d in self.__data];
    
    # update data
    def update(self, data = [], row = 0, col = 0):
        self.__data, self.__row, self.__col = self.verify(data, row, col);
        self.__trans, self.__det, self.__inv = None, None, None;
        pass;
    
    @property
    def size(self):
        return (self.__row, self.__col);
    
    @property
    def row(self):
        return self.__row;
        
    @property
    def col(self):
        return self.__col;
    
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
    
    # matrix determinant
    @property
    def det(self):
        if self.__det == None:
            groups, ionList = self.__getDetParams__();
            # print(self.__row, self.__col, groups, ionList)
            if groups and ionList:
                self.__det = self.__getDetVal__(groups, ionList);
        return self.__det;

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


# test func
if __name__ == "__main__":
    mt = Matrix([5,6,7,8], 2);
    print(mt.inv);