import json
import os

# ================= 配置区 =================
# 您的 GitHub Raw 基础路径 (注意：末尾保留斜杠)
# 格式: https://raw.githubusercontent.com/<用户名>/<仓库名>/refs/heads/<分支名>/
BASE_URL = "https://raw.githubusercontent.com/Limtide/mock_post_data/refs/heads/main/"

# 需要替换的目标文件夹关键词 (防止误伤其他数据)
# 只要字符串里包含这些词，就会被转换
TARGET_PATHS = ["db/items/", "db/profiles/"]
# =========================================

def to_github_raw():
    file_path = 'db.json'
    
    if not os.path.exists(file_path):
        print("❌ 错误：找不到 db.json 文件")
        return

    try:
        print("🔄 正在读取 db.json...")
        with open(file_path, 'r', encoding='utf-8') as f:
            db_data = json.load(f)

        replaced_count = 0

        # 递归遍历函数，处理任意层级的 JSON
        def process_node(data):
            nonlocal replaced_count
            
            if isinstance(data, dict):
                for key, value in data.items():
                    # 如果值是字符串，检查是否需要替换
                    if isinstance(value, str):
                        # 1. 统一路径分隔符 (把 Windows 的 \ 变成 /)
                        clean_value = value.replace("\\", "/")
                        
                        # 2. 检查是否包含目标路径 (比如 db/items/) 且不是 http 开头的
                        if any(t in clean_value for t in TARGET_PATHS) and not clean_value.startswith("http"):
                            
                            # 3. 去掉开头的 ./ 或 / (为了拼接 URL)
                            if clean_value.startswith("./"):
                                clean_value = clean_value[2:]
                            if clean_value.startswith("/"):
                                clean_value = clean_value[1:]
                                
                            # 4. 拼接最终 URL
                            final_url = BASE_URL + clean_value
                            data[key] = final_url
                            
                            print(f"✅ 替换: {value} \n   -> {final_url}")
                            replaced_count += 1
                    
                    # 递归处理字典或列表
                    else:
                        process_node(value)
            
            elif isinstance(data, list):
                for item in data:
                    process_node(item)

        # 开始处理
        process_node(db_data)
        
        # 保存回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(db_data, f, ensure_ascii=False, indent=2)

        print("-" * 50)
        print(f"🎉 处理完成！共替换了 {replaced_count} 个本地路径。")
        print(f"🔗 所有图片现在都指向: {BASE_URL}...")
        print("-" * 50)

    except Exception as e:
        print(f"❌ 发生错误: {e}")

if __name__ == '__main__':
    to_github_raw()
    