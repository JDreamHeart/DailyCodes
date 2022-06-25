import os;

SERVICE_NAME = "Service.cs"

def getServicePath():
    return os.path.join(os.getcwd(), SERVICE_NAME);

def getTemplate(func, params):
    func = func.capitalize();
    funcFirstLower = func[0].lower() + s[1:];
    return f"""
        public delegate void t_{funcFirstLower}({params} rsp);
        public t_{funcFirstLower} {func};
        protected void f_{funcFirstLower}({params} rsp) {{
            if ({func} != null) {{
                {func}(rsp);
            }}
        }}
""";