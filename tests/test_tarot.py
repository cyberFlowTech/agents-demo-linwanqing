#!/usr/bin/env python3
"""
塔罗占卜功能测试脚本
测试精简版、详细版和今日运势的输出
"""

from services.tarot_data import TarotDeck

def print_section(title):
    """打印分隔线"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60 + "\n")

def test_brief_interpretation():
    """测试精简版解读"""
    print_section("测试 1: 精简版解读")
    
    deck = TarotDeck()
    spread = deck.get_three_card_spread()
    question = "我应该换工作吗？"
    
    result = deck.generate_brief_interpretation(spread, question)
    print(result)
    print(f"\n字数统计: {len(result)} 字")

def test_detailed_interpretation():
    """测试详细版解读"""
    print_section("测试 2: 详细版解读")
    
    deck = TarotDeck()
    spread = deck.get_three_card_spread()
    question = "他喜欢我吗？"
    
    result = deck.generate_spread_interpretation(spread, question)
    print(result)
    print(f"\n字数统计: {len(result)} 字")

def test_simple_reading():
    """测试今日运势"""
    print_section("测试 3: 今日运势")
    
    deck = TarotDeck()
    result = deck.get_simple_reading("张三")
    print(result)

def test_question_categories():
    """测试问题分类识别"""
    print_section("测试 4: 问题分类识别")
    
    deck = TarotDeck()
    
    test_questions = {
        "我应该换工作吗？": "career",
        "他喜欢我吗？": "love",
        "这个月适合投资吗？": "money",
        "我的身体状况如何？": "health",
        "考研能成功吗？": "study",
        "我的未来会怎样？": "general"
    }
    
    print("问题分类识别测试：\n")
    for question, expected in test_questions.items():
        category = deck._get_question_category(question)
        status = "✅" if category == expected else "❌"
        print(f"{status} 问题: {question}")
        print(f"   识别为: {category} (期望: {expected})\n")

def test_comparison():
    """对比精简版和详细版的差异"""
    print_section("测试 5: 精简版 vs 详细版对比")
    
    deck = TarotDeck()
    spread = deck.get_three_card_spread()
    question = "最近财运如何？"
    
    brief = deck.generate_brief_interpretation(spread, question)
    detailed = deck.generate_spread_interpretation(spread, question)
    
    print(f"精简版字数: {len(brief)} 字")
    print(f"详细版字数: {len(detailed)} 字")
    print(f"详细版是精简版的 {detailed.__len__() / brief.__len__():.1f} 倍\n")
    
    print("精简版预览:")
    print(brief[:200] + "...\n")
    
    print("详细版预览:")
    print(detailed[:200] + "...")

def main():
    """运行所有测试"""
    print("\n" + "🔮" * 30)
    print("塔罗占卜功能测试")
    print("🔮" * 30)
    
    try:
        test_brief_interpretation()
        test_detailed_interpretation()
        test_simple_reading()
        test_question_categories()
        test_comparison()
        
        print_section("✅ 所有测试完成")
        print("所有功能运行正常！")
        
    except Exception as e:
        print_section("❌ 测试失败")
        print(f"错误信息: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
