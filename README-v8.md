# Akşam Matinesi v8

- `index.html`: Canlı TMDB kataloğu, haftalık kuşak kartları ve editörün seçkileri.
- `reji.html`: v7 reji paneli; mevcut yayın kuyruğu korunur.
- `config.js`: İsteğe bağlı canlı TMDB katalog yapılandırması.

## Önemli
GitHub Pages statik olduğu için `reji.html` içindeki `localStorage` TMDB anahtarı diğer ziyaretçilere aktarılmaz.
Herkes için canlı katalog isteniyorsa `config.js` içinde bir TMDB tarayıcı API anahtarı ayarlanabilir,
**ancak bu anahtar herkese açık olacaktır**. Güvenli üretim çözümü sunucusuz proxy veya GitHub Actions
üzerinden periyodik JSON katalog üretimidir. Önceden sohbet içinde paylaşılan anahtarın yenilenmesi önerilir.

## Yükleme
1. Eski dosyaları yedekleyin.
2. `index.html`, `reji.html`, `config.js` dosyalarını depo köküne yükleyin.
3. `yayinlar.json` dosyanızı **değiştirmeyin**.
4. GitHub Pages güncellenince sayfayı Ctrl+F5 ile yenileyin.

Haftalık kartlar tıklanınca TMDB keşif filtreleriyle katalog açılır. API anahtarı yoksa açık hata gösterilir.
