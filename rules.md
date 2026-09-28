# cards.json kuralları

Bu dosya, `cards.json` dosyasına yeni kelime eklerken uyulacak kuralları anlatır. Kullanıcı bir fotoğraf (ders notu, tahta, kitap sayfası) ve bir tarih verdiğinde, fotoğraftaki Almanca kelimeler bu kurallara göre karta dönüştürülür.

## 0. İki liste: Notizen ve Buch

Kartlar iki listeye ayrılır. Hangi listeye ait olduğu `source` alanında yazar ve uygulamada ayrı sekmelerde görünür.

| Kullanıcının isteği | Fotoğraftan alınan | `source` | Gruplama alanı | Uygulamadaki sekme |
|---|---|---|---|---|
| "**elle yazılmış** kelimeleri ekle" | Sadece el yazısıyla yazılmış kelimeler (ders notları) | `"notes"` | `date` (dersin tarihi) | Notizen |
| "**altı çizili** kelimeleri oku" | Sadece kitapta altı çizili kelimeler | `"book"` | `chapter` (Kapitel numarası) | Buch |

- Fotoğrafta iki tür de varsa **sadece istenen tür** alınır, diğeri yok sayılır.
- Hangi türün istendiği belli değilse (ör. sadece "bu fotoğraftaki kelimeleri ekle") **sor**, tahmin etme.
- **Notizen** kartlarında `date` olur, `chapter` olmaz. **Buch** kartlarında `chapter` olur, `date` olmaz.
- Tekrar kontrolü iki listeye birden bakar: kelime Notizen veya Buch listesinin herhangi birinde varsa tekrar eklenmez (bkz. adım 4).

Uygulama (`index.html`) bu dosyadaki alan adlarını okur. Alan adlarını değiştirmek veya yeni alan eklemek uygulamayı da değiştirmeyi gerektirir.

---

## 1. Süreç

1. **Tarihi veya Kapitel'i netleştir.**
   - Notizen için: kullanıcının verdiği tarih `YYYY-MM-DD` biçiminde yazılır ("bugün" denirse bugünün tarihi).
   - Buch için: kullanıcının verdiği Kapitel numarası (ör. "Kapitel 3" → `3`). Fotoğraftaki sayfada bölüm başlığı görünse bile kullanıcının verdiği numara esas alınır; ikisi çelişirse sor.
   - Verilmemişse sor, tahmin etme.
2. **Fotoğrafı oku.** Almanca kelimeleri ve varsa yanlarındaki notları çıkar.
   - El yazısı okunmuyorsa veya bir kelimeden emin değilsen **tahmin etme**. Kartları yazmadan önce belirsiz kelimeleri kullanıcıya liste hâlinde sor.
   - Belirgin yazım hatalarını düzelt (ör. `Lieferkete` → `Lieferkette`) ve bunu özette belirt.
   - Almanca olmayan satırları (Türkçe notlar, sayfa numaraları vb.) kelime olarak alma. Yanında yazan Türkçe anlam varsa `meaning.tr` için ipucu olarak kullan.
3. **Sözlük biçimine indir** (bkz. bölüm 3). Fotoğrafta çekimli, çoğul veya çekimlenmiş hâlde geçen her kelimenin sözlük biçimini kullan.
4. **Tekrarları kontrol et.** Listede zaten olan bir kelime için yeni kart **eklenmez**. Sözlük biçimine indirilmiş bütün kelimeleri tek komutla kontrol et:
   ```bash
   python3 check_cards.py Rahmen "sich verbrennen" gliedern Wortschatz
   ```
   - Betik her kelime için `VAR` (mevcut kartın `id`, listesi, türü ve tarihiyle) veya `YENİ` yazar. İki listeye birden bakar. Artikel, `sich`, büyük/küçük harf ve umlaut yazımı (`ä`/`ae`) fark etmez.
   - `VAR` olanları ekleme, özette "zaten var (liste, tarih/Kapitel)" olarak belirt; ör. "zaten var (Notizen, 28.09.2026)" veya "zaten var (Buch, Kapitel 2)". Tarihini veya içeriğini değiştirme.
   - Tek istisna: aynı yazılışta ama **farklı türde** bir kelime (ör. mevcut `Essen` isim, yeni gelen `essen` fiil). Bu yeni bir kelimedir, bölüm 4'teki `id` kuralıyla eklenir.
   - Mevcut kartları kullanıcı istemedikçe değiştirme.
5. **Kartları yaz.** Yeni kartları `cards` dizisinin **sonuna**, fotoğraftaki sırayla ekle.
6. **Doğrula** (bkz. bölüm 6) ve kullanıcıya bir özet tablo göster: kelime, tür, artikel, çekimler, varsa belirsizlikler ve atlanan tekrarlar.
7. **Commit ve push** yalnızca kullanıcı isterse yapılır.

---

## 2. Kart yapısı

Alanlar her kartta bu sırayla yazılır (2 boşluk girinti, UTF-8, `\u` kaçışı yok):

```json
{
  "id": "gliedern",
  "source": "notes",
  "date": "2026-09-28",
  "word": "gliedern",
  "type": "verb",
  "article": null,
  "plural": null,
  "reflexive": false,
  "forms": {
    "praesens": "gliedert",
    "praeteritum": "gliederte",
    "perfekt": "hat gegliedert"
  },
  "meaning": {
    "de": "Etwas in Teile oder Abschnitte ordnen und strukturieren",
    "tr": "bölümlere ayırmak, yapılandırmak",
    "en": "to structure, to divide into sections",
    "uk": "поділяти на частини, структурувати",
    "ar": "يقسّم إلى أجزاء، ينظّم",
    "it": "suddividere, strutturare"
  },
  "synonyms": ["strukturieren", "einteilen"],
  "antonyms": ["vermischen"],
  "example": {
    "de": "Bitte gliedern Sie Ihren Text in Einleitung, Hauptteil und Schluss.",
    "tr": "…", "en": "…", "uk": "…", "ar": "…", "it": "…"
  },
  "note": "etwas (Akk.) gliedern"
}
```

| Alan | Tür | Kural |
|---|---|---|
| `id` | string | Benzersiz. Bkz. bölüm 4. |
| `source` | string | `"notes"` (elle yazılmış ders notu) veya `"book"` (kitapta altı çizili). Bkz. bölüm 0. |
| `date` | string | **Sadece Notizen kartlarında.** Dersin tarihi, `YYYY-MM-DD`. Uygulamadaki tarih filtresi buradan oluşur. |
| `chapter` | number | **Sadece Buch kartlarında**, `date` yerine. Kapitel numarası, pozitif tam sayı (`"Kapitel 3"` değil `3`). Uygulamadaki Kapitel filtresi buradan oluşur. |
| `word` | string | Sözlük biçimi, artikelsiz. Bkz. bölüm 3. |
| `type` | string | `noun`, `verb`, `adjective`, `adverb`, `phrase` değerlerinden biri. Bkz. bölüm 3.6. |
| `article` | string \| null | Sadece isimlerde: `der`, `die`, `das`. Diğer türlerde `null`. Kartın rengi buna göre belirlenir. |
| `plural` | string \| null | Sadece isimlerde, **artikelsiz** çoğul (uygulama başına "die" ekler). Çoğulu yoksa veya kullanılmıyorsa `null`. |
| `reflexive` | boolean | Fiil "sich" ile kullanılıyorsa `true`, diğer her durumda `false`. |
| `forms` | object | **Sadece fiillerde** vardır, diğer türlerde alan hiç yazılmaz. Bkz. bölüm 5. |
| `meaning` | object | 6 dilin hepsi zorunlu. Bkz. bölüm 3.7. |
| `synonyms` / `antonyms` | string[] | 0–3 öğe. Yoksa `[]`. İsimler artikelle (`"die Einfassung"`), fiiller mastar hâliyle yazılır. |
| `example` | object | 6 dilin hepsi zorunlu. Bkz. bölüm 3.8. |
| `note` | string \| null | Rektion ve dilbilgisi notları. Fiillerde zorunlu. Bkz. bölüm 5.4. |

Bir **Buch** kartı aynı yapıdadır; tek fark `date` yerine `chapter` alanıdır ve `source` alanından hemen sonra gelir:

```json
{
  "id": "wortschatz",
  "source": "book",
  "chapter": 3,
  "word": "Wortschatz",
  ...
}
```

Dosyanın üst kısmındaki `version` ve `language` alanlarına dokunma.

---

## 3. Kelimeyi sözlük biçimine indirme

### 3.1 Fiiller
- Çekimli hâl → **mastar**: `gliedert`, `gliederte`, `hat gegliedert` → `gliedern`.
- Ayrılabilen fiiller birleşik mastar olarak yazılır: `greift … auf` → `aufgreifen`.
- Dönüşlü fiiller `sich` ile yazılır ve `reflexive: true` olur: `ich habe mich verbrannt` → `sich verbrennen`.
- Sabit bir edatla kullanılan fiilde `word` sadece fiildir, edat `note` alanına yazılır. İstisna: edat olmadan anlamı değişiyorsa edatla yazılabilir (mevcut örnek: `bitten um`).
- Kişisiz fiiller (`es mangelt`) mastar olarak yazılır (`mangeln`), kişisiz kullanım `note` alanında belirtilir.

### 3.2 İsimler
- Tekil, yalın hâl (Nominativ), büyük harfle: `den Gurten` → `Gurt`, `article: "der"`.
- Çoğul `plural` alanına artikelsiz yazılır (`Gurte`). Sayılamayan veya çoğulu kullanılmayan isimlerde `null` (`Hygiene`, `Eisen`).
- Sadece çoğul kullanılan isimlerde (`die Leute`) `word` çoğul hâli, `article: "die"`, `plural: null` olur ve `note` alanına "nur Plural" yazılır.
- n-Deklination (zayıf) isimlerde `note` alanına belirt: `"n-Deklination: den/dem/des Kunden"`.
- Birden fazla artikeli olan isimlerde (`der/das Joghurt`) en yaygın olanı `article` alanına yaz, diğerini `note` alanına ekle.

### 3.3 Sıfatlar
- Çekimsiz temel hâl: `schwerwiegender Fehler` → `schwerwiegend`.
- Karşılaştırma biçimleri temel hâle indirilir: `effizienter` → `effizient`.
- Düzensiz karşılaştırma varsa `note` alanına yaz: `"gut – besser – am besten"`.
- Edatla kullanılan sıfatların edatını ve halini `note` alanına yaz: `"stolz auf + Akk."`.
- Sıfat olarak kullanılan ortaçlar (Partizip) `adjective` olarak alınır ve `note` alanında kaynağı belirtilir: `"Partizip I von „mangeln“"`.

### 3.4 Zarflar
- Olduğu gibi yazılır (`bislang`), `type: "adverb"`.

### 3.5 Kalıplar
- Birden fazla kelimeden oluşan sabit ifadeler (`veranlagt sein`, `in Frage kommen`) `type: "phrase"` olarak yazılır.
- Tam kullanım kalıbı `note` alanına yazılır: `"für etwas (Akk.) veranlagt sein"`.
- Kalıplarda `forms` alanı yazılmaz.

### 3.6 Diğer türler
- Uygulama şu an yalnızca `noun`, `verb`, `adjective`, `adverb`, `phrase` türlerini tanır.
- Edat, bağlaç gibi başka bir tür gerekirse yeni bir `type` değeri uydurma. Kullanıcıya sor, gerekirse `index.html` içindeki `TYPE_LABELS` listesi de güncellenir.

### 3.7 Anlamlar (`meaning`)
- `de`: Basit, B1–B2 seviyesinde, kısa bir Almanca açıklama. Kelimenin kendisini açıklamanın içinde tekrar etme.
- `tr`, `en`, `uk`, `ar`, `it`: Sözlük tarzında kısa karşılıklar. Birden fazla anlam varsa virgülle ayrılır, en yaygın anlam önce yazılır.
  - Fiillerde her dilin mastar biçimi kullanılır: TR "-mek/-mak", EN "to …", IT "-are/-ere/-ire", UK mastar, AR mastar veya geniş zaman.
- Ukraynaca gerçek Ukraynaca olmalı, Rusça değil. Arapça Modern Standart Arapça olmalı.

### 3.8 Örnek cümleler (`example`)
- `de`: Kelimeyi doğal kullanan tek bir cümle. B1–B2 seviyesinde, günlük hayat veya iş bağlamında.
- Fotoğrafta kelimenin geçtiği bir cümle varsa önce onu kullan (gerekirse düzelterek).
- Fiillerde, mümkünse Rektion'u gösteren bir cümle seç (`Ich bitte dich um Hilfe.`).
- Diğer 5 dil, Almanca cümlenin doğal ve sadık çevirisidir.

---

## 4. `id` kuralları
- Tamamen küçük harf, `word` alanından türetilir.
- `ä → ae`, `ö → oe`, `ü → ue`, `ß → ss`.
- Boşluklar `-` olur: `sich verbrennen` → `sich-verbrennen`.
- Harf, rakam ve `-` dışındaki karakterler atılır.
- Aynı yazılışa sahip farklı bir kart zaten varsa (ör. `Essen` isim ve `essen` fiil), yeni karta türünü ek olarak ver: `essen-verb`.
- Mevcut kartların `id` değerleri asla değiştirilmez. Kaydedilen kartlar ve son bakılan kart bu değerle hatırlanır.

---

## 5. Fiillere özel kurallar

### 5.1 `forms` alanı
Her fiil kartında zorunludur:

| Anahtar | İçerik | Örnek |
|---|---|---|
| `praesens` | Präsens, 3. tekil şahıs (er/sie/es) | `gliedert` |
| `praeteritum` | Präteritum, 3. tekil şahıs | `gliederte` |
| `perfekt` | Yardımcı fiil (`hat`/`ist`) + Partizip II | `hat gegliedert` |

### 5.2 Özel durumlar
- **Ayrılabilen fiiller:** `greift auf` · `griff auf` · `hat aufgegriffen`
- **Dönüşlü fiiller:** `verbrennt sich` · `verbrannte sich` · `hat sich verbrannt`
- **`sein` ile Perfekt** (yer değiştirme, durum değişikliği, `bleiben`, `sein`, `werden`): `stirbt aus` · `starb aus` · `ist ausgestorben`
- **Kişisiz fiiller:** `es mangelt` · `es mangelte` · `es hat gemangelt`
- **Edatlı fiiller:** Edat çekimlere de eklenir: `bittet um` · `bat um` · `hat um … gebeten`
- **İki biçimi olan fiiller** (`verwendete` / `verwandte`): En yaygın olanı `forms` alanına, diğerini `note` alanına yaz.
- **Hem `haben` hem `sein` alan fiiller** (ör. `fahren`): `perfekt` alanına en yaygın kullanımı yaz, diğerini ve farkını `note` alanında açıkla.

### 5.3 Düzensiz fiiller
- Güçlü veya karışık çekimli fiillerde `forms` zaten düzensizliği gösterir. Ayrıca `note` alanına "unregelmäßig" yazmak isteğe bağlıdır.
- Präsens'te ünlü değişimi varsa (`sterben → stirbt`) bu `praesens` alanında görünür, ek not gerekmez.

### 5.4 Rektion (Dativ / Akkusativ) — `note` alanı
Her fiil kartında `note` alanı **fiilin Rektion'u ile başlar**. Rektion `jemand` / `etwas` ve parantez içinde hal kısaltmasıyla yazılır:

| Durum | `note` örneği |
|---|---|
| Akkusativ nesne | `etwas (Akk.) vertiefen` |
| Dativ nesne | `jemandem (Dat.) helfen` |
| Dativ + Akkusativ | `jemandem (Dat.) etwas (Akk.) geben` |
| Edatlı nesne | `jemanden (Akk.) um etwas (Akk.) bitten` |
| Kişisiz + edat | `es mangelt jemandem (Dat.) an etwas (Dat.)` |
| Dönüşlü | `sich (Akk.) an etwas (Dat.) verbrennen` |
| Nesnesiz | `intransitiv (ohne Objekt)` |

- Yaygın bir Genitiv kullanımı varsa o da yazılır: `jemandes (Gen.) gedenken`.
- Başka notlar Rektion'dan sonra `; ` ile eklenir: `"etwas (Akk.) verwenden; Präteritum auch: verwandte"`.
- Rektion'u sadece fiillerde değil, edatla kullanılan isim, sıfat ve kalıplarda da `note` alanına yaz.

---

## 6. Doğrulama

Kartları ekledikten sonra şunu çalıştır ve çıktının `Hata yok` olduğundan emin ol:

```bash
python3 check_cards.py --validate
```

Betik şunları kontrol eder: geçerli JSON, benzersiz ve kurala uygun `id`, `source` değeri, Notizen kartlarında `date` biçimi, Buch kartlarında `chapter` (ve karşı alanın olmaması), `type` değeri, isimlerde `article`, 6 dilin hepsinde `meaning` ve `example`, fiillerde `forms` ve Rektion (`note`), `reflexive` ile `word` uyumu ve aynı kelimenin iki kez eklenmemesi.

Ek olarak `git diff` ile yalnızca yeni kartların eklendiğini, mevcut kartların değişmediğini kontrol et.
