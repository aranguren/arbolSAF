# ÁrbolSAF Tool Redesign — Design Spec

**Date:** 2026-04-03  
**Status:** Approved  

---

## Context

The current ÁrbolSAF tool guides users through a 5-step wizard to select and evaluate tree species for agroforestry systems. The existing flow forces users to browse species without any filtering, and ends abruptly after a registration form with no visual summary of the final selection.

This redesign adds **2 new steps** and restructures **3 existing steps** to:
1. Let users filter and rank species by their own priorities **before** selecting
2. Consolidate the three separate evaluation tables (climate, soil, morphology) into a single card-based step
3. End the wizard with an interactive radar chart comparing all selected species across their 6 value dimensions

---

## New Step Flow

| # | Step | Status |
|---|------|--------|
| 0 | **Explorar** — filter + priority weighting | **NEW** |
| 1 | **Seleccionar** — species selection table (pre-sorted by relevance) | Modified |
| 2 | **Evaluar** — per-species cards with Climate / Soil / Morphology tabs | **Redesigned** (merges old steps 2, 3, 4) |
| 3 | **Registrar** — producer registration form | Unchanged |
| 4 | **Radar** — multi-species radar chart | **NEW** |

Total: 5 steps (down from 5 steps + separate intro, but richer content per step).

---

## Step 0 — Explorar (NEW)

### Layout
Two-column layout: filter sidebar (260px) on the left, species table on the right.

### Left panel: Priority sliders
Six sliders (0–100%), one per value dimension:
- Madera, Fruta, Suelo, Microclima, Biodiversidad, Otros Usos

Each slider sets a weight used to compute a **relevance score** per species:

```
relevance = (VALOR_MADERA × w_madera + VALOR_FRUTA × w_fruta + ... ) / sum(weights)
```

### Left panel: Hard filters
- **Familia** — multi-select chips (derived from `FamilyModel`)
- **Zona climática** — chips (derived from climate variable ranges)
- **Tipo de suelo** — chips (from `v106_tipo_suelo_optimo`)
- **IVIM range** — min/max numeric inputs
- **Estado IUCN** — chips (from `v56_categoria_amenaza_iucn`: LC, NT, VU, EN, CR)

### Right panel: Species table
- Search bar (common name / scientific name)
- DataTable columns: Nombre común, Nombre científico, Familia, Usos destacados (badges), IVIM, Relevancia ↓
- Table re-sorts and filters live as sliders/chips change
- "Relevancia" column shows a visual bar + numeric score
- **Clicking "Continuar a selección"** persists the current filter state and sort order into Step 1

### Data
- Species data already loaded via `/arbolsaf/especie/listado/json/` — no new endpoint needed
- Relevance score computed in JS from existing `VALOR_*` fields and slider weights
- Filter state stored in a new `filter_config` JS object alongside `species_selected`

---

## Step 1 — Seleccionar (Modified)

### Changes from current
- Species table arrives **pre-sorted by relevance score** from Step 0
- Active filters from Step 0 are applied (can be cleared with a "Show all" toggle)
- Product filter buttons (Suelo, Madera, etc.) remain, but default selection reflects the highest-weighted dimension from Step 0
- Everything else (checkboxes, IVIM column, selected species summary table) unchanged

---

## Step 2 — Evaluar (Redesigned — replaces old steps 2, 3, 4)

### Layout
Responsive card grid (`auto-fill`, min 320px per card). One card per selected species.

### Card structure
Each card has three sections:

**Header**
- Species icon placeholder + common name + scientific name
- Two semaphore toggles inline: Clima (green/red) and Suelo (green/red)
- Replaces the separate traffic-light tables from old steps 2 and 3

**Tabbed body** (three tabs per card)
- `🌡 Clima` — temp min/max, elevation range, precipitation range, tolerance
- `🌱 Suelo` — soil type, fertility demand, acidity tolerance, pH range, drainage
- `🌿 Morfología` — guild, phenology, root type, bark, crown shape/density, foliage, height/width
- Notes textarea at the bottom of every tab panel (shared across tabs, stored once per species)

**Footer**
- IVIM badge
- "✕ Eliminar" button — removes species from all tables + unchecks in Step 1

### Data model changes
`species_selected[]` entries gain no new fields — `SEMAFORO_PASO_2`, `SEMAFORO_PASO_3`, `NOTAS` already exist. The semaphore buttons now live on the card header instead of table rows.

---

## Step 3 — Registrar (Unchanged)

No changes to layout, fields, or backend handling. The registration form and its cascading region/province/district selects remain as-is.

---

## Step 4 — Radar (NEW)

### Layout
Two-column layout: radar chart (flex-fill) on the left, side panel (280px) on the right. Full viewport height using flexbox (`height: 100vh`, `overflow: hidden`).

### Radar chart
- Library: **Chart.js** (already available or added via CDN)
- Type: `radar`
- Axes (6): Madera, Fruta, Suelo, Microclima, Biodiversidad, Otros Usos
- One dataset per selected species, color-coded
- `maintainAspectRatio: false` so chart fills available height
- Animated transitions (`duration: 500ms`) when toggling species

### Side panel
Two cards stacked vertically:

**Especies legend card**
- One row per species: color dot, common name, scientific name, relevance score badge
- Clicking a row toggles that species on/off in the radar (with animation)
- Hidden species shown with strikethrough text + faded dot

**Semáforos summary card**
- Table: species name | Clima semaphore dot | Suelo semaphore dot
- Read-only; reflects assessments from Step 2

### PDF integration
- "🖨 Generar PDF" button at bottom right (replaces the submit button from old Step 5)
- Submits same AJAX POST to `/arbolsaf/herramienta/pdf/` with `species_selected` + form data
- The radar chart is NOT included in the PDF (wkhtmltopdf cannot render Chart.js reliably)
- PDF template (`tool_pdf.html`) receives the semaphore results from Step 2 as before

---

## Files to modify

| File | Change |
|------|--------|
| `arbolsaf/templates/arbolsaf/tool/tool.html` | Add Step 0 panel, add Step 4 panel, redesign Steps 2–4 panels into new Step 2 card grid, update progress bar to 5 steps |
| `apps/static/assets/js/tool_arbolsaf.js` | Add `filter_config` object, add relevance scoring, add `createStep0Table()`, replace `conditionSpecies()` / `conditionSpeciesTwo()` / `asociationSpecies()` with `createEvalCard()`, add `initRadarChart()` and `toggleSpecies()` |
| `arbolsaf/templates/arbolsaf/tool/tool_pdf.html` | Minor: use `SEMAFORO_PASO_2` / `SEMAFORO_PASO_3` from card-based step (field names unchanged) |

### New JS dependency
Add Chart.js via CDN in `tool.html`:
```html
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
```

---

## Data flow summary

```
Step 0: filter_config (weights + chips)
    ↓ relevance score computed per species
Step 1: species_selected[] populated (checkboxes)
    ↓
Step 2: species_selected[i].SEMAFORO_PASO_2, SEMAFORO_PASO_3, NOTAS updated
    ↓
Step 3: register_form["FORM DATA"] populated
    ↓
Step 4: radar rendered from species_selected[].VALOR_* fields
    → PDF: AJAX POST to /arbolsaf/herramienta/pdf/ (unchanged backend)
```

---

## Verification

1. **Step 0 filters**: Change a slider → species table re-sorts by relevance. Toggle a chip → table filters live. Proceed → Step 1 table shows same order.
2. **Step 1 pre-sort**: Species with highest relevance score appear first; "Show all" toggle resets filters.
3. **Step 2 cards**: Select 3 species → 3 cards appear. Click tabs → Climate/Soil/Morphology data switches. Toggle semaphore → header indicator updates. Remove species → card disappears + Step 1 checkbox unchecked.
4. **Step 4 radar**: All selected species appear as polygons. Click legend item → species animates out/in. Semaphore table reflects Step 2 choices.
5. **PDF**: Click "Generar PDF" → file downloads. Open PDF → producer data, species list, semaphore results visible.
6. **No backend changes required** — all modifications are frontend only.
