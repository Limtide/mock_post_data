import json
import os

def upgrade_db_json():
    file_path = 'db.json'
    
    if not os.path.exists(file_path):
        print("❌ 找不到 db.json")
        return

    try:
        print("🔄 正在读取 db.json...")
        with open(file_path, 'r', encoding='utf-8') as f:
            db_data = json.load(f)

        # 假设数据都在 feed_mixed 字段里
        # 如果您的 json 是直接的一个数组，请改用 data_list = db_data
        if "feed_mixed" in db_data:
            data_list = db_data["feed_mixed"]
        else:
            data_list = db_data # 兼容纯数组格式

        count_video = 0
        count_image = 0

        for post in data_list:
            # 默认为图片 (0)
            post_type = 0
            
            # 检查 clips 数组里有没有视频
            if "clips" in post and isinstance(post["clips"], list):
                for clip in post["clips"]:
                    # 只要发现有一个片段是视频 (type == 1)
                    if clip.get("type") == 1:
                        post_type = 1
                        break
            
            # ✅ 【关键步骤】把 type 字段加到最外层
            post["type"] = post_type
            
            if post_type == 1:
                count_video += 1
            else:
                count_image += 1

        # 保存回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(db_data, f, ensure_ascii=False, indent=2)

        print("-" * 30)
        print("✅ 升级完成！")
        print(f"📹 标记为视频贴: {count_video} 条")
        print(f"🖼️ 标记为图片贴: {count_image} 条")
        print("现在的 JSON 结构已经完美适配您的 API 代码了！")

    except Exception as e:
        print(f"❌ 发生错误: {e}")

if __name__ == '__main__':
    upgrade_db_json()