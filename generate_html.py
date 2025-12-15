import json
import os
from urllib.parse import urlparse

# 1. 配置路径
INPUT_FILE = 'feed_data.json'      # 原始包含 https 链接的文件
OUTPUT_FILE = 'feed_data_soft_local.json'  # 替换后保存的文件名
DOWNLOAD_ROOT = 'downloads'        # 你存放资源的根文件夹

def local_link_replacer():
    if not os.path.exists(INPUT_FILE):
        print(f"❌ 错误：找不到文件 {INPUT_FILE}")
        return

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        data_list = json.load(f)

    print(f"开始处理 {len(data_list)} 条数据的链接替换...")

    for item in data_list:
        # --- 1. 替换作者头像链接 ---
        if item.get('author') and item['author'].get('avatar'):
            url = item['author']['avatar']
            if url.startswith('http'):
                filename = os.path.basename(urlparse(url).path)
                item['author']['avatar'] = f"{DOWNLOAD_ROOT}/avatars/{filename}"

        # --- 2. 替换 Clips (图片/视频) 链接 ---
        clips = item.get('clips') or []
        for clip in clips:
            url = clip.get('url')
            if url and url.startswith('http'):
                filename = os.path.basename(urlparse(url).path)
                clip['url'] = f"{DOWNLOAD_ROOT}/items/{filename}"

        # --- 3. 替换音乐链接 ---
        if item.get('music') and item['music'].get('url'):
            url = item['music']['url']
            if url and url.startswith('http'):
                filename = os.path.basename(urlparse(url).path)
                item['music']['url'] = f"{DOWNLOAD_ROOT}/musics/{filename}"

    # 保存结果
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data_list, f, ensure_ascii=False, indent=4)

    print(f"✅ 链接替换完成！新文件已保存为: {OUTPUT_FILE}")
    print("现在 JSON 中的 URL 已经全部指向本地 downloads 文件夹。")

if __name__ == "__main__":
    local_link_replacer()