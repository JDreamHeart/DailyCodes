-- @Author: JimZhang
-- @Date:   2018-07-06 21:08:13
-- @Last Modified by:   JimDreamHeart
-- @Last Modified time: 2018-07-07 17:27:51

local Matrix = import(".Matrix");

local mat = {};

function mat.create(data, row, col)
	return Matrix.new(data, row, col);
end

return mat;