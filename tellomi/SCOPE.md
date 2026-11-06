# 范围：只接现有聊天

这棵源码还不是可用的 Tellomi macOS 客户端。本机没有 Mac，没有跑 Xcode。

现在只准备接 teamgram 聊天。不接发现，不接 @tellomi。不为桌面补和聊天验收无关的 Telegram 服务。

邮箱登录和收发测试不在这一批。

首阶段聊天验收（都还没跑过）：登录、退出、会话列表、历史收发、图片和文件、已读、断线重连后的同步。

这不是已经接上的聊天连接。登录验收还没做。

DC 和 RSA 写在 `tellomi/server/tellomi-server.json`。种子是 `8.137.39.82:10443`，DC 1 和 DC 2 相同。构建前 `tellomi/apply_mtproto.py` 把它写进钉住的 `telegram-ios`：替换 Telegram 种子、关掉备用发现、握手只用 Tellomi 的公钥。`api_id` / `api_hash` 与 iOS 客户端一致。没有 Mac，没有跑过登录或收发，所以不能说已经接通。

跳过构建前的脚本时，子模块仍是上游种子。三个共享 scheme 和 `scripts/prepare-telegram-api.py` 都会先跑这个脚本；子模块没初始化时脚本失败，构建停住。

更新地址在实际使用的 `Telegram-Mac/Release.xcconfig` 里是空字符串。空字符串不会自动变回 Telegram 的更新域名；读取处对空地址直接失败。`SUPublicDSAKeyFile` 指向随包的本地公钥文件，用来校验更新包，它自己不会发起连接。没有更新地址时，不会去拉 Telegram 的更新。

显示名是 Tellomi。主程序和分享扩展的 bundle id 改成 `app.tellomi.macos` 和 `app.tellomi.macos.share`。目标名、签名团队，以及各个内部框架的 bundle id 仍是上游的，不能说已经全部改完。

没有 Mac，没有原生编译。libprisma 的 pin 仍是 `31a5d6fbbef8136e4a2b3adaf7b95e2ccaa7436d`，这次没有改。
