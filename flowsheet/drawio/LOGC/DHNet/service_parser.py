import os;
import re;

PB_FILE_PATH = os.path.join(os.getcwd(), "PB.cs");
SERVICE_FILE_PATH = os.path.join(os.getcwd(), "Service.cs");

class ServiceParser(object):

    def getServiceName(self, serviceName):
        return serviceName + "Impl";

    def replaceServiceName(self, line, serviceName):
        return line.replace(serviceName, self.getServiceName(serviceName), 1);
    
    def getInstance(self, serviceName):
        newServiceName = self.getServiceName(serviceName);
        return f"""
        static {newServiceName} m_instance;
        public static {newServiceName} Instance {{
            get {{
                if (m_instance == null) {{
                    m_instance = new {newServiceName}();
                }}
                return m_instance;
            }}
        }}
""";

    def getTemplate(self, ret, func, argType, arg):
        funcContent = f"""
            if (NET_{func} != null) {{
                NET_{func}({arg});
            }}""";
        if ret != "void":
            funcContent = f"""
            if (NET_{func} != null) {{
                return NET_{func}({arg});
            }}
            return default({ret});""";

        return f"""
        public delegate {ret} TYPE_{func}({argType} {arg});
        public static TYPE_{func} NET_{func};
        protected {ret} CALL_{func}({argType} {arg}) {{{funcContent}
        }}
""";
    
    def parse(self, inputPath, outputPath):
        if not os.path.exists(inputPath):
            return;
        newContent = "";
        with open(inputPath, "r+") as f:
            isLackClassBraceLeft, serviceName = False, "";
            for line in f.readlines():
                ret = re.search("public\s+class\s+(\w*Service)", line);
                if ret:
                    isLackClassBraceLeft = True;
                    serviceName = ret.group(1);
                    line = self.replaceServiceName(line, serviceName);
                if isLackClassBraceLeft:
                    braceLeftIdx = line.find("{");
                    if braceLeftIdx >= 0:
                        newContent += "".join([line[:braceLeftIdx+1], self.getInstance(serviceName), line[braceLeftIdx+1:]])
                        isLackClassBraceLeft = False;
                        serviceName = "";
                        continue;
                if not ret:
                    ret = re.search("public\s+delegate\s+(\w+)\s+(\w+)\s*\((\w+)\s+(\w+)\);", line);
                    if ret:
                        newContent += self.getTemplate(ret.group(1), ret.group(2), ret.group(3), ret.group(4));
                        continue;
                newContent += line;
        with open(outputPath, "w+") as f:
            f.write(newContent);

if __name__ == "__main__":
    s = ServiceParser();
    s.parse(PB_FILE_PATH, SERVICE_FILE_PATH);