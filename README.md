# md_render

AstrBot 插件：将 Markdown 消息自动渲染为图片发送。

## 功能

- **自动渲染**：检测到 LLM 回复中包含 Markdown 格式（标题、表格、代码块、粗体、斜体等）时，自动渲染为 PNG 图片追加发送
- **手动渲染**：通过 `/render <markdown>` 指令手动渲染任意文本
- **主题切换**：支持深色/浅色主题，通过指令或配置面板切换

## 指令

| 指令 | 说明 |
|------|------|
| `/render <markdown>` | 手动渲染 Markdown 为图片 |
| `/render dark` | 切换为深色主题 |
| `/render light` | 切换为浅色主题 |

## 配置项

| 选项 | 默认值 | 说明 |
|------|--------|------|
| mode | auto | `auto` 自动渲染 / `manual` 仅响应 /render 指令 |
| theme | dark | `dark` 或 `light` |
| width | 600 | 图片宽度（px） |

## 系统依赖

容器内需要安装 `wkhtmltoimage`（包含在 `wkhtmltopdf` 包中）。

备用安装脚本：`/opt/astrbot/install_wkhtmltox.sh`

## 文件结构

```
md_render/
  __init__.py       — package 标识
  main.py           — 插件主逻辑
  themes.py         — 主题定义（新增主题只改这里）
  template.py       — HTML 模板生成
  _conf_schema.json — 配置面板 schema
  metadata.yaml     — 插件元信息
  requirements.txt  — Python 依赖
```
