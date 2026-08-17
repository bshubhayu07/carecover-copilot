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

export const TRANSLATIONS = {
  English: {
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
  },
  "Hindi (हिंदी)": {
    emergency: "आपातकालीन सूचना: यदि आपको या आपके परिवार को चिकित्सा आपात स्थिति है, तो तुरंत 112 / 108 पर कॉल करें।",
    site_lang: "ऐप और साइट इंटरफ़ेस भाषा",
    tab1: "अपलोड और निष्कर्षण",
    tab2: "अपनी नीति से पूछें",
    tab3: "अस्पताल के विकल्प खोजें",
    tab4: "देखभाल यात्रा और सुरक्षा",
    upload_header: "नीति दस्तावेज़ अपलोड करें",
    upload_sub: "अपनी मूल स्वास्थ्य बीमा नीति (PDF) अपलोड करें",
    load_demo_base: "डेमो मूल नीति लोड करें",
    topup_expander: "दोहरी-नीति और सुपर टॉप-अप तुलना इंजन",
    topup_desc: "संयुक्त बीमा राशि की गणना के लिए एक द्वितीयक सुपर टॉप-अप नीति अपलोड करें।",
    upload_topup_label: "द्वितीयक सुपर टॉप-अप नीति (PDF)",
    load_demo_topup: "डेमो सुपर टॉप-अप नीति लोड करें",
    topup_deductible_label: "टॉप-अप डिडक्टिबल सीमा (INR)",
    dual_breakdown: "दोहरी नीति सुरक्षा विवरण:",
    primary_cover: "प्राथमिक नीति कवर",
    topup_cover: "टॉप-अप नीति कवर",
    combined_si: "कुल संयुक्त बीमा राशि",
    extracted_summary: "निकालना नीति सारांश",
    base_coverage: "मूल नीति कवरेज",
    secondary_topup_coverage: "द्वितीयक सुपर टॉप-अप कवरेज",
    insurer_name: "बीमाकर्ता का नाम",
    policy_name: "नीति का नाम",
    sum_insured: "बीमा राशि",
    room_eligibility: "कमरे की पात्रता",
    copay_terms: "सह-भुगतान की शर्तें",
    preauth_req: "पूर्व-स्वीकृति आवश्यक",
    dl_pdf_summary: "नीति सारांश डाउनलोड (PDF)",
    dl_pdf_preauth: "पूर्व-स्वीकृति TPA फॉर्म (PDF)",
    ask_header: "अपनी कवरेज के बारे में प्रश्न पूछें",
    hosp_header: "अस्पताल नेटवर्क और रूम मिलान",
    journey_header: "देखभाल यात्रा और दावा अनुमानक"
  },
  "Bengali (বাংলা)": {
    emergency: "জরুরী নোটিশ: কোনো চিকিৎসা জরুরী পরিস্থিতি হলে অবিলম্বে ১১২ / ১০৮ নম্বরে কল করুন।",
    site_lang: "অ্যাপ ও সাইট ইন্টারফেস ভাষা",
    tab1: "আপলোড ও তথ্য সংগ্রহ",
    tab2: "আপনার পলিসি প্রশ্ন করুন",
    tab3: "হাসপাতাল অপশন খুঁজুন",
    tab4: "কেয়ার যাত্রা ও নিরাপত্তা",
    upload_header: "পলিসি নথি আপলোড করুন",
    upload_sub: "আপনার মূল স্বাস্থ্য বীমা পলিসি (PDF) আপলোড করুন",
    load_demo_base: "ডেমো মূল পলিসি লোড করুন",
    topup_expander: "দ্বৈত-পলিসি ও সুপার টপ-अप তুলনা ইঞ্জিন",
    topup_desc: "একত্রিত বীমা রাশি এবং ডিডাক্টিবল ট্রিগার গণনা করার জন্য দ্বিতীয় পলিসি লোড করুন।",
    upload_topup_label: "দ্বিতীয় সুপার টপ-আপ পলিসি (PDF)",
    load_demo_topup: "ডেমো সুপার টপ-আপ পলিসি লোড করুন",
    topup_deductible_label: "টপ-আপ ডিডাক্টিবল থ্রেশহোল্ড (INR)",
    dual_breakdown: "দ্বৈত-পলিসি সুরক্ষা বিবরণ:",
    primary_cover: "প্রাথমিক পলিসি কভার",
    topup_cover: "টপ-আপ পলিসি কভার",
    combined_si: "মোট একত্রিত বীমা রাশি",
    extracted_summary: "সংগৃহীত পলিসি সারাংশ",
    base_coverage: "মূল পলিসি কভারেজ",
    secondary_topup_coverage: "দ্বিতীয় সুপার টপ-আপ কভারেজ",
    insurer_name: "বীমাকারীর নাম",
    policy_name: "পলিসির নাম",
    sum_insured: "বীমা রাশি",
    room_eligibility: "রুমের যোগ্যতা",
    copay_terms: "কো-পে শর্তাবলী",
    preauth_req: "প্রাক-অনুমোদন প্রয়োজন",
    dl_pdf_summary: "পলিসি সারাংশ ডাউনলোড (PDF)",
    dl_pdf_preauth: "প্রাক-অনুমোদন TPA ফর্ম (PDF)",
    ask_header: "আপনার কভারেজ সম্পর্কে প্রশ্ন জিজ্ঞাসা করুন",
    hosp_header: "হাসপাতাল নেটওয়ার্ক ও রুম ম্যাচিং",
    journey_header: "কেয়ার যাত্রা ও দাবি হিসাবক"
  }
};
