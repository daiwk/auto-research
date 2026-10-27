# 网站功能演示

[返回项目入口](../../project-readme.md) · [可暂停的 MP4](site-tour.mp4) · [动画 WebP](site-tour.webp)

演示使用真实网站的操作状态，另加章节字幕；没有生成虚构界面或模拟实验成绩。
内容依次介绍首页入口、论文库、主题目录、四层问答、解释与来源、最近新增和公开实验看板。
每轮不超过一分钟，无声；README 默认播放 WebP，减少动态效果偏好下显示静态封面。
MP4 可暂停或逐段查看。录制日期、各段时长、尺寸、帧数和文件 SHA256 见 [媒体回执](site-tour.json)。

## 更新演示

1. 先通过问答完整性检查并构建网站，打开实际页面，导出各操作状态的截图。
2. 写一份 storyboard JSON：记录源码提交、录制日期与截图文件路径，逐段给出标题、字幕、秒数。
3. 使用已安装的 FFmpeg、ImageMagick、libwebp 和 Python Pillow 生成视频并转换：

```bash
python scripts/create_site_tour.py /path/to/storyboard.json --output docs/assets/media
```

macOS 默认使用 `Heiti-SC-Medium`；其它系统可用 `magick -list font` 查已安装中文字体，
再传 `--font`。脚本先编码真实画面的 MP4，再从视频的章节边界取帧压成动画 WebP，
检查 MP4 与 WebP 时长一致、存在多帧且动画小于 8 MiB；也生成减少动态效果用的静态封面。
临时 PNG 和编码列表会自动清理，保留源 MP4、WebP、封面与回执。

storyboard 的单段字段为 `file`、`title`、`caption`、`seconds`；根字段为
`recorded`、`source_commit`、`scenes`。所有段落秒数之和必须大于零且不超过 60 秒。
