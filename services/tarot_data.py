import random

# Major Arcana - 专业版塔罗牌库
MAJOR_ARCANA = [
    {
        "name": "The Fool (愚者)", 
        "meaning_upright": "新的开始，冒险，天真，潜力", 
        "meaning_reversed": "鲁莽，冒险，不顾后果",
        "deep_meaning_upright": "站在悬崖边缘的愚者，象征着人生旅程的起点。这是一个充满无限可能的时刻，宇宙在召唤你迈出勇敢的第一步。放下恐惧，拥抱未知，你内在的智慧会指引方向。",
        "deep_meaning_reversed": "当愚者逆位时，他提醒你：勇气与鲁莽之间只有一线之隔。现在可能不是冒险的最佳时机，过度的天真可能让你陷入险境。请在行动前三思，确保你的选择建立在理性之上。"
    },
    {
        "name": "The Magician (魔术师)", 
        "meaning_upright": "力量，技巧，专注，行动，足智多谋", 
        "meaning_reversed": "操纵，计划不周，潜能未发",
        "deep_meaning_upright": "魔术师手持权杖，掌控四大元素。这张牌告诉你：此刻的你拥有实现梦想所需的一切资源和能力。天时地利人和皆已具备，只需集中意志，化思想为行动，奇迹将会显现。",
        "deep_meaning_reversed": "逆位的魔术师警示着能量的错误使用。你可能将才华用于操纵他人，或是拥有技能却迟迟不敢施展。重新审视你的动机，让能量流向正确的方向，莫让天赋白白浪费。"
    },
    {
        "name": "The High Priestess (女祭司)", 
        "meaning_upright": "直觉，神秘，潜意识，内在的声音", 
        "meaning_reversed": "隐藏的议程，需要倾听内在声音",
        "deep_meaning_upright": "女祭司守护着神圣的知识之门，她提醒你：并非所有真理都能用言语表达。此刻你需要倾听内心深处的声音，相信直觉的指引。答案不在外界喧嚣中，而在你灵魂深处的宁静里。",
        "deep_meaning_reversed": "当女祭司逆位，你可能与内在智慧失去了连接。外界的噪音掩盖了直觉的低语，或是有人在刻意隐瞒真相。这是重新建立内在连接的时刻，静心冥想，让迷雾散去。"
    },
    {
        "name": "The Empress (皇后)", 
        "meaning_upright": "丰饶，母性，创造力，自然，美", 
        "meaning_reversed": "创造力受阻，依赖他人",
        "deep_meaning_upright": "皇后象征着大地母亲的丰盛与慈爱。这是创造与孕育的能量，无论是新项目、新关系还是新生命。宇宙的丰盛正在向你流淌，放松身心，让创造力自然绽放，美好将会降临。",
        "deep_meaning_reversed": "逆位的皇后暗示创造力被压抑或枯竭。你可能过度依赖他人的照顾，或是忽视了自我滋养。是时候重新连接你的创造源泉，学会先爱自己，才能更好地滋养他人。"
    },
    {
        "name": "The Emperor (皇帝)", 
        "meaning_upright": "权威，结构，控制，父性", 
        "meaning_reversed": "暴政，僵化，冷酷",
        "deep_meaning_upright": "皇帝坐于王座之上，代表秩序与权威。他告诉你：现在是建立结构、制定规则的时刻。用理性和逻辑掌控局面，发挥领导力，为梦想搭建稳固的框架，成功需要纪律与坚持。",
        "deep_meaning_reversed": "当皇帝逆位时，权威可能变为暴政。过度的控制欲让人窒息，僵化的规则阻碍发展。或许你正被某种权威压制，是时候重新审视权力的边界，寻找刚性与柔性的平衡。"
    },
    {
        "name": "The Hierophant (教皇)", 
        "meaning_upright": "传统，顺从，道德，教育，信仰", 
        "meaning_reversed": "叛逆，打破常规，新的信仰",
        "deep_meaning_upright": "教皇是传统智慧的守护者，他提醒你：不必重新发明轮子。前人的经验和传统的教导中蕴含着宝贵的智慧。此刻适合寻求导师指引，遵循既定的道路，在传统中找到属于你的位置。",
        "deep_meaning_reversed": "逆位的教皇召唤着叛逆的灵魂。传统的束缚可能已不再适合你，是时候打破陈旧的信念，寻找属于自己的真理。真正的智慧不在教条中，而在你勇敢质疑的过程里。"
    },
    {
        "name": "The Lovers (恋人)", 
        "meaning_upright": "爱，和谐，关系，价值观对齐，选择", 
        "meaning_reversed": "不和谐，失衡，错误的价值观",
        "deep_meaning_upright": "恋人牌代表着神圣的结合与和谐。这不仅关乎爱情，更是价值观的共鸣。你正面临重要的选择，听从内心真实的呼唤，选择与你灵魂共振的道路。真正的和谐来自内在的一致性。",
        "deep_meaning_reversed": "当恋人逆位，关系中的不和谐显现。价值观的冲突、沟通的障碍，或是内心的矛盾让你痛苦。这是重新审视关系和选择的时刻，诚实面对内心，不要为了和谐而牺牲真实的自己。"
    },
    {
        "name": "The Chariot (战车)", 
        "meaning_upright": "控制，意志力，胜利，决心", 
        "meaning_reversed": "失控，缺乏方向，攻击性",
        "deep_meaning_upright": "战车手驾驭两匹相反方向的马，象征着意志力与掌控力的胜利。你正在正确的道路上前进，即使面对相反的力量，坚定的决心会带你走向成功。保持专注，胜利就在前方。",
        "deep_meaning_reversed": "逆位的战车暗示你失去了方向感。内在的矛盾让你停滞不前，或是过度的侵略性让你偏离轨道。放慢脚步，重新审视目标，找回内在的平衡，才能重新出发。"
    },
    {
        "name": "Strength (力量)", 
        "meaning_upright": "力量，勇气，耐心，控制，同情", 
        "meaning_reversed": "软弱，自我怀疑，缺乏自律",
        "deep_meaning_upright": "真正的力量不在于暴力，而在于温柔。这张牌中，女子用爱与耐心驯服雄狮。你拥有战胜任何挑战的内在力量，关键是用同情心对待自己和他人。柔能克刚，耐心与勇气将为你赢得一切。",
        "deep_meaning_reversed": "当力量逆位，内在的恐惧与自我怀疑占据上风。你可能对自己过于严苛，或是缺乏面对困难的勇气。重新连接你的内在力量，记住：你比想象中更强大，温柔对待自己是勇气的表现。"
    },
    {
        "name": "The Hermit (隐士)", 
        "meaning_upright": "内省，孤独，寻求真理，指引", 
        "meaning_reversed": "孤独，孤立，迷失方向",
        "deep_meaning_upright": "隐士举起明灯，独自行走在寂静的山巅。这是灵魂探索的时刻，你需要暂时远离喧嚣，向内寻找答案。在独处中，你会找到真正的智慧。真理的光芒，只在静默中才能显现。",
        "deep_meaning_reversed": "逆位的隐士警示着过度的孤立。你可能将自己封闭在象牙塔中，与世界失去连接，或是在独处中迷失方向。适度的独处是智慧，过度的孤立则是逃避。是时候重新与外界建立连接了。"
    },
    {
        "name": "Wheel of Fortune (命运之轮)", 
        "meaning_upright": "好运，业力，生命周期，命运，转折点", 
        "meaning_reversed": "厄运，抵抗变化，打破循环",
        "deep_meaning_upright": "命运之轮永不停息地转动，提醒着万物循环的真理。你正处于生命的转折点，好运即将降临。接受变化，顺应宇宙的节奏，你会发现一切都是最好的安排。命运的齿轮正朝着有利于你的方向转动。",
        "deep_meaning_reversed": "当命运之轮逆转，挑战与困境接踵而至。但请记住：轮子总会继续转动，低谷之后必是高峰。不要抗拒变化，这可能是宇宙在推动你打破旧有的循环，走向新的可能。"
    },
    {
        "name": "Justice (正义)", 
        "meaning_upright": "公正，真理，法律，因果", 
        "meaning_reversed": "不公，缺乏责任，不诚实",
        "deep_meaning_upright": "正义女神手持天平与利剑，象征着宇宙的因果法则。你的行为会得到公正的回报，善有善报，恶有恶报。此刻需要做出基于真理和公正的决定，诚实面对自己，宇宙的天平不会失衡。",
        "deep_meaning_reversed": "逆位的正义暗示着不公与失衡。你可能正遭受不公平的待遇，或是逃避应负的责任。诚实面对真相，即使它令人不安。只有直面因果，才能重新找回内在的平衡。"
    },
    {
        "name": "The Hanged Man (倒吊人)", 
        "meaning_upright": "暂停，投降，放手，新的视角", 
        "meaning_reversed": "拖延，无谓的牺牲，停滞",
        "deep_meaning_upright": "倒吊人自愿悬挂，换取新的视角与智慧。有时候，停下来比前进更重要。此刻需要放下执着，从不同角度看待问题。在暂停中，你会获得意想不到的洞见。臣服于当下，答案会自然显现。",
        "deep_meaning_reversed": "当倒吊人逆位，停滞变成了拖延。你可能在做无谓的牺牲，或是困在某种局面中无法自拔。是时候重新行动起来，停止扮演受害者，主动打破僵局，重新掌控自己的人生。"
    },
    {
        "name": "Death (死神)", 
        "meaning_upright": "结束，改变，转变，过渡", 
        "meaning_reversed": "抵抗改变，无法放手",
        "deep_meaning_upright": "死神并非终结，而是转化的开始。旧的必须死去，新的才能诞生。你正经历深刻的蜕变，虽然过程可能痛苦，但这是必经之路。拥抱变化，放下过去，凤凰涅槃，重生即将到来。",
        "deep_meaning_reversed": "逆位的死神显示你在抗拒必然的改变。死死抓住已经死去的东西，只会让痛苦延续。放手并不意味着失败，而是为新生腾出空间。停止抵抗，让该结束的自然结束。"
    },
    {
        "name": "Temperance (节制)", 
        "meaning_upright": "平衡，适度，耐心，目的", 
        "meaning_reversed": "失衡，过度，缺乏长期愿景",
        "deep_meaning_upright": "天使在水流间自如地调和，象征着完美的平衡与和谐。此刻需要中庸之道，避免极端。耐心地整合对立的元素，在看似矛盾的事物间找到平衡点。时间会证明，温和与适度是最强大的力量。",
        "deep_meaning_reversed": "节制逆位时，平衡被打破。你可能走向了某个极端，过度纵欲或过度节制。缺乏耐心让你急功近利，忽视了长远的目标。重新找回中心，在平衡中才能走得更远。"
    },
    {
        "name": "The Devil (恶魔)", 
        "meaning_upright": "束缚，上瘾，物质主义，性", 
        "meaning_reversed": "摆脱束缚，通过力量重获自由",
        "deep_meaning_upright": "恶魔牌揭示着我们自己制造的牢笼。欲望、上瘾、物质的诱惑让你成为囚徒。但请仔细看：锁链是松的，你随时可以逃脱。觉察到束缚的本质，认清什么在控制你，这是解脱的第一步。",
        "deep_meaning_reversed": "逆位的恶魔带来解放的信息。你正在或即将打破束缚你的枷锁。无论是戒除不良习惯，还是摆脱有毒关系，自由就在前方。继续保持觉知，重新夺回对生命的掌控权。"
    },
    {
        "name": "The Tower (高塔)", 
        "meaning_upright": "突变，混乱，启示，觉醒", 
        "meaning_reversed": "避免灾难，不仅是延迟",
        "deep_meaning_upright": "雷电击中高塔，一切轰然倒塌。这是最令人恐惧却也最解放的牌。建立在虚假基础上的结构必须崩塌，真理才能显现。混乱之后是觉醒，毁灭之后是重建。接受这场风暴，它在为你清理障碍。",
        "deep_meaning_reversed": "逆位的高塔暗示灾难可能被推迟，但并未真正避免。你可能在抗拒必要的改变，勉强维持摇摇欲坠的结构。与其被动等待崩塌，不如主动拆除，在掌控中转型总比被动崩溃要好。"
    },
    {
        "name": "The Star (星星)", 
        "meaning_upright": "希望，信仰，目的，更新，灵性", 
        "meaning_reversed": "缺乏信仰，绝望，消极",
        "deep_meaning_upright": "暴风雨后，星星在夜空中闪耀。这是希望与疗愈的能量，宇宙在告诉你：最黑暗的时刻已经过去。保持信念，继续前行，你正走在正确的道路上。灵性的甘露正在滋养你的灵魂，重生已经开始。",
        "deep_meaning_reversed": "当星星逆位，希望的光芒似乎黯淡了。你可能陷入绝望，对未来失去信心。但请记住：星星依然存在，只是暂时被乌云遮蔽。重新连接你的信念，即使是微弱的希望之光，也能指引你走出黑暗。"
    },
    {
        "name": "The Moon (月亮)", 
        "meaning_upright": "幻觉，恐惧，焦虑，潜意识，直觉", 
        "meaning_reversed": "释放恐惧，压抑的情绪，困惑",
        "deep_meaning_upright": "月光下，一切都不如看起来那样。月亮牌警示着幻象与恐惧，你可能正处于迷雾中，难以分辨真实与虚幻。相信直觉，但不要被恐惧支配。穿越这片迷雾需要勇气，潜意识中有宝藏，也有怪兽。",
        "deep_meaning_reversed": "逆位的月亮暗示恐惧正在消散，或是你开始看清真相。压抑的情绪可能浮上水面，虽然痛苦，但这是疗愈的开始。不要逃避内心的阴影，正视它们，困惑会逐渐变为清晰。"
    },
    {
        "name": "The Sun (太阳)", 
        "meaning_upright": "积极，有趣，温暖，成功，活力", 
        "meaning_reversed": "暂时的消极，缺乏清晰",
        "deep_meaning_upright": "太阳普照大地，驱散一切阴霾。这是塔罗牌中最积极的能量，代表成功、喜悦与生命力。你的努力即将开花结果，真理大白于天下。尽情享受这份温暖与光明，你值得拥有这一切美好。",
        "deep_meaning_reversed": "即使太阳逆位，它依然在天空中。你可能暂时感到低落，或是成功被延迟，但这只是暂时的阴云。调整心态，重拾乐观，太阳的光芒终将再次照耀在你身上。"
    },
    {
        "name": "Judgement (审判)", 
        "meaning_upright": "审判，重生，内在召唤，宽恕", 
        "meaning_reversed": "自我怀疑，拒绝召唤",
        "deep_meaning_upright": "天使的号角响起，唤醒沉睡的灵魂。这是觉醒与重生的时刻，你被召唤去活出更高的人生目的。过去的一切经历都在为此刻做准备。宽恕自己和他人，回应内在的召唤，新的生命篇章即将开启。",
        "deep_meaning_reversed": "逆位的审判显示你在回避内在的召唤。自我怀疑让你裹足不前，或是你拒绝承认需要改变的真相。倾听那个微弱的声音，它在呼唤你成为更好的自己。不要再拖延，是时候回应了。"
    },
    {
        "name": "The World (世界)", 
        "meaning_upright": "完成，整合，成就，旅行", 
        "meaning_reversed": "未完成，缺乏封闭",
        "deep_meaning_upright": "世界牌象征着完满与成就，一个循环的圆满结束。你已经走过了漫长的旅程，整合了所学的一切智慧。此刻值得庆祝，你到达了重要的里程碑。但记住：每个结束都是新开始的前奏。",
        "deep_meaning_reversed": "当世界逆位，目标尚未完成，或是你感到缺少某种闭环。可能是外在的阻碍，也可能是内在尚未准备好。不要气馁，审视还需要完成什么，再坚持一下，完满就在不远处。"
    },
]

class TarotDeck:
    def __init__(self):
        self.cards = MAJOR_ARCANA
    
    def draw_card(self):
        """Draws a random card and determines orientation."""
        card = random.choice(self.cards)
        is_upright = random.choice([True, False])
        
        # 使用 meaning 字段作为关键词来源
        keywords = card["meaning_upright"] if is_upright else card["meaning_reversed"]
        
        return {
            "name": card["name"],
            "orientation": "正位" if is_upright else "逆位",
            "name_full": f"{card['name']} ({'正位' if is_upright else '逆位'})",
            "meaning": card["meaning_upright"] if is_upright else card["meaning_reversed"],
            "deep_meaning": card["deep_meaning_upright"] if is_upright else card["deep_meaning_reversed"],
            "keywords": keywords,  # 使用 meaning 作为关键词
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
                "meaning": card["meaning_upright"] if is_upright else card["meaning_reversed"],
                "deep_meaning": card["deep_meaning_upright"] if is_upright else card["deep_meaning_reversed"]
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

    def _get_question_category(self, question: str) -> str:
        """根据问题关键词判断类别"""
        question_lower = question.lower()
        
        if any(word in question_lower for word in ['工作', '事业', '职业', '升职', '跳槽', '换工作', '创业', '项目']):
            return 'career'
        elif any(word in question_lower for word in ['爱情', '恋爱', '感情', '喜欢', '表白', '复合', '分手', '结婚', '对象']):
            return 'love'
        elif any(word in question_lower for word in ['金钱', '财运', '赚钱', '投资', '理财', '收入', '经济']):
            return 'money'
        elif any(word in question_lower for word in ['健康', '身体', '疾病', '治疗', '养生']):
            return 'health'
        elif any(word in question_lower for word in ['学习', '考试', '学业', '考研', '留学']):
            return 'study'
        else:
            return 'general'

    def _get_one_line_advice(self, category: str, positive_count: int) -> str:
        """生成一句话核心建议(20字以内)"""
        advice_map = {
            'career': {
                3: "趁热打铁,主动争取晋升或新机会",
                2: "稳扎稳打,展示你的专业能力",
                1: "韬光养晦,先积累实力再出手",
                0: "停下来反思,可能方向需要调整"
            },
            'love': {
                3: "真诚表达,勇敢迈出那一步",
                2: "保持沟通,用心经营这段关系",
                1: "理性观察,别被一时激情冲昏头",
                0: "学会放手,勉强没有幸福"
            },
            'money': {
                3: "财运亨通,可适当投资但别贪心",
                2: "稳健理财,避免冲动消费",
                1: "守住本金,暂时别碰高风险投资",
                0: "控制开支,重新审视财务规划"
            },
            'health': {
                3: "精力充沛,保持良好生活习惯",
                2: "注意休息,劳逸结合最重要",
                1: "警惕信号,该检查就去检查",
                0: "重视健康,立即改掉不良习惯"
            },
            'study': {
                3: "学习高效,这是突破的好时机",
                2: "方法对了,坚持就能看到成果",
                1: "遇到瓶颈,换个角度试试",
                0: "状态不佳,调整心态重新开始"
            },
            'general': {
                3: "运势极佳,大胆去做想做的事",
                2: "方向正确,保持耐心稳步前行",
                1: "三思后行,避免冲动决策",
                0: "接受改变,这是蜕变的时机"
            }
        }
        
        return advice_map.get(category, advice_map['general']).get(positive_count, "听从内心的声音")
    
    def _generate_card_relationship(self, spread) -> str:
        """
        生成牌与牌之间的关联解读
        分析三张牌的正逆位组合，生成完整的因果故事线
        """
        # 获取每张牌的状态
        past_positive = "正位" in spread[0]['orientation']
        present_positive = "正位" in spread[1]['orientation']
        future_positive = "正位" in spread[2]['orientation']
        
        # 根据三张牌的正逆位组合(8种情况)生成故事线
        pattern = (
            ('P' if past_positive else 'R') +
            ('P' if present_positive else 'R') +
            ('P' if future_positive else 'R')
        )
        
        # 8种能量流动模式
        relationship_map = {
            'PPP': "过去的积累正在开花结果,现在的努力延续好运,未来充满希望。这是完美的正向循环,继续保持!",
            
            'PPR': "过去和现在都很顺利,但要警惕未来的转折。前期的成功可能让你放松警惕,记得善始善终。",
            
            'PRP': "过去打下了好基础,虽然现在遇到阻碍,但这只是暂时的考验。坚持过去的方向,曙光就在前方。",
            
            'PRR': "过去的优势正在消退,现在的困境可能延续到未来。是时候反思策略,不要让沉没成本拖累你。",
            
            'RPP': "过去的困难成为宝贵经验,现在开始好转,未来值得期待。你正走出低谷,保持信心前行!",
            
            'RPR': "过去虽艰难但现在有起色,可惜未来可能再遇波折。把握当下机会,为可能的反复做好准备。",
            
            'RRP': "长期的困境即将结束,转机已现。所有苦难都是为了最后的蜕变,黎明就在眼前,再坚持一下!",
            
            'RRR': "这是深刻的转化期,旧模式必须彻底打破。虽然痛苦,但这是重生的必经之路,接受改变才能涅槃。"
        }
        
        return relationship_map.get(pattern, "能量在流动变化,需要灵活应对当下的局面。")
    
    def _analyze_card_transition(self, card1: dict, card2: dict, transition_type: str) -> str:
        """
        分析两张牌之间的能量转换
        transition_type: "past_to_present" 或 "present_to_future"
        """
        card1_positive = "正位" in card1['orientation']
        card2_positive = "正位" in card2['orientation']
        
        card1_name = card1['name'].split('(')[0].strip()
        card2_name = card2['name'].split('(')[0].strip()
        
        if transition_type == "past_to_present":
            # 过去到现在的转换
            if card1_positive and card2_positive:
                transitions = [
                    f"过去{card1_name}的能量延续至今,{card2_name}正是前期积累的开花结果",
                    f"从{card1_name}到{card2_name},正向能量不断累积,形势越来越好",
                    f"{card1_name}为{card2_name}打下了坚实基础,好运在持续"
                ]
            elif card1_positive and not card2_positive:
                transitions = [
                    f"过去{card1_name}虽好,但{card2_name}逆位提醒你:成功可能带来松懈",
                    f"从{card1_name}到{card2_name}逆位,顺境中出现了需要警惕的信号",
                    f"{card1_name}的优势正在消退,{card2_name}逆位是转折的预警"
                ]
            elif not card1_positive and card2_positive:
                transitions = [
                    f"过去{card1_name}逆位的困境正在结束,{card2_name}带来了转机",
                    f"从{card1_name}逆位到{card2_name},你正在走出低谷,曙光已现",
                    f"{card1_name}逆位的教训成为养分,{card2_name}是重生的开始"
                ]
            else:  # 两张都逆位
                transitions = [
                    f"从{card1_name}逆位到{card2_name}逆位,困境还在延续,需要更深层的改变",
                    f"{card1_name}逆位的问题未解决,{card2_name}逆位显示阻碍在累积",
                    f"能量持续低迷,从{card1_name}到{card2_name}都在提醒你必须调整"
                ]
        
        else:  # present_to_future
            # 现在到未来的转换
            if card1_positive and card2_positive:
                transitions = [
                    f"现在{card1_name}的努力将在未来开花,{card2_name}是美好的预示",
                    f"从{card1_name}到{card2_name},能量在正向累积,未来值得期待",
                    f"{card1_name}正为{card2_name}的到来铺路,保持当前方向"
                ]
            elif card1_positive and not card2_positive:
                transitions = [
                    f"现在{card1_name}虽好,但{card2_name}逆位警告:要防范未来的变数",
                    f"从{card1_name}到{card2_name}逆位,需要在当下就做好应对准备",
                    f"{card1_name}的优势可能无法延续,{card2_name}逆位提醒善始善终"
                ]
            elif not card1_positive and card2_positive:
                transitions = [
                    f"现在{card1_name}逆位虽艰难,但{card2_name}显示未来会好转",
                    f"从{card1_name}逆位到{card2_name},这是黎明前的黑暗,坚持住",
                    f"{card1_name}逆位是暂时的考验,{card2_name}承诺了光明的未来"
                ]
            else:  # 两张都逆位
                transitions = [
                    f"从{card1_name}逆位到{card2_name}逆位,困境可能持续,需要彻底转变",
                    f"{card1_name}逆位的问题若不解决,{card2_name}逆位显示会延续到未来",
                    f"当前的挑战未结束,{card2_name}逆位提醒必须在当下就行动"
                ]
        
        return random.choice(transitions)
    
    def _generate_complete_story(self, spread) -> str:
        """
        根据三张牌生成完整的叙事故事
        """
        past_card = spread[0]['name'].split('(')[0].strip()
        present_card = spread[1]['name'].split('(')[0].strip()
        future_card = spread[2]['name'].split('(')[0].strip()
        
        past_pos = "正位" in spread[0]['orientation']
        present_pos = "正位" in spread[1]['orientation']
        future_pos = "正位" in spread[2]['orientation']
        
        # 根据正逆位组合生成叙事
        pattern = (
            ('P' if past_pos else 'R') +
            ('P' if present_pos else 'R') +
            ('P' if future_pos else 'R')
        )
        
        story_templates = {
            'PPP': f"这是一个充满祝福的旅程。{past_card}为你打下了坚实的基础,{present_card}让你正处于最佳状态,{future_card}则预示着美好的结局。三股正向能量汇聚,宇宙在为你开绿灯,大胆前行吧!",
            
            'PPR': f"前路需要警惕。{past_card}和{present_card}给了你良好的开端,但{future_card}逆位提醒:不要被前期的顺利冲昏头脑。越接近成功越要谨慎,善始还需善终。",
            
            'PRP': f"这是一次暂时的低谷。{past_card}证明你的方向是对的,虽然{present_card}逆位带来了阻碍,但{future_card}承诺了光明的未来。坚持住,这只是黎明前的黑暗。",
            
            'PRR': f"需要及时止损。{past_card}的优势正在消失,{present_card}逆位显示问题已经出现,{future_card}逆位警告可能恶化。不要让沉没成本拖累你,该调整就调整,该放手就放手。",
            
            'RPP': f"恭喜你正在走出困境!{past_card}逆位的艰难时期已经过去,{present_card}带来了转机,{future_card}预示着越来越好。过去的苦难都是养分,美好的明天在向你招手。",
            
            'RPR': f"形势在反复波动。{past_card}逆位后出现了{present_card}的好转,但{future_card}逆位提示可能再次遇到挑战。把握当下的机会,同时为可能的反复做好心理准备。",
            
            'RRP': f"长夜即将结束。{past_card}逆位和{present_card}逆位让你经历了漫长的困难期,但{future_card}显示曙光已现。所有的苦难都是为了最后的蜕变,再坚持一下,胜利就在前方!",
            
            'RRR': f"这是深刻的转化期。{past_card}逆位、{present_card}逆位、{future_card}逆位,三重逆境迫使你彻底改变。虽然痛苦,但这是破茧成蝶的必经之路。旧的不去新的不来,接受转变,迎接重生。"
        }
        
        return story_templates.get(pattern, f"{past_card}、{present_card}、{future_card}的能量组合显示,局势复杂多变,需要灵活应对。")
    
    def _get_advice_by_category(self, category: str, spread) -> str:
        """根据问题类别生成针对性建议"""
        # 分析牌面趋势
        positive_count = sum(1 for c in spread if "正位" in c['orientation'])
        
        advice_templates = {
            'career': {
                3: "事业运势极佳，这是展现才华的最佳时机。把握机遇，勇敢迈出那一步，宇宙会助你一臂之力。",
                2: "事业发展稳中向好，但需要克服某些障碍。保持专业态度，用智慧化解难题，成功指日可待。",
                1: "职场环境复杂，需要谨慎行事。此刻不宜冒进，先韬光养晦，积蓄力量，等待更好的时机。",
                0: "事业正面临重大考验。这是宇宙在提醒你：是时候深刻反思了。必要的改变虽艰难，却是通往成功的必经之路。"
            },
            'love': {
                3: "爱情能量充盈，真心会得到回应。相信直觉，勇敢表达，幸福就在不远处。若已有伴侣,关系将更上一层楼。",
                2: "感情整体向好,但需要双方共同努力。真诚沟通,相互理解,小波折反而会让关系更坚固。",
                1: "感情之路并不平坦,需要冷静思考。不要被一时的激情蒙蔽双眼,听从内心最真实的声音。",
                0: "感情正处于重大转折点。有些关系该放下就要放下,执着只会带来更多痛苦。相信结束即是新开始。"
            },
            'money': {
                3: "财运亨通,投资有道。但切记不可贪心,稳健前行才是长久之计。",
                2: "财务状况稳定,有小幅增长。保持理性,避免冲动消费,细水长流方能聚财。",
                1: "财运波动较大,需谨慎理财。此刻不宜冒险投资,守住本金比追求暴利更重要。",
                0: "财务面临挑战,可能有意外支出。重新审视金钱观,学会取舍,物质的匮乏往往是精神富足的契机。"
            },
            'health': {
                3: "身心状态良好,精力充沛。保持健康的生活方式,定期检查,预防胜于治疗。",
                2: "整体健康,但需注意某些小问题。多倾听身体的信号,适当休息,劳逸结合。",
                1: "身心压力较大,需要特别关注。学会放松,调整作息,必要时寻求专业帮助。",
                0: "健康亮起红灯,这是身体在警告你。务必重视,改变不良习惯,治病也要医心。"
            },
            'study': {
                3: "学业运势极佳,悟性大开。此刻的努力会事半功倍,保持专注,成功在望。",
                2: "学习进展顺利,但需持续努力。找对方法,合理规划,稳扎稳打方能厚积薄发。",
                1: "学习遇到瓶颈,需要调整策略。不要气馁,换个角度思考,突破就在眼前。",
                0: "学习状态低迷,需要彻底反思。找出问题根源,可能需要寻求他人指导,重建学习系统。"
            },
            'general': {
                3: "整体运势极佳,一切顺遂。把握当下,勇敢前行,宇宙正在为你铺路。",
                2: "大方向正确,虽有小挑战,但无碍大局。保持信念,稳步前行,终将达成所愿。",
                1: "前路迷雾重重,需要谨慎决策。静心思考,向内寻找答案,不要被外界左右。",
                0: "正处于重大转折期,虽有困难,但这是蜕变的阵痛。接受改变,在混乱中寻找新秩序。"
            }
        }
        
        return advice_templates.get(category, advice_templates['general'])[positive_count]

    def generate_brief_interpretation(self, spread, question):
        """生成精简版塔罗解读 - 结论优先布局"""
        category = self._get_question_category(question)
        positive_count = sum(1 for c in spread if "正位" in c['orientation'])
        
        # 1. 一句话结论 + 星级评分
        if positive_count == 3:
            verdict = "✅ 大吉 - 天时地利人和,放手去做!"
            stars = "🌟🌟🌟🌟🌟"
        elif positive_count == 2:
            verdict = "🟢 吉 - 整体有利,把握机会"
            stars = "🌟🌟🌟🌟"
        elif positive_count == 1:
            verdict = "🟡 平 - 谨慎行事,三思后行"
            stars = "🌟🌟"
        else:
            verdict = "🔴 慎 - 暂缓行动,重新规划"
            stars = "🌟"
        
        # 2. 一句话核心建议
        one_line_advice = self._get_one_line_advice(category, positive_count)
        
        # 3. 生成牌阵故事线(新增 - 关联解读)
        story_arc = self._generate_card_relationship(spread)
        
        # 4. 极简牌面信息(只显示牌名,不显示详细含义)
        card_symbols = {
            0: "🔹",  # 逆位
            1: "🔸"   # 正位
        }
        
        brief_cards = " | ".join([
            f"{card_symbols[1 if '正位' in c['orientation'] else 0]}{['过去','现在','未来'][i]}:{c['name'].split('(')[0].strip()}"
            for i, c in enumerate(spread)
        ])
        
        # 5. 组合结果 - 精简换行,信息紧凑
        return (
            f"{verdict} {stars}\n"
            f"💡 {one_line_advice}\n\n"
            f"🎴 {brief_cards}\n"
            f"🔗 {story_arc}\n\n"
            f"👉 点击【详细解读】查看完整分析"
        )

    def generate_spread_interpretation(self, spread, question):
        """生成专业级塔罗解读 - 强化牌面关联"""
        # 判断问题类别
        category = self._get_question_category(question)
        
        # 计算正位数量和星级
        positive_count = sum(1 for c in spread if "正位" in c['orientation'])
        
        if positive_count == 3:
            stars = "🌟🌟🌟🌟🌟"
            overall = "【Overall: Excellent (极好)】\n牌阵呈现完美的能量流动，三张正位牌象征着宇宙的全力支持。此刻天时地利人和皆已具备，这是千载难逢的黄金时机。"
        elif positive_count == 2:
            stars = "🌟🌟🌟🌟"
            overall = "【Overall: Favorable (有利)】\n整体能量趋向正面，虽有小波折但大势已定。两张正位牌显示主导力量偏向积极，只需保持信念、稳步前行，便能达成所愿。"
        elif positive_count == 1:
            stars = "🌟🌟"
            overall = "【Overall: Caution (警示)】\n牌面显示局势复杂，正反能量交织。此刻需要格外谨慎，深思熟虑每一个决定。挑战与机遇并存，唯有保持清醒的头脑，才能在迷雾中找到正确的道路。"
        else:
            stars = "🌟"
            overall = "【Overall: Transformation (转化)】\n三张逆位牌预示着重大的转折期。旧有的模式必须打破，这是痛苦却必要的蜕变过程。虽然眼前困难重重，但这正是宇宙在推动你走向更高的维度。"
        
        # 生成开场白
        openings = [
            "✨ 我看到了你的问题在星空中激起涟漪...",
            "🔮 塔罗的智慧开始流淌,让我为你解读命运的密语...",
            "🌙 牌面已展开,宇宙正在诉说你的故事...",
            "⭐ 我感受到你内心的召唤,让塔罗为你指引方向..."
        ]
        opening = random.choice(openings)
        
        # 生成详细的三张牌解读 + 关联分析
        past_reading = (
            f"【过去】{spread[0]['name_full']}\n"
            f"{spread[0]['deep_meaning']}\n"
            f"💫 这张牌揭示: {spread[0]['meaning']}"
        )
        
        # 现在牌 - 与过去建立联系
        past_to_present = self._analyze_card_transition(spread[0], spread[1], "past_to_present")
        present_reading = (
            f"【现在】{spread[1]['name_full']}\n"
            f"{spread[1]['deep_meaning']}\n"
            f"💫 这张牌揭示: {spread[1]['meaning']}\n"
            f"🔗 承接过去: {past_to_present}"
        )
        
        # 未来牌 - 与过去和现在建立联系
        present_to_future = self._analyze_card_transition(spread[1], spread[2], "present_to_future")
        future_reading = (
            f"【未来】{spread[2]['name_full']}\n"
            f"{spread[2]['deep_meaning']}\n"
            f"💫 这张牌揭示: {spread[2]['meaning']}\n"
            f"🔗 发展脉络: {present_to_future}"
        )
        
        # 生成完整故事线
        complete_story = self._generate_complete_story(spread)
        
        # 生成针对性建议
        specific_advice = self._get_advice_by_category(category, spread)
        
        # 生成行动指引
        action_guides = []
        for i, card in enumerate(spread):
            position = ["关于过去", "关于现在", "关于未来"][i]
            if "正位" in card['orientation']:
                action_guides.append(f"✦ {position}: 把握这股正向能量,顺势而为")
            else:
                action_guides.append(f"✦ {position}: 觉察到挑战,调整策略应对")
        
        # 生成大师结语
        endings = [
            "记住:塔罗是镜子,映照的是你内心的智慧。答案一直都在你心中。",
            "命运并非刻在石头上,你的每个选择都在书写未来。",
            "牌面只是提示,真正的力量在于你如何回应。相信自己,你比想象中更强大。",
            "宇宙的指引已给予,接下来的路要靠你自己走。祝福你,勇敢的灵魂。"
        ]
        ending = random.choice(endings)
        
        # 组合完整解读 - 减少换行
        full_interpretation = (
            f"{opening}\n"
            f"{overall} {stars}\n\n"
            f"{past_reading}\n\n"
            f"{present_reading}\n\n"
            f"{future_reading}\n\n"
            f"━━━━━━━━━━━━━━━━━\n"
            f"【完整故事线】\n{complete_story}\n\n"
            f"【大师建议】\n{specific_advice}\n\n"
            f"【行动指引】\n" + "\n".join(action_guides) + "\n\n"
            f"🕯️ {ending}"
        )
        
        return full_interpretation
