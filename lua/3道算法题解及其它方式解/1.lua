
local number = {"1", "2", "3", "4", "5", "6", "7", "8", "9", "0"}
local numberLen = #number

function printNumberTable(number)
	local str = number[1]
	for i=2, numberLen do
		str = str .. number[i]
	end
	print(str)
end

function permutation(number, begin)
	if begin > numberLen-1 then
		printNumberTable(number)
	else
		for temp = begin, numberLen do
			if number[1] == "0" then
				break
			end
			number[begin], number[temp] = number[temp], number[begin];
			permutation(number, begin+1)
			number[begin], number[temp] = number[temp], number[begin];
		end
	end
end

local o = os.time();
permutation(number, 1)
print("时间开销" .. (os.time() - o) .. "秒");
