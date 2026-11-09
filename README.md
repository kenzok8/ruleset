# ruleset

个人自用的规则名单与配置模板。按**内核**分目录，因为不同内核的配置语法、规则格式、概念完全不通，混在一起没法维护。

```
rule/       规则名单真源（跨内核共享，配置里用 raw URL 引用）
mihomo/     Clash 系内核的配置模板
sing-box/   sing-box 内核
dae/        dae / daed 内核
honk/       honk 内核（dae 的 Rust 重写，语法同源）
clients/    不属于上述内核的客户端（Shadowrocket 等）
icon/       策略组图标
```

## 和 openwrt-tower 的分工

[Tower](https://github.com/kenzok8/openwrt-tower) 是路由器上跑的配置工作台：整理订阅 → 选规则 → 导出 OpenClash / Nikki / Clashoo / Momo / dae / Honk / sing-box / Surge 等客户端配置，内置 32 份 ACL4SSR 名单。

所以本仓库不往「配置生成器」方向堆，只负责两件事：

1. **规则名单真源** —— 自己手维护、Tower 和手动配置都指向这里
2. **少量人肉导入的模板** —— 桌面端 Verge、VPS 服务端这种不适合在线生成的场景

需要批量生成配置请去 Tower；需要一份能直接导入的 yaml / json 就在这里拿。

---

## 一、规则名单（`rule/`）

配置里通过 raw URL 引用，改完推到 `main` 就生效。

| 文件 | 格式 | 内容 | 用途 |
|------|------|------|------|
| `rule/Direct.list` | classical | 520 条：阿里 / 字节 / 腾讯 / B 站 / 网易等国内大厂域名 | 直连补充，防国内站走代理变慢或触发风控 |
| `rule/ProxyLite.list` | classical | 26 条：Plex、国外 DNS 服务器 IP | 代理补充，Plex 远程访问和 DoH 必须走代理 |
| `rule/AI.list` | classical | Perplexity / Grok / Copilot / HuggingFace / Poe / Cursor 等 | AI 兜底组。OpenAI / Claude / Gemini / Muse 各自有独立名单，这份管其余 AI 站 |
| `rule/Claude.list` | classical | Anthropic / Claude 自有域名 + 依赖的第三方域名 + 自有网段 | Claude 组。替代 `geosite:anthropic`，把 datadog / sift 这类漏网的第三方也拽进同一出口 |
| `rule/Claude.json` | sing-box source | 与 Claude.list 同一套规则 | 给 sing-box 用（`format: source`）。改名单时两个文件一起改 |
| `rule/Muse.list` | classical | `muse.ai`（Meta 旗下的个人 AI Agent） | Muse 组。geosite 里没有 muse 这个 code，只能手写域名 |
| `rule/ApplePush.list` | classical | APNs 推送域名 + Apple 推送 IP 段 | 独立推送组，国内 iPhone 建议 APNs 走代理 |
| `rule/FakeIPFilter-CN.list` | domain text | 局域网、国内 NTP、运营商一键登录、音乐/游戏/Apple 更新 CDN | fake-ip 白名单（国内段），命中返回真实 IP |
| `rule/FakeIPFilter-NotCN.list` | domain text | 国外 NTP、STUN、Switch/PS/Xbox 联机、Netflix、Disney+、Plex | fake-ip 白名单（国外段） |

**为什么要 fake-ip 白名单**：fake-ip 会给每个域名返回假的 `198.18.x.x`。时间同步、STUN 打洞、游戏机联机、局域网设备这几类拿到假 IP 后，表现是「网页能开，但时间不更新 / 联机失败 / 找不到 NAS」。所以必须放行真实解析。

引用地址（把 `main` 换成其他分支即切换）：

```
https://raw.githubusercontent.com/kenzok8/ruleset/main/rule/Direct.list
https://raw.githubusercontent.com/kenzok8/ruleset/main/rule/ProxyLite.list
https://raw.githubusercontent.com/kenzok8/ruleset/main/rule/AI.list
https://raw.githubusercontent.com/kenzok8/ruleset/main/rule/Claude.list
https://raw.githubusercontent.com/kenzok8/ruleset/main/rule/Claude.json
https://raw.githubusercontent.com/kenzok8/ruleset/main/rule/Muse.list
https://raw.githubusercontent.com/kenzok8/ruleset/main/rule/ApplePush.list
https://raw.githubusercontent.com/kenzok8/ruleset/main/rule/FakeIPFilter-CN.list
https://raw.githubusercontent.com/kenzok8/ruleset/main/rule/FakeIPFilter-NotCN.list
```

> `raw.githubusercontent.com` 被墙时，前缀换成 `https://cdn.jsdelivr.net/gh/kenzok8/ruleset@main/`。

---

## 二、Mihomo / Clash（`mihomo/`）

| 文件 | 适合谁 | 说明 |
|------|--------|------|
| `config.yaml` | **推荐** | 多订阅 + 完整分流 + 图标 + fake-ip 白名单。走 fake-ip 但不强制 DNS 全走代理，追求「能上、能分流」 |
| `config-fakeip.yaml` | 在意 DNS 泄漏 | 分流规则和 `config.yaml` 一样，只换 DNS：国内走国内 DNS，国外走国外 DNS 并从代理出口，输出前做 geoip 校验防污染 |
| `config-full.yaml` | 要全端口 + TUN | 开了 http / socks / redir / tproxy / mixed 五端口，带 geo 自动更新 |
| `config-basic.yaml` | 单订阅、快速跑通 | 只有一个机场占位，规则最少 |
| `config-compat.yaml` | Clash Premium 内核 | 全部 text/yaml 规则，不用 mrs |
| `kenzo.yaml` | 自用 | 个人模板，订阅已占位化。AI 分 OpenAI / Claude / Gemini / Muse / AI 其他 五组 |
| `fx.yaml` | 覆写模板（Overwrite） | **不含订阅和节点**，只有 global / dns / tun / proxy-groups / rules。配合 Clash Verge 的「覆写 / Overwrite」或 OpenClash 的「覆写设置」叠加到自己的配置上，直连目标统一写 `DIRECT` 而不是 `🌐 直连`，因为覆写时不确定主配置有没有定义后者 |
| `openclash/` | OpenClash 专用 | `openclash.uci` 是 UCI 配置（放 `/etc/config/openclash`），`kenzo.ini` / `kenzo_mini.ini` 是 OpenClash 的自定义规则集订阅格式 |

### 客户端对应

| 客户端 | 用哪个 |
|--------|--------|
| Clash Verge Rev / FlClash | `config.yaml` |
| luci-app-fchomo / momo / nikki | `config.yaml` |
| luci-app-openclash（Meta 内核） | `config.yaml` |
| luci-app-openclash（Premium 内核） | `config-compat.yaml` |

### 关于图标

`proxy-groups` 的 `icon:` 需要 mihomo v1.18.0+，Clash Verge Rev / zashboard / FlClash / metacubexd 能显示。老客户端直接忽略这个字段，不影响分流。

图标自托管在 `icon/`：

- 品牌 logo：来自 [homarr-labs/dashboard-icons](https://github.com/homarr-labs/dashboard-icons)（Apache-2.0）
- 国家旗帜：来自 [lipis/flag-icons](https://github.com/lipis/flag-icons)（MIT）
- 通用图标（rocket / direct / home / globe / fish / auto / all / bell / film）：本仓库自绘

加图标就是加一行 `icon: "https://raw.githubusercontent.com/kenzok8/ruleset/main/icon/<名字>.svg"`。

---

## 三、dae（`dae/`）

| 文件 | 说明 |
|------|------|
| `config.dae` | 完整版。AI 分 OpenAI / Claude / Gemini / Muse 四组（Muse 用 `domain(suffix: muse.ai)` 手写，geosite 里没这个 code；Claude 组另补了 datadog / sift 等第三方域名和 Anthropic 网段兜底），YouTube / Google / Telegram / Steam 等平台各自分组，国内外 DNS 分流 |
| `config.min.dae` | 精简版。只有一个 Proxy 组，先跑通再说 |

### 依赖的 geo 数据

```
/usr/share/v2ray/geosite.dat
/usr/share/v2ray/geoip.dat
```

OpenWrt 装 `v2ray-geosite` + `v2ray-geoip`，`luci-app-daede` 的「更新 geo」会下载 [Loyalsoldier/v2ray-rules-dat](https://github.com/Loyalsoldier/v2ray-rules-dat) 的版本。

用到的 geosite 代码（已核对存在）：`cn`、`geolocation-!cn`、`private`、`openai`、`anthropic`、`google-gemini`、`category-ai-!cn`、`youtube`、`google`、`github`、`onedrive`、`microsoft`、`microsoft@cn`、`apple`、`apple@cn`、`telegram`、`tiktok`、`netflix`、`paypal`、`binance`、`okx`、`category-cryptocurrency`、`steam`、`steam@cn`。

### 三个必须改的地方

1. `subscription` 的 `sub` —— dae **只支持 v2ray / URL 格式订阅**，mihomo 格式要先用 sub-store 转
2. `global` 的 `lan_interface` —— x86 软路由一般是 `br-lan`，用 `ip a` 确认
3. `group` 的地区正则 —— 改成你机场节点名里真实出现的关键字

组名只能用英文和数字，不能用中文和 emoji。

---

## 四、Honk（`honk/`）

Honk 是 dae 的 Rust + eBPF 重写，语法同源，差异见 [honk/README.md](honk/README.md)：

- `global` / `experimental` 可以和其它配置写在同一份 `config.dae` 里（本仓库就是单文件），也可以拆到 `system.dae` 用 `include` 引入，内核两种都吃
- DNS `upstream` 定义时就绑定出口（`-> direct` / `-> proxy`）
- `experimental.native_api` 是 Doona 面板的连接入口，另有可选的 `clash_api`

| 文件 | 说明 |
|------|------|
| `config.dae` | 单文件：订阅 + 策略组 + DNS + 路由 + `global` + `experimental` |

> `luci-app-honk` 的**托管模式**会自己生成两份（`config.dae` + `system.dae` + `include`），因为设置页要靠改 `system.dae` 调监听端口和 Clash API。导入本仓库这份单文件后跑的是**手动模式**，端口由文件决定，LuCI 里那些设置项变只读。

内核要求：Linux **6.12+** 且带 BTF（`/sys/kernel/btf/vmlinux`）。低于 6.12（如 24.10 的 6.6）或没有 BTF，honk 直接起不来。

---

## 五、sing-box / HomeProxy（`sing-box/`）

要求 **sing-box 1.12 以上**。配置按 1.14 的新 DNS 写法、HTTP 客户端写法重写过，用 1.15 校验通过——旧版的 `use_all_providers` / `includes` 是转换器字段，原生内核从来就不认，已经去掉。

| 文件 | 适合谁 | 入口 |
|------|--------|------|
| `config-tun.json` | 桌面 / 手机 TUN，自动接管系统路由 | TUN |
| `config-tproxy.json` | OpenWrt 透明代理 | tproxy 7894 + mixed 7890 |
| `config-mixed.json` | 只要端口，局域网共享 | mixed 7890 + socks 7891 |

三份由 `gen.py` 生成：改规则 / 策略组 / DNS 只改 `gen.py`，在本目录跑 `python3 gen.py`，再用 `sing-box check -c config-tun.json` 校验。

**节点是占位的**：`outbounds` 里 `REPLACE-HK`、`REPLACE-JP`、`REPLACE-US`、`REPLACE-SG` 四段换成自己的节点，地区分组和自动测速组会跟着生效。节点多的时候建议配合转换器生成。

规则集全部直连下载（`http_clients` 指向 `direct`），避开「要先开代理才能下规则集」的死循环。国内直连 `raw.githubusercontent.com` 不通时，把 `gen.py` 里的 `MIRROR` 换成镜像前缀（比如 `https://ghfast.top/https://raw.githubusercontent.com`）再生成一遍。

需要 fake-ip 时改 `gen.py` 的 `dns_block()`：`servers` 里加 `{"type": "fakeip", "tag": "fakeip", "inet4_range": "198.18.0.0/15"}`，`rules` 最前面加 `{"query_type": ["A", "AAAA"], "server": "fakeip"}`。

注意 sing-box 只吃 `.srs` 二进制或 source 格式的 JSON，**不能**直接吃 `rule/*.list`。Claude 组用本仓库的 `rule/Claude.json`（`format: source`），其余规则集仍指向上游 MetaCubeX 的 `sing` 分支。

`homeproxy` 和 `homeproxy无订阅自行添加.txt` 是 HomeProxy 插件的 UCI 配置，不是 sing-box 配置文件。

---

## 六、其他客户端（`clients/`）

| 目录 | 说明 |
|------|------|
| `clients/shadowrocket/` | Shadowrocket 防 DNS 泄漏配置 |
