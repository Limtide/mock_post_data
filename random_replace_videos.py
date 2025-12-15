import json
import os
import random

# 定义公共视频池
VIDEO_POOL = [
    "db/items/item_video1.mp4",
    "db/items/item_video2.mp4",
    "db/items/item_video3.mp4",
    "db/items/item_video4.mp4",
    "db/items/item_video5.mp4",
    "db/items/item_video6.mp4",
    "db/items/item_video7.mp4",
    "db/items/item_video8.mp4",
    "db/items/item_video9.mp4",
    "db/items/item_video10.mp4",

]

def update_videos_randomly():
    file_path = 'db.json'
    
    if not os.path.exists(file_path):
        print("❌ 错误：找不到 db.json 文件")
        return

    try:
        print("🔄 正在读取 db.json...")
        with open(file_path, 'r', encoding='utf-8') as f:
            db_data = json.load(f)

        replaced_count = 0

        # 定义一个递归函数来查找所有可能有 clips 的地方
        # 这样无论您的结构是 feed, feed_mixed 还是其他，都能找到
        def traverse_and_replace(data):
            nonlocal replaced_count
            if isinstance(data, dict):
                # 如果当前对象有 clips 列表，检查它
                if 'clips' in data and isinstance(data['clips'], list):
                    for clip in data['clips']:
                        # type: 1 代表视频
                        if clip.get('type') == 1:
                            # 随机选一个新 URL
                            new_url = random.choice(VIDEO_POOL)
                            clip['url'] = new_url
                            replaced_count += 1
                
                # 继续遍历字典的其他值
                for key, value in data.items():
                    traverse_and_replace(value)
            
            elif isinstance(data, list):
                # 如果是列表，遍历每个元素
                for item in data:
                    traverse_and_replace(item)

        # 开始遍历整个 JSON
        traverse_and_replace(db_data)
        
        # 写入回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(db_data, f, ensure_ascii=False, indent=2)

        print("-" * 40)
        print(f"✅ 成功！共随机替换了 {replaced_count} 个视频链接。")
        print("   您的 App 现在会随机播放 7 种不同的测试视频。")
        print("-" * 40)

    except Exception as e:
        print(f"❌ 发生错误: {e}")

if __name__ == '__main__':
    update_videos_randomly()