# 范围：只接现有聊天

这棵源码还不是可用的 Tellomi macOS 客户端。本机没有 Mac，没有跑 Xcode。

现在只准备接 teamgram 聊天。不接发现，不接 @tellomi。不为桌面补和聊天验收无关的 Telegram 服务。

邮箱登录先不做。总仓 `AGENTS.md` 写明邮箱登录暂缓。

首阶段聊天验收（都还没跑过）：登录、退出、会话列表、历史收发、图片和文件、已读、断线重连后的同步。

默认编译带 `TELLOMI_BUILD`：

- 显示名是 Tellomi
- 更新地址和 AppCenter 配置清空，不连 Telegram 的更新服务器
- 不使用上游的 api id / api hash
- 在创建网络参数之前失败
- 没设置 `TELLOMI_DC_CONFIG` 和 `TELLOMI_SERVER_PUBLIC_KEY`，或文件不存在，直接失败
- 两个文件都在，这一轮也不把它们送进 MTProto，避免退回 Telegram 生产数据中心和公钥

地址和公钥都不写在仓库里。
