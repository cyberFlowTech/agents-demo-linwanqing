#!/usr/bin/env python3
"""
塔罗占卜 V3 功能演示
展示渐进式翻牌的完整流程
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from services.tarot_data import TarotDeck

def print_separator(title=""):
    """打印分隔线"""
    if title:
        print(f"\n{'='*50}")
        print(f"  {title}")
        print(f"{'='*50}\n")
    else:
        print("\n" + "━"*50 + "\n")


def demo_progressive_reading():
    """演示渐进式翻牌流程"""
    
    print_separator("🎴 塔罗占卜 V3 - 渐进式翻牌演示")
    
    # 模拟用户问题
    question = "我应该换工作吗？"
    print(f"💭 用户问题: {question}\n")
    
    # 准备阶段
    print("━━━━━━━━━━━━━━━━━")
    print("🔮 准备阶段")
    print("━━━━━━━━━━━━━━━━━")
    print("请闭上眼睛，在心中默念问题三次...")
    print("\n塔罗之灵将为你揭示：")
    print("🎴 过去 - 事情的根源")
    print("🎴 现在 - 当前的状态")
    print("🎴 未来 - 发展的趋势")
    print("\n[🎴 我准备好了]")
    
    input("\n按回车键开始翻牌...")
    
    # 生成牌阵
    deck = TarotDeck()
    spread = deck.get_three_card_spread()
    position_names = ["过去", "现在", "未来"]
    position_meanings = [
        "这张牌揭示了事情的根源",
        "这张牌展现了当前的状态",
        "这张牌预示着发展的趋势"
    ]
    
    # 逐张翻牌
    for i, (card, position, meaning) in enumerate(zip(spread, position_names, position_meanings), 1):
        print_separator(f"翻开第 {i} 张牌")
        
        print("🎴 翻牌中...\n")
        
        card_symbol = "🔸" if "正位" in card['orientation'] else "🔹"
        
        print(f"🎴 第 {i} 张牌 - {position}")
        print("━━━━━━━━━━━━━━━━━")
        print(f"{card_symbol} {card['name_full']}")
        print("━━━━━━━━━━━━━━━━━")
        print(f"💫 {meaning}")
        
        # 简短解读
        brief = card['meaning'][:40] + "..." if len(card['meaning']) > 40 else card['meaning']
        print(f"{brief}\n")
        
        print(f"已翻开 {i}/3 张")
        
        if i < 3:
            print(f"\n[➡️ 翻开第 {i+1} 张 ({position_names[i]})]")
            print("[⏸️ 让我想想]")
            input("\n按回车继续...")
        else:
            print("\n[📊 查看完整解读]")
            input("\n按回车查看完整结果...")
    
    # 完整结果
    print_separator("🔮 完整占卜结果")
    
    # 计算正位数
    positive_count = sum(1 for c in spread if "正位" in c['orientation'])
    
    # 星级
    stars = "⭐" * min(5, max(1, positive_count + 1))
    
    print(f"💭 {question}")
    print("━━━━━━━━━━━━━━━━━\n")
    print(f"✨ 整体趋势: {stars}")
    
    # 一句话建议
    advice_map = {
        3: "天时地利人和，大胆行动",
        2: "时机已到，积极把握",
        1: "谨慎评估，稳步推进",
        0: "暂缓决策，等待时机"
    }
    advice = advice_map.get(positive_count, "保持平常心，顺其自然")
    print(f"📌 核心建议: {advice}\n")
    
    # 牌阵信息
    cards_display = " | ".join([
        f"{c['name'].split('(')[0]}({c['orientation']})" 
        for c in spread
    ])
    print(f"🎴 牌阵: {cards_display}\n")
    
    # 整体能量
    print("🌊 整体能量:")
    brief_interpretation = deck.generate_brief_interpretation(spread, question)
    
    # 提取能量流部分
    if "整体能量" in brief_interpretation:
        energy_part = brief_interpretation.split("整体能量")[1].split("\n\n")[0]
        print(energy_part)
    
    print("\n[📖 查看深度解读]")
    print("[🔁 再占一次] [🌙 今日运势]")
    
    input("\n按回车查看深度解读...")
    
    # 深度解读
    print_separator("📖 深度解读")
    
    print(f"💭 {question}\n")
    print(f"🎴 {cards_display}")
    print("━━━━━━━━━━━━━━━━━\n")
    
    detailed = deck.generate_spread_interpretation(spread, question)
    print(detailed)
    
    print_separator()
    print("✅ 演示完成！")
    print("\n📋 新版特点:")
    print("  • 固定三张牌阵（过去→现在→未来）")
    print("  • 渐进式翻牌（每张单独解读）")
    print("  • 可暂停思考（用户掌控节奏）")
    print("  • 产品经理级文案打磨")
    print("  • 保留所有优秀功能（星级、关联、排行榜）")


def demo_comparison():
    """对比展示：旧版 vs 新版"""
    
    print_separator("📊 版本对比")
    
    print("旧版 tarot_v2.py:")
    print("  • 动态牌数（1-5张）")
    print("  • 按顺序抽牌")
    print("  • 用户选择何时停止")
    print("  • 动态生成牌位含义")
    print()
    print("新版 tarot.py (V3):")
    print("  • 固定3张（过去→现在→未来）")
    print("  • 渐进式翻牌 + 可暂停")
    print("  • 更专业的牌阵体系")
    print("  • 产品经理级文案")
    print()
    print("核心优势:")
    print("  ✅ 更专业的塔罗体验（经典三张牌阵）")
    print("  ✅ 更强的仪式感（逐步揭示 + 暂停功能）")
    print("  ✅ 更精炼的文案（每个字都经过打磨）")
    print("  ✅ 保留所有功能（星级、关联、群组排行）")


if __name__ == "__main__":
    print("\n🎴 塔罗占卜 V3 演示程序\n")
    print("1. 完整流程演示")
    print("2. 版本对比")
    print()
    
    choice = input("请选择 (1/2，直接回车默认为1): ").strip() or "1"
    
    if choice == "1":
        demo_progressive_reading()
    elif choice == "2":
        demo_comparison()
    else:
        print("无效选择")
