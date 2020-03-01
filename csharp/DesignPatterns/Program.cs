using System;

namespace DesignPatterns
{
    // 基础类
    public abstract class BaseObj {
        protected string desc = "base";

        public virtual string getDeac() {
            return desc;
        }
        
        public abstract int getID();
    }

    // 测试类
    public class TestObj : BaseObj {
        public TestObj() {
            desc = "test"; 
        }

        public override int getID() {
            return 233;
        }
    }

    // 修饰实现类
    public class DecorateTestObj : BaseObj {
        private BaseObj baseObj;

        public DecorateTestObj(BaseObj baseObj) {
            this.baseObj = baseObj; 
        }

        public override string getDeac() {
            return "Decorate[" + baseObj.getDeac() + "]";
        }

        public override int getID() {
            return baseObj.getID() * 10;
        }
    }

    class Program
    {
        static void Main(string[] args)
        {
            TestObj testObj = new TestObj();
            Console.WriteLine("Desc: {0}, ID: {1}.", testObj.getDeac(), testObj.getID());

            // 进行装饰
            DecorateTestObj newTestObj = new DecorateTestObj(testObj);
            Console.WriteLine("Desc: {0}, ID: {1}.", newTestObj.getDeac(), newTestObj.getID());
            Console.ReadLine();
        }
    }
}
