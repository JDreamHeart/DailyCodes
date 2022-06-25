using System;

namespace DH.Net {
    public class Service {
        
        // 检测版本回调
        public delegate void t_checkVersionRsp(CheckVersionRsp rsp);
        public t_checkVersionRsp CheckVersionRsp;
        protected void f_checkVersionRsp(CheckVersionRsp rsp) {
            if (CheckVersionRsp != null) {
                CheckVersionRsp(rsp);
            }
        }

        // 获取游戏信息
        public delegate void t_getGameInfoRsp(GameInfo gameInfo);
        public t_getGameInfoRsp GetGameInfoRsp;
        protected void f_getGameInfoRsp(GameInfo gameInfo) {
            if (GetGameInfoRsp != null) {
                GetGameInfoRsp(gameInfo);
            }
        }

    }

    public class GameService : Service {

        // 检测版本
        public void CheckVersionReq(CheckVersionReq req) {

            // 回调
            CheckVersionRsp rsp = new CheckVersionRsp();
            f_checkVersionRsp(rsp);
        }

        // 登陆
        public void LoginReq(LoginReq req) {

        }

        // 创建角色请求
        public void CreateRoleReq(CreateRoleReq req) {

        }
    }
}