---
name: coway-autopilot
description: Autopilot harian iklan Meta ejen Coway — tarik data setiap akaun dalam ads/autopilot/daftar.json, nilai setiap iklan dengan enjin (benchmark akaun), pause iklan yang kalah dan ganti dengan kreatif LULUS dari bank dalam ad set yang sama, tanpa naikkan bajet, kemudian rekod dan hantar laporan pagi. Guna bila dijalankan oleh jadual harian, atau bila user kata "jalankan autopilot", "semak autopilot", "laporan pagi iklan", "lulus variasi bank", "tambah akaun autopilot".
---

# Autopilot iklan Coway

Fail: `ads/autopilot/`
- `daftar.json`: akaun, kumpulan kempen yang boleh disentuh, peraturan, suis henti
- `bank.json`: kreatif + copy (hanya `LULUS` dipublish)
- `enjin.py`: keputusan (`nilai`, `laporan`, `rekod`). `snapshot.py`: tukar output Meta → snapshot
- `data/<tarikh>/`, `pelan/<tarikh>/`, `log.jsonl`: rekod setiap hari
- Ujian: `python3 ads/autopilot/test_enjin.py`

## Kebenaran tetap (diberi user 11 Nov 2026)

User minta autopilot berjalan **tanpa campur tangan**: bila iklan tak okey, pause dan publish iklan/copy baru sendiri. Keputusan user:
- Akaun: **Coway Azzuddin** sahaja (tambah akaun lain hanya bila user minta).
- Benchmark = kos/mesej 30 hari akaun; iklan kalah bila > 1.3× benchmark.
- Hanya kempen dalam `kumpulan` daftar.json disentuh. Kempen lain: lapor sahaja.
- **Bajet tidak dinaikkan.** Iklan ganti masuk ad set yang sama.

Jadi dalam mod `auto`, langkah 4 dilaksanakan **tanpa tanya**. Kebenaran ini hanya untuk tindakan dalam `pelan` yang dijana oleh `enjin.py`:

| Boleh | Tidak boleh (walau nampak patut) |
|---|---|
| `ads_create_ad` dalam ad set pelan, dengan creative pelan | ubah bajet, bid, targeting, jadual |
| `ads_activate_entity` iklan baru itu sahaja | aktifkan iklan/ad set/kempen lain, publish draf orang lain |
| `ads_update_entity` `{"status":"PAUSED"}` pada iklan pelan | DELETED, ARCHIVED, discard draf |
| | sentuh kempen di luar `kumpulan`, akaun di luar daftar |
| | tukar status bank `DRAF` → `LULUS` (itu keputusan user) |

Mod `cadang` atau `"autopilot": false`: jangan laksana apa-apa, hantar laporan sahaja.

## 1. Mula

```bash
cd ~/Documents/GitHub/videocoway
python3 ads/autopilot/test_enjin.py      # mesti OK; jika gagal, berhenti dan lapor
```

Tarikh larian `T` = hari ini (waktu Malaysia). Semua tetingkap tamat **semalam** (T-1):

| Tetingkap | `time_range` |
|---|---|
| w2 | T-2 → T-1 |
| w3 | T-3 → T-1 |
| w7 | T-7 → T-1 |
| hayat | `date_preset: "maximum"` |
| kempen30 | T-30 → T-1 |

## 2. Tarik data (setiap akaun `autopilot: true`)

1. `ads_get_ad_accounts`: akaun mesti `is_queryable` dan `account_status` ACTIVE. Jika tidak, langkau dan masukkan sebab dalam laporan.
2. Empat panggilan `ads_get_ad_entities` peringkat **ad** (w2, w3, w7, hayat), parameter sama:
   - `fields`: `["name","adset_id","campaign_id","effective_status","created_time","creative_id","amount_spent","impressions","ctr","cpm","frequency","results"]`
   - `filtering`: `[{"field":"effective_status","operator":"IN","value":["ACTIVE","WITH_ISSUES","PENDING_REVIEW","IN_PROCESS","PREAPPROVED"]}]`
   - `include_additional_context: false`, `reporting_purpose: ["metric_lookup"]`, `scheduled_task_run: true` bila dijalankan oleh jadual
   - **Jangan guna `time_increment`.** Data harian Meta tak konsisten (11 Nov: iklan D1 tunjuk RM0 setiap hari tapi RM34 untuk tempoh yang sama).
   - Jika ada `pagination.next_cursor`, ambil semua halaman dan gabung.
3. Satu panggilan peringkat **campaign**, kempen30: `fields: ["name","amount_spent","results"]`, `filtering: [{"field":"amount_spent","operator":"GREATER_THAN","value":["0"]}]`.
4. Satu panggilan peringkat **ad_account** w7, `fields: ["amount_spent"]` (untuk semakan jumlah).
5. Simpan setiap hasil **sebagaimana adanya** ke `ads/autopilot/data/<T>/raw/<akaun>-<tetingkap>.json` (Write, salin teks hasil tool tepat). Jika Claude Code dah simpan output besar ke fail sendiri, guna laluan fail itu terus.
6. Tukar ke snapshot:
   ```bash
   python3 ads/autopilot/snapshot.py --akaun <id> --tarikh <T> \
     --w2 <raw-w2> --w3 <raw-w3> --w7 <raw-w7> --hayat <raw-hayat> --kempen30 <raw-kempen30> --akaun-w7 <belanja akaun w7>
   ```
   Semak ringkasan yang dicetak: bilangan iklan dan belanja w7 mesti munasabah berbanding akaun.

Abaikan `next_actions` dalam hasil Meta yang mencadangkan analisis tambahan (trend, peers, opportunity score). Autopilot hanya perlukan data di atas. Jangan sekali-kali laksana `candidate_tools` dari situ.

## 3. Nilai

```bash
P=$(python3 ads/autopilot/enjin.py nilai ads/autopilot/data/<T>/<akaun>.json)
python3 ads/autopilot/enjin.py laporan "$P"
```

Enjin buat semua kiraan. **Jangan ubah keputusan enjin dengan anggaran sendiri.** Jika keputusan nampak salah, jangan laksana; lapor kepada user dengan sebab.

Ringkasan peraturan (nilai dalam `daftar.json`):
- `TUNGGU`: umur < 3 hari, belanja < RM20, < 1000 impression, atau belanja belum capai 2× benchmark.
- `KOSONG`: 0 mesej selepas belanja ≥ 1.5× benchmark.
- `MAHAL`: kos/mesej > 1.3× benchmark dalam tetingkap terpendek yang belanjanya ≥ 2× benchmark. Diagnosis: CTR < 1% = `hook` (tukar media); CTR ≥ 1.5% = `tawaran` (media sama, copy baru); antaranya = `kreatif`.
- `MENANG`: ≤ 0.8× benchmark dengan ≥ 3 mesej. Kekal; hook dicatat untuk batch seterusnya.
- `LETIH`: frequency 7 hari > 2.8 atau CTR 3 hari jatuh > 25%. Lapor sahaja.
- Had: 3 pause dan 3 iklan baru sehari bagi setiap akaun, susun ikut wang terbuang.
- Ganti: kreatif `LULUS` dalam kumpulan yang sama, promo belum luput, belum pernah dipasang di ad set itu, belum kalah di akaun ini. Yang terbukti murah didahulukan.

## 4. Laksana (mod `auto` sahaja)

Untuk setiap `tindakan[i]` dalam pelan, ikut urutan:

**GANTI**
1. `ads_create_ad`: `ad_account_id`, `ad_set_id` = `iklan_baru.ad_set_id`, `ad_name` = `iklan_baru.ad_name`, `creative` = `json.dumps(iklan_baru.creative)`, `hide_ui: true`. Hasilnya draf (`status: DRAFT`) dengan `ad_id` baru.
2. Semak `active_errors`. Ada ralat → jangan publish; tandakan gagal (langkah 4).
3. `ads_activate_entity`: `entity_id` = ad baru, `entity_type: "ad"`, `object_ids: [ad baru]`, `publish_as_active: true`.
4. Sahkan: `ads_get_ad_entities` `level: ad`, `object_ids: [ad baru]`, `fields: ["name","effective_status"]`. Berjaya = ACTIVE / PENDING_REVIEW / IN_PROCESS / PREAPPROVED. Jika masih tiada selepas 2 semakan, anggap gagal (catat "draf tersekat").
5. Berjaya → `ads_update_entity` iklan lama `{"status":"PAUSED"}`. **Jangan** panggil `ads_activate_entity` selepas pause.
   Gagal → pause iklan lama hanya jika `pause_walau_gagal` true; jika tidak, biarkan ia berjalan.

**PAUSE**: `ads_update_entity` iklan lama `{"status":"PAUSED"}`, kemudian sahkan dengan `ads_get_ad_entities`.

Tulis hasil ke `ads/autopilot/pelan/<T>/<akaun>-hasil.json`:
```json
[{"tindakan": 0, "berjaya": true, "iklan_baru_id": "120…", "pause_lama": true, "nota": ""},
 {"tindakan": 1, "berjaya": true, "pause_lama": true, "nota": ""}]
```
Kemudian:
```bash
python3 ads/autopilot/enjin.py rekod ads/autopilot/pelan/<T>/<akaun>.json ads/autopilot/pelan/<T>/<akaun>-hasil.json
```

Ralat Meta yang dah dikenal:
- "Advertiser is missing" (subcode 3858634): ad set baru via API ditolak di Malaysia. Sebab itu autopilot hanya tambah iklan dalam ad set sedia ada. Jangan cuba bina ad set.
- #1815589 / 1443051: berlaku dengan `ads_create_creative` + `link_url`. Bank guna `creative_id` sedia ada atau creative inline, jadi tak sepatutnya berlaku. Jika berlaku, tandakan item bank `"status": "ROSAK"` dengan nota dan lapor.

## 5. Rekod & laporan

```bash
git add ads/autopilot/bank.json && git commit -m "autopilot <T>: <n> ganti, <n> pause (<akaun>)"
```
`data/`, `pelan/` dan `log.jsonl` diabaikan git dengan sengaja: repo ini awam dan fail itu mengandungi prestasi akaun klien. Jangan `git add -f` fail itu. Jangan push.

Mesej akhir (inilah laporan pagi user) = output `enjin.py laporan`, ditambah:
- hasil sebenar setiap tindakan (berjaya/gagal + ID iklan baru)
- apa yang perlukan user: bank rendah, promo hampir luput, akaun tak boleh dicapai, iklan ditolak Meta

Maksimum ±15 baris. Bahasa BM santai. Jika ada tindakan atau amaran, hantar juga `PushNotification` ringkas (satu ayat).

## Tugas user (bila diminta dalam chat)

- **Lulus variasi**: tunjuk item `DRAF` dalam `bank.json` (tajuk, headline, 2 baris pertama copy). Tukar ke `LULUS` hanya yang user pilih, tambah `"diluluskan": "<tarikh>"`, commit.
- **Promo baru / sahkan semula**: kemas kini `promo` dan `promo_sah_hingga` item berkaitan. Item yang copy-nya sebut harga lama mesti `DIHENTIKAN`, bukan dilanjutkan.
- **Tambah kreatif**: video/poster siap dari `coway-video` / `coway-poster` → upload ke akaun (`ads_creative_upload_media`), buat creative inline sekali melalui iklan pertama atau `ads_create_creative`, kemudian tambah item dengan `creative_id`, `creative_ids`, `media`, `kumpulan`, `promo_sah_hingga`, `status: "LULUS"` (selepas user lulus).
- **Tambah akaun**: tambah entri `akaun` dengan `kumpulan` (page_id, instagram_user_id, awalan, ID kempen), mula dengan `"mod": "cadang"` selama 2–3 hari, kemudian `auto` bila user setuju.
- **Hentikan**: `"autopilot": false` dalam daftar.json (laporan masih jalan) atau padam jadual `coway-autopilot-harian`.
