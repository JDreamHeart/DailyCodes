using System;

namespace DH.Net {
    public class ServiceImpl {
        static ServiceImpl m_instance;
        public static ServiceImpl Instance {
            get {
                if (m_instance == null) {
                    m_instance = new ServiceImpl();
                }
                return m_instance;
            }
        }


        public delegate void TYPE_LoginReq(LoginReq req);
        public static TYPE_LoginReq NET_LoginReq;
        protected void CALL_LoginReq(LoginReq req) {
            if (NET_LoginReq != null) {
                NET_LoginReq(req);
            }
        }

        public delegate GetGameInfoRsp TYPE_GetGameInfoReq(GetGameInfoReq req);
        public static TYPE_GetGameInfoReq NET_GetGameInfoReq;
        protected GetGameInfoRsp CALL_GetGameInfoReq(GetGameInfoReq req) {
            if (NET_GetGameInfoReq != null) {
                return NET_GetGameInfoReq(req);
            }
            return default(GetGameInfoRsp);
        }
    }
}