document.addEventListener("DOMContentLoaded", async () => {
  try {
    const response = await fetch("data/recommendations.json");
    if (!response.ok) {
      console.error("recommendations.json bulunamadı:", response.status);
      return;
    }
    
    const movies = await response.json();
    const movie = movies.find(m => !m.posted) || movies[0];

    if (!movie) return;

    // Metin alanlarını bağla
    const titleEl = document.getElementById("movieTitle");
    const imdbEl = document.getElementById("movieImdb");
    const overviewEl = document.getElementById("movieOverview");
    const castEl = document.getElementById("movieCast");
    const platformEl = document.getElementById("moviePlatform");
    const posterEl = document.getElementById("moviePoster");

    if (titleEl) titleEl.textContent = `${movie.title} (${movie.year || ''})`;
    if (imdbEl) imdbEl.textContent = `★ ${movie.imdb}`;
    if (overviewEl) overviewEl.textContent = movie.overview;
    if (castEl) castEl.innerHTML = `<strong>Oyuncular:</strong> ${movie.cast}`;
    if (platformEl) platformEl.textContent = movie.platform ? `🍿 ${movie.platform}` : '';

    // AFİŞİ GÖSTEREN KISIM:
    // Deponuzdaki "posters/iskandalo.jpg" dosyasını veya JSON'daki yolu alır
    const posterPath = movie.poster_file || movie.poster_url || "posters/iskandalo.jpg";
    if (posterEl) {
      posterEl.src = posterPath;
    }

    // X Paylaşım Butonu
    const shareBtn = document.getElementById("btnShareX");
    if (shareBtn) {
      shareBtn.onclick = () => {
        const text = `📅 Akşam Matinesi | Saat 19:45\n\n🔴 ${movie.title} (${movie.imdb}/10)\n👥 ${movie.cast}\n📌 ${movie.overview}\n\n${movie.platform ? '🍿 ' + movie.platform + '\n' : ''}#Sinema #FilmÖnerisi #AkşamMatinesi`;
        navigator.clipboard.writeText(text);
        alert("Tweet metni panoya kopyalandı! X açılıyor...");
        window.open(`https://twitter.com/intent/tweet?text=${encodeURIComponent(text)}`, "_blank");
      };
    }
  } catch (err) {
    console.error("Hata:", err);
  }
});
