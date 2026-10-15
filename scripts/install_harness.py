#!/usr/bin/env python3
"""Install the guard, skill and audit command into Codex, Gemini CLI, OpenCode, Cursor or Copilot CLI.
Usage. install_harness.py <tool> [install|doctor|uninstall] [--dry-run]. Configs are merged, never replaced."""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import time

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GUARD_NAME = "app-store-compliance-guard.sh"
PAYLOAD_DIRS = ("docs", "data", "references", "templates", "scripts")
TOOLS = ("codex", "gemini", "opencode", "cursor", "copilot")
SUBMIT = "fast" + "lane deliver"
PROBLEMS = []


def home():
    h = os.environ.get("HOME")
    if not h:
        sys.exit("HOME is not set, so there is no folder to install into.")
    return h


def skill_dir():
    return os.path.join(home(), ".agents", "skills", "app-store-compliance")


def layout(tool):
    """Where each tool keeps its hooks, its hook config and its commands, from each tool's own docs."""
    h = home()
    if tool == "codex":
        base = os.environ.get("CODEX_HOME") or os.path.join(h, ".codex")
        return {
            "base": base,
            "hooks": os.path.join(base, "hooks"),
            "config": os.path.join(base, "hooks.json"),
            "command": None,
        }
    if tool == "gemini":
        base = os.path.join(h, ".gemini")
        return {
            "base": base,
            "hooks": os.path.join(base, "hooks"),
            "config": os.path.join(base, "settings.json"),
            "command": os.path.join(base, "commands", "app-store-audit.toml"),
        }
    if tool == "opencode":
        base = os.path.join(
            os.environ.get("XDG_CONFIG_HOME") or os.path.join(h, ".config"), "opencode"
        )
        return {
            "base": base,
            "hooks": os.path.join(base, "hooks"),
            "config": os.path.join(base, "plugins", "app-store-compliance.js"),
            "command": os.path.join(base, "commands", "app-store-audit.md"),
        }
    if tool == "cursor":
        base = os.path.join(h, ".cursor")
        return {
            "base": base,
            "hooks": os.path.join(base, "hooks"),
            "config": os.path.join(base, "hooks.json"),
            "command": None,
        }
    base = os.path.join(h, ".copilot")
    return {
        "base": base,
        "hooks": os.path.join(base, "hooks"),
        "config": os.path.join(base, "hooks", "app-store-compliance.json"),
        "command": None,
    }


def shown(path):
    h = home()
    return "~" + path[len(h) :] if path.startswith(h + os.sep) else path


def hook_cmd(guard):
    return "bash '" + guard.replace("'", "'\\''") + "'"


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


def write_atomic(path, text):
    folder = os.path.dirname(path)
    os.makedirs(folder, exist_ok=True)
    real = os.path.realpath(path)
    if os.path.exists(real):
        shutil.copy2(
            real,
            path + ".bak-" + time.strftime("%Y%m%d-%H%M%S") + "-" + str(os.getpid()),
        )
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(real) or folder, prefix=".asc-")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(text)
    if os.path.exists(real):
        shutil.copymode(real, tmp)
    os.replace(tmp, real)


def entry_key(tool):
    return {
        "codex": "PreToolUse",
        "gemini": "BeforeTool",
        "cursor": "beforeShellExecution",
        "copilot": "preToolUse",
    }[tool]


def entry_lists(data, tool):
    """The hook groups this tool runs before a shell command, created if missing. None when the shape is wrong."""
    hooks = data.setdefault("hooks", {})
    if not isinstance(hooks, dict):
        return None
    groups = hooks.setdefault(entry_key(tool), [])
    if not isinstance(groups, list) or not all(isinstance(g, dict) for g in groups):
        return None
    return groups


def is_ours(item, guard):
    if not isinstance(item, dict):
        return False
    c = str(item.get("command", item.get("bash", ""))).strip()
    return c in (hook_cmd(guard), "bash " + guard, 'bash "' + guard + '"')


def ours_in(tool, groups, guard):
    if tool in ("codex", "gemini"):
        return [
            h
            for g in groups
            for h in (g.get("hooks") if isinstance(g.get("hooks"), list) else [])
            if is_ours(h, guard)
        ]
    return [g for g in groups if is_ours(g, guard)]


def new_entry(tool, guard):
    cmd = hook_cmd(guard)
    if tool == "codex":
        return {
            "matcher": "Bash",
            "hooks": [{"type": "command", "command": cmd, "timeout": 120}],
        }
    if tool == "gemini":  # Gemini counts the timeout in milliseconds
        return {
            "matcher": "run_shell_command",
            "hooks": [{"type": "command", "command": cmd, "timeout": 120000}],
        }
    if tool == "cursor":
        return {"command": cmd, "timeout": 120}
    return {"type": "command", "bash": cmd, "timeoutSec": 120}


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
        '    const r = spawnSync("bash", [' + json.dumps(guard) + "], {\n"
        '      input: JSON.stringify({ tool_name: "Bash", tool_input: { command }, cwd: directory }),\n'
        '      encoding: "utf8", timeout: 120000, cwd: directory,\n'
        "    });\n"
        '    if (r.status === 2) throw new Error((r.stdout || "") + (r.stderr || "") || "Blocked by the App Store compliance guard.");\n'
        "  },\n"
        "});\n"
    )


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
        body.replace('"""', "'''")
        + "\n\nThe target project is {{args}}. When it is empty, use the current folder.\n"
    )
    return "description = " + json.dumps(desc) + '\nprompt = """\n' + body + '"""\n'


def manual_block(tool, guard):
    if tool == "opencode":
        return plugin_source(guard)
    data = {"hooks": {entry_key(tool): [new_entry(tool, guard)]}}
    if tool == "gemini":
        data["tools"] = {"enableHooks": True}
    if tool in ("cursor", "copilot"):
        data["version"] = 1
    return (
        "\nMerge this into "
        + shown(layout(tool)["config"])
        + " yourself.\n\n"
        + json.dumps(data, indent=2)
        + "\n"
    )


def register(tool, lay, guard, dry):
    if tool == "opencode":
        if dry:
            print("  would write the OpenCode plugin " + shown(lay["config"]))
            return True
        write_atomic(lay["config"], plugin_source(guard))
        ok("plugin written to " + shown(lay["config"]))
        return True
    data = load_json(lay["config"])
    if data is None:
        fail(
            shown(lay["config"])
            + " is not valid JSON, repeats a key, is read-only, or has an unexpected shape. It was not changed."
        )
        print(manual_block(tool, guard))
        return False
    if tool in ("cursor", "copilot"):
        data.setdefault("version", 1)
    if tool == "gemini" and not isinstance(data.setdefault("tools", {}), dict):
        fail(
            shown(lay["config"])
            + " has a tools key that is not an object. It was not changed."
        )
        print(manual_block(tool, guard))
        return False
    groups = entry_lists(data, tool)
    if groups is None:
        fail(
            shown(lay["config"])
            + " has a hooks key with an unexpected shape. It was not changed."
        )
        print(manual_block(tool, guard))
        return False
    changed = False
    if tool == "gemini" and data["tools"].get("enableHooks") is not True:
        data["tools"]["enableHooks"] = (
            True  # Gemini CLI before 0.26 runs no hook without this
        )
        changed = True
    if not ours_in(tool, groups, guard):
        groups.append(new_entry(tool, guard))
        changed = True
    if not changed:
        ok("hook already registered in " + shown(lay["config"]))
        return True
    if dry:
        print(
            "  would add one hook entry to "
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


def unregister(tool, lay, guard):
    if tool == "opencode":
        if os.path.exists(lay["config"]):
            os.remove(lay["config"])
        return True
    if not os.path.exists(lay["config"]):
        return True
    data = load_json(lay["config"])
    if data is None:
        return False
    hooks = data.get("hooks")
    key = entry_key(tool)
    if (
        not isinstance(hooks, dict)
        or not isinstance(hooks.get(key), list)
        or not ours_in(tool, hooks[key], guard)
    ):
        return True
    groups = hooks[key]
    if tool in ("codex", "gemini"):
        kept = []
        for g in groups:
            had = any(is_ours(h, guard) for h in g.get("hooks", []))
            g["hooks"] = [h for h in g.get("hooks", []) if not is_ours(h, guard)]
            if g["hooks"] or not had:
                kept.append(g)
    else:
        kept = [g for g in groups if not is_ours(g, guard)]
    if kept:
        hooks[key] = kept
    else:
        hooks.pop(key)
    if not hooks:
        data.pop("hooks")
    if tool == "copilot" and set(data) <= {"version"}:
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


def copy_payload(tool, lay, guard):
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
    with open(os.path.join(sk, ".installed-by"), "w", encoding="utf-8") as f:
        f.write("\n".join(sorted(read_owners() | {tool})) + "\n")
    os.makedirs(lay["hooks"], exist_ok=True)
    shutil.copy2(os.path.join(REPO, "agent-os", "hooks", GUARD_NAME), guard)
    os.chmod(guard, 0o755)
    if lay["command"]:
        os.makedirs(os.path.dirname(lay["command"]), exist_ok=True)
        with open(lay["command"], "w", encoding="utf-8") as f:
            f.write(command_text(tool, guard))
    ok("guard, skill and command copied")


def payload_for(tool, command, cwd):
    if tool == "gemini":
        return {
            "hook_event_name": "BeforeTool",
            "tool_name": "run_shell_command",
            "tool_input": {"command": command},
            "cwd": cwd,
        }
    if tool == "cursor":
        return {
            "hook_event_name": "beforeShellExecution",
            "command": command,
            "cwd": cwd,
        }
    if tool == "copilot":
        return {
            "toolName": "bash",
            "toolArgs": json.dumps({"command": command}),
            "cwd": cwd,
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


def run_hook(cmd_line, payload, cwd):
    env = {
        k: v
        for k, v in os.environ.items()
        if k not in ("CLAUDE_PROJECT_DIR", "GEMINI_PROJECT_DIR")
    }
    r = subprocess.run(
        ["bash", "-c", cmd_line],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        cwd=cwd,
        env=env,
        timeout=180,
    )
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


def verify(tool, lay, guard):
    print("\nChecking the " + tool + " install.")
    if os.path.isfile(guard):
        ok("guard present at " + shown(guard))
    else:
        fail("guard missing at " + shown(guard))
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
            ok("version " + f.read().strip())
    if lay["command"]:
        if os.path.isfile(lay["command"]):
            ok("audit command at " + shown(lay["command"]))
        else:
            fail("audit command missing at " + shown(lay["command"]))
    app = sample_app()
    try:
        if tool == "opencode":
            check_plugin(lay, app)
        else:
            check_hook(tool, lay, guard, app)
    finally:
        shutil.rmtree(app, ignore_errors=True)
    print("")
    if PROBLEMS:
        print(
            str(len(PROBLEMS))
            + " problem(s) above. Fix them, then run. bash "
            + os.path.join(REPO, "scripts", "install.sh")
            + " --tool "
            + tool
            + " doctor"
        )
        return 1
    print("Install verified.")
    print("Check your app now.   bash " + shown(guard) + ' "/path/to/your/app"')
    tips = {
        "codex": "Open Codex and run /hooks once to approve the new hook. Codex runs no new or changed hook until you do.",
        "gemini": "Restart Gemini CLI so it loads the hook. Skills need Gemini CLI 0.24 or later, the hook works from 0.22.",
        "opencode": "Restart OpenCode so it loads the plugin.",
        "cursor": "Restart Cursor so it loads ~/.cursor/hooks.json.",
        "copilot": "Start a new Copilot CLI session so it loads the hook.",
    }
    print(tips[tool])
    return 0


def check_plugin(lay, app):
    if not os.path.isfile(lay["config"]):
        fail("plugin missing at " + shown(lay["config"]))
        return
    rc = run_plugin(lay["config"], SUBMIT, app)
    if rc is None:
        note(
            "node not found, so the plugin was not exercised here. OpenCode runs it with its own runtime."
        )
        return
    if rc == 2:
        ok("the plugin stops a submit command")
    else:
        fail("the plugin did not stop a submit command (exit " + str(rc) + ")")
    if run_plugin(lay["config"], "ls -la", app) == 0:
        ok("the plugin lets an ordinary command through")
    else:
        fail("the plugin stopped an ordinary command")


def check_hook(tool, lay, guard, app):
    data = load_json(lay["config"]) or {}
    hooks = data.get("hooks") if isinstance(data.get("hooks"), dict) else {}
    groups = hooks.get(entry_key(tool))
    found = ours_in(tool, groups, guard) if isinstance(groups, list) else []
    if not found:
        fail("no hook entry for the guard in " + shown(lay["config"]))
        return
    ok("hook registered in " + shown(lay["config"]))
    if tool == "gemini" and (data.get("tools") or {}).get("enableHooks") is not True:
        fail(
            "tools.enableHooks is not true in "
            + shown(lay["config"])
            + ", so Gemini CLI before 0.26 runs no hook"
        )
    line = found[0].get("command") or found[0].get("bash")
    rc, _ = run_hook(line, payload_for(tool, SUBMIT, app), "/")
    if rc == 2:
        ok(
            "the registered command blocks a submit command in "
            + tool
            + "'s own payload shape"
        )
    else:
        fail(
            "the registered command did not block a submit command (exit "
            + str(rc)
            + ", expected 2)"
        )
    rc, out = run_hook(line, payload_for(tool, "ls -la", app), "/")
    if rc == 0 and not out:
        ok("the registered command stays silent on an ordinary command")
    else:
        fail(
            "the registered command reacted to an ordinary command (exit "
            + str(rc)
            + ")"
        )


def uninstall(tool, lay, guard, dry):
    if dry:
        print(
            "Dry run. Would remove the guard, the command and the hook entry for "
            + tool
            + "."
        )
        return 0
    done = unregister(tool, lay, guard)
    for p in (guard, lay["command"]):
        if p and os.path.exists(p):
            os.remove(p)
    owners = read_owners() - {tool}
    if owners:
        with open(
            os.path.join(skill_dir(), ".installed-by"), "w", encoding="utf-8"
        ) as f:
            f.write("\n".join(sorted(owners)) + "\n")
        print(
            "Removed the "
            + tool
            + " guard and hook. The shared skill stays for "
            + ", ".join(sorted(owners))
            + "."
        )
    else:
        shutil.rmtree(skill_dir(), ignore_errors=True)
        print("Removed the " + tool + " guard, hook and the shared skill.")
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
    args = [a for a in argv if a != "--dry-run"]
    dry = len(args) != len(argv)
    if not args or args[0] not in TOOLS:
        print(
            "Usage. install_harness.py <"
            + "|".join(TOOLS)
            + "> [install|doctor|uninstall] [--dry-run]",
            file=sys.stderr,
        )
        return 2
    tool = args[0]
    mode = args[1] if len(args) > 1 else "install"
    if mode not in ("install", "doctor", "uninstall"):
        print("Unknown mode. " + mode, file=sys.stderr)
        return 2
    lay = layout(tool)
    guard = os.path.join(lay["hooks"], GUARD_NAME)
    if mode == "doctor":
        return verify(tool, lay, guard)
    if mode == "uninstall":
        return uninstall(tool, lay, guard, dry)
    if dry:
        print("Dry run. Nothing is written.")
        print("  would copy the guard to " + shown(guard))
        print("  would copy the skill to " + shown(skill_dir()))
        if lay["command"]:
            print("  would write the audit command to " + shown(lay["command"]))
        register(tool, lay, guard, True)
        return 0
    print("Installing the App Store Compliance Playbook for " + tool)
    copy_payload(tool, lay, guard)
    if not register(tool, lay, guard, False):
        verify(tool, lay, guard)
        return 1
    return verify(tool, lay, guard)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
