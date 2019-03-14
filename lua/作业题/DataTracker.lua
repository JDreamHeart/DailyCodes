 --- //[[OjorsOu@boyaa.com|欧卓鸿]] 2017/10/23 19:37//
## 数据变更追踪（DataTracker）
### 使用场景
> 当发现某个数据通过日志比较难看出问题，vs debug又比较耗时的时候，可以使用DataTracker进行该数据的变化追踪。


### 接口

```lua
  --[[
      @param obj 需要监控的目标
      @param keys 需要监控的字段
  ]]
  DataTracker.trackingDataModify(obj, keys)  
  
  --[[
      值为1表示非中断监控，输出修改次数与对应位置栈信息；
      值为2表示中断监控，修改马上抛出error中断运行；
      没有值默认为1；
  ]]
  keys = { k1 = 1, k2 = 2, "k3"}
```

### 使用案例
  * **中断追踪**
    * 这种方式会在修改处中断程序的运行，并以error的形式抛出修改处的栈信息


```lua

  -- Useage：
  local user = { nickName = "Jay", money = 100, seat = 1, mid = 1001 }
  local traceKeys = { money = 2 } -- 监控money字段的变化
  DataTracker.trackingDataModify(user, traceKeys)
        
  user.money = 50
```

```lua
  -- Output：
  开始监控：money
  lua: ...n\framework\common\BYFramework\tools\DataTracker.lua:77: 你没权限创建或修改 -> money
  stack traceback:
  [C]: in function 'error'
  ...n\framework\common\BYFramework\tools\DataTracker.lua:77: in function 
  <...n\framework\common\BYFramework\tools\DataTracker.lua:66>
  ...n\framework\common\BYFramework\tools\DataTracker.lua:93: in main chunk
  [C]: ?
```

  * **非中断追踪**
    * 这种方式区别于中断方式，数据修改时不会中断程序运行，而是输出数据的修改次数和修改处的栈信息


```lua

  -- Useage：
  local user = { nickName = "Jay", money = 100, seat = 1, mid = 1001 }
  local traceKeys = { "nickName", money = 1 } -- 监控nickName（默认为1）、money字段的变化
  DataTracker.trackingDataModify(user, traceKeys)
        
  user.nickName = "Kay"
  user.money = 200
  user.money = 300
  
```

```lua

  -- Output：
  开始监控：nickName, money
  第1次修改nickName，上次值：Jay，当前值：Kay
  stack traceback:
	...n\framework\common\BYFramework\tools\DataTracker.lua:74: in function <...n\framework\common\BYFramework\tools\DataTracker.lua:66>
	...n\framework\common\BYFramework\tools\DataTracker.lua:94: in main chunk
	[C]: ?
  第1次修改money，上次值：100，当前值：200
  stack traceback:
	...n\framework\common\BYFramework\tools\DataTracker.lua:74: in function <...n\framework\common\BYFramework\tools\DataTracker.lua:66>
	...n\framework\common\BYFramework\tools\DataTracker.lua:95: in main chunk
	[C]: ?
  第2次修改money，上次值：200，当前值：300
  stack traceback:
	...n\framework\common\BYFramework\tools\DataTracker.lua:74: in function <...n\framework\common\BYFramework\tools\DataTracker.lua:66>
	...n\framework\common\BYFramework\tools\DataTracker.lua:96: in main chunk
	[C]: ?
  
```