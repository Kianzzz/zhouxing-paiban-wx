# 主题结构规范

主题文件是 UTF-8 JSON。5 套内置主题位于 `assets/style-library/<theme-id>.json`，由 `scripts/rebuild_design_system.py` 生成；用户确认的学习主题位于 `assets/learned-style-library/<theme-id>.json`，不受重建脚本清理。参考项目只用于研究组件分层、配色角色和兼容策略，不复制其主题名称、组件代码或完整视觉骨架。

## 必填结构

```json
{
  "id": "example-theme",
  "name": "示例主题",
  "description": "一句话视觉定位",
  "order": 1,
  "default": false,
  "accent": "#01A539",
  "hue_range": 80,
  "heading_label": null,
  "css": ".note-to-mp { ... }",
  "evidence": {
    "source_type": "screenshot | url | mixed",
    "source": "不包含正文的来源说明",
    "observed": [],
    "inferred": [],
    "unobserved": [],
    "confidence": "high | medium | low"
  }
}
```

## 字段规则

- `id`：小写短横线 ID，与文件名一致。
- `name`：工具栏显示名称。当前顺序为绿白清简、墨蓝刊读、石墨档案、沙金手记、雾紫叙事。
- `order`：内置主题使用 1–5；学习主题从 100 开始，整个合并库内不得重复。
- `default`：整个合并库只能有一个默认主题；学习主题必须为 `false`。
- `accent`：原主题主色，用于换色基准。
- `hue_range`：0–180，决定哪些有彩色与主色属于同一可迁移色族；默认 80。
- `heading_label`：需要编号标签时填写，如 `TITEL`；否则为 `null`。
- `css`：完整主题 CSS。选择器必须以 `.note-to-mp` 为根，至少覆盖容器、H1–H3、正文、引用、代码、代码块和图片。
- `evidence`：记录来源和证据等级，不保存参考文章正文。`source_type` 必须是 `screenshot`、`url`、`mixed` 或 `original`；三个证据数组不能同时为空，高置信度必须至少有一项直接观察证据。

每个主题可提供自己的编号词，如 `TITEL`、`EDITION`、`OPINION`、`FILE`、`JOURNAL`、`STORY`、`STEP`；预览层将其转换为 `01 / 02 / 03` 顺序标签。

## 组件库

`assets/component-library.json` 必须恰好包含 `h1`、`h2`、`h3`、`quote`、`code`、`inline-code`、`strong`、`em`、`ordered-list`、`unordered-list`、`table`、`divider`、`link` 十三个模块。有序列表与无序列表必须使用独立选择器，不能让一种列表的设置覆盖另一种。每个模块的第一项必须是 `theme`，表示不覆盖完整主题；其余样式使用 `{{accent}}`、`{{soft}}`、`{{pale}}`、`{{dark}}`、`{{shadow}}` 色彩角色，由当前主色实时计算。组件覆盖在主题 CSS 之后，字号、字重和间距覆盖又位于组件之后。

## 换色逻辑

页面解析 CSS 中的十六进制和 `rgb/rgba` 颜色。与原主色同色系的颜色按 H/S/L 相对偏移迁移到新主色；alpha 保持不变，中性色保持不变。原主题为黑白灰时，只迁移深色识别元素，避免正文整体染色。

## 兼容限制

禁止 `@import`、`@font-face`、JavaScript、外链背景图、CSS expression、动画、关键帧、hover 和 CSS counter。学习主题不得包含媒体查询；内置品牌源样式只允许已有的简单窄屏规则，不能新增复杂响应式依赖。字体只能使用本规范支持的系统字体栈。预览外壳的交互动效不属于主题 CSS，也不会进入复制后的正文。
