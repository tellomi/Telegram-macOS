# UPSTREAM_PATCHES — 原生 macOS

上游是 `TelegramMessenger/telegram-macos` `561169337e838c3281f7cfe24652757a5b522df9`。只登记相对这一提交的 Tellomi 改动。依赖子模块没有改内容。

| 文件 | 原因 |
| --- | --- |
| `Telegram-Mac/app/TellomiConnection.swift` | 新文件。禁网 stub：缺配置就失败；配置文件在也不送进 MTProto，不回退 Telegram 生产。不是已完成的连接。 |
| `Telegram.xcodeproj/project.pbxproj` | 把上面的文件编进主目标和分享扩展。 |
| `Telegram-Mac/app/AppDelegate.swift` | `TELLOMI_BUILD` 时，在 `NetworkInitializationArguments` 之前调用守卫。 |
| `TelegramShare/ShareViewController.swift` | 分享扩展同样在连网之前调用守卫。 |
| `packages/ApiCredentials/Sources/ApiCredentials/Config.swift` | `TELLOMI_BUILD` 不返回上游 api id / api hash。 |
| `Telegram-Mac/Info.plist` | 显示名改为 Tellomi。目标名仍是上游的，避免改 Xcode 目标结构。 |
| `configurations/*.xcconfig`、`Telegram-Mac/{Debug,Beta,Release}.xcconfig` | 默认加上 `-DTELLOMI_BUILD`。清空更新地址和 AppCenter 配置，避免连到 Telegram 的更新服务。 |

没有改发现、AI、邮箱登录。没有写入 DC、api hash 或 RSA。
