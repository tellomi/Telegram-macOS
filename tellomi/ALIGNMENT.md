# 总仓 clients/macos 对齐

复审要核对的基线是总仓 `tellomi/tellomi` 的 `clients/macos` @ `59f5c5801885a90ad5ef7f180fd99ca786a80bc1`（#1833 squash，原 head `82cfb8993e221e082372a8ab3c3a1229189fe266`）。

导入 tip 是 `e8b916851de51980cef3e9236ab65d78c5feffb7`。它的根树 OID 是 `e7b3b1a8a014783ac8f501055ee75c5ed9f8670a`。已推送的附注标签 `verified-b5651a40` 指向这个导入 tip，说明文字仍是「对 `b5651a4054c5a804e79ee4421afb59f6fd3626ca` 做 subtree split」。这次没有移动、没有 force 改写这个标签。

附注标签 `verified-59f5c580` 现在在本仓能看到，对象仍是导入 tip `e8b916851de51980cef3e9236ab65d78c5feffb7`。标签说明声称这棵树等于总仓 `59f5c580:clients/macos`，也等于 `b5651a40:clients/macos`。那是标签作者的声明。下面的探测没有拿到总仓对象，所以本仓不能复核这两个树 OID，也不能把这个标签当成复核结果。没有移动、没有 force 改写 `verified-b5651a40` 或 `verified-59f5c580`。

## 本环境的探测（2026-11-06）

GitHub App 安装令牌只能看见 `tellomi/Telegram-macOS`。

```text
gh api repos/tellomi/tellomi/commits/59f5c5801885a90ad5ef7f180fd99ca786a80bc1
-> HTTP 404 Not Found

git ls-remote https://github.com/tellomi/tellomi.git HEAD
-> remote: Repository not found.

git cat-file -t 59f5c5801885a90ad5ef7f180fd99ca786a80bc1
-> fatal: git cat-file: could not get object info

git cat-file -t b5651a4054c5a804e79ee4421afb59f6fd3626ca
-> fatal: git cat-file: could not get object info
```

本仓对象库里没有这两个提交，也没有 `82cfb8993e221e082372a8ab3c3a1229189fe266`。公开的 `tellomi/Telegram`、`tellomi/Telegram-iOS`、`tellomi/Telegram-Windows`、`tellomi/teamgram-server` 里同样没有这几个 SHA。

因此这里不能证明 `b5651a40:clients/macos` 与 `59f5c580:clients/macos` 相同，也不能证明导入 tip 的树等于其中任何一个。相对公开上游 `TelegramMessenger/telegram-macos` `561169337e838c3281f7cfe24652757a5b522df9` 的差量仍然只说明上游 pin，不能代替这个基线。

## 同日再探（迁移收口）

导入 tip 的根树在本仓用 `git rev-parse e8b916851de51980cef3e9236ab65d78c5feffb7^{tree}` 算出，仍是 `e7b3b1a8a014783ac8f501055ee75c5ed9f8670a`。

`gh api repos/tellomi/tellomi` 仍是 HTTP 404。`git ls-remote https://github.com/tellomi/tellomi.git HEAD` 仍是 `Repository not found`。`git cat-file -t` 对 `59f5c5801885a90ad5ef7f180fd99ca786a80bc1` 和 `b5651a4054c5a804e79ee4421afb59f6fd3626ca` 都拿不到对象。

所以这次仍然没有算出：

- `59f5c5801885a90ad5ef7f180fd99ca786a80bc1:clients/macos`
- `b5651a4054c5a804e79ee4421afb59f6fd3626ca:clients/macos`

`tellomi/prove_macos_tree.sh` 在没有 `TELLOMI_MONOREPO` 时退出码是 2。这不是匹配。标签在场也不改变这个退出码。

## 有总仓克隆时怎么核对

在能读到 `tellomi/tellomi` 的机器上，不要设置 `TELLOMI_BASE` 或 `TELLOMI_LATER`：

```bash
TELLOMI_MONOREPO=/path/to/tellomi tellomi/prove_macos_tree.sh
```

脚本打印三个树 OID：

- `59f5c580:clients/macos`
- `b5651a40:clients/macos`
- 导入 tip `e8b916851de51980cef3e9236ab65d78c5feffb7^{tree}`，必须仍是 `e7b3b1a8a014783ac8f501055ee75c5ed9f8670a`

三个 OID 相同：导入 tip 就是该基线，退出码 0。脚本接着打印 `e8b91685..HEAD` 的路径清单。这份清单只应包含独立仓库的路径改写、停用的 GitLab CI、README、清凭证，以及迁移收口的门禁：

```text
A	.github/workflows/tellomi-migration-gate.yml
M	.gitignore
M	README.md
M	Resources/config/GoogleService-Info.plist
A	tellomi/ALIGNMENT.md
M	tellomi/NOTICE.md
M	tellomi/UPSTREAM.md
M	tellomi/UPSTREAM_PATCHES.md
M	tellomi/check_tellomi_guard.py
A	tellomi/prove_macos_tree.sh
A	tellomi/upstream-ci-disabled/README.md
R100	.gitlab-ci.yml	tellomi/upstream-ci-disabled/gitlab-ci.yml
A	tools/networklab/tdlib_lab.local.json.example
M	tools/networklab/tdlib_lab.py
```

源码没有另做 subtree 丢文件。清单若多出别的路径，先看那份 diff。后面的连接配置不在这一份清单里。

OID 不同：退出码 1，并列出 `59f5c580:clients/macos` 与后续 tip、以及与导入树的差异。不要 force 改已经指向导入 tip 的 `verified-59f5c580`。

没有克隆：退出码 2。这不是匹配。

`verified-59f5c580` 已经指向导入 tip。不要移动它，也不要 force 改 `verified-b5651a40`。HEAD 比导入 tip 多了独立仓库调整，不要把 HEAD 标成「树与 59f5c580 相同」。

手工等价命令：

```bash
git -C /path/to/tellomi rev-parse \
  59f5c5801885a90ad5ef7f180fd99ca786a80bc1:clients/macos \
  b5651a4054c5a804e79ee4421afb59f6fd3626ca:clients/macos
git rev-parse e8b916851de51980cef3e9236ab65d78c5feffb7^{tree}
git diff --name-status e8b916851de51980cef3e9236ab65d78c5feffb7 HEAD
git rev-parse verified-b5651a40^{}
```

`git rev-parse verified-b5651a40^{}` 应仍是 `e8b916851de51980cef3e9236ab65d78c5feffb7`。
