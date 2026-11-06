# 协议探测记录

这不是 macOS 客户端的登录或收发结果。临时脚本只在这次检查时运行，没有放进仓库，也没有进 Xcode 工程。它不调用 `auth.sendCode`、`auth.signIn` 或 `auth.signUp`，不读取 api hash，不对邮箱或手机号发码。

目标是生产 MTProto：`8.137.39.82:10443`。预发端口 `11443` 没有探测。探测发生在把 10443 从错误的 dev 标注改回生产端口之前；当时只建立了授权钥，没有用户会话，也没有写入账号或消息。之后没有再连这台服务器。

## 传输和调用

| 项 | 记录 |
| --- | --- |
| 传输 | TCP，混淆后的 abridged（首包含 `0xefefefef`） |
| 有没有已授权用户会话 | 没有。只有一把临时授权钥 |
| layer | 握手请求没有包 `initConnection` 或 `invokeWithLayer`。客户端钉的 layer 是 232，这次线上没有带这个数字 |
| `phone_code_hash` | 没有 |
| `purpose` | 没有 |
| 参数结构 | `req_pq_multi` 只有 nonce。`req_DH_params` 带 nonce、server nonce、p、q、服务器报出的指纹，以及加密的 `p_q_inner_data_dc`（内层 dc 为 1）。`set_client_DH_params` 带加密的 `client_DH_inner_data`。最后是未封装的 `ping` |

## 响应

| 步骤 | 结果 |
| --- | --- |
| `req_pq_multi` | `resPQ`。nonce 对得上。服务器给出两只指纹，其中一只对上仓库里的公钥 |
| `req_DH_params` | `server_DH_params_ok`（`0xd0e8075c`），dc 1 |
| `set_client_DH_params` | `dh_gen_ok`（`0x3bcbf734`）。`new_nonce` 的校验哈希对得上 |
| `ping` | 超时。没有收到错误帧 |

没有出现 `AUTH_RESTART`。这次没有发登录请求，所以这只说明握手和随后的 ping 没返回这个错误，不能据此判断邮箱登录的后端实现。

## 没有做的事

- 没有调用邮箱登录。服务端文档把邮箱放在 `auth.sendCode` 的 `phone_number` 里；这次没有发这个请求。
- 没有会话列表，没有消息收发。
- 没有原生编译。机器是 Linux，clang 是 Ubuntu 18.1.3，目标 `x86_64-pc-linux-gnu`。没有 `swiftc`、`xcodebuild`、`xcrun`、Xcode 或 Apple SDK。
