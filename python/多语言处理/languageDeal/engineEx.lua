--文字对应的字符串表
local defaultLanguage = {
}

-- 重写label.props
local labelOldProps = UI.Label.props
UI.Label.props = function(self,props)
    if props.text then
    	if defaultLanguage[props.text] then
    		if s_glb_str[defaultLanguage[props.text]] then
    			props.text = s_glb_str[defaultLanguage[props.text]]
    		end
    	end
    end
    return labelOldProps(self,props)
end

-- 重写button.props
local buttonOldProps = UI.Button.props
UI.Button.props = function(self,arg)
    if arg.label then
    	if defaultLanguage[arg.label] then
    		local key = defaultLanguage[arg.label]
    		if s_glb_str[key] then
    			arg.label = s_glb_str[key]
    		end
    	end
    end
    return buttonOldProps(self,arg)
end

-- 重写inputView.props
local inputViewOldProps = UI.InputView.props
UI.InputView.props = function(self,arg)
    if arg.placeholder then
    	if defaultLanguage[arg.placeholder] then
    		local key = defaultLanguage[arg.placeholder]
    		if s_glb_str[key] then
    			arg.placeholder = s_glb_str[key]
    		end
    	end
    end
    return inputViewOldProps(self,arg)
end




