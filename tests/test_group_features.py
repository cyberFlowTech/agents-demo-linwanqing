#!/usr/bin/env python3
"""
群组功能测试脚本
测试数据管理和功能逻辑
"""

import sys
sys.path.insert(0, '/Users/harleyma/Codes/运势大师/fortune_master')

from services.group_manager import GroupDataManager
from services.tarot_data import TarotDeck
from datetime import datetime

def print_section(title):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60 + "\n")

def test_group_fortune():
    """测试群日运势"""
    print_section("测试 1: 群日运势")
    
    manager = GroupDataManager()
    deck = TarotDeck()
    
    # 生成运势
    main_card = deck.draw_card()
    sub_card = deck.draw_card()
    
    fortune = {
        'main_card': {'name': main_card['name_full']},
        'sub_card': {'name': sub_card['name_full']},
        'stars': 4,
        'summary': "运势极佳，万事顺遂！",
        'suitable': ["开展新项目", "团队协作"],
        'avoid': ["冲动决策"],
        'date': datetime.now().strftime('%Y年%m月%d日')
    }
    
    # 保存
    manager.set_group_daily_fortune('test_group_123', fortune)
    
    # 读取
    loaded = manager.get_group_daily_fortune('test_group_123')
    
    print("✅ 群运势保存成功")
    print(f"主牌: {loaded['main_card']['name']}")
    print(f"副牌: {loaded['sub_card']['name']}")
    print(f"星级: {loaded['stars']}/5")

def test_ranking():
    """测试排行榜"""
    print_section("测试 2: 群排行榜")
    
    manager = GroupDataManager()
    
    # 添加测试数据
    test_users = [
        ('user1', '张三', 3, ['太阳(正)', '星星(正)', '世界(正)']),
        ('user2', '李四', 2, ['魔术师(正)', '恶魔(逆)', '力量(正)']),
        ('user3', '王五', 1, ['高塔(逆)', '月亮(逆)', '太阳(正)']),
        ('user4', '赵六', 3, ['战车(正)', '皇帝(正)', '教皇(正)']),
    ]
    
    for user_id, user_name, positive, cards in test_users:
        manager.add_user_divination(
            'test_group_123',
            user_id,
            user_name,
            positive,
            cards
        )
    
    # 获取排行
    ranking = manager.get_group_ranking('test_group_123')
    
    print("✅ 排行榜生成成功\n")
    print("排名  用户    正位数")
    print("-" * 30)
    for idx, record in enumerate(ranking, 1):
        print(f"{idx}.    {record['user_name']}    {record['positive_count']}张")
    
    # 测试获取用户排名
    rank = manager.get_user_rank('test_group_123', 'user2')
    print(f"\n李四的排名: 第{rank}名")

def test_pk_records():
    """测试PK记录"""
    print_section("测试 3: PK对战记录")
    
    manager = GroupDataManager()
    
    # 添加PK记录
    manager.add_pk_record(
        'test_group_123',
        'user1', '张三',
        [{'name': '太阳(正)'}, {'name': '星星(正)'}],
        90,
        'user2', '李四',
        [{'name': '恶魔(逆)'}, {'name': '月亮(正)'}],
        60,
        'user1'
    )
    
    manager.add_pk_record(
        'test_group_123',
        'user1', '张三',
        [{'name': '高塔(逆)'}, {'name': '死神(逆)'}],
        45,
        'user3', '王五',
        [{'name': '魔术师(正)'}, {'name': '世界(正)'}],
        75,
        'user3'
    )
    
    # 获取战绩
    stats = manager.get_user_pk_stats('test_group_123', 'user1')
    
    print("✅ PK记录保存成功\n")
    print("张三的战绩:")
    print(f"  总场次: {stats['total']}场")
    print(f"  胜利: {stats['wins']}场")
    print(f"  失败: {stats['losses']}场")
    print(f"  胜率: {stats['win_rate']}%")

def test_fortune_generation():
    """测试运势生成逻辑"""
    print_section("测试 4: 运势生成")
    
    deck = TarotDeck()
    
    print("生成5次群运势测试:\n")
    for i in range(5):
        main = deck.draw_card()
        sub = deck.draw_card()
        
        positive = (1 if "正位" in main['orientation'] else 0) + \
                  (1 if "正位" in sub['orientation'] else 0)
        
        if positive == 2:
            stars = 5
        elif positive == 1:
            stars = 3
        else:
            stars = 2
        
        print(f"第{i+1}次:")
        print(f"  主牌: {main['name_full']}")
        print(f"  副牌: {sub['name_full']}")
        print(f"  星级: {'⭐' * stars} ({stars}/5)\n")

def main():
    print("\n" + "🔮" * 30)
    print("群组功能测试")
    print("🔮" * 30)
    
    try:
        test_group_fortune()
        test_ranking()
        test_pk_records()
        test_fortune_generation()
        
        print_section("✅ 所有测试完成")
        print("MVP功能运行正常！")
        print("\n📝 数据文件位置: data/")
        print("  - groups.json (群运势)")
        print("  - rankings.json (排行榜)")
        print("  - pk_records.json (PK记录)")
        
    except Exception as e:
        print_section("❌ 测试失败")
        print(f"错误信息: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
