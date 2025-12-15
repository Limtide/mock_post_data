import json
import os

# 1. 定义那 7 个导致报错的超大文件名 (精准打击)
OVERSIZE_FILES = [
    "item_video113.mp4",
    "item_video160.mp4",
    "item_video175.mp4",
    "item_video181.mp4",
    "item_video24.mp4",
    "item_video42.mp4",
    "item_video67.mp4"
]

# 2. 新的公共测试视频 URL (更小、更快，仅 2MB)
PUBLIC_VIDEO_URL = "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4"

def fix_db_json():
    file_path = 'db.json'
    
    if not os.path.exists(file_path):
        print("❌ 错误：找不到 db.json 文件")
        return

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            db_data = json.load(f)

        replaced_count = 0

        # 遍历 feed_mixed (只有混合模式里有视频)
        if "feed_mixed" in db_data:
            for item in db_data["feed_mixed"]:
                if 'clips' in item:
                    for clip in item['clips']:
                        current_url = clip.get('url', '')
                        
                        # 检查这个链接是否包含那 7 个大文件中的任意一个
                        for bad_file in OVERSIZE_FILES:
                            if bad_file in current_url:
                                print(f"🔧 修复: {bad_file} \n    -> 替换为小视频 (ForBiggerBlazes.mp4)")
                                clip['url'] = PUBLIC_VIDEO_URL
                                replaced_count += 1
                                break
        
        # 保存修改后的文件
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(db_data, f, ensure_ascii=False, indent=2)

        print("-" * 40)
        print(f"✅ db.json 修复完成！共替换了 {replaced_count} 处大文件引用。")
        print(f"🔗 新视频地址已更新为: {PUBLIC_VIDEO_URL}")
        print("-" * 40)

    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == '__main__':
    fix_db_json()