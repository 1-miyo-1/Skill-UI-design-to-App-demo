# 05 Restore interactions

Common interactions + code patterns. The core is the **"trigger → state → render/animate"** three-part pattern.

## Carousel (home page contacts)

State lives in `activeIndex`; left/right switches the index; CSS transition animates. The middle item enlarges, the sides shrink.

```jsx
const [activeIndex, setActiveIndex] = useState(1)
// middle item (i === activeIndex) gets .is-active, sides get .is-side
<button onClick={() => setActiveIndex(i => Math.max(0, i - 1))}>‹</button>
```

```css
.carousel__item { transition: transform .3s, opacity .3s; }
.carousel__item.is-active { transform: scale(1); }
.carousel__item.is-side  { transform: scale(.9); opacity: .6; }
```

## Pointer drag (floating ball) ⚠️ scaling pitfall

After the page is scaled with `transform: scale`, **don't convert with `clientWidth`, use `getBoundingClientRect()`**:

```js
const rect = parent.getBoundingClientRect()
const dx = (e.clientX - start.clientX) / rect.width * 100   // convert to percent
```

Otherwise the drag drifts (a pitfall we hit). Full three-part pattern:

```jsx
onPointerDown={e => { dragRef.current = { x: e.clientX, y: e.clientY }; setDragging(true) }}
onPointerMove={e => { if (dragRef.current) setPos({ ... }) }}   // convert to % via rect
onPointerUp={() => { dragRef.current = null; setDragging(false) }}
```

## Long-press trigger (SOS)

In `onPointerDown`, `setTimeout(1000)`; if there's movement during that time, `clearTimeout`; when it fires, switch to the rail state.

```jsx
const timer = useRef(null)
const onDown = () => { timer.current = setTimeout(() => setSos(true), 1000) }
const onMove = () => { clearTimeout(timer.current) }   // movement → cancel long-press
const onUp   = () => { clearTimeout(timer.current) }
```

## Countdown (emergency call)

`useEffect` + `setTimeout` decrement by 1 each second; when it reaches zero, switch stage; between stages use another timer to advance.

```jsx
useEffect(() => {
  if (count <= 1) { setCalling(true); return }
  const t = setTimeout(() => setCount(c => c - 1), 1000)
  return () => clearTimeout(t)
}, [count])
```

## Weak hint bubble (auto-fades a few seconds after entering the page)

"fade in → stay a few seconds → fade out", same as the home onboarding bubble, using two `setTimeout`s + opacity transition:

```jsx
const [visible, setVisible] = useState(false)
useEffect(() => {
  const t1 = setTimeout(() => setVisible(true), 400)    // fade in 0.4s after entering
  const t2 = setTimeout(() => setVisible(false), 4400)  // fade out after 4.4s
  return () => { clearTimeout(t1); clearTimeout(t2) }
}, [])
```

```css
.hint { opacity: 0; transition: opacity .5s ease-in; }
.hint.is-visible { opacity: 1; }
```

## Self-check

Walk each interaction by hand on a real device / preview; don't just check "it compiles".
