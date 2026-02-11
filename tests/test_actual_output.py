#!/usr/bin/env python3
"""
快速测试：验证星级和紧凑布局是否生效
"""
import sys
sys.path.insert(0, '/Users/harleyma/Codes/运势大师/fortune_master')

from services.tarot_data import TarotDeck

def test_actual_output():
    """测试实际输出"""
    print("=" * 80)
    print("测试：实际输出效果")
    print("=" * 80 + "\n")
    
    deck = TarotDeck()
    
    # 测试不同的正位数量
    test_cases = [
        ("我应该换工作吗？", 3, "PPP"),
        ("这段感情会有结果吗？", 2, "PPR"),
        ("现在适合投资吗？", 1, "PRP"),
        ("我的健康状况如何？", 0, "RRR"),
    ]
    
    for question, positive_count, pattern in test_cases:
        print(f"\n{'='*80}")
        print(f"问题: {question}")
        print(f"正位数: {positive_count}/3  ({pattern})")
        print(f"{'='*80}\n")
        
        # 构造牌阵
        spread = []
        for pos in pattern:
            card = deck.draw_card()
            card['orientation'] = "正位" if pos == 'P' else "逆位"
            card['name_full'] = f"{card['name']} ({'正位' if pos == 'P' else '逆位'})"
            spread.append(card)
        
        # 生成解读
        interpretation = deck.generate_brief_interpretation(spread, question)
        
        # 模拟完整输出（包括外层包装）
        result_text = (
            f"🔮 塔罗占卜结果\n"
            f"━━━━━━━━━━━━━━━━━\n"
            f"💭 {question}\n"
            f"━━━━━━━━━━━━━━━━━\n"
            f"{interpretation}"
        )
        
        print(result_text)
        print()
        
        # 统计行数
        line_count = result_text.count('\n') + 1
        print(f"📏 总行数: {line_count}")
        
        # 检查星级
        if "🌟" in result_text:
            star_count = result_text.count("🌟")
            print(f"⭐ 星级显示: ✅ ({star_count}星)")
        else:
            print(f"⭐ 星级显示: ❌ 未找到星级")
        
        print()

if __name__ == "__main__":
    test_actual_output()
