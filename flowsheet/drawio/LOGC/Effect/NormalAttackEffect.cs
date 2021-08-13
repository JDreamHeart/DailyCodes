using System;


namespace DH.Logic {

    public class NormalAttackEffect: EffectBase {
        EffectGrid m_effectGrid;

        public bool IsValid() {
            return false;  // 一次即失效
        }

        public void HandleData(EffectDataBoard dataBoard) {
            dataBoard.normalDamage += m_val;
        }

        public void HandleUI(void effectInfo) {

        }

        public void Attach(EffectGrid effectGrid) {
            m_effectGrid = effectGrid;
        }

        public void Detach() {
            Destroy(m_effectGrid);
        }
    }

}