# Tesla Wrap Workflow · 特斯拉涂装工作流

从车机自定义涂装反复返工中整理出的可复用 Agent Skill：选择官方 UV 模板、检查上车朝向与镜像、局部去标、验证画面完整性，并控制每张 PNG 的大小。

## 内容

- [SKILL.md](SKILL.md)：完整制作与修复流程
- [踩坑复盘](references/pitfalls.md)：失败模式、对应防线与验收记录
- [提示模板](references/prompt-patterns.md)：生成、局部修复和去标
- [文件校验脚本](scripts/validate_wrap.py)：PNG / ZIP 校验与 SHA256

## 使用

将本仓库作为完整 skill 目录，按所用 Agent 平台支持的方式加载。可提出：

> 为 2025 款焕新 Model Y 制作车机涂装，使用匹配版本的官方模板，不含特斯拉车标，单张不超过 1 MB。分别报告文件、模板和实际车机映射的验证状态。

## 文件校验

依赖 Python 3 和 Pillow：

```bash
python -m pip install Pillow
python scripts/validate_wrap.py output.png --width 1024 --height 1024 --max-bytes 1000000
python scripts/validate_wrap.py batch.zip --width 1024 --height 1024 --max-bytes 1000000
```

宽高按实际车型官方模板调整。严格小于 1 MB 时使用 `--max-bytes 999999`。脚本检查 PNG 签名、块 CRC、IEND、完整解码、尺寸、文件大小和 ZIP 内 PNG，并输出 SHA256；不会修改输入。

文件能解码不代表画面完整，也不代表 UV 朝向正确。模板边界、内容缺失、旋转和镜像需要单独检查；未进行真实车机测试时不能宣称已验证上车效果。

## 适用范围

用于车机自定义纹理，不适用于实体车衣生产刀模。车型模板与上传规格应以 [Tesla 官方 custom-wraps 仓库](https://github.com/teslamotors/custom-wraps) 的当前说明为准。本仓库不包含官方模板或影视图像资产，也不代表 Tesla 官方项目。
