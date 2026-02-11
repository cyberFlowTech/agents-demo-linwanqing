#!/usr/bin/env python3
"""
数据迁移脚本：JSON 文件 → SQLite
将旧版本的 JSON 文件数据导入到新的 SQLite 数据库中。

用法：
  cd fortune_master
  python scripts/migrate_to_sqlite.py

注意：
- 此脚本可以安全地重复执行（幂等操作，使用 INSERT OR REPLACE）
- 迁移完成后旧文件不会被删除，需要手动清理
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime

# 添加项目根目录到 path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from db.database import db


def migrate_user_memories():
    """迁移用户记忆文件"""
    memory_dir = project_root / "data" / "user_memories"
    if not memory_dir.exists():
        print("⏭️  跳过：用户记忆目录不存在")
        return 0

    count = 0
    for json_file in memory_dir.glob("*.json"):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                memory = json.load(f)

            user_id = json_file.stem  # 文件名去掉 .json
            user_name = memory.get('user_name', '朋友')
            conversation_count = memory.get('conversation_count', 0)
            memory_json = json.dumps(memory, ensure_ascii=False)
            updated_at = memory.get('last_updated', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

            db.execute_sync(
                """INSERT OR REPLACE INTO user_memories
                   (user_id, user_name, memory_data, conversation_count, updated_at)
                   VALUES (?, ?, ?, ?, ?)
                """,
                (user_id, user_name, memory_json, conversation_count, updated_at),
            )
            count += 1
        except Exception as e:
            print(f"  ❌ 迁移失败: {json_file.name} | {e}")

    print(f"✅ 用户记忆：已迁移 {count} 条")
    return count


def migrate_groups():
    """迁移群组运势数据"""
    groups_file = project_root / "data" / "groups.json"
    if not groups_file.exists():
        print("⏭️  跳过：群组数据文件不存在")
        return 0

    try:
        with open(groups_file, 'r', encoding='utf-8') as f:
            groups = json.load(f)
    except Exception as e:
        print(f"❌ 读取群组数据失败: {e}")
        return 0

    count = 0
    for group_id, group_data in groups.items():
        fortune_date = group_data.get('fortune_date')
        fortune = group_data.get('fortune')
        if fortune_date and fortune:
            fortune_json = json.dumps(fortune, ensure_ascii=False)
            db.execute_sync(
                """INSERT OR REPLACE INTO group_fortunes
                   (group_id, fortune_date, fortune_data)
                   VALUES (?, ?, ?)
                """,
                (group_id, fortune_date, fortune_json),
            )
            count += 1

    print(f"✅ 群组运势：已迁移 {count} 条")
    return count


def migrate_rankings():
    """迁移排行榜数据"""
    rankings_file = project_root / "data" / "rankings.json"
    if not rankings_file.exists():
        print("⏭️  跳过：排行榜数据文件不存在")
        return 0

    try:
        with open(rankings_file, 'r', encoding='utf-8') as f:
            rankings = json.load(f)
    except Exception as e:
        print(f"❌ 读取排行榜数据失败: {e}")
        return 0

    count = 0
    for group_id, date_records in rankings.items():
        for date_str, records in date_records.items():
            for record in records:
                cards_json = json.dumps(record.get('cards', []), ensure_ascii=False)
                try:
                    db.execute_sync(
                        """INSERT OR REPLACE INTO group_rankings
                           (group_id, user_id, user_name, positive_count, cards, ranking_date)
                           VALUES (?, ?, ?, ?, ?, ?)
                        """,
                        (
                            group_id,
                            record['user_id'],
                            record['user_name'],
                            record.get('positive_count', 0),
                            cards_json,
                            date_str,
                        ),
                    )
                    count += 1
                except Exception as e:
                    print(f"  ❌ 排行记录迁移失败: {e}")

    print(f"✅ 排行榜：已迁移 {count} 条")
    return count


def migrate_pk_records():
    """迁移 PK 对战记录"""
    pk_file = project_root / "data" / "pk_records.json"
    if not pk_file.exists():
        print("⏭️  跳过：PK 记录文件不存在")
        return 0

    try:
        with open(pk_file, 'r', encoding='utf-8') as f:
            pk_records = json.load(f)
    except Exception as e:
        print(f"❌ 读取 PK 记录失败: {e}")
        return 0

    count = 0
    for group_id, records in pk_records.items():
        for record in records:
            user1 = record.get('user1', {})
            user2 = record.get('user2', {})
            winner_id = record.get('winner_id')
            if winner_id == 'draw':
                winner_id = None

            try:
                db.execute_sync(
                    """INSERT INTO pk_records
                       (group_id, user1_id, user1_name, user1_cards, user1_score,
                        user2_id, user2_name, user2_cards, user2_score, winner_id)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        group_id,
                        user1.get('id', ''),
                        user1.get('name', ''),
                        json.dumps(user1.get('cards', []), ensure_ascii=False),
                        user1.get('score', 0),
                        user2.get('id', ''),
                        user2.get('name', ''),
                        json.dumps(user2.get('cards', []), ensure_ascii=False),
                        user2.get('score', 0),
                        winner_id,
                    ),
                )
                count += 1
            except Exception as e:
                print(f"  ❌ PK 记录迁移失败: {e}")

    print(f"✅ PK 记录：已迁移 {count} 条")
    return count


def main():
    print("=" * 50)
    print("📦 数据迁移：JSON → SQLite")
    print("=" * 50)
    print()

    # 初始化数据库（建表）
    db.init_tables()
    print("✅ 数据库表已创建\n")

    # 执行迁移
    total = 0
    total += migrate_user_memories()
    total += migrate_groups()
    total += migrate_rankings()
    total += migrate_pk_records()

    print()
    print("=" * 50)
    print(f"📊 迁移完成！共迁移 {total} 条数据")
    print(f"📁 数据库文件: {db.db_path}")
    print()
    print("⚠️  旧 JSON 文件未被删除，确认无误后可手动清理：")
    print("   rm -rf data/user_memories/")
    print("   rm -rf data/user_memories_backup/")
    print("   rm data/groups.json data/rankings.json data/pk_records.json")
    print("=" * 50)


if __name__ == "__main__":
    main()
