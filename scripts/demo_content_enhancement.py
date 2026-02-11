#!/usr/bin/env python3
"""
塔罗占卜 - 文案优化演示
展示信息增强后的效果
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from services.tarot_data import TarotDeck

def print_separator(char="━", length=50):
    print(char * length)


def demo_enhanced_card_reading():
    """演示增强后的单张牌解读"""
    
    print("\n" + "=" * 60)
    print("  🎴 单张牌解读 - 信息增强演示")
    print("=" * 60 + "\n")
    
    deck = TarotDeck()
    spread = deck.get_three_card_spread()
    
    # 模拟翻第1张牌（过去）
    card = spread[0]
    position = "过去"
    card_symbol = "🔸" if "正位" in card['orientation'] else "🔹"
    
    print("🎴 第 1 张牌 - 过去")
    print_separator()
    print(f"{card_symbol} {card['name_full']}\n")
    
    print("📍 位置意义: 事情的根源")
    print("💭 解读方向: 回顾引发当前局面的关键因素")
    print_separator()
    print()
    
    print("🔍 牌面信息:")
    if "正位" in card['orientation']:
        deep_meaning = card.get('deep_meaning_upright', card['meaning'])
    else:
        deep_meaning = card.get('deep_meaning_reversed', card['meaning'])
    
    print(deep_meaning)
    print()
    
    print("💡 针对【过去】的建议:")
    card_name = card['name'].split('(')[0].strip()
    if "正位" in card['orientation']:
        advice = f"{card_name}在过去位显示，这段经历为你奠定了良好基础。回顾这些积累，它们是你当下的优势。别忘记这份初心和经验。"
    else:
        advice = f"{card_name}逆位提醒，过去某些未解决的问题可能在影响现状。不必沉湎于过往，但要从中吸取教训，避免重蹈覆辙。"
    print(advice)
    print()
    
    print_separator()
    print("进度: 1/3")
    print()
    
    input("按回车查看暂停思考优化...")
    
    # 暂停思考
    print("\n⏸️ 已暂停")
    print_separator()
    print()
    print("💭 停下来，让刚才那张牌的信息在心中沉淀...\n")
    print("思考一下:")
    print("• 这张牌与你的问题有什么共鸣？")
    print("• 它是否点出了某个你忽略的细节？")
    print("• 它传递的能量是鼓励还是提醒？\n")
    print("准备好后，继续翻开下一张牌。\n")
    
    input("按回车查看深度解读优化...")


def demo_enhanced_deep_reading():
    """演示增强后的深度解读"""
    
    print("\n" + "=" * 60)
    print("  📖 深度解读 - 时间线与风险机会分析")
    print("=" * 60 + "\n")
    
    deck = TarotDeck()
    spread = deck.get_three_card_spread()
    
    print("💭 问题: 我应该换工作吗\n")
    
    print("🎴 牌阵:")
    print(f"过去: {spread[0]['name'].split('(')[0]}({spread[0]['orientation']})")
    print(f"现在: {spread[1]['name'].split('(')[0]}({spread[1]['orientation']})")
    print(f"未来: {spread[2]['name'].split('(')[0]}({spread[2]['orientation']})")
    print_separator()
    print()
    
    print("[... 原有解读内容 ...]\n")
    print_separator()
    print()
    
    # 时间线建议
    print("⏰ 时间线建议:\n")
    
    past_upright = "正位" in spread[0]['orientation']
    present_upright = "正位" in spread[1]['orientation']
    future_upright = "正位" in spread[2]['orientation']
    
    if present_upright:
        print("✓ 近期(1-2周): 当前势头良好，是推进计划的好时机。")
        print("  把握这段时间，做重要的决定或行动。\n")
    else:
        print("⚠ 近期(1-2周): 现在不宜冒进，先解决眼前的问题，")
        print("  调整状态，做好准备工作。\n")
    
    if present_upright and future_upright:
        print("✓ 中期(1-3月): 保持当前策略，稳步推进。好运气会延续，")
        print("  但不要松懈。\n")
    elif not present_upright and future_upright:
        print("↗ 中期(1-3月): 局面会好转。现在的努力会有回报，")
        print("  坚持下去，转机即将出现。\n")
    else:
        print("→ 中期(1-3月): 需要耐心调整。成功需要时间积累，")
        print("  保持定力，稳扎稳打。\n")
    
    positive_count = sum(1 for c in spread if "正位" in c['orientation'])
    if positive_count >= 2:
        print("✓ 长期(3月+): 整体趋势向好，值得长期投入。建立系统，")
        print("  着眼未来，布局长远目标。\n")
    else:
        print("→ 长期(3月+): 需要耐心和毅力。成功需要时间积累，")
        print("  保持定力，稳扎稳打。\n")
    
    print_separator()
    print()
    
    # 风险与机会
    print("⚠️ 风险与机会:\n")
    
    print("🚨 需要注意:")
    risks = []
    for idx, card in enumerate(spread):
        position = ["过去", "现在", "未来"][idx]
        card_name = card['name'].split('(')[0].strip()
        if "逆位" in card['orientation']:
            if idx == 0:
                risks.append(f"• 警惕过去{card_name}的问题再次出现")
            elif idx == 1:
                risks.append(f"• 当前{card_name}逆位是主要挑战点")
            else:
                risks.append(f"• 未来{card_name}需要提前防范")
    
    if not risks:
        risks.append("• 整体风险较低，主要是别掉以轻心")
    
    for risk in risks:
        print(risk)
    
    print()
    print("✨ 可以把握:")
    opportunities = []
    for idx, card in enumerate(spread):
        position = ["过去", "现在", "未来"][idx]
        card_name = card['name'].split('(')[0].strip()
        if "正位" in card['orientation']:
            if idx == 0:
                opportunities.append(f"• 过去的{card_name}经验是你的优势资源")
            elif idx == 1:
                opportunities.append(f"• 当前{card_name}的能量支持你采取行动")
            else:
                opportunities.append(f"• 未来{card_name}的趋势值得期待和布局")
    
    if positive_count == 3:
        opportunities.append("• 天时地利人和，这是难得的完美时机")
    
    for opp in opportunities:
        print(opp)
    
    print()


def demo_comparison():
    """对比展示：优化前 vs 优化后"""
    
    print("\n" + "=" * 60)
    print("  📊 优化前 vs 优化后对比")
    print("=" * 60 + "\n")
    
    print("【优化前】单张牌信息:")
    print("-" * 40)
    print("🎴 第 1 张牌 - 过去")
    print("━━━━━━━━━━━━━━━━━")
    print("🔸 命运之轮 (正位)")
    print("━━━━━━━━━━━━━━━━━")
    print("💫 这张牌揭示了事情的根源")
    print("好运，业力，生命周期...")
    print()
    print("已翻开 1/3 张")
    print()
    print("📊 信息量: ~60字, 2个模块, 可操作性: 低")
    print()
    
    print()
    print("【优化后】单张牌信息:")
    print("-" * 40)
    print("🎴 第 1 张牌 - 过去")
    print("━━━━━━━━━━━━━━━━━")
    print("🔸 命运之轮 (正位)")
    print()
    print("📍 位置意义: 事情的根源")
    print("💭 解读方向: 回顾引发当前局面的关键因素")
    print("━━━━━━━━━━━━━━━━━")
    print()
    print("🔍 牌面信息:")
    print("命运之轮永不停息地转动，提醒着万物循环的真理。")
    print("你正处于生命的转折点，好运即将降临。接受变化，")
    print("顺应宇宙的节奏，你会发现一切都是最好的安排。")
    print()
    print("💡 针对【过去】的建议:")
    print("命运之轮在过去位显示，这段经历为你奠定了良好基础。")
    print("回顾这些积累，它们是你当下的优势。别忘记这份初心")
    print("和经验。")
    print()
    print("━━━━━━━━━━━━━━━━━")
    print("进度: 1/3")
    print()
    print("📊 信息量: ~200字, 5个模块, 可操作性: 高")
    print()
    
    print("\n" + "=" * 60)
    print("提升: 字数 +233%, 模块 +150%, 可操作性 质变")
    print("=" * 60)


if __name__ == "__main__":
    print("\n🎴 塔罗占卜 - 文案优化演示\n")
    print("1. 单张牌解读增强")
    print("2. 深度解读增强（时间线+风险机会）")
    print("3. 优化前后对比")
    print()
    
    choice = input("请选择 (1/2/3，直接回车默认为1): ").strip() or "1"
    
    if choice == "1":
        demo_enhanced_card_reading()
    elif choice == "2":
        demo_enhanced_deep_reading()
    elif choice == "3":
        demo_comparison()
    else:
        print("无效选择")
    
    print("\n✅ 演示完成！")
    print("\n核心改进:")
    print("  • 单张牌: 位置意义 + 深度含义 + 针对性建议")
    print("  • 暂停思考: 3个引导性问题")
    print("  • 深度解读: 时间线建议 + 风险机会分析")
    print("  • 定位转变: 从'算命工具'到'决策顾问'\n")
