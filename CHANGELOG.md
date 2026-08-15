# CareCover Copilot - Versioned Changelog & Release History

## [v2.4.0-enterprise] - 2026-08-16
### Added
- **22 Official Scheduled Languages of India**: Full support for all 22 8th Schedule constitutional languages of India plus English.
- **Upload Hardening & Safety Rules**: Implemented 25MB file size limit, 50-page maximum limit, and `%PDF-` magic-byte content validation.
- **Data Provenance & Feed Governance**: Record-level insurer/TPA feed IDs (`FEED-NIVABUPA-20260816-01`), SHA-256 feed verification hashes, and daily refresh schedules.
- **Feedback & Escalation Loop**: Built-in response flagging and ticket generation for erroneous guidance or hospital network updates.
- **CERT-In Incident Response Integration**: Documented 6-hour breach intimation runbook compliant with CERT-In Cyber Security Directions 70B.
- **Proportional Room Rent Penalty Simulator**: Dynamic math model estimating out-of-pocket room rent deductions and co-pay splits.
- **Indian Numbering System (INR)**: Currency formatting using Indian Lakhs & Crores (`INR 5,00,000`, `INR 15,00,000`).

## [v2.3.0] - 2026-08-15
- Integrated Secondary Super Top-Up comparison engine.
- Formatted PDF export for Pre-Authorization TPA forms.
- Real-time token streaming Q&A assistant.

## [v2.0.0] - 2026-08-14
- Initial release with PyMuPDF parsing, ChromaDB vector indexing, and Groq Llama-3.3-70B integration.
