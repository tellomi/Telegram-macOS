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
| `README.md` | 用带来源说明的仓库 README 替换 GitHub 初始化的两行 README。上游正文留在下面。这是必要的文档替换，不是 force 覆盖 main。 |
| `Resources/config/GoogleService-Info.plist` | 去掉上游 Google `API_KEY`、`GCM_SENDER_ID`、`GOOGLE_APP_ID`、Firebase 项目 `telegram-9c34c` 和冒充 `ru.keepcoder.Telegram` 的 `BUNDLE_ID`。敏感字段留空，`BUNDLE_ID` 为 `app.tellomi.macos`，`PROJECT_ID` 为 `tellomi-placeholder`。没有写入 Tellomi 生产密钥。`FirebaseApp.configure()` 仍是注释。 |
| `tools/networklab/tdlib_lab.py` | `api_id` / `api_hash` 只从 `TDLIB_API_ID`、`TDLIB_API_HASH` 或未跟踪的 `tools/networklab/tdlib_lab.local.json` 读取。仓库内没有可用默认值。 |
| `tools/networklab/tdlib_lab.local.json.example`、`.gitignore` | 示例只有空字段。真正的本地文件被忽略，不入库。 |
| `tellomi/check_tellomi_guard.py` | 拒绝 plist 里的上游 Firebase 标识和非空密钥字段，以及 lab 脚本里的非空默认凭证。 |
| `tellomi/ALIGNMENT.md`、`tellomi/prove_macos_tree.sh` | 记下相对总仓 `clients/macos` @ `59f5c5801885a90ad5ef7f180fd99ca786a80bc1` 的核对方法。本环境读不到 `tellomi/tellomi`，所以没有用总仓对象算出 `59f5c580:clients/macos` 或 `b5651a40:clients/macos`。后来出现的附注标签 `verified-59f5c580` 没有被当成这个计算结果，也没有 force 改写。 |
| `tellomi/check_tellomi_guard.py`、`.github/workflows/tellomi-migration-gate.yml` | 迁移收口的测试门禁：守卫、导入树 OID、tip 上的凭证扫描，以及没有总仓时证明脚本必须退出 2。不构建安装包，不上传，不部署。 |

没有改发现、AI、邮箱登录。没有写入 DC、api hash 或 RSA。
