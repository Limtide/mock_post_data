import json
import os

def generate_exact_db():
    # 源文件名
    file_images = 'feed_data_local.json'
    file_mixed = 'feed_data_local_with_video.json'
    
    # 检查文件是否存在
    if not os.path.exists(file_images) or not os.path.exists(file_mixed):
        print("错误：请确保两个源 JSON 文件都在当前目录下。")
        return

    try:
        # 1. 原封不动读取数据
        with open(file_images, 'r', encoding='utf-8') as f:
            data_images = json.load(f)
        
        with open(file_mixed, 'r', encoding='utf-8') as f:
            data_mixed = json.load(f)

        # 2. 组装 db.json 结构
        # 直接将原始列表挂载到对应端点，不做任何字段修改
        db_data = {
            "feed_images": data_images,  # 对应纯图片模式
            "feed_mixed": data_mixed     # 对应混合模式
        }

        # 3. 写入 db.json
        with open('db.json', 'w', encoding='utf-8') as f:
            json.dump(db_data, f, ensure_ascii=False, indent=2)

        print("✅ db.json 生成成功！(数据未做任何修改)")
        print(f"  - API 端点 1: /feed_images (数据量: {len(data_images)})")
        print(f"  - API 端点 2: /feed_mixed  (数据量: {len(data_mixed)})")

    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == '__main__':
    generate_exact_db()