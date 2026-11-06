# 范围：只接现有聊天

这棵源码还不是可用的 Tellomi macOS 客户端。本机没有 Mac，没有跑 Xcode。

现在只准备接 teamgram 聊天。不接发现，不接 @tellomi。不为桌面补和聊天验收无关的 Telegram 服务。

邮箱登录先不做。总仓 `AGENTS.md` 写明邮箱登录暂缓。

首阶段聊天验收（都还没跑过）：登录、退出、会话列表、历史收发、图片和文件、已读、断线重连后的同步。

默认编译带 `TELLOMI_BUILD`。这不是已经接上聊天服务器。

网络边界是一个禁网 stub，不是完成的连接：

- 显示名是 Tellomi。更新地址和 AppCenter 配置清空，不连 Telegram 的更新服务器。
- 不使用上游的 api id / api hash。
- `AppDelegate` 和分享扩展在构造 `NetworkInitializationArguments` 之前调用 `TellomiConnection.refuseTelegramDefaults()`。这个函数的返回类型是 `Never`，后面的 MTProto 初始化到不了。
- 没设置 `TELLOMI_DC_CONFIG` 或 `TELLOMI_SERVER_PUBLIC_KEY`，或文件不存在：失败，原因是缺配置。
- 两个文件都在：仍然失败。原因是 MTProto 接入还没写，文件不会被读进协议栈，也不会改用 Telegram 的生产数据中心或公钥。

地址和公钥都不写在仓库里。真正把这两份文件送进 MTProto 是以后的聊天接入，不在这一支。
