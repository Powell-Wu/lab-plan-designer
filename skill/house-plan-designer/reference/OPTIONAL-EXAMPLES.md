# 可选上游示例素材说明

本公开快照不包含上游 `reference/` 下的 PNG/JPG 参考位图，也不包含与这些输入图关联的 `example-spec.json`。这些素材的授权和虚构来源无法仅凭派生工作树独立确认，因此不作为公开交付内容。

`example-gen*.py` 等脚本作为通用代码参考保留。部分脚本中的 `underlay.image`、示例截图或输入文件名指向未随包提供的可选素材；运行这些特定示例前，用户必须提供自己有权使用的输入图并核对路径。

核心交付不依赖这些可选素材：

- `examples/rf-electronics-lab/` 的 A/B HouseSpec 和静态 HTML 可独立使用。
- `examples/duplex-villa/` 的虚构住宅 HouseSpec 和静态 HTML 可独立使用。
- `scripts/build.py`、`check.mjs`、`qa.mjs`、`elecaudit.mjs` 对以上内置案例的构建与检查不需要上游 reference 位图。
- 图像/CAD 识别脚本只在使用者另行提供输入图时运行，缺失可选示例图不会影响核心构建和检查。
