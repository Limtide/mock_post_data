import json
import os

def sort_json_file(file_path='feed_data.json', reverse=False):
    """
    读取 JSON 文件并按 post_id 排序
    :param file_path: 文件路径
    :param reverse: False=从小到大(升序), True=从大到小(降序)
    """
    
    # 1. 检查文件是否存在
    if not os.path.exists(file_path):
        print(f"❌ 错误: 找不到文件 {file_path}")
        return

    print(f"正在读取 {file_path} ...")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data_list = json.load(f)
            
        if not data_list:
            print("文件为空，无需排序。")
            return

        print(f"读取成功，共 {len(data_list)} 条数据。")
        print("正在按 post_id 进行排序...")

        # 2. 核心排序逻辑
        # key=lambda x: int(x.get('post_id', 0)) 
        # 解释：取出 post_id 并转为整数(int)进行比较。
        # 如果不转 int，字符串排序 "100" 会排在 "2" 前面，这通常不是你想要的。
        data_list.sort(key=lambda x: int(x.get('post_id', 0)), reverse=reverse)

        # 3. 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data_list, f, ensure_ascii=False, indent=4)
            
        print(f"✅ 排序完成！已保存到 {file_path}")
        
        # 打印前3个ID验证一下
        print("前3个ID示例:", [item.get('post_id') for item in data_list[:3]])

    except Exception as e:
        print(f"❌ 发生错误: {e}")

if __name__ == "__main__":
    # 默认是从小到大排序 (升序)
    sort_json_file('feed_data_with_video.json', reverse=False)
    
    # 如果你想从大到小排序 (最新的ID在前面)，请把上面改为:
    # sort_json_file('feed_data.json', reverse=True)