# 基于Python+wxPython实现俄罗斯方块游戏

----

## 游戏要素拆分
  * 场景：可以理解为方块的可移动区域（相当于背景）；
  * 方块：分成移动中（即正在下落的）的和已固定的格子；
  * 定时器：按一定时间（可能会根据所得分数进行变化）刷新移动中的方块位置；
  * 碰撞检测：判断移动或旋转的下一步位置中，是否有已固定的格子，若有则不许移动；
  * 结束判断：当已固定格子超出顶部时，则游戏结束。


## 1. 场景
场景是构成游戏的必要部分，是承载游戏中所有物体的基石。  
一个游戏中可以有多个场景，其中存在场景管理器（一般是全局变量），来进行如场景启动、切换和停止等操作。  
而这里的俄罗斯方块只需一个场景，而且的场景也很简单，只需根据其尺寸和颜色配置，构建出一个平面即可。  


## 2. 方块
这里的方块，可以理解为游戏物体，其尺寸由背景尺寸和方块数量（背景尺寸/方块数量）决定，然后可按照一定的组合方式，构建出一个形状，如I、J、L、O、S、Z、T。  

如下所示，该函数用于获取对应形状的方块位置列表。  
```py
# 根据传入位置，返回对应形状的方块位置列表
def getMovingItemPosList(startPos, key = None):
    if not key:
        key = random.choice(["I", "J", "L", "O", "S", "Z", "T"]);
    if key == "I":
        return [
            [startPos[0]-3, startPos[1]],
            [startPos[0]-2, startPos[1]],
            [startPos[0]-1, startPos[1]],
            [startPos[0], startPos[1]]
        ];
    elif key == "J":
        return [
            [startPos[0]-2, startPos[1]],
            [startPos[0]-1, startPos[1]],
            [startPos[0], startPos[1]],
            [startPos[0], startPos[1]-1],
        ];
    elif key == "L":
        return [
            [startPos[0]-2, startPos[1]],
            [startPos[0]-1, startPos[1]],
            [startPos[0], startPos[1]],
            [startPos[0], startPos[1]+1],
        ];
    elif key == "O":
        return [
            [startPos[0]-1, startPos[1]],
            [startPos[0]-1, startPos[1]+1],
            [startPos[0], startPos[1]],
            [startPos[0], startPos[1]+1],
        ];
    elif key == "S":
        return [
            [startPos[0]-1, startPos[1]+1],
            [startPos[0]-1, startPos[1]],
            [startPos[0], startPos[1]],
            [startPos[0], startPos[1]-1],
        ];
    elif key == "Z":
        return [
            [startPos[0]-1, startPos[1]-1],
            [startPos[0]-1, startPos[1]],
            [startPos[0], startPos[1]],
            [startPos[0], startPos[1]+1],
        ];
    elif key == "T":
        return [
            [startPos[0]-1, startPos[1]-1],
            [startPos[0]-1, startPos[1]],
            [startPos[0]-1, startPos[1]+1],
            [startPos[0], startPos[1]],
        ];
    raise Exception("Error key[{}]".format(key));
```

在游戏中，将方块分成了两种类型：移动中的和已固定的。  

其中，**移动中的**方块在每次移动时，会先检测是否能移动，若不能且本次移动方向是**向下的**，则会将这些方块设置为**已固定的**。


## 3. 定时器
每次定时器的回调中，将移动中的方块向下移动（如果可以移动的话），同时判定是否要对速度进行升级，是的话则会重置该定时器的时间间隔。  

## 4. 碰撞检测

## 5. 结束判断
