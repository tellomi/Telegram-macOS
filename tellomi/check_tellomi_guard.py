# Copyright 2026 重庆半格智能科技有限公司
# SPDX-License-Identifier: AGPL-3.0-only
"""结构检查：macOS 守卫还在，telegram-ios 没有被整包复制进来。不编译客户端。"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
MAC = ROOT / "clients" / "macos"
TEL = MAC / "tellomi"
UPSTREAM = "561169337e838c3281f7cfe24652757a5b522df9"
IOS_PIN = "fb0e62ba8a147f0821da6aa63c09da7d79a10111"


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
    if "refuseTelegramDefaults" not in app or "refuseTelegramDefaults" not in share:
        problems.append("主程序或分享扩展没有在连网前调用守卫")
    if "TELLOMI_DC_CONFIG" not in guard or "TELLOMI_SERVER_PUBLIC_KEY" not in guard:
        problems.append("守卫没有同时要求地址和公钥")
    if "will not fall back" not in guard:
        problems.append("守卫在文件存在时仍可能继续走上游")
    if "TELLOMI_BUILD" not in config:
        problems.append("api 凭证没有 Tellomi 分支")
    stable = (MAC / "configurations/Stable.xcconfig").read_text(encoding="utf-8")
    if "osx.telegram.org" in stable or "APPCENTER_SECRET =" not in stable:
        problems.append("Stable.xcconfig 仍指向 Telegram 更新")
    if "-DTELLOMI_BUILD" not in stable:
        problems.append("Stable.xcconfig 没有定义 TELLOMI_BUILD")
    for path in TEL.rglob("*"):
        if not path.is_file() or path.name == "check_tellomi_guard.py":
            continue
        text = path.read_text(encoding="utf-8")
        for banned in ("149.154.", "8.137.39.82", "3975f648bb682ee889f35483bc618d1c"):
            if banned in text:
                problems.append(f"{path.relative_to(ROOT)} 含有不该写入的配置")
    listed = subprocess.check_output(["git", "-C", str(ROOT), "ls-files", "-s", "clients/macos"], text=True)
    links = [line for line in listed.splitlines() if line.startswith("160000 ")]
    if len(links) != 11:
        problems.append(f"gitlink 数量是 {len(links)}，期望 11")
    if not any(IOS_PIN in line and line.endswith("clients/macos/submodules/telegram-ios") for line in links):
        problems.append("telegram-ios gitlink 不对")
    ios_files = subprocess.check_output(
        ["git", "-C", str(ROOT), "ls-files", "clients/macos/submodules/telegram-ios"],
        text=True,
    ).splitlines()
    blobs = [line for line in ios_files if not line.endswith("clients/macos/submodules/telegram-ios")]
    if blobs:
        problems.append("telegram-ios 被整包放进来了")
    if "发现" not in scope or "邮箱" not in scope:
        problems.append("SCOPE.md 没有写发现和邮箱")
    if problems:
        print("\n".join(problems), file=sys.stderr)
        return 1
    print(f"tellomi macos guard ok ({len(links)} submodule pins)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
