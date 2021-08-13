using System;


namespace DH.Logic {

    // 在触发战斗内的效果类型（RoleAttrChange除外）后，均需对己方和敌方触发RoleAttrChange类型
    // 有分敌我的类型有：RoleAttrChange
    public enum TriggerType {
        FightStart, // 战斗开始触发效果（一般用于诅咒效果）
        Settle, // 结算时触发效果（一般用于诅咒效果）
        FightEnd, // 战斗结束触发效果（一般用于诅咒效果）
        
        RoleAttrChange, // 角色属性变更时触发效果【注意进行标记已触发该类型，从而避免属性变更和触发效果互相循环】
        RoleDefend, // 在触发己方和敌方的RoleAttrChange后，触发该类型

        RoundStart, // 回合开始时触发效果
        RoundEnd, // 回合结束时触发效果

        BeforeOutCard, // 出牌前触发效果（一般用于检测当前出牌是否生效）
        OutCard, // 出牌时触发效果【紧接着触发AfterXXOutCard】
        AfterMasterOutCard, // 己方出牌后触发效果
        AfterEnemyOutCard, // 敌方出牌后触发效果

        UseSkill, // 使用技能时触发效果

        MasterDiscard, // 己方弃牌（主动或被动）时触发效果
        EnemyDiscard, // 敌方弃牌（主动或被动）时触发效果
    }

    public interface EffectBase {
        bool IsValid();
        bool HandleData(EffectDataBoard dataBoard);  // 返回值：是否成功触发
        void HandleUI(void effectInfo);
    }

    public class EffectDataBoardItem {
        Int64 normalDamage; // 普通伤害
        Int64 weirdDamage; // 诡气伤害
    }

    public class EffectDataBoard {
        void m_gData;
        
        public void gData {
            get {
                return m_gData;
            }
        }

        public void fightData {
            get {
                return;
            }
        }
        
        public EffectDataBoard(void gData) {
            m_gData = gData;
        }

        bool m_isInverse = false;
        public void SetInverse(bool isInverse=true) {
            m_isInverse = isInverse;
        }

        EffectDataBoardItem m_masterData = new EffectDataBoardItem();
        EffectDataBoardItem m_enemyData = new EffectDataBoardItem();

        public EffectDataBoardItem masterData {
            get {
                if (m_isInverse) {
                    return m_enemyData;
                }
                return m_masterData;
            }
        }

        public EffectDataBoardItem enemyData {
            get {
                if (m_isInverse) {
                    return m_masterData;
                }
                return m_enemyData;
            }
        }

        public bool isOutCardSucc = true;  // 是否成功出牌

        public List<Int64> triggerEffectList = new List<Int64>();  // 成功触发的效果ID列表

    }

    public class EffectMgr {
        List<EffectBase> m_effectList = new List<EffectBase>();

        EffectListUI m_effectListUI;

        public void pbData {
            get {
                return;
            }
        }

        public void AddEffect(EffectInfo effectInfo) {
            EffectBase effect = new EffectBase(effectInfo);

            // TODO:根据效果类型将效果插入到合适位置
            m_effectList.Add(effect);
            
            if (m_effectListUI != null) {
                EffectGrid effectGrid = m_effectListUI.AddEffect(effect);
                effect.Attach(effectGrid);
            }

        }
        
        public void RemoveEffect(EffectBase effect) {
            effect.Detach();
            m_effectList.Remove(effect);
        }

        public void RemoveEffect(EffectType effectType) {
            List<EffectBase> rmList = new List<EffectBase>();
            foreach (EffectBase effect in m_effectList) {
                if (effect.type == effectType) {
                    rmList.Add(effect);
                }
            }
            foreach (EffectBase effect in rmList) {
                this.RemoveEffect(effect);
            }
        }

        public EffectDataBoard TriggerEffect(TriggerType type, EffectDataBoard dataBoard) {
            List<EffectBase> rmList = new List<EffectBase>();
            foreach (EffectBase effect in m_effectList) {
                effect.HandleData(dataBoard);
                if (!effect.IsValid()) {
                    rmList.Add(effect);
                }
            }

            foreach (EffectBase effect in rmList) {
                this.RemoveEffect(effect);
            }
        }

        public void RefreshEffect(void pbData) {
            if (m_effectListUI == null) {
                return;
            }

            // TODO: 先删掉不存在的效果

            // TODO: 根基pbData处理效果相关UI
            foreach (EffectBase effect in m_effectList) {
                effect.HandleUI(effectInfo);
            }

            // TODO: 新增效果
            this.AddEffect(effectInfo);
        }
    }
}