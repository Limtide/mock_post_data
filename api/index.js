// 导入根目录的 db.json
const db = require('../db.json');

export default function handler(req, res) {
  // 1. 获取 URL 参数
  // count: 返回数量，默认 10
  // accept_video: 是否接收视频 ('true' 或 'false')
  const { count = 10, accept_video } = req.query;

  const limit = parseInt(count);
  const includeVideo = accept_video === 'true';

  // 2. 获取数据源 (假设数据在 feed_mixed 字段中)
  // 如果您的 db.json 结构不同，请修改这里，比如 db.list 或 db
  let dataPool = db.feed_mixed ? [...db.feed_mixed] : [];

  // 3. 筛选逻辑
  if (!includeVideo) {
    // 如果 accept_video 不为 true，则过滤掉所有 type == 1 (视频) 的数据
    dataPool = dataPool.filter(item => item.type !== 1);
  }

  // 4. 随机洗牌 (Fisher-Yates 算法)
  // 确保每次调用返回的顺序都不同
  for (let i = dataPool.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [dataPool[i], dataPool[j]] = [dataPool[j], dataPool[i]];
  }

  // 5. 截取指定数量
  const result = dataPool.slice(0, limit);

  // 6. 返回 JSON 结果
  res.status(200).json(result);
}