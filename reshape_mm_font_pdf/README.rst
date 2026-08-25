==================================
Myanmar Font Reshaper for Reports
==================================

.. image:: https://img.shields.io/badge/licence-LGPL--3-blue.svg
   :target: https://www.gnu.org/licenses/lgpl-3.0.en.html
   :alt: License: LGPL-3

This module fixes Myanmar font rendering issues (such as incorrect character order, broken glyphs, and misplaced diacritics) in Odoo HTML and PDF reports by automatically reordering and reshaping Myanmar Unicode characters before rendering.

Features (ပါဝင်သော လုပ်ဆောင်ချက်များ)
=====================================
* **Automatic Character Reordering:** Corrects the sequence of Myanmar characters such as *ThaWaiHtoo* (ေ) and *YaYit* (ြ).
* **Glyph Substitution:** Automatically substitutes complex conjuncts, subjoined consonants (ပါဠိဆင့်/အက္ခရာဆင့်များ), and variants like *KinZi* (င်္).
* **Seamless Integration:** Overrides `ir.actions.report` to process HTML string output directly before PDF conversion without affecting database records.

Requirements (လိုအပ်ချက်များ)
===========================
* Custom Myanmar Font (e.g., Pyidaungsu Font) installed on the system and declared in your report's CSS.

Configuration & Usage (အသုံးပြုပုံ)
===================================
1. Install this module in your Odoo instance.
2. Generate any PDF or HTML report containing Myanmar Unicode text.
3. The module automatically hooks into `_prepare_html` and reshapes the text output. No extra setup is required.

Known Issues / Limitations
==========================
* Reshaping logic relies on character index positioning; non-standard Unicode strings or raw ASCII mixes inside text blocks might require additional handling.

Credits (ကျေးဇူးတင်လွှာ)
=======================

Authors
-------
* S.W.Nwe

Reference & Acknowledgements
----------------------------
* This module is based on the Myanmar font rendering / reshaping logic developed by **White Star Myanmar**.
* Special thanks to **White Star Myanmar** for their contributions to the Myanmar Odoo community.

Maintainers
-----------
This module is maintained by S.W.Nwe.