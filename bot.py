import os
import sys
import json
import tempfile
import requests
import tweepy

# 1. Ortam Değişkenleri
API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET = os.getenv("TWITTER_API_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

if not all([API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET]):
    print("HATA: Twitter API anahtarlarından biri veya birkaçı eksik!")
    sys.exit(1)

# 2. İstemciler
# v1.1 Media Upload için:
auth = tweepy.OAuth1UserHandler(
    API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
)
api_v1 = tweepy.API(auth)

# v2 Client:
client_v2 = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)

def load_today_movie():
    json_path = os.path.join("data", "recommendations.json")
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"{json_path} dosyası bulunamadı.")
        
    with open(json_path, "r", encoding="utf-8") as f:
        movies = json.load(f)
    
    for movie in movies:
        if not movie.get("posted", False):
            return movie, movies, json_path
            
    return movies[0], movies, json_path

def download_or_get_image(poster_path_or_url):
    """
    Hem yerel dosya yolunu (posters/film.jpg) hem de web URL'lerini destekler.
    """
    if not poster_path_or_url:
        return None, False

    # Eğer yerel dosya varsa doğrudan kullan
    if os.path.exists(poster_path_or_url):
        print(f"Yerel afiş dosyası bulundu: {poster_path_or_url}")
        return poster_path_or_url, False

    # Web URL ise indir
    if poster_path_or_url.startswith("http://") or poster_path_or_url.startswith("https://"):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://www.imdb.com/"
        }
        print(f"Afiş indiriliyor: {poster_path_or_url}")
        res = requests.get(poster_path_or_url, headers=headers, stream=True, timeout=20)
        if res.status_code == 200:
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
            for chunk in res.iter_content(chunk_size=8192):
                tmp.write(chunk)
            tmp_path = tmp.name
            print(f"Afiş geçici dosyaya kaydedildi: {tmp_path}")
            return tmp_path, True
        else:
            print(f"Afiş indirilemedi! HTTP Durum Kodu: {res.status_code}")
            return None, False

    return None, False

def main():
    movie, all_movies, json_path = load_today_movie()
    
    film_adi = movie.get("title", "")
    imdb = movie.get("imdb", "")
    oyuncular = movie.get("cast", "")
    aciklama = movie.get("overview", "")
    poster_src = movie.get("poster_file") or movie.get("poster_url", "")
    platform = movie.get("platform", "")
    
    platform_satiri = f"🍿 {platform}\n" if platform else ""
    tweet_text = (
        f"📅 Akşam Matinesi | Saat 19:45\n\n"
        f"🔴 {film_adi} ({imdb}/10)\n"
        f"👥 {oyuncular}\n"
        f"📌 {aciklama}\n\n"
        f"{platform_satiri}"
        f"#Sinema #FilmÖnerisi #AkşamMatinesi"
    )
    
    media_ids = []
    tmp_path, is_temp = download_or_get_image(poster_src)
    
    if tmp_path:
        try:
            print(f"Afiş X sunucusuna yükleniyor (media_upload)...")
            media = api_v1.media_upload(filename=tmp_path)
            media_ids.append(media.media_id)
            print(f"Afiş başarıyla yüklendi! Media ID: {media.media_id}")
        except Exception as e:
            print(f"KRİTİK HATA - Görsel X'e yüklenemedi: {e}")
            print("İpucu: Access Token yetkilerinizin 'Read and write' olduğundan ve token'ı yeniden generate ettiğinizden emin olun.")
        finally:
            if is_temp and os.path.exists(tmp_path):
                os.remove(tmp_path)

    print(f"Tweet paylaşılıyor... (Görsel sayısı: {len(media_ids)})")
    if media_ids:
        res = client_v2.create_tweet(text=tweet_text, media_ids=media_ids)
    else:
        res = client_v2.create_tweet(text=tweet_text)
        
    print(f"Tweet başarıyla yayınlandı! ID: {res.data['id']}")
    
    # posted durumunu güncelle
    movie["posted"] = True
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(all_movies, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
