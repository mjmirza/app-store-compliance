#!/usr/bin/env python3
"""Install the guard, skill and audit command into every supported AI coding tool other than Claude Code.
Usage. install_harness.py <tool> [install|doctor|uninstall] [--dry-run] [--repo DIR]. Configs are merged, never replaced."""

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GUARD_NAME = "app-store-compliance-guard.sh"
PAYLOAD_DIRS = ("docs", "data", "references", "templates", "scripts")
SUBMIT = "fast" + "lane deliver"
PROBLEMS = []
UNVERIFIED = []
KIMI_BEGIN = "# >>> app-store-compliance guard >>>"
KIMI_END = "# <<< app-store-compliance guard <<<"
KIMI_SEP_FILE = ".app-store-compliance-kimi-sep"

# How each tool runs a hook before a shell command, from each vendor's hook reference.
# style nested. groups of {matcher, hooks:[...]} under the event. flat. a list of entries under the event.
SPECS = {
    "codex": {
        "name": "Codex CLI",
        "style": "nested",
        "event": "PreToolUse",
        "matcher": "Bash",
        "timeout": ("timeout", 120),
    },
    "gemini": {
        "name": "Gemini CLI",
        "style": "nested",
        "event": "BeforeTool",
        "matcher": "run_shell_command",
        "timeout": ("timeout", 120000),
    },
    "grok": {
        "name": "Grok",
        "style": "nested",
        "event": "PreToolUse",
        "matcher": "Bash|run_terminal_command|run_terminal_cmd|bash|monitor",
        # Grok Build's shell tools. A matcher must cover all of them, so an old Bash-only entry is repaired.
        "tools": ("run_terminal_command", "run_terminal_cmd", "bash", "monitor"),
        "timeout": ("timeout", 120),
    },
    "qwen": {
        "name": "Qwen Code",
        "style": "nested",
        "event": "PreToolUse",
        "matcher": "run_shell_command",
        "timeout": ("timeout", 120),
    },
    "droid": {
        "name": "Factory Droid",
        "style": "nested",
        "event": "PreToolUse",
        "matcher": "Execute",
        "timeout": ("timeout", 120),
    },
    "auggie": {
        "name": "Augment Auggie",
        "style": "nested",
        "event": "PreToolUse",
        "matcher": "launch-process",
        "timeout": ("timeout", 120000),
    },
    "cursor": {"name": "Cursor", "style": "flat", "event": "beforeShellExecution"},
    "copilot": {"name": "Copilot CLI and VS Code", "style": "copilot"},
    "copilot-repo": {"name": "Copilot cloud agent and JetBrains", "style": "copilot"},
    "windsurf": {"name": "Windsurf", "style": "flat", "event": "pre_run_command"},
    "kimi": {"name": "Kimi Code", "style": "toml"},
    "opencode": {"name": "OpenCode", "style": "plugin"},
}
TOOLS = tuple(SPECS)
AFTER = {
    "codex": "Open Codex and run /hooks once to approve the new hook. Codex runs no new or changed hook until you do.",
    "gemini": "Restart Gemini CLI so it loads the hook. Skills need Gemini CLI 0.24 or later, the hook works from 0.22.",
    "grok": "Start a new Grok session so it loads the hook.",
    "qwen": "Restart Qwen Code so it loads the hook.",
    "droid": "Start a new Droid session so it loads the hook.",
    "auggie": "Start a new Auggie session so it loads the hook.",
    "cursor": "Restart Cursor so it loads ~/.cursor/hooks.json.",
    "copilot": "Start a new Copilot CLI session, and reload VS Code, so they load the hook.",
    "copilot-repo": "Commit .github/hooks to your default branch. The Copilot cloud agent reads hooks only from there.",
    "windsurf": "Restart Windsurf so it loads the hook.",
    "kimi": "Restart Kimi Code so it loads the hook.",
    "opencode": "Restart OpenCode so it loads the plugin.",
}


def home():
    h = os.environ.get("HOME")
    if not h:
        sys.exit("HOME is not set, so there is no folder to install into.")
    return h


def qwen_dir():
    """Qwen Code's global folder. QWEN_HOME wins, with a leading tilde expanded, as Qwen's own Storage does."""
    v = os.environ.get("QWEN_HOME")
    if not v:
        return os.path.join(home(), ".qwen")
    if v == "~" or v.startswith("~/") or v.startswith("~\\"):
        v = os.path.join(home(), v[2:])
    return os.path.abspath(v)


def kimi_dir():
    """Kimi Code's data folder. KIMI_CODE_HOME wins, with a leading tilde expanded, as its docs describe."""
    v = os.environ.get("KIMI_CODE_HOME")
    if not v:
        return os.path.join(home(), ".kimi-code")
    if v == "~" or v.startswith("~/") or v.startswith("~\\"):
        v = os.path.join(home(), v[2:])
    return os.path.abspath(v)


def copilot_dir():
    """Copilot CLI's user folder. COPILOT_HOME wins, as the hooks reference describes."""
    v = os.environ.get("COPILOT_HOME")
    if not v:
        return os.path.join(home(), ".copilot")
    if v == "~" or v.startswith("~/") or v.startswith("~\\"):
        v = os.path.join(home(), v[2:])
    return os.path.abspath(v)


def skill_dir():
    return os.path.join(home(), ".agents", "skills", "app-store-compliance")


def layout(tool, repo_dir=None):
    """Where each tool keeps its hooks, its hook config and its commands, from each tool's own docs."""
    h = home()
    if tool == "copilot-repo":
        base = os.path.join(repo_dir or "", ".github")
        return {
            "hooks": os.path.join(base, "hooks"),
            "config": os.path.join(base, "hooks", "app-store-compliance.json"),
            "command": None,
            "wrap": True,
        }
    if tool == "opencode":
        base = os.path.join(
            os.environ.get("XDG_CONFIG_HOME") or os.path.join(h, ".config"), "opencode"
        )
        return {
            "hooks": os.path.join(base, "hooks"),
            "config": os.path.join(base, "plugins", "app-store-compliance.js"),
            "command": os.path.join(base, "commands", "app-store-audit.md"),
            "wrap": True,
        }
    if tool == "droid":
        base = os.path.join(h, ".factory")
        hooks_json, settings = (
            os.path.join(base, "hooks.json"),
            os.path.join(base, "settings.json"),
        )
        # Droid reads settings.json hooks only while hooks.json is absent. Creating hooks.json would switch them off.
        uses_settings = not os.path.exists(hooks_json) and has_hooks_key(settings)
        return {
            "hooks": os.path.join(base, "hooks"),
            "config": settings if uses_settings else hooks_json,
            "command": None,
            "wrap": uses_settings,
        }
    bases = {
        "codex": os.environ.get("CODEX_HOME") or os.path.join(h, ".codex"),
        "gemini": os.path.join(h, ".gemini"),
        "grok": os.path.join(h, ".grok"),
        "qwen": qwen_dir(),
        "auggie": os.path.join(h, ".augment"),
        "cursor": os.path.join(h, ".cursor"),
        "copilot": copilot_dir(),
        "windsurf": os.path.join(h, ".codeium", "windsurf"),
        "kimi": kimi_dir(),
    }
    base = bases[tool]
    configs = {
        "codex": "hooks.json",
        "gemini": "settings.json",
        "grok": os.path.join("hooks", "app-store-compliance.json"),
        "qwen": "settings.json",
        "auggie": "settings.json",
        "cursor": "hooks.json",
        "copilot": os.path.join("hooks", "app-store-compliance.json"),
        "windsurf": "hooks.json",
        "kimi": "config.toml",
    }
    command = (
        os.path.join(base, "commands", "app-store-audit.toml")
        if tool == "gemini"
        else None
    )
    return {
        "hooks": os.path.join(base, "hooks"),
        "config": os.path.join(base, configs[tool]),
        "command": command,
        "wrap": True,
    }


def has_hooks_key(path):
    try:
        with open(path, encoding="utf-8") as f:
            return isinstance(json.load(f).get("hooks"), dict)
    except Exception:
        return False


def shown(path):
    h = home()
    return "~" + path[len(h) :] if path.startswith(h + os.sep) else path


def hook_cmd(tool, guard):
    if tool == "copilot-repo":
        return (
            "bash ./.github/hooks/" + GUARD_NAME
        )  # the cloud agent runs it from the repository root
    if tool == "auggie":
        return guard  # Auggie runs a script path by its extension and shebang, never a shell string
    return "bash '" + guard.replace("'", "'\\''") + "'"


def ps_cmd(tool, guard):
    """The Windows handler Copilot runs in PowerShell. It pipes the payload to bash and keeps the guard's exit code."""
    target = "./.github/hooks/" + GUARD_NAME if tool == "copilot-repo" else guard
    if tool != "copilot-repo" and shutil.which("cygpath"):
        r = subprocess.run(["cygpath", "-m", guard], capture_output=True, text=True)
        target = r.stdout.strip() or guard
    return "$input | & bash '" + target.replace("'", "''") + "'; exit $LASTEXITCODE"


def ok(msg):
    print("  ok    " + msg)


def note(msg):
    print("  note  " + msg)


def fail(msg):
    print("  FAIL  " + msg)
    PROBLEMS.append(msg)


def load_json(path):
    """The parsed object, {} when the file is absent or empty, None when it is unsafe to rewrite."""
    if not os.path.exists(path):
        return {}

    def no_repeats(pairs):
        keys = [k for k, _ in pairs]
        if len(keys) != len(set(keys)):
            raise ValueError("repeated key")
        return dict(pairs)

    try:
        with open(path, encoding="utf-8") as f:
            text = f.read()
        data = json.loads(text, object_pairs_hook=no_repeats) if text.strip() else {}
    except Exception:
        return None
    if not isinstance(data, dict) or not os.access(path, os.W_OK):
        return None
    return data


def write_atomic(path, text, newline=None):
    folder = os.path.dirname(path)
    os.makedirs(folder, exist_ok=True)
    real = os.path.realpath(path)
    if os.path.exists(real):
        shutil.copy2(
            real,
            path + ".bak-" + time.strftime("%Y%m%d-%H%M%S") + "-" + str(os.getpid()),
        )
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(real) or folder, prefix=".asc-")
    with os.fdopen(fd, "w", encoding="utf-8", newline=newline) as f:
        f.write(text)
    if os.path.exists(real):
        shutil.copymode(real, tmp)
    os.replace(tmp, real)


def events(tool):
    """(event key, style) pairs this tool's file carries. Copilot carries its own form and the Claude form VS Code reads."""
    spec = SPECS[tool]
    if spec["style"] == "copilot":
        return [("preToolUse", "copilot"), ("PreToolUse", "vscode")]
    return [(spec["event"], spec["style"])]


def new_entry(tool, style, cmd):
    spec = SPECS[tool]
    if style == "nested":
        key, value = spec["timeout"]
        return {
            "matcher": spec["matcher"],
            "hooks": [{"type": "command", "command": cmd, key: value}],
        }
    if style == "copilot":
        return {
            "type": "command",
            "bash": cmd,
            "powershell": ps_cmd(tool, guard_of(cmd)),
            "timeoutSec": 120,
        }
    if style == "vscode":
        return {"type": "command", "command": cmd, "timeout": 120}
    if tool == "windsurf":
        return {"command": cmd, "show_output": True}
    return {"command": cmd, "timeout": 120}


def guard_of(cmd):
    """The guard path inside a bash command line this installer wrote."""
    if cmd.startswith("bash '") and cmd.endswith("'"):
        return cmd[6:-1].replace("'\\''", "'")
    return cmd[5:] if cmd.startswith("bash ") else cmd


def is_ours(item, cmd, guard):
    if not isinstance(item, dict):
        return False
    c = str(item.get("command", item.get("bash", ""))).strip()
    return c in (cmd, "bash " + guard, 'bash "' + guard + '"', "bash '" + guard + "'")


def ours_in(style, groups, cmd, guard):
    if style == "nested":
        return [
            h
            for g in groups
            for h in (g.get("hooks") if isinstance(g.get("hooks"), list) else [])
            if is_ours(h, cmd, guard)
        ]
    return [g for g in groups if is_ours(g, cmd, guard)]


def matcher_hits(m, name):
    if m in (None, "", "*"):
        return True
    try:
        return re.fullmatch(str(m), name) is not None
    except re.error:
        return False


def dispatches(tool, style, group, h):
    """True when the tool would run this handler for a shell call and give it time to finish."""
    spec = SPECS[tool]
    if style == "nested" and not all(
        matcher_hits(group.get("matcher"), t) for t in spec.get("tools", (spec["matcher"],))
    ):
        return False
    if style in ("nested", "copilot", "vscode") and h.get("type", "command") != "command":
        return False
    # Qwen requires the type, and reads a command timeout of 1000 or more as milliseconds
    if tool == "qwen" and h.get("type") != "command":
        return False
    if h.get("async") not in (None, False):
        return False
    if tool == "cursor" and (
        h.get("type", "command") != "command"
        or not all(matcher_hits(h.get("matcher"), c) for c in ("fastlane deliver", "eas submit --platform ios", "xcrun altool --upload-app"))
    ):
        return False
    shell_tools = {"copilot": ("bash", "powershell"), "vscode": ("runInTerminal", "run_in_terminal")}.get(style)
    if shell_tools and "matcher" in h and not all(matcher_hits(h.get("matcher"), t) for t in shell_tools):
        return False
    if tool == "windsurf":
        return True
    if tool == "auggie" and not (
        str(h.get("command", "")).endswith(".sh") and os.access(str(h.get("command", "")), os.X_OK)
    ):
        return False
    if style == "copilot":
        ps = h.get("powershell")
        if ps != ps_cmd(tool, guard_of(str(h.get("bash", "")))):
            return False
    key, want = {"nested": spec.get("timeout"), "copilot": ("timeoutSec", 120)}.get(
        style
    ) or ("timeout", 120)
    t = h.get(key)
    if not isinstance(t, (int, float)) or isinstance(t, bool):
        return False
    if tool == "qwen" and t >= 1000:
        t = t / 1000
    return t >= want


def live_in(tool, style, groups, cmd, guard):
    """Our handlers that would actually run, the ones doctor may certify."""
    if style == "nested":
        return [
            h
            for g in groups
            for h in (g.get("hooks") if isinstance(g.get("hooks"), list) else [])
            if is_ours(h, cmd, guard) and dispatches(tool, style, g, h)
        ]
    return [g for g in groups if is_ours(g, cmd, guard) and dispatches(tool, style, None, g)]


def without_ours(style, groups, cmd, guard):
    """The groups with every handler of ours removed, dropping a group only we filled."""
    if style != "nested":
        return [g for g in groups if not is_ours(g, cmd, guard)]
    kept = []
    for g in groups:
        hs = g.get("hooks") if isinstance(g.get("hooks"), list) else []
        mine = [h for h in hs if is_ours(h, cmd, guard)]
        if mine:
            g["hooks"] = [h for h in hs if not is_ours(h, cmd, guard)]
            if not g["hooks"]:
                continue
        kept.append(g)
    return kept


def container(lay, data):
    """The object that holds the event lists, created if missing. None when the shape is wrong."""
    if not lay["wrap"]:
        return data
    hooks = data.setdefault("hooks", {})
    return hooks if isinstance(hooks, dict) else None


def plugin_source(guard):
    return (
        "// App Store Compliance Playbook guard for OpenCode. Runs the guard before every shell command\n"
        "// and stops the command when the guard exits 2. Installed by scripts/install_harness.py.\n"
        'import { spawnSync } from "node:child_process";\n\n'
        "export const AppStoreCompliance = async ({ directory }) => ({\n"
        '  "tool.execute.before": async (input, output) => {\n'
        '    if (input.tool !== "bash") return;\n'
        "    const command = output && output.args ? output.args.command : undefined;\n"
        '    if (typeof command !== "string") return;\n'
        "    // OpenCode loads both plugin folders, so a call one copy already checked is skipped by the other.\n"
        "    const seen = (globalThis.__appStoreComplianceSeen ||= new WeakSet());\n"
        "    if (seen.has(output)) return;\n"
        "    seen.add(output);\n"
        '    const r = spawnSync("bash", [' + json.dumps(guard) + "], {\n"
        '      input: JSON.stringify({ tool_name: "Bash", tool_input: { command }, cwd: directory }),\n'
        '      encoding: "utf8", timeout: 120000, cwd: directory,\n'
        "    });\n"
        '    if (r.status === 2) throw new Error((r.stdout || "") + (r.stderr || "") || "Blocked by the App Store compliance guard.");\n'
        '    if (r.error || (r.status !== 0 && r.status !== 1)) {\n'
        '      const why = "The App Store compliance guard could not run (" + (r.error ? r.error.message : "exit " + r.status) + "). Run install.sh --tool opencode doctor.";\n'
        '      if (/fastlane|eas |xcrun|altool|notarytool|transporter|gradle|bundletool|xcodebuild|flutter|expo|capacitor|cap |cordova|ionic|unity|dotnet|tauri|npm|pnpm|yarn|bun |make|turbo|nx |lerna/i.test(command.replace(/[\\\\\\x27"`]/g, "").replace(/\\s+/g, " "))) throw new Error(why);\n'
        '      console.error(why);\n'
        '    }\n'
        "  },\n"
        "});\n"
    )


def legacy_plugin(lay):
    """OpenCode before 1.0 loads plugin/, current OpenCode loads plugins/. The plugin goes in both."""
    return os.path.join(
        os.path.dirname(os.path.dirname(lay["config"])),
        "plugin",
        os.path.basename(lay["config"]),
    )


def kimi_block(cmd):
    return (
        "\n".join(
            [
                KIMI_BEGIN,
                "[[hooks]]",
                'event = "PreToolUse"',
                'matcher = "^Bash$"',
                "command = " + json.dumps(cmd),
                "timeout = 120",
                KIMI_END,
            ]
        )
        + "\n"
    )


def kimi_entry(text):
    """The [[hooks]] table inside our marked block, {} when it does not parse, None when absent."""
    m = re.search(re.escape(KIMI_BEGIN) + r"\r?\n(.*?)" + re.escape(KIMI_END), text, re.S)
    if not m:
        return None
    try:
        import tomllib

        hooks = tomllib.loads(m.group(1)).get("hooks")
        return hooks[0] if isinstance(hooks, list) and hooks and isinstance(hooks[0], dict) else {}
    except ImportError:
        out = {}
        for line in m.group(1).splitlines():
            k, eq, v = line.partition("=")
            if eq:
                try:
                    out[k.strip()] = json.loads(v.strip())
                except ValueError:
                    return {}
        return out
    except Exception:
        return {}


def kimi_live(h):
    """True when Kimi would run this handler before a shell command and give it time to finish."""
    if not h or h.get("event") != "PreToolUse" or not isinstance(h.get("command"), str):
        return False
    # Kimi accepts only these four keys and an integer timeout up to 600, and refuses the whole config otherwise
    if set(h) - {"event", "matcher", "command", "timeout"}:
        return False
    t = h.get("timeout")
    ok_time = isinstance(t, int) and not isinstance(t, bool) and 120 <= t <= 600
    return ok_time and matcher_hits(h.get("matcher"), "Bash")


def command_text(tool, guard):
    with open(
        os.path.join(REPO, "agent-os", "commands", "app-store-audit.md"),
        encoding="utf-8",
    ) as f:
        md = f.read()
    md = md.replace("~/.claude/hooks/" + GUARD_NAME, shown(guard)).replace(
        "~/.claude/skills/app-store-compliance", shown(skill_dir())
    )
    if tool == "opencode":
        return md
    head, _, body = md.partition("\n---\n")
    desc = head.split("description:", 1)[-1].strip()
    body = (
        body.replace('\\', '\\\\').replace('"""', "'''")
        + "\n\nThe target project is {{args}}. When it is empty, use the current folder.\n"
    )
    return "description = " + json.dumps(desc) + '\nprompt = """\n' + body + '"""\n'


def manual_block(tool, lay, cmd):
    if tool == "opencode":
        return plugin_source(cmd)
    if tool == "kimi":
        return (
            "\nAppend this to "
            + shown(lay["config"])
            + " yourself.\n\n"
            + kimi_block(cmd)
        )
    events_map = {ev: [new_entry(tool, st, cmd)] for ev, st in events(tool)}
    data = {"hooks": events_map} if lay["wrap"] else events_map
    if tool == "gemini":
        data["tools"] = {"enableHooks": True}
    if tool in ("cursor", "copilot", "copilot-repo"):
        data["version"] = 1
    return (
        "\nMerge this into "
        + shown(lay["config"])
        + " yourself.\n\n"
        + json.dumps(data, indent=2)
        + "\n"
    )


def register(tool, lay, guard, dry):
    cmd = hook_cmd(tool, guard)
    style = SPECS[tool]["style"]
    if style == "plugin":
        if dry:
            print(
                "  would write the OpenCode plugin "
                + shown(lay["config"])
                + " and "
                + shown(legacy_plugin(lay))
            )
            return True
        for path in (lay["config"], legacy_plugin(lay)):
            write_atomic(path, plugin_source(guard))
        ok(
            "plugin written to "
            + shown(lay["config"])
            + " and "
            + shown(legacy_plugin(lay))
        )
        return True
    if style == "toml":
        return register_kimi(lay, cmd, dry)
    data = load_json(lay["config"])
    if data is None:
        fail(
            shown(lay["config"])
            + " is not valid JSON, repeats a key, is read-only, or has an unexpected shape. It was not changed."
        )
        print(manual_block(tool, lay, cmd))
        return False
    fixed = False
    if tool in ("cursor", "copilot", "copilot-repo") and "version" not in data:
        data["version"] = 1
        fixed = True
    if tool == "cursor" and not (type(data.get("version")) is int and data.get("version") >= 1):
        data["version"] = 1
        fixed = True
    # Copilot rejects the whole hooks file unless version is the number 1, and true is not 1
    if tool in ("copilot", "copilot-repo") and not (type(data.get("version")) is int and data.get("version") == 1):
        data["version"] = 1
        fixed = True
    if tool == "gemini" and not isinstance(data.setdefault("tools", {}), dict):
        fail(
            shown(lay["config"])
            + " has a tools key that is not an object. It was not changed."
        )
        print(manual_block(tool, lay, cmd))
        return False
    box = container(lay, data)
    changed = fixed
    for ev, st in events(tool):
        groups = box.setdefault(ev, []) if isinstance(box, dict) else None
        if not isinstance(groups, list) or not all(isinstance(g, dict) for g in groups):
            fail(
                shown(lay["config"])
                + " has hooks with an unexpected shape. It was not changed."
            )
            print(manual_block(tool, lay, cmd))
            return False
        if not live_in(tool, st, groups, cmd, guard):
            # An entry of ours that would never run is replaced, never left beside the new one.
            groups[:] = without_ours(st, groups, cmd, guard)
            groups.append(new_entry(tool, st, cmd))
            changed = True
    if tool == "gemini" and data["tools"].get("enableHooks") is not True:
        data["tools"]["enableHooks"] = (
            True  # Gemini CLI before 0.26 runs no hook without this
        )
        changed = True
    if not changed:
        ok("hook already registered in " + shown(lay["config"]))
        return True
    if dry:
        print(
            "  would add the hook entry to "
            + shown(lay["config"])
            + ", keeping every other key, with a backup"
        )
        return True
    write_atomic(lay["config"], json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    ok(
        "hook added to "
        + shown(lay["config"])
        + " (a backup sits next to it when the file already existed)"
    )
    return True


KIMI_KEY = r"""(?:hooks|"hooks"|'hooks')"""


def kimi_hooks_taken(text):
    """True when the file already defines hooks as a key or a table, which a [[hooks]] block cannot join."""
    t = text.replace("\r", "")
    return bool(
        re.search(r"^[ \t]*" + KIMI_KEY + r"[ \t]*[=.]", t, re.M)
        or re.search(r"^[ \t]*\[[ \t]*" + KIMI_KEY + r"[ \t]*[\].]", t, re.M)
        or re.search(r'^[ \t]*\[?[ \t]*"[^"\n]*\\[uU]', t, re.M)
    )


def toml_still_valid(before, after):
    """False when a file that parsed before no longer parses. True when no TOML parser is available."""
    try:
        import tomllib
    except ImportError:
        return True
    try:
        tomllib.loads(before)
    except Exception:
        return True
    try:
        tomllib.loads(after)
    except Exception:
        return False
    return True


def register_kimi(lay, cmd, dry):
    path = lay["config"]
    text = ""
    if os.path.exists(path):
        if not os.access(path, os.W_OK):
            fail(shown(path) + " is read-only. It was not changed.")
            print(manual_block("kimi", lay, cmd))
            return False
        with open(path, encoding="utf-8", newline="") as f:
            text = f.read()
    nl = "\r\n" if "\r\n" in text else "\n"
    if KIMI_BEGIN in text:
        h = kimi_entry(text)
        if kimi_live(h) and h.get("command") == cmd:
            ok("hook already registered in " + shown(path))
            return True
        if dry:
            print("  would rewrite the guard block in " + shown(path) + ", with a backup")
            return True
        pattern = re.escape(KIMI_BEGIN) + r".*?" + re.escape(KIMI_END) + r"(\r?\n)?"
        repaired = re.sub(pattern, lambda _m: kimi_block(cmd).replace("\n", nl), text, count=1, flags=re.S)
        if kimi_hooks_taken(re.sub(pattern, "", text, count=1, flags=re.S)) or not toml_still_valid(text, repaired):
            fail(shown(path) + " defines hooks another way, so the guard block cannot be repaired. It was not changed.")
            print(manual_block("kimi", lay, cmd))
            return False
        write_atomic(path, repaired, newline="")
        ok("guard block repaired in " + shown(path) + " (a backup sits next to it)")
        return True
    if kimi_hooks_taken(text):
        fail(shown(path) + " defines hooks inline, so a [[hooks]] block cannot be added. It was not changed.")
        print(manual_block("kimi", lay, cmd))
        return False
    if dry:
        print(
            "  would append one [[hooks]] block to "
            + shown(path)
            + ", keeping everything else, with a backup"
        )
        return True
    sep = "" if not text or text.endswith(nl + nl) else (nl if text.endswith(nl) else nl + nl)
    if not toml_still_valid(text, text + sep + kimi_block(cmd).replace("\n", nl)):
        fail(shown(path) + " would not stay valid TOML with a [[hooks]] block. It was not changed.")
        print(manual_block("kimi", lay, cmd))
        return False
    write_atomic(path, text + sep + kimi_block(cmd).replace("\n", nl), newline="")
    os.makedirs(lay["hooks"], exist_ok=True)
    with open(os.path.join(lay["hooks"], KIMI_SEP_FILE), "w", encoding="utf-8") as f:
        f.write(json.dumps(sep))
    ok(
        "hook appended to "
        + shown(path)
        + " (a backup sits next to it when the file already existed)"
    )
    return True


def unregister(tool, lay, guard):
    cmd = hook_cmd(tool, guard)
    style = SPECS[tool]["style"]
    if style == "plugin":
        for path in (lay["config"], legacy_plugin(lay)):
            if os.path.exists(path):
                os.remove(path)
        return True
    if not os.path.exists(lay["config"]):
        return True
    if style == "toml":
        with open(lay["config"], encoding="utf-8", newline="") as f:
            text = f.read()
        if KIMI_BEGIN not in text:
            return True
        m = re.search(re.escape(KIMI_BEGIN) + r".*?" + re.escape(KIMI_END) + r"(\r?\n)?", text, flags=re.S)
        before, after = text[: m.start()], text[m.end() :]
        sep_file = os.path.join(lay["hooks"], KIMI_SEP_FILE)
        try:
            with open(sep_file, encoding="utf-8") as f:
                sep = json.loads(f.read() or '""')
        except (OSError, ValueError):
            sep = ""
        sep = "\n" * sep if isinstance(sep, int) else (sep if isinstance(sep, str) else "")
        # Drop only the newlines the install added in front of a block it appended at the end.
        if sep and not after and before.endswith(sep):
            before = before[: -len(sep)]
        write_atomic(lay["config"], before + after, newline="")
        if os.path.exists(sep_file):
            os.remove(sep_file)
        return True
    data = load_json(lay["config"])
    if data is None:
        return False
    box = data.get("hooks") if lay["wrap"] else data
    if not isinstance(box, dict):
        return True
    changed = False
    for ev, st in events(tool):
        groups = box.get(ev)
        if not isinstance(groups, list) or not ours_in(st, groups, cmd, guard):
            continue
        kept = without_ours(st, groups, cmd, guard)
        if kept:
            box[ev] = kept
        else:
            box.pop(ev)
        changed = True
    if not changed:
        return True
    if lay["wrap"] and not box:
        data.pop("hooks")
    if tool in ("copilot", "copilot-repo", "grok") and set(data) <= {"version"}:
        os.remove(lay["config"])
        return True
    write_atomic(lay["config"], json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    return True


def read_owners():
    try:
        with open(os.path.join(skill_dir(), ".installed-by"), encoding="utf-8") as f:
            return {line.strip() for line in f if line.strip() in TOOLS}
    except OSError:
        return set()


def write_owners(owners):
    """Replaces .installed-by in one step, so a reader never sees it empty or half written."""
    sk = skill_dir()
    fd, tmp = tempfile.mkstemp(dir=sk, prefix=".asc-owners-")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write("\n".join(sorted(owners)) + "\n")
    os.replace(tmp, os.path.join(sk, ".installed-by"))


def read_guards():
    """Every installed guard path and its tool, so two folders of one tool each own the skill."""
    out = {}
    try:
        with open(os.path.join(skill_dir(), ".guards"), encoding="utf-8") as f:
            for line in f:
                t, tab, path = line.rstrip("\n").partition("\t")
                if tab and t in TOOLS and path:
                    out[path] = t
    except OSError:
        pass
    return out


def write_guards(guards):
    sk = skill_dir()
    fd, tmp = tempfile.mkstemp(dir=sk, prefix=".asc-guards-")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write("".join(guards[g] + "\t" + g + "\n" for g in sorted(guards)))
    os.replace(tmp, os.path.join(sk, ".guards"))


def copy_payload(tool, lay, guard):
    if tool != "copilot-repo":
        sk = skill_dir()
        os.makedirs(sk, exist_ok=True)
        shutil.copy2(
            os.path.join(REPO, "agent-os", "skill", "SKILL.md"),
            os.path.join(sk, "SKILL.md"),
        )
        shutil.copy2(
            os.path.join(REPO, ".citation-allowlist"),
            os.path.join(sk, ".citation-allowlist"),
        )
        if os.path.exists(os.path.join(REPO, "VERSION")):
            shutil.copy2(os.path.join(REPO, "VERSION"), os.path.join(sk, "VERSION"))
        for d in PAYLOAD_DIRS:
            shutil.rmtree(os.path.join(sk, d), ignore_errors=True)
            shutil.copytree(
                os.path.join(REPO, d),
                os.path.join(sk, d),
                ignore=shutil.ignore_patterns("__pycache__"),
            )
        write_owners(read_owners() | {tool})
        write_guards(dict(read_guards(), **{guard: tool}))
    os.makedirs(lay["hooks"], exist_ok=True)
    shutil.copy2(os.path.join(REPO, "agent-os", "hooks", GUARD_NAME), guard)
    os.chmod(guard, 0o755)
    if lay["command"]:
        os.makedirs(os.path.dirname(lay["command"]), exist_ok=True)
        with open(lay["command"], "w", encoding="utf-8") as f:
            f.write(command_text(tool, guard))
    ok("guard copied" if tool == "copilot-repo" else "guard, skill and command copied")


def payload_for(tool, style, command, cwd):
    """The exact JSON each tool sends its hook, from each vendor's hook reference."""
    if tool == "gemini":
        return {
            "hook_event_name": "BeforeTool",
            "tool_name": "run_shell_command",
            "tool_input": {"command": command},
            "cwd": cwd,
        }
    if tool == "qwen":
        return {
            "hook_event_name": "PreToolUse",
            "tool_name": "run_shell_command",
            "tool_input": {"command": command},
            "cwd": cwd,
        }
    if tool == "grok":
        return {
            "hookEventName": "PreToolUse",
            "toolName": "run_terminal_command",
            "toolInput": {"command": command},
            "cwd": cwd,
        }
    if tool == "droid":
        return {
            "hook_event_name": "PreToolUse",
            "tool_name": "Execute",
            "tool_input": {"command": command},
            "cwd": cwd,
        }
    if tool == "auggie":
        return {
            "hook_event_name": "PreToolUse",
            "tool_name": "launch-process",
            "tool_input": {"command": command},
            "workspace_roots": [cwd],
        }
    if tool == "cursor":
        return {
            "hook_event_name": "beforeShellExecution",
            "command": command,
            "cwd": cwd,
        }
    if tool == "windsurf":
        return {
            "agent_action_name": "pre_run_command",
            "tool_info": {"command_line": command, "cwd": cwd},
        }
    if style == "copilot":
        return {
            "toolName": "bash",
            "toolArgs": json.dumps({"command": command}),
            "cwd": cwd,
        }
    if style == "vscode":
        return {
            "hook_event_name": "PreToolUse",
            "tool_name": "runInTerminal",
            "tool_input": {"command": command},
            "cwd": cwd,
        }
    if tool == "kimi":
        return {
            "hook_event_name": "PreToolUse",
            "tool_name": "Bash",
            "tool_input": {"command": command},
        }
    return {
        "hook_event_name": "PreToolUse",
        "tool_name": "Bash",
        "tool_input": {"command": command},
        "cwd": cwd,
    }


def sample_app():
    d = tempfile.mkdtemp()
    os.makedirs(os.path.join(d, "App"))
    with open(os.path.join(d, "App", "Info.plist"), "w") as f:
        f.write("<plist><dict></dict></plist>")
    with open(os.path.join(d, "App", "X.swift"), "w") as f:
        f.write(
            'import CoreLocation\nclass A { func signIn(){} func createAccount(){} }\nlet m=CLLocationManager()\nlet u="https://staging.example.com"\nimport Stripe\n'
        )
    return d


def run_hook(cmd_line, payload, cwd, tool=None):
    env = {
        k: v
        for k, v in os.environ.items()
        if k not in ("CLAUDE_PROJECT_DIR", "GEMINI_PROJECT_DIR", "AUGMENT_PROJECT_DIR")
    }
    argv = [cmd_line] if tool == "auggie" else ["bash", "-c", cmd_line]
    try:
        r = subprocess.run(
            argv, input=json.dumps(payload), capture_output=True, text=True,
            cwd=cwd, env=env, timeout=180,
        )
    except OSError as e:
        return 126, str(e)
    return r.returncode, (r.stdout + r.stderr).strip()


def run_plugin(plugin, command, cwd):
    """Loads the OpenCode plugin in node and calls its hook the way OpenCode does. None when node is absent."""
    if not shutil.which("node"):
        return None
    js = (
        "const m = await import(process.argv[1]);"
        "const h = await m.AppStoreCompliance({ directory: process.argv[3] });"
        'try { await h["tool.execute.before"]({ tool: "bash" }, { args: { command: process.argv[2] } }); process.exit(0); }'
        "catch (e) { process.exit(2); }"
    )
    r = subprocess.run(
        ["node", "--input-type=module", "-e", js, "file://" + plugin, command, cwd],
        capture_output=True,
        text=True,
        timeout=180,
    )
    return r.returncode


def verify(tool, lay, guard, repo_dir):
    print("\nChecking the " + SPECS[tool]["name"] + " install.")
    if os.path.isfile(guard):
        ok("guard present at " + shown(guard))
    else:
        fail("guard missing at " + shown(guard))
    if tool != "copilot-repo":
        sk = skill_dir()
        need = (
            "SKILL.md",
            "data/rejection-patterns.json",
            "data/regulatory-deadlines.json",
            "docs/PRE-SUBMISSION-CHECKLIST.md",
            "scripts/deadline-checker.py",
            "scripts/validate-privacy-manifest.py",
            ".citation-allowlist",
        )
        missing = [p for p in need if not os.path.exists(os.path.join(sk, p))]
        if missing:
            fail("skill payload is missing " + " ".join(missing))
        else:
            ok("skill payload complete at " + shown(sk))
        if os.path.isfile(os.path.join(sk, "VERSION")):
            with open(os.path.join(sk, "VERSION")) as f:
                inst = f.read().strip()
            ok("version " + inst)
            repo_v = os.path.join(REPO, "VERSION")
            if os.path.isfile(repo_v):
                with open(repo_v) as f:
                    cur = f.read().strip()
                if cur and cur != inst:
                    note("this checkout is version " + cur + ". Run install.sh --tool " + tool + " again to update.")
    if lay["command"]:
        if os.path.isfile(lay["command"]):
            ok("audit command at " + shown(lay["command"]))
        else:
            fail("audit command missing at " + shown(lay["command"]))
    app = sample_app()
    try:
        style = SPECS[tool]["style"]
        if style == "plugin":
            check_plugin(lay, app)
        elif style == "toml":
            check_kimi(lay, guard, app)
        else:
            check_hooks(tool, lay, guard, app, repo_dir)
    finally:
        shutil.rmtree(app, ignore_errors=True)
    print("")
    if PROBLEMS:
        extra = " --repo " + repo_dir if repo_dir else ""
        print(
            str(len(PROBLEMS))
            + " problem(s) above. Fix them, then run. bash "
            + os.path.join(REPO, "scripts", "install.sh")
            + " --tool "
            + tool
            + extra
            + " doctor"
        )
        return 1
    if UNVERIFIED:
        print("Installed, but not fully verified. " + "; ".join(UNVERIFIED) + ". Install node and run doctor to verify.")
    else:
        print("Install verified.")
    if tool != "copilot-repo":
        print("Check your app now.   bash " + shown(guard) + ' "/path/to/your/app"')
    print(AFTER[tool])
    return 0


def check_plugin(lay, app):
    for path in (lay["config"], legacy_plugin(lay)):
        if not os.path.isfile(path):
            fail("plugin missing at " + shown(path))
            return
    rc = run_plugin(lay["config"], SUBMIT, app)
    if rc is None:
        note(
            "node not found, so the plugin was not exercised here. OpenCode runs it with its own runtime."
        )
        UNVERIFIED.append("the OpenCode plugin was not exercised (node not found)")
        return
    if rc == 2:
        ok("the plugin stops a submit command")
    else:
        fail("the plugin did not stop a submit command (exit " + str(rc) + ")")
    if run_plugin(lay["config"], "ls -la", app) == 0:
        ok("the plugin lets an ordinary command through")
    else:
        fail("the plugin stopped an ordinary command")


def check_kimi(lay, guard, app):
    try:
        with open(lay["config"], encoding="utf-8") as f:
            text = f.read()
    except OSError:
        text = ""
    if KIMI_BEGIN not in text:
        fail("no hook block for the guard in " + shown(lay["config"]))
        return
    try:
        import tomllib

        tomllib.loads(text)
        ok(
            "hook registered in "
            + shown(lay["config"])
            + ", and the file still parses as TOML"
        )
    except ImportError:
        ok("hook registered in " + shown(lay["config"]))
    except Exception:
        fail(shown(lay["config"]) + " no longer parses as TOML")
        return
    h = kimi_entry(text)
    if not kimi_live(h):
        fail(
            "the guard block in "
            + shown(lay["config"])
            + " would not run before a shell command. Check its event, matcher and timeout, or run install again"
        )
        return
    prove(h["command"], "kimi", "toml", app, app)


def check_hooks(tool, lay, guard, app, repo_dir):
    cmd = hook_cmd(tool, guard)
    data = load_json(lay["config"]) or {}
    box = data.get("hooks") if lay["wrap"] else data
    box = box if isinstance(box, dict) else {}
    found_any = False
    for ev, st in events(tool):
        groups = box.get(ev)
        found = live_in(tool, st, groups, cmd, guard) if isinstance(groups, list) else []
        if not found:
            if isinstance(groups, list) and ours_in(st, groups, cmd, guard):
                fail(
                    "the " + ev + " entry in " + shown(lay["config"])
                    + " names the guard but would never run it. Check its matcher, type and timeout, or run install again"
                )
            else:
                fail("no " + ev + " hook entry for the guard in " + shown(lay["config"]))
            continue
        found_any = True
        line = found[0].get("command") or found[0].get("bash")
        prove(line, tool, st, app, repo_dir or "/")
        if st == "copilot":
            prove_ps(found[0]["powershell"], tool, app, repo_dir or "/")
    if found_any:
        ok("hook registered in " + shown(lay["config"]))
    if tool in ("copilot", "copilot-repo") and not (type(data.get("version")) is int and data.get("version") == 1):
        fail("version is not 1 in " + shown(lay["config"]) + ", so Copilot rejects the whole hooks file")
    if tool == "cursor" and not (type(data.get("version")) is int and data.get("version") >= 1):
        fail("version is not a positive whole number in " + shown(lay["config"]) + ", so Cursor rejects the hooks file")
    hc = data.get("hooksConfig")
    if tool == "gemini" and isinstance(hc, dict) and hc.get("enabled") is False:
        fail("hooksConfig.enabled is false in " + shown(lay["config"]) + ", so Gemini CLI runs no hook, the guard included")
    if tool in ("qwen", "copilot", "copilot-repo") and data.get("disableAllHooks") is True:
        fail("disableAllHooks is true in " + shown(lay["config"]) + ", so the tool runs no hook, the guard included")
    if tool == "gemini" and (data.get("tools") or {}).get("enableHooks") is not True:
        fail(
            "tools.enableHooks is not true in "
            + shown(lay["config"])
            + ", so Gemini CLI before 0.26 runs no hook"
        )


def prove(line, tool, style, app, run_dir):
    """Feeds a submit command and an ordinary one to the registered command, in the tool's own payload shape."""
    label = {"vscode": " for VS Code", "copilot": " for Copilot"}.get(style, "")
    rc, _ = run_hook(line, payload_for(tool, style, SUBMIT, app), run_dir, tool)
    if rc == 2:
        ok(
            "the registered command blocks a submit command in this tool's own payload shape"
            + label
        )
    else:
        fail(
            "the registered command did not block a submit command"
            + label
            + " (exit "
            + str(rc)
            + ", expected 2)"
        )
    rc, out = run_hook(line, payload_for(tool, style, "ls -la", app), run_dir, tool)
    if rc == 0 and not out:
        ok("the registered command stays silent on an ordinary command" + label)
    else:
        fail(
            "the registered command reacted to an ordinary command"
            + label
            + " (exit "
            + str(rc)
            + ")"
        )


def prove_ps(line, tool, app, run_dir):
    """Runs the Windows handler in PowerShell when one is installed here, as Copilot does on Windows."""
    shell = shutil.which("pwsh") or shutil.which("powershell")
    if not shell:
        ok("the Windows powershell handler is registered (PowerShell is not installed here to run it)")
        return
    r = subprocess.run(
        [shell, "-NoProfile", "-NonInteractive", "-Command", line],
        input=json.dumps(payload_for(tool, "copilot", SUBMIT, app)),
        capture_output=True, text=True, cwd=run_dir, timeout=180,
    )
    if r.returncode == 2:
        ok("the Windows powershell handler blocks a submit command")
    else:
        fail("the Windows powershell handler did not block a submit command (exit " + str(r.returncode) + ")")


def uninstall(tool, lay, guard, dry):
    if dry:
        print(
            "Dry run. Would remove the guard, the command and the hook entry for "
            + SPECS[tool]["name"]
            + "."
        )
        return 0
    done = unregister(tool, lay, guard)
    for p in (guard, lay["command"]):
        if p and os.path.exists(p):
            os.remove(p)
    if tool == "copilot-repo":
        print("Removed the guard and the hook from the repository.")
    else:
        guards = read_guards()
        guards.pop(guard, None)
        owners = (read_owners() - {tool}) | set(guards.values())
        if owners:
            write_owners(owners)
            write_guards(guards)
            print(
                "Removed the "
                + SPECS[tool]["name"]
                + " guard and hook. The shared skill stays for "
                + ", ".join(sorted(owners))
                + "."
            )
        else:
            shutil.rmtree(skill_dir(), ignore_errors=True)
            print(
                "Removed the "
                + SPECS[tool]["name"]
                + " guard, hook and the shared skill."
            )
    if not done:
        print(
            "Could not edit "
            + shown(lay["config"])
            + ". Remove the "
            + GUARD_NAME
            + " entry by hand."
        )
        return 1
    return 0


def main(argv):
    dry = "--dry-run" in argv
    args = [a for a in argv if a != "--dry-run"]
    repo_dir = None
    if "--repo" in args:
        i = args.index("--repo")
        if i + 1 >= len(args):
            print("--repo needs a folder.", file=sys.stderr)
            return 2
        repo_dir = os.path.abspath(args[i + 1])
        del args[i : i + 2]
    if not args or args[0] not in TOOLS:
        print(
            "Usage. install_harness.py <"
            + "|".join(TOOLS)
            + "> [install|doctor|uninstall] [--dry-run] [--repo DIR]",
            file=sys.stderr,
        )
        return 2
    tool = args[0]
    mode = args[1] if len(args) > 1 else "install"
    if mode not in ("install", "doctor", "uninstall"):
        print("Unknown mode. " + mode, file=sys.stderr)
        return 2
    if tool == "copilot-repo" and (not repo_dir or not os.path.isdir(repo_dir)):
        print(
            "copilot-repo installs into your app's repository. Pass --repo with that folder.",
            file=sys.stderr,
        )
        return 2
    lay = layout(tool, repo_dir)
    guard = os.path.join(lay["hooks"], GUARD_NAME)
    if mode == "doctor":
        return verify(tool, lay, guard, repo_dir)
    if mode == "uninstall":
        return uninstall(tool, lay, guard, dry)
    if dry:
        print("Dry run. Nothing is written.")
        print("  would copy the guard to " + shown(guard))
        if tool != "copilot-repo":
            print("  would copy the skill to " + shown(skill_dir()))
        if lay["command"]:
            print("  would write the audit command to " + shown(lay["command"]))
        register(tool, lay, guard, True)
        return 0
    print("Installing the App Store Compliance Playbook for " + SPECS[tool]["name"])
    copy_payload(tool, lay, guard)
    if not register(tool, lay, guard, False):
        verify(tool, lay, guard, repo_dir)
        return 1
    return verify(tool, lay, guard, repo_dir)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
