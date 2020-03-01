using System;
using System.Collections.Generic;
using System.Text;

namespace DesignPatterns {
    // 基础类
    public abstract class BaseObj {
        private string desc = "base";

        public virtual string getDeac() {
            return desc;
        }
        
        public abstract int getID();
    }

    // 修饰类
    public abstract class DecorateObj : BaseObj {
        public abstract string getDeac();
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
    public class DecorateTestObj : DecorateObj {
        private BaseObj baseObj;

        public DecorateTestObj(BaseObj baseObj) {
            this.baseObj = baseObj; 
        }

        public override string getDeac() {
            return baseObj.getDeac() + ", Decorate";
        }

        public override int getID() {
            return baseObj.getID() * 10;
        }
    }

    // 测试
    public class Test {
        public static void Main(string[] args) {
            TestObj testObj = new TestObj();
            Console.WriteLine("Desc: {0}, ID: {1}.", testObj.getDeac(), testObj.getID());

            // 进行装饰
            newTestObj = new DecorateTestObj(testObj);
            Console.WriteLine("Desc: {0}, ID: {1}.", newTestObj.getDeac(), newTestObj.getID());
            Console.ReadLine();
        }
    }
}