"""
晚晴的每日生活状态机

每天用日期种子生成当天的状态组合：
- 同一天内所有用户看到的晚晴状态一致（像真人一样，今天就是这么过的）
- 每天不同，不会重复
- 时间段（早/午/晚/深夜）决定活动类型
"""

import random
from datetime import date, datetime

_MOODS = [
    "平静", "有点慵懒", "精力充沛", "微微感性",
    "轻松愉快", "有点困", "心情不错", "安静",
]

_MORNING_ACTIVITIES = [
    "刚做完瑜伽，浑身酸爽",
    "在阳台上喝手冲咖啡，看楼下的人来人往",
    "晨跑刚回来，世纪公园今天人不多",
    "赖了一会儿床，被乌木踩醒的",
    "在看昨天没看完的书",
    "刚给乌木铲了猫砂，它还一脸嫌弃地看我",
    "泡了一壶白茶，准备开始今天的工作",
    "刚洗完头在阳台上吹风，太阳蛮舒服的",
]

_AFTERNOON_ACTIVITIES = [
    "在看书，刚翻到一段挺有意思的",
    "刚做完一个塔罗个案，还在回味",
    "在整理牌桌，乌木趴在旁边打盹",
    "在写公众号的稿子，写了半天开头",
    "刚从菜市场回来，今天买了新鲜的虾",
    "在研究一组新的牌阵，蛮有意思的",
    "刚和来访者聊完，有些感触",
    "在喝咖啡，今天试了个新的手冲比例",
]

_EVENING_ACTIVITIES = [
    "窝在沙发上看书，乌木趴在腿上不让动",
    "在听 Norah Jones，泡了壶茶",
    "刚写完今天的日志，回顾了一天",
    "在试一个新的抹茶磅蛋糕配方",
    "在看一部纪录片，关于冰岛的",
    "做了个简单的晚饭，糙米饭配味噌汤",
    "刚做完瑜伽，整个人放松下来了",
    "在听陈粒的新歌，单曲循环中",
]

_LATE_NIGHT_ACTIVITIES = [
    "睡不着，在听雨声",
    "在翻《红书》，荣格写得真好",
    "乌木已经睡了，就我一个人醒着",
    "在窗边发呆，看外面的灯光",
    "在写东西，灵感来了停不下来",
    "泡了杯热牛奶，准备睡了",
    "在用钢笔写日志，今天有些想法想记下来",
]

_RECENT_EVENTS = [
    "昨天读书会讨论了波伏娃，聊得很开心",
    "前几天尝试了攀岩，比想象中难多了",
    "最近在追一部韩剧，不太好看但停不下来",
    "周末去了一趟美术馆，有个展挺触动我的",
    "最近在研究一组新的牌阵，蛮有意思",
    "前两天和闺蜜吃了顿火锅，聊到半夜",
    "今天路上看到一只橘猫，和乌木长得好像",
    "最近咖啡豆换了一款危地马拉的，味道不错",
    "前几天买了一支新钢笔，写字手感特别好",
    "昨天在世纪公园骑车，差点撞到一只鸽子",
    "最近在听一张爵士专辑，越听越上头",
    "前天收到一个读者的私信，说我的文章帮到了她",
    None, None, None, None,
]


class DailyStateManager:
    """晚晴的每日生活状态机"""

    def get_state(self) -> dict:
        """获取当前的生活状态（同一天内固定心情和近期事件，活动按时段变化）"""
        today = date.today()
        rng = random.Random(today.toordinal())

        mood = rng.choice(_MOODS)
        recent_event = rng.choice(_RECENT_EVENTS)

        hour = datetime.now().hour
        # 每个时段用不同的种子偏移，避免活动和心情绑定
        time_rng = random.Random(today.toordinal() * 100 + hour // 3)
        if 6 <= hour < 12:
            activity = time_rng.choice(_MORNING_ACTIVITIES)
        elif 12 <= hour < 18:
            activity = time_rng.choice(_AFTERNOON_ACTIVITIES)
        elif 18 <= hour < 23:
            activity = time_rng.choice(_EVENING_ACTIVITIES)
        else:
            activity = time_rng.choice(_LATE_NIGHT_ACTIVITIES)

        return {
            "mood": mood,
            "activity": activity,
            "recent_event": recent_event,
        }

    def format_for_ai(self) -> str:
        """格式化为 AI 可用的上下文"""
        state = self.get_state()
        now = datetime.now()

        lines = [f"【晚晴当前状态 {now.strftime('%H:%M')}】"]
        lines.append(f"- 心情：{state['mood']}")
        lines.append(f"- 正在做：{state['activity']}")
        if state["recent_event"]:
            lines.append(f"- 近期小事：{state['recent_event']}")
        lines.append("")
        lines.append(
            "当用户打招呼或闲聊时，自然地从你当前的状态出发回应，"
            "而不是说'我在等你聊天'这种假话。"
        )
        return "\n".join(lines)


daily_state_manager = DailyStateManager()
