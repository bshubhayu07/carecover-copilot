# CareCover Copilot - Design Tokens & Brand Style Guide

**Extracted from Stitch Project:** Smart Path Follower (`4755921041399727980`)  
**Design Theme:** CareCover Enterprise Healthcare System  
**Aesthetic:** Corporate / Modern / Clinical Precision  

---

## 🎨 1. Color Palette

### 1.1 Brand & Surface Colors
- **Primary Deep Trust Blue:** `#003178` (`rgb(0, 49, 120)`) - Headers, Primary CTAs, Navigation
- **Primary Container Blue:** `#0D47A1` (`rgb(13, 71, 161)`) - Dark Headers & Accent Cards
- **Secondary Healing Green:** `#1B6D24` / `#2E7D32` - Positive Cashless Statuses & Approved Indicators
- **Secondary Container Light Green:** `#A0F399` (10% Opacity Chips)
- **Tertiary Deep Navy:** `#00356C` - Secondary Navigation & Badges
- **Clinical White Canvas:** `#FFFFFF` - Card background surfaces & modal dialogs
- **Surface Gray:** `#F8FAFC` - Main background canvas
- **Surface Soft Blue Tint:** `#F3FAFF` - Secondary containers & message bubbles
- **Border Subtle Gray:** `#E2E8F0` - 1px Low-contrast card borders

### 1.2 Status & Functional Accents
- **Status Warning Orange:** `#ED6C02` - Pre-Auth 48h Intimation Notices
- **Status Error / Emergency Red:** `#D32F2F` - ER 112/108 Escalation Banners
- **Indian Rupee Accent Green:** `#1B5E20` - Financial Metrics & Sum Insured Values
- **Audit Tag Gray:** `#737783` - RAG-TRACE and Feed Provenance badges

---

## ✒️ 2. Typography Specification

**Primary Typeface:** `Inter` (Google Fonts) — Optimized for vertical descenders across all 22 Indian languages.

| Token Name | Font Size | Weight | Line Height | Letter Spacing | Usage |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `headline-lg` | 32px | 700 (Bold) | 40px | -0.02em | Main Page Titles |
| `headline-md` | 24px | 600 (SemiBold) | 32px | 0 | Section Headers |
| `headline-sm` | 20px | 600 (SemiBold) | 28px | 0 | Card Titles |
| `body-lg` | 18px | 400 (Regular) | 28px | 0 | Lead Paragraphs |
| `body-md` | 16px | 400 (Regular) | 24px | 0 | General Body Text |
| `body-sm` | 14px | 400 (Regular) | 20px | 0 | Form Labels & Tooltips |
| `label-caps` | 12px | 700 (Bold) | 16px | +0.05em | Metadata & Feed Badges |
| `data-mono` | 14px | 500 (Medium) | 20px | 0 | INR Currency Values (`INR 5,00,000`) |

---

## 📐 3. Layout, Elevation & Components

### 3.1 Spacing & Radius
- **Base Grid:** 8px spacing system (`4px`, `8px`, `16px`, `24px`, `32px`, `64px`)
- **Container Max Width:** `1200px` (Centered 12-column grid on desktop)
- **Border Radius:** `0.25rem` (4px soft corners for cards & inputs)
- **Chip Radius:** `9999px` (Pill-shaped status chips)

### 3.2 Component Tokens
- **Primary Button:** `#003178` solid fill, white text, 4px border-radius, hover brightness transition.
- **Emergency Banner:** `#D32F2F` solid banner with urgent 112/108 call out.
- **Policy Card:** White background (`#FFFFFF`), 1px `#E2E8F0` border, low-contrast ambient shadow on hover.
- **RAG Badge:** Soft `#F3FAFF` container, `#00356C` monospace text.
