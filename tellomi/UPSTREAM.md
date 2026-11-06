# 上游与更新

| 项 | 值 |
| --- | --- |
| 官方仓库 | https://github.com/TelegramMessenger/telegram-macos |
| 旧地址 | https://github.com/macosswift/telegram 会 301 到上面 |
| `overtake/TelegramSwift` | 2026-11-06 GitHub API 返回 404，不能当现行源码 |
| 分支 | `master`（没有 tag，也没有 GitHub Release） |
| 提交 | `561169337e838c3281f7cfe24652757a5b522df9`（2026-11-04） |
| 许可 | GPL-2.0，原文在 `clients/macos/LICENSE` |
| API layer | 232 |
| 服务端 | `tellomi/teamgram-server` master README：API Layer 232 |

layer 不在 macOS 仓库根上，而在它钉住的上游 iOS 依赖里：`submodules/telegram-ios` = `TelegramMessenger/Telegram-iOS` `fb0e62ba8a147f0821da6aa63c09da7d79a10111`。该提交的 `submodules/TelegramCore/Sources/State/Serialization.swift` 里 `currentLayer()` 返回 232。这和现行服务端同层，所以用这个 master 尖，没有为了“兼容”去改 layer，也没有另找更旧的提交。

这个 gitlink 不是 `tellomi/Telegram-iOS`。Tellomi 的 iOS 产品继续在那个独立仓库改。这里不把整份 Telegram-iOS 再复制进来。

工作树里提交了上游跟踪的源码。没有提交上游自己 gitignore 掉、但历史上又被加进索引的实验产物：`tools/perflab/**/results`、`xcuserdata`、`.claude/settings.local.json`。这些不是 `INSTALL.md` 要求的构建输入。

11 个依赖只钉在仓库根 `.gitmodules`，路径前缀 `clients/macos/`。内容不入库。`tg_owt` 和 `telegram-ios` 体积很大，按上游规则在要编译的机器上初始化，不整包放进总仓。

```bash
git submodule update --init --depth 1 clients/macos/submodules/rlottie
```

`submodules/libprisma` 钉的是 `31a5d6fbbef8136e4a2e5f7a8ba665da32857a631`，URL 是 `https://github.com/desktop-app/libprisma`。2026-11-06 这个提交在该仓库不存在，GitHub 提交搜索也是 0。该仓库 master 是另一个提交 `94640c63c20eacdf70e37e23198d9ab53c802ebd`。没有改钉，避免用另一个提交假装兼容。Xcode 工程引用 `submodules/libprisma/libprisma/grammars.dat`（代码高亮）。聊天协议本身不在这个库里。

要换上游：取 `TelegramMessenger/telegram-macos` 的新 master 提交，先读它钉的 `telegram-ios` 里 `currentLayer()`。只有这个数字仍等于 teamgram-server 当时的 layer，才更新源码和 gitlink。不要把根仓库改成 submodule。`clients/macos/tellomi/` 更新时保留。

连接配置：总仓 `AGENTS.md` 和 `docs/TELLOMI_RULES.md` 写了生产地址和端口。teamgram-server 里 `proto/mtproto/crypto/tools/public_key.pem` 是一份公钥；`tg_public_key.pem` 是 Telegram 的公钥，不能拿来当 Tellomi 的。没有一份已经核对过、可以写进客户端的「地址 + 这份公钥」组合，所以本轮不把地址或公钥写进源码。
