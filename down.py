import json
import os
import requests
import urllib3
import time
from urllib.parse import urlparse

# 1. 配置
INPUT_FILE = 'feed_data_with_video.json'          # 输入文件
OUTPUT_FILE = 'feed_data_local_with_video.json'   # 输出文件
DOWNLOAD_ROOT = 'downloads'            # 资源保存的根目录

# 禁用 SSL 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 配置网络请求
session = requests.Session()
session.trust_env = False
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def download_file(url, sub_folder):
    """
    通用下载函数
    """
    if not url:
        return None

    try:
        # 创建目录
        save_dir = os.path.join(DOWNLOAD_ROOT, sub_folder)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        # 提取文件名
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        
        # 防止文件名为空
        if not filename or '.' not in filename:
            ext = '.mp4' if 'video' in sub_folder else '.jpg'
            filename = f"file_{int(time.time())}{ext}"

        local_path = os.path.join(save_dir, filename)

        # 下载
        if not os.path.exists(local_path):
            print(f"   ⬇️ 下载中: {filename} ...", end="", flush=True)
            resp = session.get(url, headers=headers, stream=True, verify=False, timeout=15)
            if resp.status_code == 200:
                with open(local_path, 'wb') as f:
                    for chunk in resp.iter_content(chunk_size=1024):
                        f.write(chunk)
                print(" [成功]")
            else:
                print(f" [失败: {resp.status_code}]")
                return url 
        else:
            print(f"   ⏩ 已存在: {filename}")

        return local_path.replace('\\', '/')

    except Exception as e:
        print(f"   ❌ 下载异常: {e}")
        return url

def process_feed_data():
    if not os.path.exists(INPUT_FILE):
        print(f"错误: 找不到文件 {INPUT_FILE}")
        return

    print(f"正在读取 {INPUT_FILE} ...")
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        data_list = json.load(f)

    total_items = len(data_list)
    print(f"共加载 {total_items} 条数据，开始处理资源下载...\n")

    for index, item in enumerate(data_list):
        post_id = item.get('post_id', 'unknown')
        print(f"[{index+1}/{total_items}] 处理 Post ID: {post_id}")

        # --- A. 处理作者头像 (安全修复) ---
        # 使用 (item.get(...) or {}) 确保即使是 None 也会变成空字典
        author = item.get('author') or {}
        avatar_url = author.get('avatar')
        if avatar_url:
            local_avatar = download_file(avatar_url, 'avatars')
            if 'author' in item and item['author']: 
                item['author']['avatar'] = local_avatar

        # --- B. 处理 Clips (安全修复) ---
        # 关键修改：使用了 (item.get('clips') or [])
        # 这样即使 JSON 里是 "clips": null，这里也会变成 []，for 循环就不会报错了
        clips = item.get('clips') or []
        
        for clip in clips:
            clip_url = clip.get('url')
            if clip_url:
                local_clip = download_file(clip_url, 'items')
                clip['url'] = local_clip

        # --- C. 处理音乐 (安全修复) ---
        music = item.get('music') or {}
        music_url = music.get('url')
        if music_url:
            local_music = download_file(music_url, 'musics')
            if 'music' in item and item['music']:
                item['music']['url'] = local_music

    print(f"\n正在保存到 {OUTPUT_FILE} ...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data_list, f, ensure_ascii=False, indent=4)
    
    print("🎉 全部完成！")

if __name__ == "__main__":
    process_feed_data()