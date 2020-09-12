using System;
using System.Collections.Generic;

public class TemplateRowX {

}

namespace ExcelParseTest
{
    public class Service {
        static Service m_instance;
        public static Service Instance {
            get {
                if (m_instance == null) {
                    m_instance = new Service();
                }
                return m_instance;
            }
        }
        
        public delegate int t_loginReq(TemplateRowX req);
        public static t_loginReq NET_LoginReq;
        protected int f_loginReq(TemplateRowX req) {
            if (NET_LoginReq != null) {
                return NET_LoginReq(req);
            }
            return default(int);
        }

        public delegate void t_getGameInfoReq(TemplateRowX req);
        public static t_getGameInfoReq NET_GetGameInfoReq;
        protected void f_getGameInfoReq(TemplateRowX req) {
            if (NET_GetGameInfoReq != null) {
                NET_GetGameInfoReq(req);
            }
        }

        public void Test(TemplateRowX req) {
            f_getGameInfoReq(req);
        }
    }

    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("========= Start ========");
            Run();
            Console.WriteLine("========= End ========");
        }

        static void Run() {
            // GameData gd = new GameData();
            // Console.WriteLine(gd);
            // var ret = gd.Get<TemplateRow>("1001");
            // var ret1 = gd.Find<TemplateRow>(1001, "key");
            // var ret2 = gd.Find<TemplateRowX>(10011);
            // var ret3 = gd.GetAll<TemplateRow>(1001);
            // var ret4 = gd.FindAll<TemplateRow>("1001");
            // Console.WriteLine("========= Ret ======== {0}, {1}, {2}, {3}, {4}", ret, ret1, ret2==null, ret3.Length, ret4.Length);

            Service.NET_GetGameInfoReq += test;
            Service.Instance.Test(new TemplateRowX());
        }

        public static void test(TemplateRowX req) {
            Console.WriteLine("2333333");
        }
    }
}
