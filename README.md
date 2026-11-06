# Bugün Ne İzlesem? (Tam Sürüm)

Her akşam 19:45'te X (Twitter) hesabınızdan filmleri afişleriyle birlikte otomatik paylaşan sistem.

## Dosya Yapısı
* `bot.py`: X API v1.1 ile afişi yükleyen ve v2 ile tweeti atan ana script.
* `.github/workflows/daily_tweet.yml`: Her gün 19:45'te botu tetikleyen GitHub Actions akışı.
* `data/recommendations.json`: Film veritabanı (afiş linkleri, açıklamalar, platform bilgileri).
* `index.html`: Günün filmini sergileyen vitrin sayfası.
* `reji.html`: Kuyruktaki filmleri gösteren kontrol paneli.

## Kurulum
1. GitHub Repository > Settings > Secrets and variables > Actions menüsüne gidin.
2. X Developer Portal'dan aldığınız şu anahtarları ekleyin:
   * `TWITTER_API_KEY`
   * `TWITTER_API_SECRET`
   * `TWITTER_ACCESS_TOKEN`
   * `TWITTER_ACCESS_TOKEN_SECRET`
   * `TWITTER_BEARER_TOKEN`
