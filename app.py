from flask import Flask, render_template, redirect, url_for, request, send_from_directory
import requests
import datetime

app = Flask(__name__)

# Daily Routine & Complete Azkar with Arabic Text & Urdu Meaning
DAILY_ROUTINE = {
    "Sunday": {
        "day_ur": "اتوار (Sunday)",
        "surah_name": "سورۃ الملک (رات کو) اور آیت الکرسی",
        "zikr_title": "یَا حَیُّ یَا قَیُّومُ (100 مرتبہ)",
        "zikr_arabic": "يَا حَيُّ يَا قَيُّومُ بِرَحْمَتِكَ أَسْتَغِيثُ",
        "zikr_urdu": "اے زندہ اور قائم رہنے والے! میں تیری ہی رحمت کے ذریعے فریاد کرتا ہوں۔",
        "fazeelat": "ہر نماز کے بعد آیت الکرسی پڑھنے کی عادت بنائیں۔"
    },
    "Monday": {
        "day_ur": "پیر (Monday)",
        "surah_name": "سورۃ الواقعہ اور سورۃ الملک",
        "zikr_title": "دُرود شریف (100 مرتبہ)",
        "zikr_arabic": "اللَّهُمَّ صَلِّ عَلَى مُحَمَّدٍ وَعَلَى آلِ مُحَمَّدٍ",
        "zikr_urdu": "اے اللہ! محمد ﷺ اور ان کی آل پر رحمت نازل فرما۔",
        "fazeelat": "پیر کا دن سنت روزے اور کثرتِ درود کا دن ہے۔"
    },
    "Tuesday": {
        "day_ur": "منگل (Tuesday)",
        "surah_name": "سورۃ الملک اور سورۃ یٰس",
        "zikr_title": "استغفار (100 مرتبہ)",
        "zikr_arabic": "أَسْتَغْفِرُ اللَّهَ رَبِّي مِنْ كُلِّ ذَنْبٍ وَأَتُوبُ إِلَيْهِ",
        "zikr_urdu": "میں اللہ سے اپنے تمام گناہوں کی معافی مانگتا ہوں جو میرا رب ہے اور اسی کی طرف رجوع کرتا ہوں۔",
        "fazeelat": "استغفار سے رزق میں برکت اور دل کو سکون ملتا ہے۔"
    },
    "Wednesday": {
        "day_ur": "بدھ (Wednesday)",
        "surah_name": "سورۃ الملک اور آخری چار قل",
        "zikr_title": "تیسرا کلمہ (100 مرتبہ)",
        "zikr_arabic": "سُبْحَانَ اللَّهِ وَالْحَمْدُ لِلَّهِ وَلَا إِلَهَ إِلَّا اللَّهُ وَاللَّهُ أَكْبَرُ",
        "zikr_urdu": "اللہ پاک ہے، تمام تعریفیں اللہ کے لیے ہیں، اللہ کے سوا کوئی معبود نہیں اور اللہ سب سے بڑا ہے۔",
        "fazeelat": "یہ کلمات جنت کے پودے ہیں۔"
    },
    "Thursday": {
        "day_ur": "جمعرات (Thursday)",
        "surah_name": "سورۃ الملک اور سورۃ الدخان",
        "zikr_title": "سبحان اللہ و بحمدہ (100 مرتبہ)",
        "zikr_arabic": "سُبْحَانَ اللَّهِ وَبِحَمْدِهِ ، سُبْحَانَ اللَّهِ الْعَظِيمِ",
        "zikr_urdu": "اللہ اپنی خوبیوں سمیت پاک ہے، عظمت والا اللہ پاک ہے۔",
        "fazeelat": "زبان پر ہلکے اور ترازو میں بہت بھاری کلمات۔"
    },
    "Friday": {
        "day_ur": "جمعہ (Friday)",
        "surah_name": "سورۃ الکہف اور سورۃ الملک",
        "zikr_title": "کثرتِ درودِ ابراہیمی (300+ مرتبہ)",
        "zikr_arabic": "اللَّهُمَّ صَلِّ عَلَى مُحَمَّدٍ وَعَلَى آلِ مُحَمَّدٍ كَمَا صَلَّيْتَ عَلَى إِبْرَاهِيمَ وَعَلَى آلِ إِبْرَاهِيمَ إِنَّكَ حَمِيدٌ مَجِيدٌ",
        "zikr_urdu": "جمعہ کے دن درود شریف کثرت سے پڑھیں، یہ بارگاہِ رسالت ﷺ میں پیش کیا جاتا ہے۔",
        "fazeelat": "جمعہ کے دن سورۃ الکہف پڑھنے والے کے لیے اگلے جمعہ تک نور روشن رہتا ہے۔"
    },
    "Saturday": {
        "day_ur": "ہفتہ (Saturday)",
        "surah_name": "سورۃ الملک اور سورۃ الفاتحہ تدبر کے ساتھ",
        "zikr_title": "لا حول ولا قوة إلا بالله (100 مرتبہ)",
        "zikr_arabic": "لَا حَوْلَ وَلَا قُوَّةَ إِلَّا بِاللَّهِ الْعَلِيِّ الْعَظِيمِ",
        "zikr_urdu": "گناہوں سے بچنے کی طاقت اور نیکی کرنے کی قوت صرف بلند و برتر اللہ کی طرف سے ہے۔",
        "fazeelat": "یہ کلمہ عرش کے نیچے کے خزانوں میں سے ایک خزانہ ہے۔"
    }
}

# Surah list cache
SURAH_LIST = []
try:
    res = requests.get("https://api.alquran.cloud/v1/surah", timeout=10).json()
    SURAH_LIST = res['data']
except Exception as e:
    print("Surah list fetch error:", e)

# Popular Authentic Reciters
RECITERS = [
    {"id": "ar.alafasy", "name": "Mishary Rashid Alafasy"},
    {"id": "ar.abdulbasitmurattal", "name": "Abdul Basit (Murattal)"},
    {"id": "ar.abdurrahmaansudais", "name": "Abdur-Rahman As-Sudais"},
    {"id": "ar.husary", "name": "Mahmoud Khalil Al-Husary"},
    {"id": "ar.minshawi", "name": "Mohamed Siddiq Al-Minshawi"}
]

# Famous Global Translations for Quran
QURAN_TRANSLATIONS = [
    {"id": "ur.jalandhry", "name": "اردو - فتح محمد جالندھری", "lang": "ur", "dir": "rtl"},
    {"id": "ur.kanzuliman", "name": "اردو - احمد رضا خان (کنز الایمان)", "lang": "ur", "dir": "rtl"},
    {"id": "ur.maududi", "name": "اردو - ابوالاعلیٰ مودودی", "lang": "ur", "dir": "rtl"},
    {"id": "ur.junagarhi", "name": "اردو - محمد جوناگڑھی", "lang": "ur", "dir": "rtl"},
    {"id": "ur.qadri", "name": "اردو - طاہر القادری", "lang": "ur", "dir": "rtl"},
    {"id": "en.sahih", "name": "English - Saheeh International", "lang": "en", "dir": "ltr"},
    {"id": "hi.hindi", "name": "हिन्दी (Hindi) - फ़ारूक़ ख़ान", "lang": "hi", "dir": "ltr"},
    {"id": "bn.bengali", "name": "বাংলা (Bengali) - মুহিউদ্দীন خان", "lang": "bn", "dir": "ltr"},
    {"id": "sd.amroti", "name": "سنڌي (Sindhi) - امروٽي", "lang": "sd", "dir": "rtl"},
    {"id": "ps.abdulwali", "name": "پښتو (Pashto) - عبد الولي", "lang": "ps", "dir": "rtl"},
    {"id": "fa.ansarian", "name": "فارسی (Persian) - انصاریان", "lang": "fa", "dir": "rtl"},
    {"id": "tr.diyanet", "name": "Türkçe (Turkish) - Diyanet", "lang": "tr", "dir": "ltr"},
    {"id": "id.indonesian", "name": "Bahasa Indonesia", "lang": "id", "dir": "ltr"},
    {"id": "fr.hamidullah", "name": "Français (French) - Hamidullah", "lang": "fr", "dir": "ltr"},
    {"id": "es.cortes", "name": "Español (Spanish) - Cortes", "lang": "es", "dir": "ltr"},
    {"id": "de.aburida", "name": "Deutsch (German) - Abu Rida", "lang": "de", "dir": "ltr"},
    {"id": "ru.kuliev", "name": "Русский (Russian) - Кулиев", "lang": "ru", "dir": "ltr"},
    {"id": "zh.jian", "name": "中文 (Chinese) - Ma Jian", "lang": "zh", "dir": "ltr"}
]

# Authentic Hadith Books List
HADITH_BOOKS = [
    {"id": "bukhari", "name": "صحیح بخاری (Sahih Bukhari)", "total": 7563},
    {"id": "muslim", "name": "صحیح مسلم (Sahih Muslim)", "total": 7500},
    {"id": "abudawud", "name": "سنن ابی داؤد (Sunan Abi Dawud)", "total": 5274},
    {"id": "tirmidhi", "name": "جامع ترمذی (Jami at-Tirmidhi)", "total": 3956},
    {"id": "nasai", "name": "سنن نسائی (Sunan an-Nasa'i)", "total": 5758},
    {"id": "ibnmajah", "name": "سنن ابن ماجہ (Sunan Ibn Majah)", "total": 4341}
]

# Hadith Languages
HADITH_LANGUAGES = [
    {"code": "urd", "name": "اردو (Urdu)", "dir": "rtl"},
    {"code": "eng", "name": "English", "dir": "ltr"},
    {"code": "ben", "name": "বাংলা (Bengali)", "dir": "ltr"},
    {"code": "ind", "name": "Bahasa Indonesia", "dir": "ltr"},
    {"code": "tur", "name": "Türkçe (Turkish)", "dir": "ltr"},
    {"code": "fra", "name": "Français (French)", "dir": "ltr"},
    {"code": "rus", "name": "Русский (Russian)", "dir": "ltr"}
]

BISMILLAH_PREFIX = "بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ"

@app.route('/')
def home():
    current_day = datetime.datetime.now().strftime("%A")
    today_routine = DAILY_ROUTINE.get(current_day, DAILY_ROUTINE["Sunday"])
    return render_template('home.html', today_routine=today_routine, current_day=current_day)

@app.route('/more')
def more_features():
    return render_template('more.html')

@app.route('/supplications')
def supplications():
    return render_template('supplications.html')

@app.route('/tasbeeh')
def tasbeeh():
    return render_template('tasbeeh.html')

@app.route('/shahadat')
def shahadat():
    return render_template('shahadat.html')

@app.route('/rules-of-stopping')
def rules_of_stopping():
    return render_template('rules_of_stopping.html')

@app.route('/pronunciation')
def pronunciation():
    return render_template('pronunciation.html')

@app.route('/salah-tracker')
def salah_tracker():
    return render_template('salah_tracker.html')

@app.route('/flashes')
def flashes():
    return render_template('flashes.html')

@app.route('/prayer-times')
def prayer_times():
    return render_template('prayer_times.html')

@app.route('/share-greetings')
def share_greetings():
    return render_template('share_greetings.html')

@app.route('/qaida')
def qaida_urdu():
    return render_template('qaida.html')

@app.route('/qaida-english')
def qaida_en():
    return render_template('qaida_english.html')

@app.route('/allah-names')
def allah_names():
    return render_template('allah_names.html')

@app.route('/qibla')
def qibla_dir():
    return render_template('qibla.html')

@app.route('/ibadaat')
def ibadaat():
    return render_template('ibadaat.html')

@app.route('/surah/<int:surah_id>')
def view_surah(surah_id):
    if surah_id < 1 or surah_id > 114:
        surah_id = 1

    reciter_id = request.args.get('reciter', 'ar.alafasy')
    valid_reciters = [r['id'] for r in RECITERS]
    if reciter_id not in valid_reciters:
        reciter_id = 'ar.alafasy'

    translation_id = request.args.get('translation', 'ur.jalandhry')
    selected_trans = next((t for t in QURAN_TRANSLATIONS if t['id'] == translation_id), QURAN_TRANSLATIONS[0])

    url = f"https://api.alquran.cloud/v1/surah/{surah_id}/editions/quran-uthmani,{selected_trans['id']},{reciter_id}"
    response = requests.get(url, timeout=15).json()
    
    surah_info = response['data'][0]
    arabic_ayahs = response['data'][0]['ayahs']
    trans_ayahs = response['data'][1]['ayahs']
    audio_ayahs = response['data'][2]['ayahs']
    
    surah_data = []
    for ar, tr, au in zip(arabic_ayahs, trans_ayahs, audio_ayahs):
        arabic_text = ar['text']
        if surah_id != 1 and ar['numberInSurah'] == 1:
            if arabic_text.startswith(BISMILLAH_PREFIX):
                arabic_text = arabic_text[len(BISMILLAH_PREFIX):].strip()

        surah_data.append({
            "number": ar['numberInSurah'],
            "arabic": arabic_text,
            "translation": tr['text'],
            "audio": au['audio']
        })
        
    return render_template(
        'index.html', 
        surah_data=surah_data, 
        surah_info=surah_info, 
        all_surahs=SURAH_LIST, 
        current_surah=surah_id,
        reciters=RECITERS,
        current_reciter=reciter_id,
        translations=QURAN_TRANSLATIONS,
        current_translation=selected_trans
    )

# Dedicated Favorites Section Route
@app.route('/favorites')
def favorites():
    return render_template('favorites.html')

# Hadith Section Route
@app.route('/hadith')
@app.route('/hadith/<book_id>')
def view_hadith(book_id=None):
    if not book_id:
        return render_template('hadith.html', show_books=True, books=HADITH_BOOKS)
    page = request.args.get('page', 1, type=int)
    lang_code = request.args.get('lang', 'urd')
    limit = 20
    start_num = (page - 1) * limit + 1
    end_num = start_num + limit

    valid_book_ids = [b['id'] for b in HADITH_BOOKS]
    if book_id not in valid_book_ids:
        book_id = 'bukhari'

    valid_langs = [l['code'] for l in HADITH_LANGUAGES]
    if lang_code not in valid_langs:
        lang_code = 'urd'

    current_book = next(b for b in HADITH_BOOKS if b['id'] == book_id)
    current_lang = next(l for l in HADITH_LANGUAGES if l['code'] == lang_code)
    
    hadiths = []
    try:
        url_trans = f"https://cdn.jsdelivr.net/gh/fawazahmed0/hadith-api@1/editions/{lang_code}-{book_id}.json"
        res_trans = requests.get(url_trans, timeout=12).json()
        raw_list_trans = res_trans.get('hadiths', [])[start_num - 1 : end_num - 1]
        
        url_ar = f"https://cdn.jsdelivr.net/gh/fawazahmed0/hadith-api@1/editions/ara-{book_id}.json"
        res_ar = requests.get(url_ar, timeout=12).json()
        raw_list_ar = res_ar.get('hadiths', [])[start_num - 1 : end_num - 1]

        for idx, (tr, ar) in enumerate(zip(raw_list_trans, raw_list_ar)):
            grades = ar.get('grades', [])
            status = "صحیح (Sahih)" if book_id in ['bukhari', 'muslim'] else "موثق / حسن"
            if grades and len(grades) > 0:
                grade_name = grades[0].get('grade', '')
                if grade_name:
                    status = grade_name

            hadiths.append({
                "intl_number": ar.get('hadithnumber', start_num + idx),
                "arabic": ar.get('text', ''),
                "translation": tr.get('text', ''),
                "status": status
            })
    except Exception as e:
        print("Hadith fetch error:", e)

    return render_template(
        'hadith.html',
        books=HADITH_BOOKS,
        current_book=current_book,
        languages=HADITH_LANGUAGES,
        current_lang=current_lang,
        hadiths=hadiths,
        page=page,
        show_books=False
    )

# PWA Routes
@app.route('/manifest.json')
def manifest():
    return send_from_directory('static', 'manifest.json')

@app.route('/sw.js')
def service_worker():
    return send_from_directory('static', 'sw.js')

TILAWAT_RECITERS = {
    "afs": {"name": "Mishary Rashid Alafasy", "server": "https://server8.mp3quran.net/afs"},
    "basit": {"name": "Abdul Basit Abdul Samad", "server": "https://server7.mp3quran.net/basit"},
    "sudais": {"name": "Abdur-Rahman As-Sudais", "server": "https://server11.mp3quran.net/sds"},
    "shur": {"name": "Saud Ash-Shuraim", "server": "https://server7.mp3quran.net/shur"},
    "ghamdi": {"name": "Saad Al-Ghamdi", "server": "https://server7.mp3quran.net/s_gmd"},
    "husary": {"name": "Mahmoud Khalil Al-Husary", "server": "https://server13.mp3quran.net/husr"},
    "minsh": {"name": "Mohamed Siddiq Al-Minshawi", "server": "https://server10.mp3quran.net/minsh"}
}

@app.route('/tilawat')
@app.route('/tilawat/<int:surah_id>')
def tilawat(surah_id=1):
    reciter_key = request.args.get('reciter', 'afs')
    if reciter_key not in TILAWAT_RECITERS:
        reciter_key = 'afs'

    formatted_surah = f"{surah_id:03d}"
    server_base = TILAWAT_RECITERS[reciter_key]["server"]
    audio_url = f"{server_base}/{formatted_surah}.mp3"

    return render_template('tilawat.html', surah_id=surah_id, audio_url=audio_url, reciters=TILAWAT_RECITERS, current_reciter=reciter_key)

if __name__ == '__main__':
    app.run(debug=True)
