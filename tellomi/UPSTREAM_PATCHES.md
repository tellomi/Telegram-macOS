# UPSTREAM_PATCHES — 原生 macOS

上游是 `TelegramMessenger/telegram-macos` `561169337e838c3281f7cfe24652757a5b522df9`。只登记相对这一提交的 Tellomi 改动。依赖子模块没有改内容。

| 文件 | 原因 |
| --- | --- |
| `Telegram-Mac/app/TellomiConnection.swift` | 禁网 stub。缺配置或 MTProto 未实现都失败。不是已完成的连接。 |
| `Telegram.xcodeproj/project.pbxproj` | 编进守卫。去掉分享扩展 Release 里会清掉编译条件的 `OTHER_SWIFT_FLAGS[arch=*]`。主程序和分享扩展的 bundle id 改为 Tellomi。 |
| `Telegram-Mac/app/AppDelegate.swift` | 无条件在 `NetworkInitializationArguments` 之前调用守卫。 |
| `TelegramShare/ShareViewController.swift` | 分享扩展同样无条件调用，不依赖宏。 |
| `packages/ApiCredentials/Sources/ApiCredentials/Config.swift` | Swift package 不再读主目标宏，也不再保留上游 api id / api hash。bundle id 改为 `app.tellomi.macos`。 |
| `Telegram-Mac/updater/AppUpdateViewController.swift` | 空的更新地址直接失败，并拒绝 Telegram 的更新域名。 |
| `Telegram-Mac/Info.plist` | 显示名改为 Tellomi。`SUFeedURL` 仍来自 xcconfig。 |
| `configurations/*.xcconfig`、`Telegram-Mac/{Debug,Beta,Release}.xcconfig` | 更新地址和 AppCenter 配置清空。 |
| `tellomi/check_tellomi_guard.py` | 独立仓库根不再是总仓。守卫从 `tellomi/` 的上一级找根，gitlink 路径不再带 `clients/macos` 前缀。 |
| `tellomi/UPSTREAM.md`、`tellomi/NOTICE.md` | 路径改成独立仓库根，不再写 `clients/macos/`。 |

| `tellomi/upstream-ci-disabled/gitlab-ci.yml` | 上游 GitLab CI 移出仓库根，避免自动部署。文件保留。 |

没有改发现、AI、邮箱登录。没有写入 DC、api hash 或 RSA。
