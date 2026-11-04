# 🎬 Bugün Ne İzleyeyim? — Otomatik X Botu & Netflix Öneri Sitesi

Bu paket, **Netflix Türkiye** kataloğundan her gün otomatik olarak yüksek puanlı bir film/dizi seçen, yapay zekâ ile 280 karakterlik X (Twitter) kancası ve web özeti hazırlayan, afişiyle birlikte **X hesabınızda tweet paylaşan** ve **web sitenizi otomatik güncelleyen** hazır bir projedir.

---

## 🚀 3 Adımda Kolay Kurulum

### 1. Adım: Dosyaları GitHub'a Yükleyin
1. [github.com](https://github.com) üzerinde yeni bir **Public** veya **Private** repository (depo) oluşturun (örneğin: `bugun-ne-izleyeyim`).
2. Bu ZIP paketindeki tüm dosyaları deponuza yükleyin (veya `git push` yapın).

---

### 2. Adım: API Anahtarlarını GitHub Secrets'a Ekleyin
GitHub deponuzda **Settings** > **Secrets and variables** > **Actions** sayfasına gidin ve **"New repository secret"** butonuna basarak şu anahtarları ekleyin:

| Secret Adı | Nereden Alınır? | Açıklama |
| :--- | :--- | :--- |
| `X_API_KEY` | [developer.x.com](https://developer.x.com) | X Consumer Key |
| `X_API_SECRET` | [developer.x.com](https://developer.x.com) | X Consumer Secret |
| `X_ACCESS_TOKEN` | [developer.x.com](https://developer.x.com) | X Access Token (*Read and Write* izinli) |
| `X_ACCESS_TOKEN_SECRET` | [developer.x.com](https://developer.x.com) | X Access Token Secret |
| `TMDB_API_KEY` | [themoviedb.org](https://www.themoviedb.org/settings/api) | Ücretsiz TMDB API Anahtarı |
| `GEMINI_API_KEY` | [aistudio.google.com](https://aistudio.google.com) | Ücretsiz Google Gemini API Anahtarı |

> ⚠️ **Önemli X Ayarı:** X Developer Portal'da uygulamanızın **User authentication settings** bölümünde **"Read and Write"** (Okuma ve Yazma) izninin açık olduğundan emin olun.

---

### 3. Adım: Web Sitesini Ücretsiz Yayına Alın & Test Edin

#### A. Web Sitesini Yayına Alma (Seçenek 1: Vercel - En Kolay & Önerilen):
1. [vercel.com](https://vercel.com) adresine gidin ve GitHub hesabınızla giriş yapın.
2. `bugun-ne-izleyeyim` reponuzu seçip **Deploy** butonuna basın.
3. Siteniz saniyeler içinde `bugun-ne-izleyeyim.vercel.app` şeklinde ücretsiz canlıya geçer!

#### B. Web Sitesini Yayına Alma (Seçenek 2: GitHub Pages):
1. GitHub reponuzda **Settings** > **Pages** sekmesine gidin.
2. **Build and deployment** altında Source olarak **"Deploy from a branch"** ve Branch olarak **"main"** seçin.
3. GitHub, sitenizi `kullaniciadiniz.github.io/bugun-ne-izleyeyim` adresinde yayına alır.

#### C. Botu Hemen Test Etme:
1. GitHub reponuzda **Actions** sekmesine tıklayın.
2. Sol menüden **"Günlük Netflix Tweeti & Site Güncellemesi"** iş akışını seçin.
3. Sağdaki **"Run workflow"** butonuna basarak botu hemen tetikleyin.
4. Bot çalışacak, X hesabınızda afişli tweet paylaşacak ve site veritabanını (`data/recommendations.json`) güncelleyecektir!

---

## ⏰ Otomasyon Zamanlaması
`.github/workflows/daily_tweet.yml` dosyası içerisinde zamanlayıcı tanımlıdır:
- Varsayılan olarak her gün **Türkiye saati ile 19:30'da** (16:30 UTC) otomatik çalışır.
- Saati değiştirmek için `.github/workflows/daily_tweet.yml` dosyasındaki cron satırını düzenleyebilirsiniz.

## 💻 Bilgisayarınızda Yerel Olarak Çalıştırmak İsterseniz:
```bash
# 1. Bağımlılıkları kurun
pip install -r requirements.txt

# 2. .env dosyanızı oluşturun ve anahtarları girin
cp .env.example .env

# 3. Test (Dry-run) modunda çalıştırma (tweet atmaz, konsolda gösterir):
python bot.py --dry-run

# 4. Gerçek çalıştırma:
python bot.py
```
