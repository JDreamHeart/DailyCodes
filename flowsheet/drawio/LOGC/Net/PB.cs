using System;
using System.Collections;
using System.Collections.Generic;

namespace DH.Net {

    // 游戏数据
    public struct GameInfo {
        public PlayerInfo player;
    }

    // 玩家数据
    public struct PlayerInfo {
        public string name; // 玩家名称
        public int skillId; // 当前安装的技能
        public StatusInfo[] statusList; // 当前状态列表
        public int gp; // 鬼气值
        public int hp; // 生命值
        public int exp; // 经验值
        public int ap; // 行动点
        public int cardCount; // 卡包中的卡牌数
    }

    // 状态数据
    public struct StatusInfo {
        public int id;
        public float val;
    }


    // 检测版本请求
    public struct CheckVersionReq {
        public string version;
    }

    // 检测版本回调
    public struct CheckVersionRsp {
        public int code;
        public string version;
        public string downloadUrl;
    }

    // 登陆请求
    public struct LoginReq {
        public string name;
        public string password;
    }

    // 创建角色
    public struct CreateRoleReq {
        public string name;
    }


}