
namespace DH.Robot {
    public class RobotOutCard {
        bool m_isCanOutCard;

        IEnumerator m_outCardCoroutinel;

        void startOutCard() {
            m_isCanOutCard = true;
            m_outCardCoroutinel = StartCoroutine(outCard());
        }
        
        void stopOutCard() {
            if (m_outCardCoroutinel != null) {
                StopCoroutine(m_outCardCoroutinel);
                m_outCardCoroutinel = null;
            }
        }

        // TODO: 抓牌之后
        void onNotifyRoundStard(RoundInfo roundInfo) {
            if (roundInfo.turn != Enemy) {
                return;
            }
            this.startOutCard();
        }

        void onNotifyRoundEnd(RoundInfo roundInfo) {
            if (roundInfo.turn != Enemy) {
                return;
            }
            this.stopOutCard();
        }

        void notifyOutCardEnd() {
            m_isCanOutCard = true;
        }

        IEnumerator outCard() {
            while (handCardList.Count > 0) {
                string cardUid = this.GetBestOutCard();
                if (cardUid.Length == 0) {
                    break;
                }
                // TODO: NET_C_OutCard.Send(req) == Success
                m_isCanOutCard = false;
                whilw (!m_isCanOutCard) {
                    yield return null;
                }
            }
            this.notifyRoundEnd();
        }

        public string GetBestOutCard() {
            // 过滤不能出的牌（是否足以消耗？是否效果中要求了手牌）
            // 消耗物: GP|AP|CardCount

            // 先按照卡牌类型排序后出牌
            //// 最大化收益（给每个效果添加评分？）【取最高评分来出？】
        }
    }
}