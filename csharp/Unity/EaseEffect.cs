using System.Collections;
using System.Collections.Generic;
using UnityEngine;
​
public enum EasingType {
    Linear,
    Ease,
}
​
[AddComponentMenu("GameScripts/EaseEffect")]
​
public class EaseEffect : MonoBehaviour
{
    Dictionary<EasingType, float[]> easingConfig = new Dictionary<EasingType, float[]>();
​
    public float m_duration = 2;
    float m_actualDuration;
​
    public Transform m_startTrans;
    public Transform m_endTrans;
    Vector3 m_startPos;
    Vector3 m_endPos;
​
    void Awake() {
        easingConfig.Add(EasingType.Linear, new float[]{0, 0, 1, 1});
        easingConfig.Add(EasingType.Ease, new float[]{0.25f, 0.1f, 0.25f, 1f});
        // todo: 添加其他类型的贝塞尔曲线参数
    }
​
    // Start is called before the first frame update
    void Start()
    {
        m_startPos = m_startTrans.position;
        m_endPos = m_endTrans.position;
        print(string.Format("EaseEffect Start: {0}, {1}", m_startPos, m_endPos));
    }
​
    // Update is called once per frame
    void Update()
    {
        if (m_duration <= 0 || m_actualDuration > m_duration) {
            return;
        }
        m_actualDuration += Time.deltaTime;
        float rate = GetProgressVal(m_actualDuration/m_duration, EasingType.Ease);
        print(string.Format("EaseEffect Update Rate: {0}", rate));
        Vector3 targetPos = m_startPos + (m_endPos - m_startPos) * rate;
        this.transform.position = targetPos;
    }
​
    public void ResetActualDuration() {
        m_actualDuration = 0;
    }
​
    // 获取阶乘结果
    public int Factorial(int num) {
        int result = 1;
        for (int i = 1; i <= num; i++) {
            result *= i;
        }
        return result;
    }
​
    public Vector2 Bezier(float t, List<Vector2> pList) {
        if (pList.Count == 0) {
            return Vector2.zero;
        } else if (pList.Count < 2) {
            return pList[0];
        }
        // 使用一般定义式
        Vector2 result = Vector2.zero;
        int n = pList.Count - 1;
        for (int i = 0; i <= n; i++) {
            float coefficient = (float)Factorial(n) / (float)(Factorial(i) * Factorial(n - i));
            result += coefficient * pList[i] * Mathf.Pow(1-t, n-i) * Mathf.Pow(t, i);
        }
        return result;
        // 直接使用3阶定义式
        // return Mathf.Pow(1-t, 3) * pList[0] + 3*t*Mathf.Pow(1-t, 2) * pList[1] + 3 * t * t *(1-t) * pList[2] + Mathf.Pow(t, 3) * pList[3];
    }
    
    // 获取对应x的进度值
    // @params x 理想值
    // @params easingType 缓动类型
    // @params err 误差系数
    public float GetProgressVal(float x, EasingType easingType, float err = 0.01f) {
        if (!easingConfig.ContainsKey(easingType)) {
            return 0;
        }
        float[] easingCfg = easingConfig[easingType];
        List<Vector2> pList = new List<Vector2>();
        pList.Add(new Vector2(0, 0));
        pList.Add(new Vector2(easingCfg[0], easingCfg[1]));
        pList.Add(new Vector2(easingCfg[2], easingCfg[3]));
        pList.Add(new Vector2(1, 1));
        Vector2 bPos = Vector2.one;
        float t = 1, mid = 1;
        err = Mathf.Max(err, 0);
        int limit = 10000; // 避免函数死循环
        while (Mathf.Abs(bPos.x - x) > err) {
            mid = mid/2f;
            if (bPos.x > x) {
                t -= mid;
            } else {
                t += mid;
            }
            bPos = Bezier(t, pList);
            limit--;
            if (limit < 0) {
                print("GetProgressVal break!");
                break;
            }
        }
        return bPos.y;
    }
}