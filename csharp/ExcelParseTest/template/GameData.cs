using System;
using System.Reflection;
using System.Collections.Generic;

class GameData {
    
    public T Get<T>(object val) {
        return single<T>("Get", val);
    }
    public T Get<T>(object val, string key) {
        return single<T>("Get", val, key);
    }
    
    public T Find<T>(object val) {
        return single<T>("Find", val);
    }
    public T Find<T>(object val, string key) {
        return single<T>("Find", val, key);
    }
    
    public T[] GetAll<T>(object val) {
        return multiple<T>("GetAll", val);
    }
    public T[] GetAll<T>(object val, string key) {
        return multiple<T>("GetAll", val, key);
    }
    
    public T[] FindAll<T>(object val) {
        return multiple<T>("FindAll", val);
    }
    public T[] FindAll<T>(object val, string key) {
        return multiple<T>("FindAll", val, key);
    }

    // 校验参数
    bool verifyArgs(object obj, ref object[] args) {
        if (args.Length == 0) {
            return false;
        }
        if (args.Length == 1) {
            string defaultKey = obj.GetType().GetProperty("DefaultKey").GetValue(obj).ToString();
            args = new object[]{args[0], defaultKey};
        }
        return true;
    }

    T single<T>(string method, params object[] args) {
        Type dataType = typeof(T);
        MethodInfo methodInfo = dataType.GetMethod("TableData");
        if (methodInfo == null) {
            return default(T);
        }
        var obj = methodInfo.Invoke(null, null);
        if (!verifyArgs(obj, ref args)) {
            return default(T);
        }
        T ret = (T) obj.GetType().GetMethod(method).Invoke(obj, args);
        return ret;
    }
    
    T[] multiple<T>(string method, params object[] args) {
        Type dataType = typeof(T);
        MethodInfo methodInfo = dataType.GetMethod("TableData");
        if (methodInfo == null) {
            return new T[0];
        }
        var obj = methodInfo.Invoke(null, null);
        if (!verifyArgs(obj, ref args)) {
            return new T[0];
        }
        T[] ret = (T[]) obj.GetType().GetMethod(method).Invoke(obj, args);
        return ret;
    }
    
}
