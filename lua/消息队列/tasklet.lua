---
-- tasklet库，更多同步操作见@{network.http2} @{network.socket2}
-- @module tasklet
-- @usage
-- local tasklet = require('tasklet')
--
-- @usage
-- -- run dynamic animations sequeucely.
-- local Am = require('animation')
-- tasklet.spawn(function()
--     while true do
--         tasklet.animate(Am.prop('x', 0, 100), Am.updator(sprite))
--         tasklet.sleep(0.5)
--         tasklet.animate(Am.prop('x', 100, 0), Am.updator(sprite))
--     end
-- end)
--
-- @usage
-- -- cancel a tasklet
-- local Http = require('network.http2')
-- tasklet.spawn(function()
--     local sprite = ...
--     local loading = tasklet.spawn(function()
--         while true do
--             sprite.rotation = sprite.rotation + tasklet.sleep(0.1)
--         end
--     end)
--     local rsp = http.request{url = 'http://www.boyaa.com'}
--     tasklet.cancel(loading)
-- end)

local M = {}

local function resume_task(task, ...)
    if task.paused then
        task.pending_args = {...}
        return
    end
    local success
    success, task.action = coroutine.resume(task.coroutine, ...)
    if not success then
        local msg = debug.traceback(task.coroutine, task.action)
        print(msg)
    elseif task.action then
        task.action(function(...)
            resume_task(task, ...)
        end)
        return
    end
end

---
-- 启动微线程。
-- @function [parent=#tasklet] spawn
-- @param #function fn
-- @param ... 传给fn的参数。
-- @usage
-- tasklet.spawn(function(arg1, arg2)
--     while true do
--         local dt = tasklet.sleep(0.1)
--         sprite.x = sprite.x + dt * 10
--     end
-- end, arg1, arg2)
function M.spawn(fn, ...)
    local co = coroutine.create(fn)
    local task = {
        coroutine = co,
    }
    resume_task(task, ...)
    return task
end
---
-- 停止微线程。
-- @function [parent=#tasklet] cancel
function M.cancel(task)
    if not task.action then
        return 'invalid task status'
    end
    if type(task.action) == 'table' and task.action.cancel then
        task.action:cancel()
    end
    task.paused = true
    task.action = nil
end

---
-- 暂停微线程。
-- @function [parent=#tasklet] pause
function M.pause(task)
    assert(task.action, 'invalid task status')
    if type(task.action) == 'table' and task.action.pause then
        task.action:pause()
    else
        task.paused = true
    end
end

---
-- 恢复微线程。
-- @function [parent=#tasklet] resume
function M.resume(task)
    assert(task.action, 'invalid task status')
    if type(task.action) == 'table' and task.action.resume then
        task.action:resume()
    else
        resume_task(task, unpack(task.pending_args))
    end
end

---
-- 在微线程中执行，暂停 n 秒
-- @function [parent=#tasklet] sleep
-- @param #number n
function M.sleep(n)
    -- sleep action
    return coroutine.yield(setmetatable({
        _handler = nil,
        cancel = function(self)
            if self._handler then
                self._handler:cancel() -- 取消定时器
            end
        end,
        pause = function(self)
            if self._handler then
                self._handler.paused = true -- 暂停定时器
                return true
            end
            return false
        end,
        resume = function(self)
            if self._handler then
                self._handler.paused = false -- 恢复定时器
                return true
            end
            return false
        end,
    }, {
        __call = function(self, callback)
            self._handler = schedule_once(callback, n) -- n毫秒后执行一次callback，返回定时器句柄
        end
    }))
end

return M
