# AstroVibe

**Field Shift: Adapting Farms with NASA Data** — NASA Space Apps Challenge 2026, Giza

AstroVibe is a bilingual (English / Arabic) decision-support web tool that helps farmers choose crop rotations that protect soil health and conserve water as the climate shifts.

**Live project:** https://claude.ai/artifact/PUsnLY5HvAA1nhaC6HjA4V
**Demo:** _add the demo video or presentation link here_

---

## The problem

Farmers face shifting temperatures, changing rainfall, water shortages, extreme heat and declining soil health. Choosing a crop rotation that holds up under these pressures is hard to do by instinct, and few simple tools let a farmer compare strategies before committing a season.

## What AstroVibe does

1. **Inputs:** region, soil texture, soil organic matter, soil salinity, irrigation access, the last crop grown, and farmer priorities (soil health, water saving, profit, climate resilience).
2. **Field Shift scenario:** sliders for warming (0 to +4 °C), rainfall change (-40% to +20%) and irrigation supply cut (0 to 60%).
3. **Ranking:** 19 crops are tested across all 12 sowing months. Three-year rotations are ranked by the farmer's priorities.
4. **Outputs:**
   - Top three rotations with soil, water, profit and resilience scores
   - **Orbit view:** planting windows today versus under the scenario, with the shift in weeks
   - Winners and losers: which crops gain or lose yield under the scenario
   - 10-year soil organic matter outlook compared with growing the same crop every year
   - Stress test: yield index today, under the scenario, and in a hot, dry year
   - Impact versus continuous cropping: irrigation saved, nitrogen credit, extra soil carbon, stress-year yield
   - **Why not this crop?** An explanation of what limits any chosen crop (temperature, heat, water, soil texture, salinity, rotation rules)
   - Regional NASA indicators and a monthly climate chart (today versus scenario)
5. **Languages:** full English and Arabic interface (right-to-left layout).

## How the model works

- **Climate:** monthly temperature and rainfall plus yearly heat-day counts define each region. The scenario shifts them.
- **Crop suitability:** temperature fit (trapezoid curve per crop), heat stress, seasonal water balance (rain plus available irrigation versus crop need), soil texture fit and salinity tolerance combine into a yield index from 0 to 100%.
- **Rotation rules:** no crop repeats within a cycle, no botanical family back to back, the first crop cannot share a family with the last crop grown, and legumes or cover crops give the next crop a small yield lift.
- **Soil carbon:** a simple annual organic matter balance (residue inputs minus temperature- and texture-dependent decomposition) is run for 10 years.
- **Scoring:** weighted sum of soil health, water saving, profit and resilience, using the farmer's priority sliders as weights.

## NASA data and resources

| Resource | How it is used |
|---|---|
| **NASA POWER** (T2M, T2M_MAX, PRECTOTCORR) | `astrovibe_nasa_power.py` retrieves monthly normals, warming and rainfall trends per decade, and days above 35 °C for any latitude/longitude. The app accepts its output in the "Use your own NASA POWER data" box. |
| **GPM IMERG, SMAP, GRACE-FO, MERRA-2** | The app shows regional indicators inspired by these datasets (rainfall trend, root-zone soil moisture percentile, groundwater trend, warming trend) for eight demo regions. |

**Important:** the eight built-in demo regions use bundled, approximate regional climatology and indicator values. They are not live retrievals. For accurate results on a specific field, run the script for that field's coordinates and paste the output into the app.

### Using your own NASA POWER data

1. Open Google Colab and paste the contents of `astrovibe_nasa_power.py`.
2. Set `LAT` and `LON` to your field's coordinates and run it.
3. Copy the JSON line it prints, for example:
   `{"T":[...12 numbers],"P":[...12 numbers],"heat":18,"tT":0.35,"tR":-3.0}`
4. In AstroVibe, open **Use your own NASA POWER data**, paste it, and press **Apply data**.

Optional keys: `tT` (warming, °C per decade), `tR` (rainfall, % per decade), `smap`, `drought`, `grace`.

## Limitations

- AstroVibe is a transparent screening model for comparing strategies. It is not a yield forecast.
- Crop parameters, yield factors and soil carbon coefficients are simplified assumptions. Soil carbon uses the top 20 cm, bulk density 1.3 g/cm³ and 58% carbon in organic matter.
- Some crops are excluded from a region where they are not commercially established.
- Results should be checked with local agronomists and soil tests before real decisions.

## Technologies

HTML, CSS and vanilla JavaScript (single page, no external libraries); Python with `requests` and `numpy` for the NASA POWER script; Google Fonts (Bricolage Grotesque, Inter, Cairo, JetBrains Mono).

## AI use

Claude (Anthropic) was used as a development assistant for code, scoring logic, interface text and the NASA POWER script. The team defined the idea and scope, and reviewed and tested the outputs.

## Team

_Add team name and members here._

---

## ملخص بالعربي

AstroVibe أداة ثنائية اللغة تساعد المزارع على اختيار دورة زراعية تحافظ على التربة وتوفّر المياه مع تغيّر المناخ. يدخل المزارع بيانات حقله وأولوياته ويحرّك سيناريو (احترار، تغيّر أمطار، نقص مياه الري)، فترتّب الأداة أفضل الدورات الزراعية وتوضح كيف تتحرك مواعيد الزراعة، وتتوقع المادة العضوية في التربة، وتختبر الدورة في سنة حارة وجافة، وتشرح لماذا استُبعد أي محصول. بيانات المناطق المضمّنة تقريبية، ولأي حقل بعينه يمكن سحب بيانات NASA POWER الحقيقية بالسكريبت المرفق ولصقها في الأداة.
