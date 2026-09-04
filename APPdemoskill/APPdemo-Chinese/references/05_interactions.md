# 05 交互还原

常见交互 + 写法模板。核心是「**触发 → 状态 → 渲染/动画**」三段式。

## 轮播（首页联系人）

状态存 `activeIndex`，左右切换改 index，CSS transition 过渡。中间项放大、两侧缩小。

```jsx
const [activeIndex, setActiveIndex] = useState(1)
// 中间项 (i === activeIndex) 加 .is-active，两侧 .is-side
<button onClick={() => setActiveIndex(i => Math.max(0, i - 1))}>‹</button>
```

```css
.carousel__item { transition: transform .3s, opacity .3s; }
.carousel__item.is-active { transform: scale(1); }
.carousel__item.is-side  { transform: scale(.9); opacity: .6; }
```

## 指针拖拽（悬浮球）⚠️ 缩放坑

页面被 `transform: scale` 缩放后，**不能用 `clientWidth` 换算，要用 `getBoundingClientRect()`**：

```js
const rect = parent.getBoundingClientRect()
const dx = (e.clientX - start.clientX) / rect.width * 100   // 换算成百分比
```

否则拖拽会漂移（本次踩坑）。完整三段式：

```jsx
onPointerDown={e => { dragRef.current = { x: e.clientX, y: e.clientY }; setDragging(true) }}
onPointerMove={e => { if (dragRef.current) setPos({ ... }) }}   // 用 rect 换算成 %
onPointerUp={() => { dragRef.current = null; setDragging(false) }}
```

## 长按触发（SOS）

`onPointerDown` 里 `setTimeout(1000)`，期间若位移则 `clearTimeout`；到点触发滑轨态。

```jsx
const timer = useRef(null)
const onDown = () => { timer.current = setTimeout(() => setSos(true), 1000) }
const onMove = () => { clearTimeout(timer.current) }   // 有位移 → 取消长按
const onUp   = () => { clearTimeout(timer.current) }
```

## 倒计时（紧急呼叫）

`useEffect` + `setTimeout` 每秒减 1，归零切换阶段；阶段间再用定时器推进。

```jsx
useEffect(() => {
  if (count <= 1) { setCalling(true); return }
  const t = setTimeout(() => setCount(c => c - 1), 1000)
  return () => clearTimeout(t)
}, [count])
```

## 弱提示气泡（进入页面几秒后自动淡出）

「淡入 → 停留几秒 → 淡出」，和首页引导气泡同款，用两个 `setTimeout` + opacity 过渡：

```jsx
const [visible, setVisible] = useState(false)
useEffect(() => {
  const t1 = setTimeout(() => setVisible(true), 400)    // 进入后 0.4s 淡入
  const t2 = setTimeout(() => setVisible(false), 4400)  // 4.4s 后淡出
  return () => { clearTimeout(t1); clearTimeout(t2) }
}, [])
```

```css
.hint { opacity: 0; transition: opacity .5s ease-in; }
.hint.is-visible { opacity: 1; }
```

## 自检

每个交互在真机/预览里手动走一遍，别只看「能编译」。
