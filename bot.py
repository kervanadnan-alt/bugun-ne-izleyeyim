import os
import sys
import json
import tempfile
import requests
import tweepy

API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET = os.getenv("TWITTER_API_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

if not all([API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET]):
    print("HATA: Twitter API anahtarları eksik!")
    sys.exit(1)

auth = tweepy.OAuth1UserHandler(
    API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
)
api_v1 = tweepy.API(auth)

client_v2 = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)

def load_today_movie():
    json_path = os.path.join("data", "recommendations.json")
    with open(json_path, "r", encoding="utf-8") as f:
        movies = json.load(f)
    for movie in movies:
        if not movie.get("posted", False):
            return movie, movies, json_path
    return movies[0], movies, json_path

def main():
    movie, all_movies, json_path = load_today_movie()
    
    film_adi = movie.get("title", "")
    imdb = movie.get("imdb", "")
    oyuncular = movie.get("cast", "")
    aciklama = movie.get("overview", "")
    poster_file = movie.get("poster_file", "")
    poster_url = movie.get("poster_url", "")
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
    
    if poster_file and os.path.exists(poster_file):
        try:
            print(f"Yerel afiş yükleniyor: {poster_file}")
            media = api_v1.media_upload(filename=poster_file)
            media_ids.append(media.media_id)
            print(f"Afiş yüklendi! ID: {media.media_id}")
        except Exception as e:
            print(f"Afiş yükleme hatası: {e}")
    elif poster_url:
        try:
            print(f"Afiş URL'den indiriliyor: {poster_url}")
            res = requests.get(poster_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
            if res.status_code == 200:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                    tmp.write(res.content)
                    tmp_p = tmp.name
                media = api_v1.media_upload(filename=tmp_p)
                media_ids.append(media.media_id)
                os.remove(tmp_p)
        except Exception as e:
            print(f"Afiş indirme/yükleme hatası: {e}")

    if media_ids:
        res = client_v2.create_tweet(text=tweet_text, media_ids=media_ids)
    else:
        res = client_v2.create_tweet(text=tweet_text)
        
    print(f"Tweet başarıyla paylaşıldı: {res.data['id']}")
    movie["posted"] = True
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(all_movies, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
