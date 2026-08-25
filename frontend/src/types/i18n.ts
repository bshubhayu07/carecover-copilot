export type IndianLanguage = 
  | "English" | "Hindi" | "Marathi" | "Bengali" | "Gujarati"
  | "Punjabi" | "Tamil" | "Telugu" | "Kannada" | "Malayalam"
  | "Odia" | "Assamese" | "Urdu" | "Sanskrit" | "Kashmiri"
  | "Nepali" | "Sindhi" | "Konkani" | "Maithili" | "Dogri"
  | "Manipuri" | "Bodo" | "Santhali";

export interface UIKeys {
  emergency_prefix: string;
  detect_btn: string;
  header_subtitle: string;
  purge_btn: string;
  theme_btn: string;
  system_online: string;
  tab1: string;
  tab2: string;
  tab3: string;
  tab4: string;
  upload_title: string;
  upload_desc: string;
  demo_base_btn: string;
  demo_base_dl: string;
  topup_title: string;
  topup_desc: string;
  demo_topup_btn: string;
  demo_topup_dl: string;
  primary_base_label: string;
  super_topup_label: string;
  combined_si_label: string;
  summary_title: string;
  summary_sub: string;
  export_pdf_btn: string;
  insurer_label: string;
  si_label: string;
  room_label: string;
  copay_label: string;
  ask_title: string;
  chat_intro: string;
  chat_placeholder: string;
  send_btn: string;
  hospital_title: string;
  hospital_desc: string;
  city_label: string;
  specialty_label: string;
  in_network_label: string;
  journey_title: string;
  [key: string]: string;
}

export type I18nDictionary = Record<IndianLanguage, UIKeys>;
