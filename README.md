# Solo Kitchen 初始化审核版

这是 `solo-kitchen` skill 的去个人化初始化副本，用于审核默认结构。

## 内容

- `skill/`：可安装/迁移的 skill 文件夹副本。
- `user-data-template/`：默认一人食用户数据模板，不包含真实个人信息。

## 默认设定

- 默认份量：1 人、1 餐。
- 库存：空。
- Obsidian：未配置。
- 可信来源：已引入原 `solo-kitchen` 的 trusted sources；其中待验证来源仍保留待验证标记。
- 位置、买菜渠道、预算、忌口、厨具、常备调料：均为空白占位。

## License

MIT License. See `LICENSE`.

## 使用方式

审核通过后，可把 `skill/` 作为新的 skill 初始版本，把 `user-data-template/` 中的文件复制到：

```text
~/.codex/user-data/solo-kitchen/
```

实际启用前仍建议走一次 orientation，补齐必填厨房档案。
