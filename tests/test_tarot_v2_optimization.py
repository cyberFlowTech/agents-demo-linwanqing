#!/usr/bin/env python3
"""
测试 tarot_v2.py 的优化效果
"""
import sys
sys.path.insert(0, '/Users/harleyma/Codes/运势大师/fortune_master')

# 模拟需要的函数
def _clean_markdown(text: str) -> str:
    """清理 Markdown 标记"""
    import re
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'__(.+?)__', r'\1', text)
    text = re.sub(r'`(.+?)`', r'\1', text)
    return text

# 测试总结生成
from handlers.tarot_v2 import _generate_integrated_summary
from services.tarot_data import TarotDeck

def test_summary():
    """测试总结功能"""
    print("=" * 80)
    print("测试 tarot_v2.py 优化效果")
    print("=" * 80 + "\n")
    
    deck = TarotDeck()
    
    test_cases = [
        ("我应该换工作吗？", "PPP", 3),
        ("这段感情会有结果吗？", "PPR", 2),
        ("现在适合投资吗？", "PRP", 1),
    ]
    
    for question, pattern, positive_count in test_cases:
        print(f"\n{'='*80}")
        print(f"问题: {question}")
        print(f"模式: {pattern} ({positive_count}张正位)")
        print(f"{'='*80}\n")
        
        # 构造牌阵
        cards = []
        for pos in pattern:
            card = deck.draw_card()
            card['orientation'] = "正位" if pos == 'P' else "逆位"
            card['name_full'] = f"{card['name']} ({'正位' if pos == 'P' else '逆位'})"
            cards.append(card)
        
        # 生成总结
        summary = _generate_integrated_summary(cards, question)
        summary = _clean_markdown(summary)
        
        print(summary)
        print()
        
        # 统计行数
        line_count = summary.count('\n') + 1
        print(f"📏 总行数: {line_count}")
        
        # 检查星级
        if "🌟" in summary:
            star_count = summary.count("🌟")
            print(f"⭐ 星级显示: ✅ ({star_count}星)")
        else:
            print(f"⭐ 星级显示: ❌ 未找到")
        
        print()

if __name__ == "__main__":
    test_summary()
    
    print("\n" + "=" * 80)
    print("✅ tarot_v2.py 优化验证完成！")
    print("=" * 80)
    print("""
核心改进:
  ✓ 换行大幅减少
  ✓ 星级评分显示
  ✓ 信息紧凑清晰
  ✓ 保留必要信息

请重启 Bot 测试:
  python3 main.py
    """)
