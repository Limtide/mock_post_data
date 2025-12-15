import os
import json
import sys

# 配置
MAX_FILE_SIZE_MB = 100  # GitHub 免费版单文件限制
JSON_FILES = ['db.json', 'feed_data_local.json', 'feed_data_local_with_video.json']

def check_large_files():
    print(f"🔍 正在扫描超过 {MAX_FILE_SIZE_MB}MB 的大文件...")
    found_large = False
    
    # 遍历当前目录
    for root, dirs, files in os.walk('.'):
        # 跳过 .git 目录
        if '.git' in dirs:
            dirs.remove('.git')
            
        for name in files:
            filepath = os.path.join(root, name)
            try:
                size_mb = os.path.getsize(filepath) / (1024 * 1024)
                if size_mb > MAX_FILE_SIZE_MB:
                    print(f"❌ [严重警告] 发现大文件: {filepath}")
                    print(f"   大小: {size_mb:.2f} MB")
                    print(f"   后果: GitHub 会在上传 100% 后拒绝接收，导致 Push 失败！")
                    found_large = True
            except OSError:
                pass
                
    if not found_large:
        print("✅ 文件大小检查通过：没有发现超过 100MB 的文件。")
    return found_large

def check_json_syntax():
    print("\n🔍 正在检查 JSON 文件语法...")
    has_error = False
    
    for filename in JSON_FILES:
        if not os.path.exists(filename):
            continue
            
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                json.load(f)
            print(f"✅ {filename}: 格式正确")
        except json.JSONDecodeError as e:
            print(f"❌ [错误] {filename} 格式有误！")
            print(f"   原因: {e.msg}")
            print(f"   行号: {e.lineno}, 列号: {e.colno}")
            has_error = True
        except Exception as e:
            print(f"⚠️ 无法读取 {filename}: {e}")

    return has_error

if __name__ == "__main__":
    print("="*40)
    print("      项目健康度自检程序")
    print("="*40 + "\n")

    large_file_error = check_large_files()
    json_error = check_json_syntax()

    print("\n" + "="*40)
    if large_file_error:
        print("🔴 结论：Push 极大概率会失败！请先删除大文件。")
    elif json_error:
        print("🟡 结论：Push 会成功，但 App 运行可能会崩溃（JSON 格式错误）。")
    else:
        print("🟢 结论：一切看起来都很完美！请耐心等待 Push 完成。")