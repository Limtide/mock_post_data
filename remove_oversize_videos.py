import json
import os

# ================= 配置区 =================

# 定义那 7 个需要被删除的“坏视频”文件名
OVERSIZE_FILES = [
    "item_video113.mp4",
    "item_video160.mp4",
    "item_video175.mp4",
    "item_video181.mp4",
    "item_video24.mp4",
    "item_video42.mp4",
    "item_video67.mp4"
]

# =========================================

def remove_bad_videos():
    file_path = 'db.json'
    
    if not os.path.exists(file_path):
        print("❌ 错误：找不到 db.json 文件")
        return

    try:
        print("🔄 正在读取 db.json ...")
        with open(file_path, 'r', encoding='utf-8') as f:
            db_data = json.load(f)

        removed_count = 0
        
        # 确定数据源位置 (兼容 feed_mixed 或 直接数组)
        # 您的最新文件似乎是直接的数组列表，这里做双重兼容
        if isinstance(db_data, list):
            data_list = db_data
        elif isinstance(db_data, dict) and "feed_mixed" in db_data:
            data_list = db_data["feed_mixed"]
        else:
            print("❌ 无法识别 JSON 结构")
            return

        # 遍历所有帖子
        for item in data_list:
            if 'clips' in item and isinstance(item['clips'], list):
                # 使用列表推导式进行过滤：
                # 只保留那些 url 不包含在 OVERSIZE_FILES 中的 clip
                original_clips = item['clips']
                
                # 过滤后的 clips
                new_clips = []
                for clip in original_clips:
                    url = clip.get('url', '')
                    is_bad = False
                    
                    # 检查当前 clip 的 url 是否包含黑名单中的任何一个文件名
                    for bad_file in OVERSIZE_FILES:
                        if bad_file in url:
                            is_bad = True
                            print(f"🗑️ 删除视频: {bad_file} (所在帖子ID: {item.get('post_id', 'Unknown')})")
                            removed_count += 1
                            break # 只要命中一个黑名单关键词就标记为坏
                    
                    # 如果不是坏视频，就保留
                    if not is_bad:
                        new_clips.append(clip)
                
                # 更新该帖子的 clips 列表
                item['clips'] = new_clips

        # 保存修改
        if removed_count > 0:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(db_data, f, ensure_ascii=False, indent=2)
            print("-" * 40)
            print(f"✅ 处理完成！共从列表中删除了 {removed_count} 个超大视频片段。")
            print("其他的 commondatastorage 视频已保留。")
            print("⚠️ 别忘了运行 git push 更新到云端！")
        else:
            print("-" * 40)
            print("👌 未发现黑名单中的文件，无需修改。")

    except Exception as e:
        print(f"❌ 发生错误: {e}")

if __name__ == '__main__':
    remove_bad_videos()