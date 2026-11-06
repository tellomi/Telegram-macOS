#!/bin/sh
# Compare this repo's import tip with tellomi/tellomi clients/macos.
# Exit 0 when the trees match. Exit 1 when they differ. Exit 2 when the
# monorepo checkout is not available, so a missing clone is not reported as a match.
set -eu

ROOT=$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)
IMPORT=e8b916851de51980cef3e9236ab65d78c5feffb7
# Optional TELLOMI_BASE / TELLOMI_LATER override the pinned SHAs for a local
# self-check only. A review run leaves them unset.
BASE=${TELLOMI_BASE:-59f5c5801885a90ad5ef7f180fd99ca786a80bc1}
LATER=${TELLOMI_LATER:-b5651a4054c5a804e79ee4421afb59f6fd3626ca}
RECORDED_IMPORT_TREE=e7b3b1a8a014783ac8f501055ee75c5ed9f8670a

import_tree=$(git -C "$ROOT" rev-parse "$IMPORT^{tree}")
echo "import commit $IMPORT"
echo "import tree   $import_tree"
echo "recorded tree $RECORDED_IMPORT_TREE"
if [ "$import_tree" != "$RECORDED_IMPORT_TREE" ]; then
    echo "import tip tree moved; refuse to compare against the recorded OID" >&2
    exit 1
fi

if [ -z "${TELLOMI_MONOREPO:-}" ]; then
    echo "TELLOMI_MONOREPO is unset."
    echo "github.com/tellomi/tellomi is not readable from this checkout (repository not found)."
    echo "The import tree above was computed in this repository. 59f5c580:clients/macos and b5651a40:clients/macos were not computed."
    if git -C "$ROOT" rev-parse -q --verify refs/tags/verified-b5651a40 >/dev/null; then
        echo "verified-b5651a40 points at $(git -C "$ROOT" rev-parse "verified-b5651a40^{}") and still means the b5651a40 subtree-split claim."
    else
        echo "verified-b5651a40 is not in this clone."
    fi
    if git -C "$ROOT" rev-parse -q --verify refs/tags/verified-59f5c580 >/dev/null; then
        echo "tag verified-59f5c580 points at $(git -C "$ROOT" rev-parse "verified-59f5c580^{}"). Its message is not a computation of the monorepo trees."
    else
        echo "tag verified-59f5c580 is not in this clone."
    fi
    echo "Exit 2 is not a match. Re-run with a local clone: TELLOMI_MONOREPO=/path/to/tellomi $0"
    exit 2
fi

if ! git -C "$TELLOMI_MONOREPO" cat-file -e "$BASE^{commit}" 2>/dev/null; then
    echo "monorepo is missing $BASE" >&2
    exit 2
fi
if ! git -C "$TELLOMI_MONOREPO" cat-file -e "$LATER^{commit}" 2>/dev/null; then
    echo "monorepo is missing $LATER" >&2
    exit 2
fi

base_tree=$(git -C "$TELLOMI_MONOREPO" rev-parse "$BASE:clients/macos")
later_tree=$(git -C "$TELLOMI_MONOREPO" rev-parse "$LATER:clients/macos")
echo "59f5c580:clients/macos $base_tree"
echo "b5651a40:clients/macos $later_tree"

status=0
if [ "$base_tree" != "$later_tree" ]; then
    echo "b5651a40:clients/macos differs from 59f5c580:clients/macos"
    git -C "$TELLOMI_MONOREPO" diff --stat "$BASE:clients/macos" "$LATER:clients/macos"
    status=1
fi
if [ "$base_tree" != "$import_tree" ]; then
    echo "import tip tree differs from ${BASE}:clients/macos"
    status=1
    cmp=$(mktemp -d)
    trap 'rm -rf "$cmp"' EXIT INT TERM
    git init -q "$cmp"
    mkdir -p "$cmp/.git/objects/info"
    {
        git -C "$ROOT" rev-parse --absolute-git-dir
        git -C "$TELLOMI_MONOREPO" rev-parse --absolute-git-dir
    } > "$cmp/git-dirs"
    while read -r git_dir; do
        printf '%s\n' "$git_dir/objects"
    done < "$cmp/git-dirs" > "$cmp/.git/objects/info/alternates"
    git -C "$cmp" diff-tree --find-renames --stat "$base_tree" "$import_tree"
fi
if [ "$status" -eq 0 ]; then
    echo "MATCH $BASE:clients/macos == $LATER:clients/macos == $IMPORT^{tree}"
    echo "Standalone commits after the import tip are:"
    git -C "$ROOT" diff --name-status "$IMPORT" HEAD
fi
exit "$status"
