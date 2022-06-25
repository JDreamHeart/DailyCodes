using System;
using System.IO;
using System.Runtime.Serialization.Formatters.Binary;
using System.Collections;
using System.Collections.Generic;

namespace JsonParse
{
    [Serializable]
    public struct GameData {
        public int gid;
        public string content;
        public PlayerData player;
    }

    [Serializable]
    public struct PlayerData {
        public int id;
        public string name;
    }

// #################################################################################

    public class BasePData {
        public int id = 1;

        public int type;

        public virtual void SetType(int type) {
            this.type = type;
            Console.WriteLine(string.Format("========== BasePData ===========", this.type));
        }

    }

    public class PData : BasePData {
        public string name = "PlayerData";

        public override void SetType(int type) {
            this.type = type * 2;
            Console.WriteLine(string.Format("========== PData ===========", this.type));
        }
    }

    public class BaseGData {
        protected BasePData m_pData;

        public BaseGData() {
            Console.WriteLine("--------- BaseGData ------------");
        }

        public void SetPData(BasePData pData) {
            m_pData = pData;
        }

        public void SetPType(int type) {
            m_pData.SetType(type);
        }
    }

    public class GData : BaseGData {
        public PData pData {
            get {
                return (PData) this.m_pData;
            }
        }
        
        public GData() {
            Console.WriteLine("--------- GData ------------");
        }

    }

    class Program
    {
        public static void TestSerializable() {
            GameData game = new GameData();
            game.gid = 1001;
            game.content = "It is game data!";
            PlayerData player = new PlayerData();
            player.id = 233;
            player.name = "测试名称";
            game.player = player;
            
            MemoryStream memoryStream = new MemoryStream();
            BinaryFormatter binaryFormatter = new BinaryFormatter();
            binaryFormatter.Serialize(memoryStream, game);
            string serializedStr = System.Convert.ToBase64String(memoryStream.ToArray());
            Console.WriteLine(string.Format("=========== serializedStr ========== {0}", serializedStr));

            byte[] restoredBytes = System.Convert.FromBase64String(serializedStr);
            MemoryStream restoredMemoryStream = new MemoryStream(restoredBytes);
            BinaryFormatter restoreBinaryFormatter = new BinaryFormatter();
            object deserializedObj = restoreBinaryFormatter.Deserialize(restoredMemoryStream);
            GameData gameData = (GameData) deserializedObj;
            Console.WriteLine(string.Format("=========== deserializedObj ========== {0}, {1}", gameData.gid, gameData.player.id));

            List<string> m_strList = new List<string>();
            m_strList.Add("111222");
            m_strList.Add("333444");
            Console.WriteLine(string.Format("========== m_strList ========= {0}", m_strList.ToString()));
        }
        
        public static void TestDataInherit() {
            GData gData = new GData();
            PData pData = new PData();
            gData.SetPData(pData);
            gData.SetPType(1);
            Console.WriteLine(gData.pData.type);
        }

        public static void TestDefaultKey() {
            GameData gData = GetDataInfo<GameData>();
            Console.WriteLine(gData);
            Console.WriteLine(gData.gid);
        }

        public static T GetDataInfo<T>() {
            return default(T);
        }
        
        static void Main(string[] args)
        {
            // TestDataInherit();
            TestDefaultKey();
        }
    }
}
