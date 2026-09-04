# 03 页面拆分与路由

> 组件粒度、全局状态提升等约定见 `references/00_project_conventions.md` §4、§5。

## 页面 → 路由表（本次示例）

> 通用做法：路由表由设计稿的页面清单推导，别照抄本例。

| 路由 | 组件 |
|------|------|
| `/` | Splash |
| `/register` | Register |
| `/onboarding` | Onboarding |
| `/home` | Home |
| `/chat/yeye` | Chat |
| `/chat/yeye/half` | ChatHalf |
| `/chat/yeye/full` | ChatFull |
| `/tools` | Tools |
| `/family` | Family |
| `/family/xiaoming` | XiaomingStory |
| `/family/xiaoming/park` | XiaomingPark |
| `/messages` | Messages |
| `/profile` | Profile |

## 自检

每个路由都有对应文件；`/` 能一路点到最深页面再点回来，中间不白屏。
