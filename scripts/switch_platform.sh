#!/bin/bash

# 快速切换 TG 平台和运行模式
# 用法:
#   ./scripts/switch_platform.sh telegram webhook
#   ./scripts/switch_platform.sh zapry temporary

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
ENV_FILE="$PROJECT_ROOT/.env"

# 参数解析
PLATFORM="${1:-}"
MODE="${2:-}"

show_usage() {
    echo "用法: $0 <platform> [mode]"
    echo ""
    echo "参数:"
    echo "  platform   : telegram | zapry (必填)"
    echo "  mode       : webhook | temporary (可选，默认 webhook)"
    echo ""
    echo "示例:"
    echo "  $0 telegram          # 切换到 Telegram 官方（webhook 模式）"
    echo "  $0 zapry temporary   # 切换到 Zapry（临时调试模式）"
    echo ""
}

# 检查参数
if [[ -z "$PLATFORM" ]]; then
    echo "❌ 错误: 未指定平台"
    show_usage
    exit 1
fi

if [[ "$PLATFORM" != "telegram" && "$PLATFORM" != "zapry" ]]; then
    echo "❌ 错误: 平台只能是 telegram 或 zapry"
    show_usage
    exit 1
fi

# 默认 webhook 模式
if [[ -z "$MODE" ]]; then
    MODE="webhook"
fi

if [[ "$MODE" != "webhook" && "$MODE" != "temporary" ]]; then
    echo "❌ 错误: 模式只能是 webhook 或 temporary"
    show_usage
    exit 1
fi

# 检查 .env 文件
if [[ ! -f "$ENV_FILE" ]]; then
    echo "❌ 错误: 未找到 .env 文件: $ENV_FILE"
    exit 1
fi

# 备份
cp "$ENV_FILE" "$ENV_FILE.backup"

# 修改 TG_PLATFORM
if grep -q "^TG_PLATFORM=" "$ENV_FILE"; then
    sed -i.tmp "s/^TG_PLATFORM=.*/TG_PLATFORM=$PLATFORM/" "$ENV_FILE"
else
    echo "TG_PLATFORM=$PLATFORM" >> "$ENV_FILE"
fi

# 修改 RUNTIME_MODE
if grep -q "^RUNTIME_MODE=" "$ENV_FILE"; then
    sed -i.tmp "s/^RUNTIME_MODE=.*/RUNTIME_MODE=$MODE/" "$ENV_FILE"
else
    echo "RUNTIME_MODE=$MODE" >> "$ENV_FILE"
fi

# 清理临时文件
rm -f "$ENV_FILE.tmp"

echo "✅ 配置已更新："
echo "   TG 平台: $PLATFORM"
echo "   运行模式: $MODE"
echo ""
echo "💡 提示: 如需恢复之前的配置，请执行："
echo "   mv $ENV_FILE.backup $ENV_FILE"
