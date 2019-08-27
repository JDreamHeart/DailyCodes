Dim args
args = ""
For i = 0 to WScript.Arguments.Count-1
	args = args + " " + WScript.Arguments(i)
Next

Set ws = CreateObject("Wscript.Shell")
ws.run "cmd /c start run.bat"+args,0