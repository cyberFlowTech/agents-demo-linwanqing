import random

# Major Arcana
MAJOR_ARCANA = [
    {"name": "The Fool (愚者)", "meaning_upright": "新的开始，冒险，天真，潜力", "meaning_reversed": "鲁莽，冒险，不顾后果"},
    {"name": "The Magician (魔术师)", "meaning_upright": "力量，技巧，专注，行动，足智多谋", "meaning_reversed": "操纵，计划不周，潜能未发"},
    {"name": "The High Priestess (女祭司)", "meaning_upright": "直觉，神秘，潜意识，内在的声音", "meaning_reversed": "隐藏的议程，需要倾听内在声音"},
    {"name": "The Empress (皇后)", "meaning_upright": "丰饶，母性，创造力，自然，美", "meaning_reversed": "创造力受阻，依赖他人"},
    {"name": "The Emperor (皇帝)", "meaning_upright": "权威，结构，控制，父性", "meaning_reversed": "暴政，僵化，冷酷"},
    {"name": "The Hierophant (教皇)", "meaning_upright": "传统，顺从，道德，教育，信仰", "meaning_reversed": "叛逆，打破常规，新的信仰"},
    {"name": "The Lovers (恋人)", "meaning_upright": "爱，和谐，关系，价值观对齐，选择", "meaning_reversed": "不和谐，失衡，错误的价值观"},
    {"name": "The Chariot (战车)", "meaning_upright": "控制，意志力，胜利，决心", "meaning_reversed": "失控，缺乏方向，攻击性"},
    {"name": "Strength (力量)", "meaning_upright": "力量，勇气，耐心，控制，同情", "meaning_reversed": "软弱，自我怀疑，缺乏自律"},
    {"name": "The Hermit (隐士)", "meaning_upright": "内省，孤独，寻求真理，指引", "meaning_reversed": "孤独，孤立，迷失方向"},
    {"name": "Wheel of Fortune (命运之轮)", "meaning_upright": "好运，业力，生命周期，命运，转折点", "meaning_reversed": "厄运，抵抗变化，打破循环"},
    {"name": "Justice (正义)", "meaning_upright": "公正，真理，法律，因果", "meaning_reversed": "不公，缺乏责任，不诚实"},
    {"name": "The Hanged Man (倒吊人)", "meaning_upright": "暂停，投降，放手，新的视角", "meaning_reversed": "拖延，无谓的牺牲，停滞"},
    {"name": "Death (死神)", "meaning_upright": "结束，改变，转变，过渡", "meaning_reversed": "抵抗改变，无法放手"},
    {"name": "Temperance (节制)", "meaning_upright": "平衡，适度，耐心，目的", "meaning_reversed": "失衡，过度，缺乏长期愿景"},
    {"name": "The Devil (恶魔)", "meaning_upright": "束缚，上瘾，物质主义，性", "meaning_reversed": "摆脱束缚，通过力量重获自由"},
    {"name": "The Tower (高塔)", "meaning_upright": "突变，混乱，启示，觉醒", "meaning_reversed": "避免灾难，不仅是延迟"},
    {"name": "The Star (星星)", "meaning_upright": "希望，信仰，目的，更新，灵性", "meaning_reversed": "缺乏信仰，绝望，消极"},
    {"name": "The Moon (月亮)", "meaning_upright": "幻觉，恐惧，焦虑，潜意识，直觉", "meaning_reversed": "释放恐惧，压抑的情绪，困惑"},
    {"name": "The Sun (太阳)", "meaning_upright": "积极，有趣，温暖，成功，活力", "meaning_reversed": "暂时的消极，缺乏清晰"},
    {"name": "Judgement (审判)", "meaning_upright": "审判，重生，内在召唤，宽恕", "meaning_reversed": "自我怀疑，拒绝召唤"},
    {"name": "The World (世界)", "meaning_upright": "完成，整合，成就，旅行", "meaning_reversed": "未完成，缺乏封闭"},
]

class TarotDeck:
    def __init__(self):
        self.cards = MAJOR_ARCANA
    
    def draw_card(self):
        """Draws a random card and determines orientation."""
        card = random.choice(self.cards)
        is_upright = random.choice([True, False])
        
        return {
            "name": card["name"],
            "orientation": "正位" if is_upright else "逆位",
            "name_full": f"{card['name']} ({'正位' if is_upright else '逆位'})",
            "meaning": card["meaning_upright"] if is_upright else card["meaning_reversed"],
            "image": None # Placeholder for image URL if we add valid ones later
        }

    def get_three_card_spread(self):
        """Draws 3 unique cards for Past, Present, Future."""
        raw_cards = random.sample(self.cards, 3)
        spread = []
        for card in raw_cards:
            is_upright = random.choice([True, False])
            spread.append({
                "name": card["name"],
                "orientation": "正位" if is_upright else "逆位",
                 "name_full": f"{card['name']} ({'正位' if is_upright else '逆位'})",
                "meaning": card["meaning_upright"] if is_upright else card["meaning_reversed"]
            })
        return spread

    def get_simple_reading(self, user_name):
        card = self.draw_card()
        return (
            f"🔮 **{user_name} 的今日塔罗** 🔮\n\n"
            f"🃏 **牌面**: {card['name_full']}\n"
            f"✨ **解读**: {card['meaning']}\n\n"
            f"💡 *大师赠言*: 心诚则灵，命由己造。"
        )

    def generate_spread_interpretation(self, spread, question):
        """Generates a structured interpretation for a 3-card spread."""
        # Note: In a real app, this might call an LLM. Here we use templates/rules.
        
        # Simple rule-based summary
        positive_count = sum(1 for c in spread if "正位" in c['orientation'])
        
        if positive_count == 3:
            summary = "前途一片光明，天时地利人和。"
            advice_tone = "乘胜追击"
        elif positive_count == 2:
            summary = "整体趋势向好，但仍需克服小障碍。"
            advice_tone = "稳步前行"
        elif positive_count == 1:
            summary = "局势不明朗，存在挑战，需要谨慎行事。"
            advice_tone = "三思后行"
        else:
            summary = "当前面临较大阻力，需要彻底的反思和改变。"
            advice_tone = "韬光养晦"

        return (
            f"🔮 **塔罗解读**\n\n"
            f"✨ **总体结论**：\n{summary}\n\n"
            f"📌 **核心信息**：\n"
            f"1. 过去：{spread[0]['meaning']}\n"
            f"2. 现在：{spread[1]['meaning']}\n"
            f"3. 未来：{spread[2]['meaning']}\n\n"
            f"🧭 **行动建议**：\n"
            f"- {advice_tone}，保持冷静。\n"
            f"- 关注内在的指引。\n\n"
            f"⚠️ **提醒**：\n塔罗指引趋势，而非决定命运。"
        )
