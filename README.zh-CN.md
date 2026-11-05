# 特斯拉涂装工作流

[English](README.md) | 简体中文

从车机自定义涂装反复返工中整理出的可复用 Agent Skill：选择官方 UV 模板、检查上车朝向与镜像、局部去标、验证画面完整性，并控制每张 PNG 的大小。

## 内容

- [SKILL.md](SKILL.md)：完整制作与修复流程
- [踩坑复盘](references/pitfalls.md)：失败模式、对应防线与验收记录
- [提示模板](references/prompt-patterns.md)：生成、局部修复和去标
- [文件校验脚本](scripts/validate_wrap.py)：PNG / ZIP 校验与 SHA256
- [模板校验脚本](scripts/validate_template.py)：与官方模板逐像素比较透明轮廓

当前 skill 正文、参考文档和提示模板为中文；英文说明见 [English README](README.md)。

## 使用

将本仓库作为完整 skill 目录，按所用 Agent 平台支持的方式加载。可提出：

> 为 2025 款焕新 Model Y 制作车机涂装，使用匹配版本的官方模板，不含特斯拉车标，单张不超过 1 MB。分别报告文件、模板和实际车机映射的验证状态。

## 文件校验

依赖 Python 3 和 Pillow，在仓库根目录运行：

```bash
python -m pip install Pillow
python scripts/validate_wrap.py output.png --width 1024 --height 1024 --max-bytes 1000000
python scripts/validate_wrap.py batch.zip --width 1024 --height 1024 --max-bytes 1000000
```

宽高按实际车型官方模板调整；示例中的 1024 × 1024 不代表所有车型要求。1 MB 按 1,000,000 字节计算，限制针对每张 PNG，不是整个 ZIP。严格小于 1 MB 时使用 `--max-bytes 999999`。

脚本检查 PNG 签名、块 CRC、IEND、完整解码、尺寸、文件大小和 ZIP 内 PNG，并输出 SHA256；不会修改输入。退出码为 `0` 表示文件校验通过，`1` 表示未通过。

文件能解码不代表画面完整，也不代表 UV 朝向正确。模板边界、内容缺失、旋转和镜像需要单独检查；未进行真实车机测试时不能宣称已验证上车效果。

## 模板轮廓校验

生成前先检查原模板的透明通道：不可见像素也可能保存黑色或白色 RGB，仅看预览容易误判为边框或背景。生成预览即使看起来合理，也可能分辨率不符或边缘存在杂点。

最终导出、压缩后运行：

```bash
python scripts/validate_template.py --template template.png --candidate output.png
python scripts/test_validate_template.py
```

只读校验器要求尺寸一致，逐字节比较透明通道，报告溢色、缺失的不透明像素、边缘差异及原模板各连通区域的面积。不透明模板不能据此推断蒙版，会被拒绝。通过只说明二维轮廓匹配，不代表图案完整、车型选对或已验证真实上车方向。原始预览与最终上传文件应明确区分。

## 适用范围

用于车机自定义纹理，不适用于实体车衣生产刀模。车型模板与上传规格应以 [Tesla 官方 custom-wraps 仓库](https://github.com/teslamotors/custom-wraps) 的当前说明为准。本仓库不包含官方模板或影视图像资产，也不代表 Tesla 官方项目。

