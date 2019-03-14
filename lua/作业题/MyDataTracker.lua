local DataTracker = {};

DataTracker._t = {};

function DataTracker:trackingDataModify(obj,trackers,isAssert)

	--未传obj或trackers，直接return，不执行以下逻辑
	if (not obj) or (not trackers) then
		return;
	end

	--判断是否需要设置元表
	local isSetMetatable = false;
	if not obj._trackers then
		obj._trackers = {};
		isSetMetatable = true;
	end
	--保存新增监控键值
	for _,tv in pairs(trackers) do
		self._t[obj] = self._t[obj] or {};
		if not self._t[obj][tv] then
			self._t[obj][tv] = {_times = 1, _isAssert = isAssert};
		else
			self._t[obj][tv]._isAssert = isAssert;
		end
		if not obj._trackers[tv] then
			obj._trackers[tv] = obj[tv];
		end
		obj[tv] = nil;
	end

	if isSetMetatable then
		--设置元表
		local mt = {
			__index = function(t,k)
				if t._trackers and t._trackers[tv] then
					return t._trackers[tv];
				else
					return rawget(t,k);
				end
			end,
			__newindex = function(t,k,v)
				if self._t[obj] and self._t[obj][k] and self._t[obj][k]._times then
					if not self._t[obj][k]._isAssert then
						print(string.format("第%d次修改键值为%s的字段，修改前值为：%s，修改后值为：%s。%s\n",
							self._t[obj][k]._times,
							tostring(k),
							tostring(t._trackers[k]), 
							tostring(v),
							debug.traceback("",2)
						));
						self._t[obj][k]._times = self._t[obj][k]._times + 1;
						t._trackers[k] = v;
					else
						assert(false,"第"..tostring(self._t[obj][k]._times or 1).."次修改键值为“"..tostring(k).."”的字段，此次你没权限修改！！");
					end
				else
					if t._trackers and t._trackers[k] then
						t._trackers[k]= nil;
					end
					rawset(t,k,v);
				end
			end
		};
		setmetatable(obj, mt);
	end
end


--测试一下

local test = {kk = "vv", kkk = "vvv"};

DataTracker:trackingDataModify(test,{"kk"});
test.kk = 0;
test.kk = "什么鬼";

DataTracker:trackingDataModify(test,{"kkk"},false);
test.kkk = "试一试";
DataTracker._t[test] = {};
-- DataTracker:trackingDataModify(test,{"kkk"},true);
test.kkk = "重置一下结果～";

print(test.kkk)
