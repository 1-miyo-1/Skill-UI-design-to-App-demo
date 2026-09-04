# 03 Pages & routes

> Component granularity, global-state lifting, etc. live in `references/00_project_conventions.md` §4, §5.

## Pages → route table (this example)

> General approach: derive the route table from the mockup's page list — don't copy this example.

| Route | Component |
|-------|-----------|
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

## Self-check

Every route has a matching file; from `/` you can click all the way to the deepest page and back without a white screen in between.
