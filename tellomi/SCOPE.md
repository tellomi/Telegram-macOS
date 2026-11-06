# 范围：只接现有聊天

这棵源码还不是可用的 Tellomi macOS 客户端。本机没有 Mac，没有跑 Xcode。

现在只准备接 teamgram 聊天。不接发现，不接 @tellomi。不为桌面补和聊天验收无关的 Telegram 服务。

邮箱登录先不做。总仓 `AGENTS.md` 写明邮箱登录暂缓。

首阶段聊天验收（都还没跑过）：登录、退出、会话列表、历史收发、图片和文件、已读、断线重连后的同步。

这不是已经接上的聊天连接。登录验收还没做。

主程序和分享扩展在构造 `NetworkInitializationArguments` 之前无条件调用 `TellomiConnection.refuseTelegramDefaults()`。它返回 `Never`，所以后面的 MTProto 初始化编译进了文件，但运行到不了。这不依赖 `TELLOMI_BUILD` 宏。`ApiCredentials` 是独立 Swift package，主工程的宏到不了它；`apiId` / `apiHash` 现在直接失败，源码里不再保留上游凭证。

缺 `TELLOMI_DC_CONFIG` 或 `TELLOMI_SERVER_PUBLIC_KEY`，或文件不存在：失败，原因是缺配置。两个文件都在：仍然失败，原因是 MTProto 接入还没写。文件不会被读进协议栈，也不会改用 Telegram 的生产数据中心或公钥。

更新地址在实际使用的 `Telegram-Mac/Release.xcconfig` 里是空字符串。空字符串不会自动变回 Telegram 的更新域名；读取处对空地址直接失败。`SUPublicDSAKeyFile` 指向随包的本地公钥文件，用来校验更新包，它自己不会发起连接。没有更新地址时，不会去拉 Telegram 的更新。

显示名是 Tellomi。主程序和分享扩展的 bundle id 改成 `app.tellomi.macos` 和 `app.tellomi.macos.share`。目标名、签名团队，以及各个内部框架的 bundle id 仍是上游的，不能说已经全部改完。

没有 Mac，没有原生编译。libprisma 的 pin 仍是 `31a5d6fbbef8136e4a2b3adaf7b95e2ccaa7436d`，这次没有改。
