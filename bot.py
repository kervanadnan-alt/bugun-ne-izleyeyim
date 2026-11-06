import os
import json
import tempfile
import requests
import tweepy

# 1. Ortam Değişkenlerinden (GitHub Secrets) API Bilgilerini Al
API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET = os.getenv("TWITTER_API_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

# 2. X (Twitter) İstemcileri
# v1.1 API (Görsel yüklemek için zorunludur)
auth = tweepy.OAuth1UserHandler(
    API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
)
api_v1 = tweepy.API(auth)

# v2 Client (Tweet oluşturmak için)
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
    
    # Paylaşılmamış ilk filmi bul
    for movie in movies:
        if not movie.get("posted", False):
            return movie, movies, json_path
            
    # Tümü paylaşıldıysa sıfırdan başa dön
    return movies[0], movies, json_path

def main():
    movie, all_movies, json_path = load_today_movie()
    
    film_adi = movie.get("title", "")
    imdb = movie.get("imdb", "")
    oyuncular = movie.get("cast", "")
    aciklama = movie.get("overview", "")
    afis_url = movie.get("poster_url", "")
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
    
    # Afişi indir ve X sunucusuna medya olarak yükle
    if afis_url:
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(afis_url, headers=headers, stream=True, timeout=15)
            if response.status_code == 200:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
                    for chunk in response.iter_content(chunk_size=8192):
                        tmp_file.write(chunk)
                    tmp_path = tmp_file.name
                
                # X'e görsel yükleme
                media = api_v1.media_upload(filename=tmp_path)
                media_ids.append(media.media_id)
                os.remove(tmp_path)
                print("Afiş görseli başarıyla yüklendi.")
        except Exception as e:
            print(f"Görsel yükleme hatası: {e}")
            
    # Tweeti gönder
    if media_ids:
        res = client_v2.create_tweet(text=tweet_text, media_ids=media_ids)
    else:
        res = client_v2.create_tweet(text=tweet_text)
        
    print(f"Tweet başarıyla atıldı! Tweet ID: {res.data['id']}")
    
    # JSON üzerinde posted durumunu güncelle
    movie["posted"] = True
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(all_movies, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
