---
name: legal-crawler
description: "Indonesian legal regulation crawler — crawl peraturan.go.id (62K+ regulations) and peraturan.bpk.go.id (303K+ regulations) via stealth Indonesian VPS tunnel. Use when: building legal knowledge bases, scraping Indonesian government regulation sites, setting up SOCKS5 proxy tunnels for geo-blocked .go.id sites, extracting regulation relationships (mencabut, mengubah, dasar hukum), or building regulation knowledge graphs. Also trigger on: peraturan.go.id, peraturan.bpk.go.id, JDIH, Indonesian law crawler, regulation parser, BPK search."
category: security
---

# Indonesian Legal Regulation Crawler

Build a comprehensive Indonesian legal regulation knowledge base by crawling dual government sources with stealth tunneling.

## Architecture

```
┌──────────────┐     SOCKS5      ┌──────────────┐     HTTPS     ┌──────────────────┐
│   Firecrawl  │ ──────────────→ │  VPS Jakarta  │ ────────────→ │ peraturan.go.id  │
│   Server     │   port 443      │  (Stunnel4)   │               │ peraturan.bpk    │
└──────────────┘                  └──────────────┘               └──────────────────┘
```

## Prerequisites

1. **Indonesian VPS** (Dihostingin Rp 25k/month) — IP must be Indonesian
2. **Firecrawl server** (self-hosted) — handles JavaScript rendering
3. **rclone** — for Google Drive auto-upload

## VPS Setup (Stealth Mode)

```bash
# SSH into VPS (port 2222)
ssh -p 2222 root@VPS_IP

# SOCKS5 server on port 443 (looks like HTTPS)
cat > /opt/socks5_server.py << 'PYEOF'
import socket, threading, select, struct
class SOCKS5Server:
    def __init__(self, host='0.0.0.0', port=443):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((host, port))
        self.server.listen(100)
    def handle(self, client):
        try:
            data = client.recv(256)
            if not data: return
            client.send(b'\x05\x00')
            data = client.recv(256)
            if not data: return
            cmd = data[1]
            if cmd != 1:
                client.send(b'\x05\x07\x00\x01\x00\x00\x00\x00\x00\x00')
                return
            atyp = data[3]
            if atyp == 1:
                addr = socket.inet_ntoa(data[4:8])
                port = struct.unpack('!H', data[8:10])[0]
            elif atyp == 3:
                dlen = data[4]
                addr = data[5:5+dlen].decode()
                port = struct.unpack('!H', data[5+dlen:7+dlen])[0]
            else:
                client.send(b'\x05\x08\x00\x01\x00\x00\x00\x00\x00\x00')
                return
            remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            remote.settimeout(10)
            remote.connect((addr, port))
            client.send(b'\x05\x00\x00\x01' + socket.inet_aton('0.0.0.0') + struct.pack('!H', 0))
            sockets = [client, remote]
            while True:
                readable, _, exceptional = select.select(sockets, [], sockets, 30)
                if exceptional: break
                for s in readable:
                    data = s.recv(65536)
                    if not data: return
                    (remote if s is client else client).send(data)
        except: pass
        finally:
            client.close()
            try: remote.close()
            except: pass
    def run(self):
        while True:
            client, addr = self.server.accept()
            threading.Thread(target=self.handle, args=(client,), daemon=True).start()
if __name__ == '__main__':
    SOCKS5Server().run()
PYEOF

# Systemd service
cat > /etc/systemd/system/socks5.service << 'EOF'
[Unit]
Description=SOCKS5 Proxy Server
After=network.target
[Service]
Type=simple
ExecStart=/usr/bin/python3 /opt/socks5_server.py
Restart=always
RestartSec=3
[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload && systemctl enable socks5 && systemctl start socks5
ufw allow 443/tcp && ufw --force enable
```

## Firecrawl Configuration

Set in Firecrawl `.env`:
```
PROXY_SERVER=socks5://VPS_IP:443
```

## peraturan.go.id Crawler

### URL Pattern
```
https://peraturan.go.id/id/{slug}
Example: https://peraturan.go.id/id/uu-no-19-tahun-2003
```

### Structured JSON Output
```json
{
  "doc_id": "UU-2003-19",
  "doc_type": "undang undang",
  "doc_title": "UNDANG-UNDANG Nomor 19 Tahun 2003 tentang BADAN USAHA MILIK NEGARA",
  "doc_form": "UNDANG-UNDANG",
  "doc_form_short": "UU",
  "doc_number": "19",
  "doc_year": "2003",
  "doc_status": "Berlaku",
  "doc_date_enacted": "19 Juni 2003",
  "relationships": {
    "mencabut": [...],
    "diubah_oleh": [...],
    "dilaksanakan_oleh": [...],
    "dasar_hukum": [...]
  }
}
```

### Relation Types (peraturan.go.id)
- `mencabut` — revokes
- `dicabut_oleh` — revoked by
- `mengubah` — amends
- `diubah_oleh` — amended by
- `dilaksanakan_oleh` — implemented by
- `melaksanakan_amanat` — implements mandate
- `dasar_hukum` — legal basis

## peraturan.bpk.go.id Crawler

### URL Pattern
```
https://peraturan.bpk.go.id/Details/{numeric_id}/{slug}
Example: https://peraturan.bpk.go.id/Details/337869/uu-no-1-tahun-2026
```

### BPK Search — Pagination & Types
```
Search URL: https://peraturan.bpk.go.id/Search?keywords=&tentang=&nomor=&jenis={id}&p={page}

Key jenis IDs:
  8  = Undang-undang (UU)
  10 = Peraturan Pemerintah (PP)
  11 = Peraturan Presiden (Perpres)
  12 = Keputusan Presiden (Keppres)
  19 = Peraturan Daerah (Perda)
  27 = Peraturan BPK
  42 = Peraturan Menteri Keuangan
  80 = Peraturan OJK
  95 = Peraturan MA

Full mapping: 269 types in CrawlerConfig.REGULATION_TYPE_MAP
See: src/config/crawler_config.py in LawRAG repo
```

### BPK-Only Fields
- `doc_date_promulgated` — tanggal pengundangan
- `doc_date_effective` — tanggal berlaku
- `doc_subject` — subjek
- `doc_source` — sumber

### Relation Types (BPK)
- `diubah_dengan` — amended by
- `dicabut_dengan` — revoked by
- `mengatur_lebih_lanjut` — further regulates
- `mencabut_sebagian` — partially revokes

### Empty Types (skip these)
36 jenis yang TIDAK ada data di BPK. See `EMPTY_REGULATION_TYPES` in CrawlerConfig.

## Data Asymmetry

| Source | Strong At | Weak At |
|--------|-----------|---------|
| peraturan.go.id | Dilaksanakan Oleh, Melaksanakan, Dasar Hukum | Diubah (baru) |
| peraturan.bpk.go.id | Diubah, Mengubah, Tanggal, Subjek | Dilaksanakan Oleh |

**Merge strategy:** Combine both sources by slug for complete relationship graph.

## Auto-Upload to Google Drive

```python
# Every 1000 files
rclone copy /path/to/data/ gdrive:corpus/metadata/ --progress --transfers 4
```

## Pitfalls

1. **BPK search uses `p=` parameter** (not `page=`)
2. **Cloudflare blocks direct HTTP** — must use Firecrawl for BPK search pages
3. **BPK detail pages work without proxy** — only search/index pages are Cloudflare-protected
4. **peraturan.go.id blocks non-Indonesian IPs** — requires SOCKS5 through Jakarta VPS
5. **Firecrawl timeout on BPK pagination** — only page 1 returns results via Firecrawl; use filter combinations (jenis+tahun) for more URLs
6. **Rate limit:** Random delay 2-5s between requests, ~32 MB/day bandwidth
7. **Stunnel4 vs raw SOCKS5:** Both work, SOCKS5 on port 443 is stealthier
8. **JSON output uses `ensure_ascii=False`** for Indonesian characters
9. **SQLite WAL mode** for concurrent crawler access
10. **Dedup by slug** — same regulation from both sources = merge target

## Key Files

| File | Purpose |
|------|---------|
| `crawler.py` | peraturan.go.id crawler (structured JSON, auto-upload) |
| `crawler_bpk.py` | BPK crawler with auto-discovery |
| `parse_relations.py` | Parser + batch converter + graph builder |
| `parse_relations_bpk.py` | BPK-specific parser (label-value format) |
| `batch_upload.py` | rclone uploader |
| `bpk_url_harvester_v5.py` | BPK URL discovery via search pagination |
| `samples/` | Example JSON files for each source |

## Environment

```
Firecrawl: http://FIRECRAWL_IP:3002/v1/scrape
Proxy: socks5://VPS_IP:443
VPS: Dihostingin Jakarta, SSH port 2222
GitHub: alkindivv/Legal-Crawler
rclone remote: gdrive:corpus/metadata/
```

## References

- `alkindivv/LawRAG` (development branch) — BPK CrawlerConfig with 269 regulation type IDs
- `suryast/indonesia-gov-apis` — 57 Indonesian gov APIs
- `Azzindani/ID_REG_KG_2511` (HuggingFace) — 750K regulation dataset
