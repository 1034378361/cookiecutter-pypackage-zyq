# 变更日志

所有项目的显著变更都将记录在此文件中。

此项目遵循[语义化版本](https://semver.org/lang/zh-CN/)，并使用[约定式提交](https://www.conventionalcommits.org/zh-hans/)格式。

## 未发布

### 新功能

* 项目初始化

## 如何更新此文件

此文件可以通过以下方式自动更新:

### 自动更新 (GitHub Actions)

以下事件将触发CHANGELOG自动更新:
- 推送新标签 (如 `v1.0.0`)
- 合并PR到主分支
- 手动触发GitHub Actions工作流

### 与发布流程集成

发布流程会自动使用CHANGELOG内容:
- 推送标签发布到PyPI时，自动提取对应版本的CHANGELOG部分
- GitHub Release的发布说明会自动使用提取的CHANGELOG内容
- 标签之间的所有变更会被正确分类并格式化

### 自定义配置

您可以通过创建配置文件来自定义CHANGELOG的生成:
- 支持`.changelog.yml`、`.changelog.json`等格式
- 可自定义提交类型映射
- 可自定义未知类型的默认分类
- 可自定义CHANGELOG标题和格式

### 手动命令

也可以使用以下命令手动更新:

```bash
# 从最新标签生成
make changelog

# 从最初提交生成完整历史
make changelog-init

# 使用自定义配置文件
python scripts/generate_changelog.py --config path/to/config.yml
```
