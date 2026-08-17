/**
 * Official Indian Numbering System Currency Formatter
 * Examples: 150000 -> ₹1,50,000 | 500000 -> ₹5,00,000 | 1500000 -> ₹15,00,000
 */
export function formatINR(val) {
  if (val === null || val === undefined || isNaN(val)) return '₹0';
  const num = Math.round(Number(val));
  const str = num.toString();

  if (str.length <= 3) return '₹' + str;

  const lastThree = str.substring(str.length - 3);
  const otherDigits = str.substring(0, str.length - 3);
  const formattedOthers = otherDigits.replace(/\B(?=(\d{2})+(?!\d))/g, ',');

  return `₹${formattedOthers},${lastThree}`;
}

export const INDIAN_22_LANGUAGES = [
  'English',
  'Assamese (অসমীয়া)',
  'Bengali (বাংলা)',
  'Bodo (बर\')',
  'Dogri (डोगरी)',
  'Gujarati (ગુજરાતી)',
  'Hindi (हिंदी)',
  'Kannada (ಕನ್ನಡ)',
  'Kashmiri (कॉशुर)',
  'Konkani (कोंकणी)',
  'Maithili (मैथिली)',
  'Malayalam (മലയാളം)',
  'Manipuri (মৈতৈলোন্)',
  'Marathi (मराठी)',
  'Nepali (नेपाली)',
  'Odia (ଓଡ଼ିଆ)',
  'Punjabi (ਪੰਜਾਬੀ)',
  'Sanskrit (संस्कृतम्)',
  'Santali (ᱥᱟᱱᱛᱟᱲᱤ)',
  'Sindhi (सिंधी)',
  'Tamil (தமிழ்)',
  'Telugu (తెలుగు)',
  'Urdu (اردو)'
];

const baseEn = {
  emergency: "EMERGENCY NOTICE: If you or a family member are experiencing a medical emergency, call 112 / 108 immediately or go directly to the nearest Casualty ER. Do not delay medical care for policy verification.",
  site_lang: "App & Site Interface Language",
  tab1: "Upload & Extract",
  tab2: "Ask Your Policy",
  tab3: "Find Hospital Options",
  tab4: "Care Journey & Safety",
  upload_header: "Upload Policy Document",
  upload_sub: "Upload your Base Health Insurance Policy (PDF)",
  load_demo_base: "Load Demo Base Policy",
  topup_expander: "Dual-Policy & Super Top-Up Comparison Engine",
  topup_desc: "Upload or load a secondary Super Top-Up policy to calculate combined sum insured and deductible triggers.",
  upload_topup_label: "Upload Secondary / Super Top-Up Policy (PDF)",
  load_demo_topup: "Load Demo Super Top-Up Policy",
  topup_deductible_label: "Top-Up Deductible Threshold (INR)",
  dual_breakdown: "Dual-Policy Protection Breakdown:",
  primary_cover: "Primary Policy Cover",
  topup_cover: "Top-Up Policy Cover",
  combined_si: "Combined Sum Insured",
  extracted_summary: "Extracted Policy Summary",
  base_coverage: "Base Policy Coverage",
  secondary_topup_coverage: "Secondary Super Top-Up Coverage",
  insurer_name: "Insurer Name",
  policy_name: "Policy Name",
  sum_insured: "Sum Insured",
  room_eligibility: "Room Eligibility",
  copay_terms: "Co-Pay Terms",
  preauth_req: "Pre-Auth Required",
  dl_pdf_summary: "Download Extracted Policy Summary (PDF)",
  dl_pdf_preauth: "Download Pre-Authorization TPA Form (PDF)",
  ask_header: "Ask Questions About Your Coverage",
  hosp_header: "Hospital Network & Room Matching",
  journey_header: "Care Journey, Claim Estimator & Safety Guidelines"
};

export const TRANSLATIONS = {
  English: baseEn,
  "Assamese (অসমীয়া)": {
    ...baseEn,
    emergency: "জৰুৰী জাননী: যদি আপোনাৰ কিবা চিকিৎসা জৰুৰী অৱস্থা হয়, তেন্তে ১০৮ / ১১২ নম্বৰত কল কৰক।",
    tab1: "আপলোড আৰু নিষ্কাশন",
    tab2: "নীতি প্ৰশ্ন কৰক",
    tab3: "হস্পিটাল বিকল্প বিচাৰক",
    tab4: "সুৰক্ষা যাত্ৰা",
    upload_header: "নীতি নথিপত্ৰ আপলোড কৰক",
    upload_sub: "আপোনাৰ স্বাস্থ্য বীমা নীতি (PDF) আপলোড কৰক",
    primary_cover: "প্ৰাথমিক কভাৰ",
    topup_cover: "টপ-আপ কভাৰ",
    combined_si: "একত্ৰিত বীমা ৰাশি"
  },
  "Bengali (বাংলা)": {
    ...baseEn,
    emergency: "জরুরী নোটিশ: কোনো চিকিৎসা জরুরী পরিস্থিতি হলে অবিলম্বে ১১২ / ১০৮ নম্বরে কল করুন।",
    tab1: "আপলোড ও তথ্য সংগ্রহ",
    tab2: "আপনার পলিসি প্রশ্ন করুন",
    tab3: "হাসপাতাল অপশন খুঁজুন",
    tab4: "কেয়ার যাত্রা ও নিরাপত্তা",
    upload_header: "পলিসি নথি আপলোড করুন",
    upload_sub: "আপনার মূল স্বাস্থ্য বীমা পলিসি (PDF) আপলোড করুন",
    primary_cover: "প্রাথমিক পলিসি কভার",
    topup_cover: "টপ-আপ পলিসি কভার",
    combined_si: "মোট একত্রিত বীমা রাশি"
  },
  "Bodo (बर')": {
    ...baseEn,
    emergency: "गाहाइ खौरां: साबसिन देहायारि खाबुनि थाखाय ११२ / १०८ आव कल खालाम।",
    tab1: "अपलोड आरो लिसन",
    tab2: "नेम सोंथि",
    tab3: "देहायारि फालि नागिर",
    tab4: "रैखाथि दावबायनाय",
    upload_header: "नेम फाइलबो अपलोड खालाम"
  },
  "Dogri (डोगरी)": {
    ...baseEn,
    emergency: "आपातकालीन सूचना: डाक्टरी आणीबाणी होने पर तुरंत 112 / 108 पर काल करो।",
    tab1: "अपलोड ते निकाल",
    tab2: "अपनी पालिसी पुच्छो",
    tab3: "अस्पताल लब्भो",
    tab4: "सुरक्षा यात्रा"
  },
  "Gujarati (ગુજરાતી)": {
    ...baseEn,
    emergency: "ઇમરજન્સી નોટિસ: જો તબીબી કટોકટી હોય તો તરત જ 112 / 108 પર કોલ કરો.",
    tab1: "અપલોડ અને નિષ્કર્ષણ",
    tab2: "તમારી પોલિસી પૂછો",
    tab3: "હોસ્પિટલ વિકલ્પો શોધો",
    tab4: "સુરક્ષા યાત્રા",
    upload_header: "પોલિસી દસ્તાવેજ અપલોડ કરો"
  },
  "Hindi (हिंदी)": {
    ...baseEn,
    emergency: "आपातकालीन सूचना: यदि आपको या आपके परिवार को चिकित्सा आपात स्थिति है, तो तुरंत 112 / 108 पर कॉल करें।",
    tab1: "अपलोड और निष्कर्षण",
    tab2: "अपनी नीति से पूछें",
    tab3: "अस्पताल के विकल्प खोजें",
    tab4: "देखभाल यात्रा और सुरक्षा",
    upload_header: "नीति दस्तावेज़ अपलोड करें",
    upload_sub: "अपनी मूल स्वास्थ्य बीमा नीति (PDF) अपलोड करें",
    topup_expander: "दोहरी-नीति और सुपर टॉप-अप तुलना इंजन",
    primary_cover: "प्राथमिक नीति कवर",
    topup_cover: "टॉप-अप नीति कवर",
    combined_si: "कुल संयुक्त बीमा राशि",
    extracted_summary: "निकालना नीति सारांश"
  },
  "Kannada (ಕನ್ನಡ)": {
    ...baseEn,
    emergency: "ತುರ್ತು ಸೂಚನೆ: ವೈದ್ಯಕೀಯ ತುರ್ತು పరిస్థಿತಿ असल्यास ತಕ್ಷಣ 112 / 108 ಗೆ ಕರೆ ಮಾಡಿ.",
    tab1: "ಅಪ್‌ಲೋಡ್ & ಸಾರಾಂಶ",
    tab2: "ನಿಮ್ಮ ಪಾಲಿಸಿ ಕೇಳಿ",
    tab3: "ಆಸ್ಪತ್ರೆ ಆಯ್ಕೆ ಹುಡುಕಿ",
    tab4: "ಸುರಕ್ಷತಾ ಪ್ರಯಾಣ",
    upload_header: "ಪಾಲಿಸಿ ದಾಖಲೆ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ"
  },
  "Kashmiri (कॉशुर)": {
    ...baseEn,
    emergency: "ہنگامی نوٹس: اگر توہی یا تہندِس خاندانَس منز کاہ طِبی ہنگامی صوُرتحال چھِ، تِلہِ کٔرِو دٔستی 112 / 108 پؠٹھ کال۔",
    tab1: "اپلوڈ تہِ نِکاس",
    tab2: "پَننِہ پالیسی مَنز پُچھِو",
    tab3: "ہسپتال انتخاب چھانٹو",
    tab4: "دیکھ بال سَفَر تہِ حِفاظت",
    upload_header: "پالیسی دستاویز اپلوڈ کٔرِو",
    upload_sub: "پَنُن ہیلتھ انشورنس پالیسی پی ڈی ایف اپلوڈ کٔرِو",
    primary_cover: "بُنیادی پالیسی کور",
    topup_cover: "ٹاپ اپ پالیسی کور",
    combined_si: "کُل مِلاوِتھ بیمہ رقم"
  },
  "Konkani (कोंकणी)": {
    ...baseEn,
    emergency: "तातडीची सुचना: भलायकेची आणीबाणी आसल्यार रोखडेंच 112 / 108 हाचेर कॉल करात.",
    tab1: "अपलोड आनी निश्कर्श",
    tab2: "तुमची पॉलिसी विचारात",
    tab3: "हॉस्पिटल सोदात",
    tab4: "सुरक्षा प्रवास"
  },
  "Maithili (मैथिली)": {
    ...baseEn,
    emergency: "आपातकालीन सूचना: डाक्टरी आपात स्थिति मे तुरंत 112 / 108 पर कॉल करू।",
    tab1: "अपलोड आ निष्कर्षण",
    tab2: "पॉलिसी सँ पूछू",
    tab3: "अस्पताल खोजू",
    tab4: "सुरक्षा यात्रा"
  },
  "Malayalam (മലയാളം)": {
    ...baseEn,
    emergency: "അടിയന്തര അറിയിപ്പ്: വൈദ്യസഹായത്തിനായി ഉടനടി 112 / 108 എന്ന നമ്പറിൽ വിളിക്കുക.",
    tab1: "അപ്‌ലോഡ് ചെയ്യുക",
    tab2: "പോളിസി ചോദിക്കുക",
    tab3: "ആശുപത്രികൾ കണ്ടെത്തുക",
    tab4: "സുരക്ഷാ യാത്ര",
    upload_header: "പോളിസി രേഖ അപ്‌ലോഡ് ചെയ്യുക"
  },
  "Manipuri (মৈতৈলোন্)": {
    ...baseEn,
    emergency: "ইমার্জেন্সী নোটিশ: অনাবাগী অৱাবা লৈরবদি ১৮০ / ১১২ দা তৌবিয়ু।",
    tab1: "অপলোড তৌবা",
    tab2: "পোলিসিগী ৱাহং",
    tab3: "হোস্পিটাল থিবা",
    tab4: "ঙাক-শেন খোঙচৎ"
  },
  "Marathi (मराठी)": {
    ...baseEn,
    emergency: "तातडीची सूचना: वैद्यकीय आणीबाणी असल्यास त्वरित ११२ / १०८ वर कॉल करा.",
    tab1: "अपलोड आणि निष्कर्ष",
    tab2: "तुमच्या पॉलिसीबद्दल विचारा",
    tab3: "रुग्णालय पर्याय शोधा",
    tab4: "काळजी प्रवास आणि सुरक्षितता",
    upload_header: "पॉलिसी दस्तऐवज अपलोड करा"
  },
  "Nepali (नेपाली)": {
    ...baseEn,
    emergency: "आपतकालीन सूचना: स्वास्थ्य आपतकाल परेमा तुरुन्त ११२ / १०८ मा कल गर्नुहोस्।",
    tab1: "अपलोड र निष्कर्ष",
    tab2: "पॉलिसीबारे सोध्नुहोस्",
    tab3: "अस्पताल खोज्नुहोस्",
    tab4: "सुरक्षा यात्रा"
  },
  "Odia (ଓଡ଼ିଆ)": {
    ...baseEn,
    emergency: "ଜରୁରୀ ସୂଚନା: ଡାକ୍ତରୀ ଜରୁରୀ ପରିସ୍ଥିତିରେ ୧୧୨ / ୧୦୮ କୁ କଲ କରନ୍ତୁ।",
    tab1: "ଅପଲୋଡ୍ ଏବଂ ନିଷ୍କର୍ଷ",
    tab2: "ନୀତି ପଚାରନ୍ତୁ",
    tab3: "ଡାକ୍ତରଖାନା ଖୋଜନ୍ତୁ",
    tab4: "ସୁରକ୍ଷା ଯାତ୍ରା"
  },
  "Punjabi (ਪੰਜਾਬੀ)": {
    ...baseEn,
    emergency: "ਐਮਰਜੈਂਸੀ ਨੋਟਿਸ: ਡਾਕਟਰੀ ਐਮਰਜੈਂਸੀ ਵਿੱਚ ਤੁਰੰਤ 112 / 108 'ਤੇ ਕਾਲ ਕਰੋ।",
    tab1: "ਅੱਪਲੋਡ ਅਤੇ ਨਿਸ਼ਕਰਸ਼",
    tab2: "ਆਪਣੀ ਪਾਲਿਸੀ ਪੁੱਛੋ",
    tab3: "ਹਸਪਤਾਲ ਲੱਭੋ",
    tab4: "ਸੁਰੱਖਿਆ ਯਾਤਰਾ"
  },
  "Sanskrit (संस्कृतम्)": {
    ...baseEn,
    emergency: "आपत्कालीनसूचना: आपत्काले सद्यः ११२ / १०८ दूरभाषं कुर्वन्तु।",
    tab1: "आरोपणं निष्कर्षणञ्च",
    tab2: "नीतिं पृच्छतु",
    tab3: "चिकित्सालयं चिनोतु",
    tab4: "सुरक्षायात्रा"
  },
  "Santali (ᱥᱟᱱᱛᱟᱲᱤ)": {
    ...baseEn,
    emergency: "ᱟᱯᱟᱛ ᱠᱷᱚᱵᱚᱨ: ᱟᱯᱟᱛ ᱚᱠᱛᱚ ᱨᱮ ᱑᱑᱒ / ᱑᱐᱘ ᱨᱮ ᱯᱷᱚᱱ ᱢᱮ।",
    tab1: "ᱟᱯᱞᱳᱰ ᱟᱨ ᱚᱰᱚᱠ",
    tab2: "ᱱᱤᱭᱟᱹᱢ ᱠᱩᱞᱤ",
    tab3: " hospital ᱯᱟᱱᱛᱮ",
    tab4: "ᱨᱩᱠᱷᱤᱭᱟᱹ ᱥᱟᱸᱜᱷᱟᱨ"
  },
  "Sindhi (सिंधी)": {
    ...baseEn,
    emergency: "हंगामी सूचना: मेडीकल इमर्जन्सीءَ ۾ 112 / 108 تي ڪال ڪريو.",
    tab1: "اپلوڊ ۽ خلاصو",
    tab2: "پاليسي بابت پڇو",
    tab3: "اسپتال ڳوليو",
    tab4: "حفاظتي سفر"
  },
  "Tamil (தமிழ்)": {
    ...baseEn,
    emergency: "அவசர அறிவிப்பு: உங்களுக்கு மருத்துவ அவசரம் என்றால் உடனடியாக 112 / 108 ஐ அழைக்கவும்.",
    tab1: "பதிவேற்றம் மற்றும் பிரித்தெடுத்தல்",
    tab2: "உங்கள் பாலிசியை கேட்கவும்",
    tab3: "மருத்துவமனை விருப்பங்கள்",
    tab4: "பாதுகாப்பு பயணம்",
    upload_header: "பாலிசி ஆவணத்தை பதிவேற்றவும்",
    primary_cover: "முதன்மை பாலிசி கவர்",
    combined_si: "மொத்த காப்பீட்டுத் தொகை"
  },
  "Telugu (తెలుగు)": {
    ...baseEn,
    emergency: "అత్యవసర నోటీసు: అత్యవసర వైద్య పరిస్థితి ఉంటే వెంటనే 112 / 108కి కాల్ చేయండి.",
    tab1: "అప్‌లోడ్ & నిష్కర్శన",
    tab2: "మీ పాలసీని అడగండి",
    tab3: "ఆసుపత్రి ఎంపికలు",
    tab4: "రక్షణ ప్రయాణం",
    upload_header: "పాలసీ పత్రాన్ని అప్‌లోడ్ చేయండి",
    primary_cover: "ప్రాధమిక పాలసీ కవర్",
    combined_si: "మొత్తం బీమా మొత్తం"
  },
  "Urdu (اردو)": {
    ...baseEn,
    emergency: "ہنگامی نوٹس: طبی ہنگامی صورتحال میں فوری طور پر 112 / 108 پر کال کریں۔",
    tab1: "اپ لوڈ اور اقتباس",
    tab2: "اپنی پالیسی سے پوچھیں",
    tab3: "ہسپتال کا انتخاب تلاش کریں",
    tab4: "حفاظتی سفر",
    upload_header: "پالیسی دستاویز اپ لوڈ کریں"
  }
};

export function getTranslation(lang) {
  if (!lang) return baseEn;
  if (TRANSLATIONS[lang]) return TRANSLATIONS[lang];
  
  // Fuzzy match fallback for language names like "Assamese" matching "Assamese (অসমীয়া)"
  const cleanLang = lang.split(' ')[0].toLowerCase();
  for (const key of Object.keys(TRANSLATIONS)) {
    if (key.toLowerCase().startsWith(cleanLang)) {
      return TRANSLATIONS[key];
    }
  }

  return baseEn;
}

export const en = baseEn;
