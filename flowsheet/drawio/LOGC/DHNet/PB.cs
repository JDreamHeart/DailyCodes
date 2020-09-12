using System;

namespace DH.Net {
    public class Service {
        public delegate void LoginReq(LoginReq req);
        public delegate GetGameInfoRsp GetGameInfoReq(GetGameInfoReq req);
    }
}