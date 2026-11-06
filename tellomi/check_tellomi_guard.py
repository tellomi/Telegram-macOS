# Copyright 2026 重庆半格智能科技有限公司
# SPDX-License-Identifier: AGPL-3.0-only
"""结构检查：macOS 守卫还在，telegram-ios 没有被整包复制进来。不编译客户端。"""
from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAC = ROOT
TEL = MAC / "tellomi"
UPSTREAM = "561169337e838c3281f7cfe24652757a5b522df9"
IOS_PIN = "fb0e62ba8a147f0821da6aa63c09da7d79a10111"
LIBPRISMA = "31a5d6fbbef8136e4a2b3adaf7b95e2ccaa7436d"
LIBPRISMA_NOT = "31a5d6fbbef8136e4a2e5f7a8ba665da32857a631"


def main() -> int:
    problems: list[str] = []
    upstream = (TEL / "UPSTREAM.md").read_text(encoding="utf-8")
    scope = (TEL / "SCOPE.md").read_text(encoding="utf-8")
    app = (MAC / "Telegram-Mac/app/AppDelegate.swift").read_text(encoding="utf-8")
    share = (MAC / "TelegramShare/ShareViewController.swift").read_text(encoding="utf-8")
    guard = (MAC / "Telegram-Mac/app/TellomiConnection.swift").read_text(encoding="utf-8")
    config = (MAC / "packages/ApiCredentials/Sources/ApiCredentials/Config.swift").read_text(encoding="utf-8")
    if UPSTREAM not in upstream or IOS_PIN not in upstream:
        problems.append("UPSTREAM.md 没有钉死 macOS 或 telegram-ios 提交")
    if "232" not in upstream:
        problems.append("UPSTREAM.md 没有写 layer 232")
    def call_is_unconditional(source: str, label: str) -> None:
        before = source.split("NetworkInitializationArguments(", 1)[0]
        if "TellomiConnection.refuseTelegramDefaults()" not in before:
            problems.append(f"{label} 在连网前没有调用守卫")
        window = before[-180:]
        if "#if TELLOMI_BUILD" in window:
            problems.append(f"{label} 的守卫仍包在 TELLOMI_BUILD 里，缺宏时会绕过")
    call_is_unconditional(app, "主程序")
    call_is_unconditional(share, "分享扩展")
    if "TELLOMI_DC_CONFIG" not in guard or "TELLOMI_SERVER_PUBLIC_KEY" not in guard:
        problems.append("守卫没有同时要求地址和公钥")
    if "MTProto wiring is not implemented" not in guard:
        problems.append("守卫没有写明 MTProto 尚未接入")
    if LIBPRISMA not in upstream or LIBPRISMA_NOT in upstream:
        problems.append("UPSTREAM.md 里的 libprisma SHA 不对")
    if "TELLOMI_BUILD" in config or "return 9" in config or "3975f648bb682ee889f35483bc618d1c" in config:
        problems.append("ApiCredentials 仍依赖主目标宏或仍保留上游凭证")
    if 'return "app.tellomi.macos"' not in config:
        problems.append("ApiCredentials 的 bundle id 仍是上游")
    project = (MAC / "Telegram.xcodeproj/project.pbxproj").read_text(encoding="utf-8")
    if 'OTHER_SWIFT_FLAGS[arch=*]' in project:
        problems.append("分享扩展仍有 arch 覆盖，会清掉继承的编译条件")
    if "ru.keepcoder.Telegram" in project:
        problems.append("主工程 bundle id 仍是上游")
    if "app.tellomi.macos" not in project:
        problems.append("主工程没有 Tellomi bundle id")
    feed = (MAC / "Telegram-Mac/updater/AppUpdateViewController.swift").read_text(encoding="utf-8")
    feed_fn = feed.split("private var updateFeedURL: URL {", 1)[1].split("private func makeUpdateDriver", 1)[0]
    if "fatalError" not in feed_fn or "does not fall back" not in feed_fn:
        problems.append("空的更新地址没有明确失败")
    if "osx.telegram.org" not in feed_fn:
        problems.append("更新地址守卫没有拒绝 Telegram 更新域")
    configs = [
        "configurations/Release.xcconfig" if (MAC / "configurations/Release.xcconfig").exists() else "Telegram-Mac/Release.xcconfig",
        "Telegram-Mac/Release.xcconfig",
        "Telegram-Mac/Debug.xcconfig",
        "Telegram-Mac/Beta.xcconfig",
        "configurations/Stable.xcconfig",
        "configurations/Beta.xcconfig",
        "configurations/Alpha.xcconfig",
        "configurations/AppStore.xcconfig",
    ]
    for rel in configs:
        text = (MAC / rel).read_text(encoding="utf-8")
        if "telegram.org" in text or "appcenter.ms" in text:
            problems.append(f"{rel} 仍有 Telegram 更新地址")
        if "SFEED_URL" in text and "SFEED_URL =" not in text:
            problems.append(f"{rel} 没有清空 SFEED_URL")
    def guarded_call_is_weak(source: str) -> bool:
        before = source.split("NetworkInitializationArguments(", 1)[0]
        return (
            "TellomiConnection.refuseTelegramDefaults()" not in before
            or "#if TELLOMI_BUILD" in before[-180:]
        )
    bad = "\n#if TELLOMI_BUILD\nTellomiConnection.refuseTelegramDefaults()\n#endif\nNetworkInitializationArguments("
    if not guarded_call_is_weak(bad):
        problems.append("负向检查没能发现被宏包住的守卫")
    restored = (MAC / "Telegram-Mac/Release.xcconfig").read_text(encoding="utf-8") + "\nSFEED_URL = https://osx.telegram.org/updates/versions.xml\n"
    if "osx.telegram.org" not in restored:
        problems.append("负向样例没有上游更新地址")
    if "osx.telegram.org" in (MAC / "Telegram-Mac/Release.xcconfig").read_text(encoding="utf-8"):
        problems.append("Release.xcconfig 被负向样例改写了")
    for path in TEL.rglob("*"):
        if not path.is_file() or path.name == "check_tellomi_guard.py":
            continue
        if "__pycache__" in path.parts or path.suffix == ".pyc":
            continue
        text = path.read_text(encoding="utf-8")
        for banned in ("149.154.", "8.137.39.82", "3975f648bb682ee889f35483bc618d1c"):
            if banned in text:
                problems.append(f"{path.relative_to(ROOT)} 含有不该写入的配置")
    listed = subprocess.check_output(["git", "-C", str(ROOT), "ls-files", "-s"], text=True)
    links = [line for line in listed.splitlines() if line.startswith("160000 ")]
    if len(links) != 11:
        problems.append(f"gitlink 数量是 {len(links)}，期望 11")
    if not any(IOS_PIN in line and line.endswith("submodules/telegram-ios") for line in links):
        problems.append("telegram-ios gitlink 不对")
    if not any(LIBPRISMA in line and line.endswith("submodules/libprisma") for line in links):
        problems.append("libprisma gitlink 不是上游树里的那个提交")
    ios_files = subprocess.check_output(
        ["git", "-C", str(ROOT), "ls-files", "submodules/telegram-ios"],
        text=True,
    ).splitlines()
    blobs = [line for line in ios_files if not line.endswith("submodules/telegram-ios")]
    if blobs:
        problems.append("telegram-ios 被整包放进来了")
    if "发现" not in scope or "邮箱" not in scope:
        problems.append("SCOPE.md 没有写发现和邮箱")
    if (ROOT / ".gitlab-ci.yml").exists():
        problems.append("仓库根还有 .gitlab-ci.yml")
    import_commit = "e8b916851de51980cef3e9236ab65d78c5feffb7"
    recorded_tree = "e7b3b1a8a014783ac8f501055ee75c5ed9f8670a"
    import_tree = subprocess.check_output(
        ["git", "-C", str(ROOT), "rev-parse", f"{import_commit}^{{tree}}"],
        text=True,
    ).strip()
    if import_tree != recorded_tree:
        problems.append(f"导入 tip 的树是 {import_tree}，记录的是 {recorded_tree}")
    # 片段拼起来再扫，避免门禁源码自己被整段凭证搜索命中。
    credential_needles = [
        "AIza" + "Sy",
        "a3406de8" + "d171bb422bb6ddf3bbd800e2",
        "945" + "75",
        "29663110" + "5913",
    ]
    credential_grep = subprocess.run(
        ["git", "-C", str(ROOT), "grep", "-I", "-n", *[arg for needle in credential_needles for arg in ("-e", needle)]],
        capture_output=True,
        text=True,
    )
    if credential_grep.returncode == 0:
        problems.append("tip 上还有上游凭证片段")
    elif credential_grep.returncode != 1:
        problems.append("凭证扫描没有正常结束")
    if not os.environ.get("TELLOMI_MONOREPO"):
        proved = subprocess.run(
            [str(TEL / "prove_macos_tree.sh")],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        if proved.returncode != 2:
            problems.append(f"没有总仓时 prove_macos_tree.sh 退出码是 {proved.returncode}，必须是 2")
        if "MATCH" in proved.stdout:
            problems.append("没有总仓时证明脚本报了 MATCH")
        if recorded_tree not in proved.stdout:
            problems.append("证明脚本没有打印已记录的导入树")
        if "was not created" in proved.stdout:
            problems.append("证明脚本仍把 verified-59f5c580 说成没有创建")
        sys.stdout.write(proved.stdout)
        if proved.stderr:
            sys.stderr.write(proved.stderr)

    def plist_string(text: str, key: str) -> str | None:
        marker = f"<key>{key}</key>"
        start = text.find(marker)
        if start < 0:
            return None
        match = re.search(r"<string>(.*?)</string>", text[start + len(marker):], re.S)
        return match.group(1) if match else None

    plist = (MAC / "Resources/config/GoogleService-Info.plist").read_text(encoding="utf-8")
    for key in ("API_KEY", "GCM_SENDER_ID", "GOOGLE_APP_ID", "STORAGE_BUCKET"):
        value = plist_string(plist, key)
        if value is None:
            problems.append(f"GoogleService-Info.plist 缺少 {key}")
        elif value.strip():
            problems.append(f"GoogleService-Info.plist 的 {key} 不是空占位")
    if plist_string(plist, "BUNDLE_ID") != "app.tellomi.macos":
        problems.append("GoogleService-Info.plist 的 bundle 不是 Tellomi 占位")
    if plist_string(plist, "PROJECT_ID") != "tellomi-placeholder":
        problems.append("GoogleService-Info.plist 的 PROJECT_ID 不是占位")
    for token in ("AIza", "telegram-9c34c", "keepcoder"):
        if token in plist:
            problems.append(f"GoogleService-Info.plist 仍含上游标识 {token}")
    lab = (MAC / "tools/networklab/tdlib_lab.py").read_text(encoding="utf-8")
    if re.search(r'os\.environ\.get\(\s*"TDLIB_API_(?:ID|HASH)"\s*,\s*"[^"]+"\s*\)', lab):
        problems.append("tdlib_lab.py 给 api 凭证留了非空默认值")
    if re.search(r"\b[0-9a-fA-F]{32}\b", lab):
        problems.append("tdlib_lab.py 仍含 32 位十六进制凭证")
    if "load_tdlib_api_credentials" not in lab or "tdlib_lab.local.json" not in lab:
        problems.append("tdlib_lab.py 没有环境变量或本地未跟踪配置入口")
    example = (MAC / "tools/networklab/tdlib_lab.local.json.example").read_text(encoding="utf-8")
    if example.count('""') < 2 or re.search(r"\b[0-9a-fA-F]{32}\b", example):
        problems.append("tdlib_lab.local.json.example 含有可用凭证")
    if problems:
        print("\n".join(problems), file=sys.stderr)
        return 1
    print(f"tellomi macos guard ok ({len(links)} submodule pins)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
