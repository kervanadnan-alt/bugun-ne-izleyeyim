import os
import sys
import json
import tweepy

API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET = os.getenv("TWITTER_API_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

if not all([API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET]):
    print("HATA: Twitter API anahtarlarından biri veya birkaçı eksik!")
    sys.exit(1)

# X v1.1 Yetkilendirme (Medya yükleme için şarttır)
auth = tweepy.OAuth1UserHandler(
    API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
)
api_v1 = tweepy.API(auth)

# X v2 Yetkilendirme (Tweet metni için)
client_v2 = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)

def get_db():
    p1 = os.path.join("data", "recommendations.json")
    if os.path.exists(p1):
        return p1
    return "recommendations.json"

def main():
    json_path = get_db()
    with open(json_path, "r", encoding="utf-8") as f:
        movies = json.load(f)

    # Sıradaki filmi seç
    movie = None
    for m in movies:
        if not m.get("posted", False):
            movie = m
            break
    if not movie:
        movie = movies[0]

    film_adi = movie.get("title", "")
    imdb = movie.get("imdb", "")
    oyuncular = movie.get("cast", "")
    aciklama = movie.get("overview", "")
    poster_file = movie.get("poster_file", "")
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
    # Yerel afişi yükle
    if poster_file and os.path.exists(poster_file):
        try:
            print(f"Afiş X sunucusuna yükleniyor: {poster_file}")
            media = api_v1.media_upload(filename=poster_file)
            media_ids.append(media.media_id)
            print(f"Afiş yüklendi! Media ID: {media.media_id}")
        except Exception as e:
            print(f"Afiş yükleme hatası: {e}")
            print("Access Token yetkisinin Read & Write olduğunu ve token yenilendiğini kontrol edin.")

    if media_ids:
        res = client_v2.create_tweet(text=tweet_text, media_ids=media_ids)
    else:
        res = client_v2.create_tweet(text=tweet_text)

    print(f"Tweet başarıyla paylaşıldı: {res.data['id']}")

    # Durumu güncelle
    movie["posted"] = True
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(movies, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
