using System;
using System.Reflection;
using System.Collections.Generic;

class GameData {

    T single<T>(string method, object val, string key) {
        Type dataType = typeof(T);
        var obj = dataType.GetMethod("TableData").Invoke(null, null);
        T ret = (T) obj.GetType().GetMethod(method).Invoke(obj, new object[]{val, key});
        return ret;
    }
    
    T[] multiple<T>(string method, object val, string key) {
        Type dataType = typeof(T);
        var obj = dataType.GetMethod("TableData").Invoke(null, null);
        T[] ret = (T[]) obj.GetType().GetMethod(method).Invoke(obj, new object[]{val, key});
        return ret;
    }
    
    public T Get<T>(object val, string key) {
        return single<T>("Get", val, key);
    }
    
    public T Find<T>(object val, string key) {
        return single<T>("Find", val, key);
    }
}
