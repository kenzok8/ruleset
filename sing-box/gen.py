#!/usr/bin/env python3
"""生成三份 sing-box 配置：config-tun.json / config-tproxy.json / config-mixed.json

改规则、策略组、DNS 只改这里，然后在本目录跑 `python3 gen.py`。
校验：`sing-box check -c config-tun.json`（1.14 及以上）。

节点是占位用的，用户把自己的节点替换掉 REPLACE-XX 那四段即可。
"""

import json

# ---------------- 占位节点 ----------------
# 换成自己的节点时，保持 tag 名称或同步改下面的分组引用。
PLACEHOLDER_NODES = [
    {
        "type": "vless",
        "tag": "REPLACE-HK",
        "server": "hk.example.com",
        "server_port": 443,
        "uuid": "00000000-0000-0000-0000-000000000000",
        "tls": {"enabled": True, "server_name": "hk.example.com"},
    },
    {
        "type": "vless",
        "tag": "REPLACE-JP",
        "server": "jp.example.com",
        "server_port": 443,
        "uuid": "00000000-0000-0000-0000-000000000000",
        "tls": {"enabled": True, "server_name": "jp.example.com"},
    },
    {
        "type": "vless",
        "tag": "REPLACE-US",
        "server": "us.example.com",
        "server_port": 443,
        "uuid": "00000000-0000-0000-0000-000000000000",
        "tls": {"enabled": True, "server_name": "us.example.com"},
    },
    {
        "type": "vless",
        "tag": "REPLACE-SG",
        "server": "sg.example.com",
        "server_port": 443,
        "uuid": "00000000-0000-0000-0000-000000000000",
        "tls": {"enabled": True, "server_name": "sg.example.com"},
    },
]

REGIONS = [
    ("🇭🇰 香港节点", "♻️ 香港自动", ["REPLACE-HK"]),
    ("🇯🇵 日本节点", "♻️ 日本自动", ["REPLACE-JP"]),
    ("🇺🇸 美国节点", "♻️ 美国自动", ["REPLACE-US"]),
    ("🇸🇬 新加坡节点", "♻️ 新加坡自动", ["REPLACE-SG"]),
]

DIRECT = "🌐 全球直连"
MAIN = "🚀 节点选择"
AUTO = "♻️ 自动选择"

# 服务分组；sing-box 没有 icon 字段，图标只在面板里按名字认
SERVICE_GROUPS = ["▶️ YouTube", "🔍 Google", "🔮 OpenAI", "🧠 Claude", "🤖 Gemini",
                  "📦 GitHub", "Ⓜ️ Microsoft", "🎵 TikTok", "📺 NETFLIX", "🍏 Apple"]

MIRROR = "https://raw.githubusercontent.com"
META = MIRROR + "/MetaCubeX/meta-rules-dat/sing/geo"

# 规则集统一直连下载：避免「要开代理才能下规则集」的死循环。
# 国内直连 raw.githubusercontent.com 不通时，把 MIRROR 换成镜像前缀，
# 例如 https://ghfast.top/https://raw.githubusercontent.com，再跑一遍 gen.py。
RULE_SETS = [
    {"type": "remote", "tag": "geosite-openai", "format": "binary", "url": META + "/geosite/openai.srs"},
    {"type": "remote", "tag": "geosite-gemini", "format": "binary", "url": META + "/geosite/google-gemini.srs"},
    {
        "type": "remote",
        "tag": "geosite-claude",
        "format": "source",
        "url": MIRROR + "/kenzok8/ruleset/main/rule/Claude.json",
    },
    {"type": "remote", "tag": "geosite-youtube", "format": "binary", "url": META + "/geosite/youtube.srs"},
    {"type": "remote", "tag": "geosite-google", "format": "binary", "url": META + "/geosite/google.srs"},
    {"type": "remote", "tag": "geosite-github", "format": "binary", "url": META + "/geosite/github.srs"},
    {"type": "remote", "tag": "geosite-tiktok", "format": "binary", "url": META + "/geosite/tiktok.srs"},
    {"type": "remote", "tag": "geosite-netflix", "format": "binary", "url": META + "/geosite/netflix.srs"},
    {"type": "remote", "tag": "geosite-apple", "format": "binary", "url": META + "/geosite/apple.srs"},
    {"type": "remote", "tag": "geosite-microsoft", "format": "binary", "url": META + "/geosite/microsoft.srs"},
    {"type": "remote", "tag": "geosite-geolocation-!cn", "format": "binary", "url": META + "/geosite/geolocation-!cn.srs"},
    {"type": "remote", "tag": "geosite-cn", "format": "binary", "url": META + "/geosite/cn.srs"},
    {"type": "remote", "tag": "geosite-private", "format": "binary", "url": META + "/geosite/private.srs"},
    {"type": "remote", "tag": "geoip-google", "format": "binary", "url": META + "/geoip/google.srs"},
    {"type": "remote", "tag": "geoip-netflix", "format": "binary", "url": META + "/geoip/netflix.srs"},
    {"type": "remote", "tag": "geoip-cn", "format": "binary", "url": META + "/geoip/cn.srs"},
    {"type": "remote", "tag": "geoip-private", "format": "binary", "url": META + "/geoip/private.srs"},
]

RULES = [
    {"action": "sniff"},
    {"protocol": "dns", "action": "hijack-dns"},
    {"clash_mode": "direct", "outbound": DIRECT},
    {"clash_mode": "global", "outbound": "GLOBAL"},
    {
        "domain": ["clash.razord.top", "yacd.metacubex.one", "yacd.haishan.me", "d.metacubex.one"],
        "outbound": DIRECT,
    },
    {"rule_set": ["geosite-private", "geoip-private"], "outbound": DIRECT},
    {"rule_set": "geosite-openai", "outbound": "🔮 OpenAI"},
    {"rule_set": "geosite-claude", "outbound": "🧠 Claude"},
    {"rule_set": "geosite-gemini", "outbound": "🤖 Gemini"},
    {"rule_set": "geosite-github", "outbound": "📦 GitHub"},
    {"rule_set": "geosite-youtube", "outbound": "▶️ YouTube"},
    {"rule_set": "geosite-microsoft", "outbound": "Ⓜ️ Microsoft"},
    {"rule_set": ["geoip-google", "geosite-google"], "outbound": "🔍 Google"},
    {"rule_set": "geosite-tiktok", "outbound": "🎵 TikTok"},
    {"rule_set": "geosite-apple", "outbound": "🍏 Apple"},
    {"rule_set": ["geoip-netflix", "geosite-netflix"], "outbound": "📺 NETFLIX"},
    {"rule_set": "geosite-geolocation-!cn", "outbound": MAIN},
    {"rule_set": ["geoip-cn", "geosite-cn"], "outbound": DIRECT},
]


def dns_block():
    return {
        "servers": [
            {"type": "udp", "tag": "dns_direct", "server": "223.5.5.5", "detour": DIRECT},
            {"type": "tls", "tag": "dns_proxy", "server": "8.8.8.8", "detour": MAIN},
        ],
        "rules": [
            {"clash_mode": "Direct", "server": "dns_direct"},
            {"clash_mode": "Global", "server": "dns_proxy"},
            {"rule_set": "geosite-cn", "action": "route", "server": "dns_direct"},
            {"rule_set": "geosite-geolocation-!cn", "server": "dns_proxy"},
        ],
        "final": "dns_proxy",
        "strategy": "ipv4_only",
    }


def outbounds():
    groups = []

    region_refs = [g for g, _, _ in REGIONS] + [a for _, a, _ in REGIONS]
    groups.append(
        {
            "type": "selector",
            "tag": MAIN,
            "outbounds": [AUTO] + region_refs + [DIRECT],
            "default": AUTO,
        }
    )

    for name in SERVICE_GROUPS:
        groups.append(
            {
                "type": "selector",
                "tag": name,
                "outbounds": [MAIN, AUTO] + region_refs + [DIRECT],
                "default": MAIN,
            }
        )

    groups.append({"type": "selector", "tag": "🔍 列表之外", "outbounds": [MAIN, DIRECT], "default": MAIN})
    groups.append({"type": "selector", "tag": DIRECT, "outbounds": ["direct"], "default": "direct"})

    for name, auto, nodes in REGIONS:
        groups.append({"type": "selector", "tag": name, "outbounds": list(nodes), "default": nodes[0]})

    all_nodes = [n for _, _, ns in REGIONS for n in ns]
    for name, auto, nodes in REGIONS:
        groups.append(
            {"type": "urltest", "tag": auto, "outbounds": list(nodes), "interval": "3m", "tolerance": 50}
        )
    groups.append(
        {"type": "urltest", "tag": AUTO, "outbounds": all_nodes, "interval": "5m", "tolerance": 50}
    )

    nodes = [dict(n) for n in PLACEHOLDER_NODES]
    for node in nodes:
        node["domain_resolver"] = "dns_direct"
    direct = {"type": "direct", "tag": "direct", "domain_resolver": "dns_direct"}
    return nodes + groups + [direct]


HTTP_CLIENTS = [{"tag": "direct-http", "detour": "direct"}]


def experimental():
    return {
        "clash_api": {
            "external_controller": "0.0.0.0:9191",
            "external_ui": "/etc/sing-box/ui",
            "secret": "",
            "external_ui_download_url": "https://ghfast.top/https://github.com/MetaCubeX/metacubexd/archive/refs/heads/gh-pages.zip",
            "external_ui_download_detour": DIRECT,
            "default_mode": "rule",
        },
        "cache_file": {"enabled": True, "path": "/etc/sing-box/cache.db", "store_fakeip": False},
    }


INBOUNDS = {
    "tun": [
        {"type": "tun", "address": ["172.19.0.1/30", "fdfe:dcba:9876::1/126"], "auto_route": True,
         "strict_route": True, "route_exclude_address": ["192.168.0.0/16", "10.0.0.0/8", "172.16.0.0/12"],
         },
    ],
    "tproxy": [
        {"type": "tproxy", "tag": "tproxy-in", "listen": "0.0.0.0", "listen_port": 7894},
        {"type": "mixed", "tag": "mixed-in", "listen": "0.0.0.0", "listen_port": 7890},
    ],
    "mixed": [
        {"type": "mixed", "tag": "mixed-in", "listen": "0.0.0.0", "listen_port": 7890},
        {"type": "socks", "tag": "socks-in", "listen": "0.0.0.0", "listen_port": 7891},
    ],
}


def build(variant):
    return {
        "log": {"level": "info", "timestamp": True},
        "dns": dns_block(),
        "inbounds": INBOUNDS[variant],
        "outbounds": outbounds(),
        "http_clients": HTTP_CLIENTS,
        "route": {
            "default_http_client": "direct-http",
            "rules": RULES,
            "rule_set": RULE_SETS,
            "final": "🔍 列表之外",
            "auto_detect_interface": variant == "tun",
        },
        "experimental": experimental(),
    }


if __name__ == "__main__":
    for variant in ("tun", "tproxy", "mixed"):
        path = f"config-{variant}.json"
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(build(variant), fh, ensure_ascii=False, indent=2)
            fh.write("\n")
        print("wrote", path)
