import requests
import json
import time
import urllib3
import os

# 禁用 SSL 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def fetch_feed_corrected(target_new_count=30, output_file='feed_data.json'):
    """
    修正版：
    1. 参数改为 accept_video_clip
    2. 检测 clips 中是否包含 .mp4
    """
    
    # --- 1. 初始化 & 加载本地旧数据 ---
    all_data_list = []
    global_existing_ids = set()

    if os.path.exists(output_file):
        try:
            if os.path.getsize(output_file) > 0:
                with open(output_file, 'r', encoding='utf-8') as f:
                    all_data_list = json.load(f)
                    for item in all_data_list:
                        pid = item.get('post_id')
                        if pid:
                            global_existing_ids.add(pid)
                print(f"[Init] 已加载旧数据: {len(all_data_list)} 条")
            else:
                print("[Init] 发现空文件，将重新覆盖。")
        except Exception as e:
            print(f"[Warning] 旧文件读取出错 ({e})")
    else:
        print("[Init] 无旧文件，将创建新文件。")

    # --- 2. 配置 ---
    url = "https://college-training-camp.bytedance.com/feed/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Content-Type": "application/json"
    }
    
    # 【核心修改】：修正参数名
    params = {
        "count": 50, 
        "accept_video_clip": "false" # 修正为下划线，且通常用字符串 "true"
    }

    session = requests.Session()
    session.trust_env = False 

    # --- 3. 循环抓取 ---
    newly_added_count = 0      
    no_new_data_batches = 0    
    page_num = 1
    
    # 统计视频数量
    video_found_count = 0

    print(f"--- 启动抓取，目标新增: {target_new_count} 条 ---")

    while newly_added_count < target_new_count:
        try:
            # 【优化点】：先打印，再请求。这样你就知道程序在动了。
            print(f"\n[Page {page_num}] 正在请求 API...", end="", flush=True)
            response = session.get(url, headers=headers, params=params, timeout=10, verify=False)
            # 【优化点】：先打印，再请求。这样你就知道程序在动了。
            print(f"\n[Page {page_num}] 请求 API结束...", end="", flush=True)
            if response.status_code != 200:
                print(f"[Error] 请求失败: {response.status_code}")
                break

            data = response.json()
            post_list = data.get('post_list', [])

            if not post_list:
                print("[Info] API未返回数据。")
                break
            
            print(f"\n>> 正在处理第 {page_num} 页 (原始: {len(post_list)} 条)...")
            
            items_to_save_this_round = []
            batch_seen_ids = set() 

            for index, item in enumerate(post_list):
                pid = item.get('post_id')

                # 基础检查
                if not pid: continue
                if pid in batch_seen_ids: continue # API内部重复
                if pid in global_existing_ids:     # 历史重复
                    batch_seen_ids.add(pid)
                    continue


                # 保存
                items_to_save_this_round.append(item)
                global_existing_ids.add(pid) 
                batch_seen_ids.add(pid)

            count_this_round = len(items_to_save_this_round)
            
            # --- 实时保存 ---
            if count_this_round > 0:
                all_data_list.extend(items_to_save_this_round)
                newly_added_count += count_this_round
                no_new_data_batches = 0 
                
                try:
                    with open(output_file, 'w', encoding='utf-8') as f:
                        json.dump(all_data_list, f, ensure_ascii=False, indent=4)
                    print(f"   ✅ 本页入库 {count_this_round} 条 (本次累计发现视频: {video_found_count})")
                except Exception as write_err:
                    print(f"   [Error] 写入文件失败: {write_err}")

            else:
                no_new_data_batches += 1
                print(f"   ⭕ 本页无新数据。")

            # 结束判断
            if newly_added_count >= target_new_count:
                print("\n✅ 任务完成！")
                break

            if no_new_data_batches >= 5:
                print("\n⛔ 连续无新数据，停止。")
                break

            page_num += 1
            time.sleep(0.5)

        except Exception as e:
            print(f"\n[Exception] 发生异常: {e}")
            break

if __name__ == "__main__":
    fetch_feed_corrected(target_new_count=100)