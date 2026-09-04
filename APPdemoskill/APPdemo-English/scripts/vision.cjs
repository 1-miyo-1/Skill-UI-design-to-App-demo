// 无原生视觉的模型（如 DeepSeek）读图：调 qwen-vl-max，拿回文字描述。
// 用法: node vision.cjs <图片路径> ["问题"]
// 前置: 设置环境变量 DASHSCOPE_API_KEY；Node 18+（内置 fetch）。
// 说明: 这是骨架，端点 / 模型名 / 鉴权按你的实际 qwen 账号微调即可。
const fs = require('fs')
const path = require('path')

const imgPath = process.argv[2]
const question = process.argv[3] || '描述这张图的整体布局、元素、配色、字体与尺寸'

if (!imgPath) {
  console.error('用法: node vision.cjs <图片路径> ["问题"]')
  process.exit(1)
}
const apiKey = process.env.DASHSCOPE_API_KEY
if (!apiKey) {
  console.error('请先设置 DASHSCOPE_API_KEY 环境变量')
  process.exit(1)
}

const MIME = {
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.webp': 'image/webp',
}
const mime = MIME[path.extname(imgPath).toLowerCase()] || 'image/png'
const b64 = fs.readFileSync(imgPath).toString('base64')

async function main() {
  const res = await fetch('https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: 'Bearer ' + apiKey,
    },
    body: JSON.stringify({
      model: 'qwen-vl-max',
      messages: [
        {
          role: 'user',
          content: [
            { type: 'image_url', image_url: { url: 'data:' + mime + ';base64,' + b64 } },
            { type: 'text', text: question },
          ],
        },
      ],
    }),
  })
  const data = await res.json()
  console.log(data.choices?.[0]?.message?.content ?? JSON.stringify(data))
}

main().catch((e) => {
  console.error(e)
  process.exit(1)
})
