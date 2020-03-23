-------------------------------------------------------------------------------
-- Prints logging information to console
--
-- @author Thiago Costa Ponte (thiago@ideais.com.br)
--
-- @copyright 2004-2011 Kepler Project
--
-------------------------------------------------------------------------------

-- function string.split(str, delimiter)
-- 	if (delimiter == '') then return false end
-- 	local pos, arr = 0, {}
-- 	-- for each divider found
-- 	for st, sp in function() return string.find(str, delimiter, pos, true) end do
-- 		table.insert(arr, string.sub(str, pos, st - 1))
-- 		pos = sp + 1
-- 	end
-- 	table.insert(arr, string.sub(str, pos))
-- 	return arr
-- end

import"logging"

function logging.console(logPattern)
    return logging.new( function(self, level, message)
		local msg = logging.prepareLogMsg(logPattern, os.date(), level, message);
        return  msg
    end
    )
end

return logging.console

