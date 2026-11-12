# 澄波实验室公开快照验收与审计

## 快照边界

本文件只描述当前独立公开快照，不涉及其他仓库的历史或发布决策。

- 快照不包含派生工作树的 `.git`、本地工作记录、虚拟环境或 `node_modules`。
- 不包含上游 `reference/` 下的 PNG/JPG 参考位图及其关联 `example-spec.json`；可选示例脚本保留，具体边界见 `skill/house-plan-designer/reference/OPTIONAL-EXAMPLES.md`。
- 保留 MIT License、NOTICE 和 ZWD11 上游署名。
- 根目录 `index.html` 是实验室主导航；住宅以 `residential-demo.html` 作为可选通用能力示例。
- 所有实验室设备、尺寸和接口均为虚构或推断，不做承重、消防、配电或水力计算承诺。

## 案例入口与资料

- 导航：`index.html`
- A：`lab-demo.html`
- B：`examples/rf-electronics-lab/lab-demo-layout-b.html`
- 住宅：`residential-demo.html`
- 生成器：`examples/rf-electronics-lab/generate_demo.py`
- 接口表：`interface-requirements.csv`
- 专业确认：`professional-review.md`
- A/B 对比：`layout-comparison.md`
- 机器结果：`verification.json`

## 已继承的案例验证

当前快照只复制此前已验证工作树中的公开必需文件。该工作树的实验室验证结果为：A/B check 全通过，完整 QA 109/109，导出文件 22/22，A/B 水电审计均为 0 problems、0 notes、0 checkIssues；132 张 QA 截图和 A/B 展示图已人工复核。

## 当前快照复验

当前目录重新执行构建和 A/B `check.mjs`，并检查住宅入口、Markdown 相对链接、敏感信息、公开图片元数据、Pages 必需文件及发布清单。最新机器可读结果见 `verification.json`，最终文件和哈希见 `release-manifest.json`。

A/B 核心检查要求：`issues`、`errors`、`dimIssues`、`dimConflicts` 均为空，墙、门窗、标签和悬空墙端检查通过。Pages 要求：根目录导航、`.nojekyll` 和 `.github/workflows/pages.yml` 均存在，导航中的案例与文档链接有效。

## 使用限制

- 完整 QA 的 109/109 是源工作树验证结果；当前快照重点复验构建、A/B 核心检查、住宅入口和公开完整性。
- 未随包提供的上游可选示例素材不能用于复现对应的上游示例；这不影响内置实验室和住宅的构建与检查。
- 自动水电是通用规划与沟通功能，不能替代真实实验室的配电、接地、EMC、冷却、消防或其他专业设计。
- 远端仓库、GitHub Pages 和可见性不在本地快照验证范围内；未来发布时需另行确认。
