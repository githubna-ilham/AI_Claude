# Module 09a — Latihan: Generative Dashboard

> Membangun fitur **Natural Language → Chart** di halaman Dashboard Fin-App. User ketik instruksi bebas, Claude analisis + ambil data via tools, app render chart dinamis.
>
> **Total estimasi**: ±2–3 jam efektif.

## Prasyarat

- [ ] Module 08 selesai — `quickAddTransaction` dengan multi-tool berfungsi.
- [ ] Tabel `transactions` di Supabase sudah berisi data (ada kolom `amount`, `category`, `type`, `date`).
- [ ] `@anthropic-ai/sdk` terinstal dan `ANTHROPIC_API_KEY` aktif.
- [ ] Halaman Dashboard sudah ada di `src/app/dashboard/page.tsx`.

## Prinsip Kontinuitas

- ✅ Tidak mengubah fitur yang sudah ada (chatbot, quick-add, RAG).
- ✅ Server Action baru di file terpisah `src/features/chart-generator.ts`.
- ✅ Komponen baru di `src/components/ChartGenerator.tsx`.

---

## 📚 Referensi Dokumentasi

- **[Recharts docs](https://recharts.org/en-US/api)** — PieChart, BarChart, LineChart, AreaChart API.
- **[Anthropic tool use](https://docs.claude.com/en/docs/agents-and-tools/tool-use/overview)** — flow 2-tool pattern.
- **[Next.js Server Actions](https://nextjs.org/docs/app/building-your-application/data-fetching/server-actions-and-mutations)** — cara panggil server action dari client component.
- **[Supabase JS — select](https://supabase.com/docs/reference/javascript/select)** — query dengan filter + aggregate.

---

## Prompt 1 — Tool Definitions + Server Action `generateChart`

### Walkthrough Manual

Prompt ini membuat **seluruh backend logic** di `src/features/chart-generator.ts`:
1. Dua tool definitions (`query_transactions` + `render_chart`)
2. Helper `queryTransactions` yang hit Supabase
3. Server Action `generateChart` yang jalankan loop Claude ↔ tools

📂 **File baru**: `src/features/chart-generator.ts`

**1. Tool `query_transactions`**

Claude pakai ini untuk mendeklarasikan data apa yang dibutuhkan. App yang query Supabase-nya.

```ts
// src/features/chart-generator.ts
const QUERY_TRANSACTIONS_TOOL: Anthropic.Messages.Tool = {
  name: "query_transactions",
  description: `Ambil data transaksi dari database untuk divisualisasikan.
Panggil tool ini PERTAMA sebelum render_chart untuk mendapatkan data.`,
  input_schema: {
    type: "object" as const,
    properties: {
      group_by: {
        type: "string",
        enum: ["category", "date", "type"],
        description: "Kelompokkan data berdasarkan: category (per kategori), date (per tanggal), type (income vs expense)",
      },
      period: {
        type: "string",
        enum: ["this_month", "last_month", "this_year"],
        description: "Periode waktu data yang diambil",
      },
      type: {
        type: "string",
        enum: ["expense", "income", "all"],
        description: "Filter tipe transaksi",
      },
    },
    required: ["group_by", "period", "type"],
  },
};
```

**2. Tool `render_chart`**

Claude pakai ini setelah dapat data untuk menentukan visualisasi yang tepat.

```ts
const RENDER_CHART_TOOL: Anthropic.Messages.Tool = {
  name: "render_chart",
  description: `Tentukan tipe chart dan konfigurasi untuk merender data yang sudah diambil.
Panggil tool ini SETELAH query_transactions berhasil mengembalikan data.`,
  input_schema: {
    type: "object" as const,
    properties: {
      chart_type: {
        type: "string",
        enum: ["pie", "bar", "line", "area"],
        description: "pie: proporsi kategori | bar: perbandingan | line/area: tren waktu",
      },
      title: {
        type: "string",
        description: "Judul chart yang informatif",
      },
      data_key: {
        type: "string",
        description: "Nama field yang jadi nilai numerik di data (mis. 'total')",
      },
      label_key: {
        type: "string",
        description: "Nama field yang jadi label di data (mis. 'category' atau 'date')",
      },
    },
    required: ["chart_type", "title", "data_key", "label_key"],
  },
};
```

**3. Helper `queryTransactions` — hit Supabase**

```ts
async function queryTransactions({
  group_by,
  period,
  type,
}: {
  group_by: "category" | "date" | "type";
  period: "this_month" | "last_month" | "this_year";
  type: "expense" | "income" | "all";
}) {
  const supabase = await createClient();
  const now = new Date();

  // Hitung rentang tanggal berdasarkan period
  let startDate: string;
  let endDate: string;

  if (period === "this_month") {
    startDate = new Date(now.getFullYear(), now.getMonth(), 1).toISOString().split("T")[0];
    endDate = new Date(now.getFullYear(), now.getMonth() + 1, 0).toISOString().split("T")[0];
  } else if (period === "last_month") {
    startDate = new Date(now.getFullYear(), now.getMonth() - 1, 1).toISOString().split("T")[0];
    endDate = new Date(now.getFullYear(), now.getMonth(), 0).toISOString().split("T")[0];
  } else {
    startDate = new Date(now.getFullYear(), 0, 1).toISOString().split("T")[0];
    endDate = new Date(now.getFullYear(), 11, 31).toISOString().split("T")[0];
  }

  // Build query
  let query = supabase
    .from("transactions")
    .select("amount, category, type, date")
    .gte("date", startDate)
    .lte("date", endDate);

  if (type !== "all") query = query.eq("type", type);

  const { data, error } = await query;
  if (error) throw new Error(error.message);

  // Aggregate di sisi app berdasarkan group_by
  const grouped: Record<string, number> = {};
  for (const row of data ?? []) {
    const key = group_by === "date" ? row.date : group_by === "type" ? row.type : row.category;
    grouped[key] = (grouped[key] ?? 0) + row.amount;
  }

  return Object.entries(grouped).map(([label, total]) => ({
    [group_by === "date" ? "date" : group_by === "type" ? "type" : "category"]: label,
    total,
  }));
}
```

**4. Server Action `generateChart`**

```ts
export async function generateChart(instruction: string): Promise<{
  chartConfig: ChartConfig | null;
  chartData: ChartRow[] | null;
  error?: string;
}> {
  const messages: Anthropic.Messages.MessageParam[] = [
    {
      role: "user",
      content: `Instruksi visualisasi data keuangan: ${instruction}
      
Gunakan tool query_transactions untuk ambil data, lalu render_chart untuk tentukan visualisasi.`,
    },
  ];

  let chartConfig: ChartConfig | null = null;
  let chartData: ChartRow[] | null = null;
  let iterations = 0;
  const MAX_ITER = 5;

  while (iterations < MAX_ITER) {
    iterations++;

    const response = await client.messages.create({
      model: "claude-haiku-4-5-20251001",
      max_tokens: 1024,
      tools: [QUERY_TRANSACTIONS_TOOL, RENDER_CHART_TOOL],
      messages,
    });

    if (response.stop_reason === "end_turn") break;

    const toolUses = response.content.filter(
      (b): b is Anthropic.Messages.ToolUseBlock => b.type === "tool_use"
    );

    if (toolUses.length === 0) break;

    messages.push({ role: "assistant", content: response.content });

    const toolResults: Anthropic.Messages.ToolResultBlockParam[] = await Promise.all(
      toolUses.map(async (tu) => {
        let result: unknown;

        if (tu.name === "query_transactions") {
          result = await queryTransactions(tu.input as any);
          chartData = result as ChartRow[];
        } else if (tu.name === "render_chart") {
          chartConfig = tu.input as ChartConfig;
          result = { ok: true };
        } else {
          result = { error: `Unknown tool: ${tu.name}` };
        }

        return {
          type: "tool_result" as const,
          tool_use_id: tu.id,
          content: JSON.stringify(result),
        };
      })
    );

    messages.push({ role: "user", content: toolResults });

    if (chartConfig && chartData) break;
  }

  if (!chartConfig || !chartData) {
    return { chartConfig: null, chartData: null, error: "Tidak dapat menghasilkan chart dari instruksi tersebut." };
  }

  return { chartConfig, chartData };
}
```

### Hasil yang Diharapkan

```ts
// src/features/chart-generator.ts — struktur file lengkap

'use server';

import Anthropic from "@anthropic-ai/sdk";
import { createClient } from "@/lib/supabase/server";

// Types
export type ChartConfig = {
  chart_type: "pie" | "bar" | "line" | "area";
  title: string;
  data_key: string;
  label_key: string;
};

export type ChartRow = Record<string, string | number>;

const client = new Anthropic();

// Tool definitions (2 tools)
const QUERY_TRANSACTIONS_TOOL: Anthropic.Messages.Tool = { /* ... */ };
const RENDER_CHART_TOOL: Anthropic.Messages.Tool = { /* ... */ };

// Helper query Supabase
async function queryTransactions(...) { /* ... */ }

// Server Action — dipanggil dari client
export async function generateChart(instruction: string): Promise<{
  chartConfig: ChartConfig | null;
  chartData: ChartRow[] | null;
  error?: string;
}> { /* ... */ }
```

### Verifikasi setelah file dibuat

1. `npx tsc --noEmit` clean.
2. Import `generateChart` dari file lain tidak error.
3. Test via script:
   ```ts
   // experiments/test-chart-gen.ts
   import { generateChart } from "@/features/chart-generator";
   const result = await generateChart("pie chart pengeluaran bulan ini");
   console.log(result);
   // → { chartConfig: { chart_type: "pie", ... }, chartData: [...] }
   ```
   Run: `npx tsx --env-file=.env.local experiments/test-chart-gen.ts`

---

<details>
<summary>Salin prompt berikut</summary>

```
Buat file src/features/chart-generator.ts berisi Server Action
generateChart untuk fitur Natural Language → Chart di Dashboard.

GOAL:
- Buat file baru src/features/chart-generator.ts dengan 'use server'.

- Export types:
  type ChartConfig = { chart_type: "pie"|"bar"|"line"|"area"; title: string; data_key: string; label_key: string }
  type ChartRow = Record<string, string | number>

- Konstanta client = new Anthropic() di module scope.

- Tool QUERY_TRANSACTIONS_TOOL:
  name: "query_transactions"
  description: ambil data transaksi untuk divisualisasikan,
    panggil PERTAMA sebelum render_chart.
  input_schema: { group_by: enum["category","date","type"],
    period: enum["this_month","last_month","this_year"],
    type: enum["expense","income","all"] }
  required: ["group_by","period","type"]

- Tool RENDER_CHART_TOOL:
  name: "render_chart"
  description: tentukan tipe chart setelah dapat data.
  input_schema: { chart_type: enum["pie","bar","line","area"],
    title: string, data_key: string, label_key: string }
  required: semua field

- Helper async queryTransactions({ group_by, period, type }):
  - Hitung startDate/endDate dari period (this_month/last_month/this_year).
  - Query Supabase: SELECT amount, category, type, date
    WHERE date BETWEEN startDate AND endDate.
  - Filter type kalau bukan "all".
  - Aggregate di app: group by field sesuai group_by,
    sum amount → return array [{ [group_by_key]: label, total: sum }].

- Export async function generateChart(instruction: string):
  - System message: instruksi + perintah pakai query_transactions dulu
    lalu render_chart.
  - Loop max 5 iterasi:
    - client.messages.create dengan 2 tools.
    - Break kalau stop_reason === "end_turn" atau tidak ada tool_use.
    - Promise.all tool_use blocks:
      * query_transactions → jalankan queryTransactions, simpan ke chartData.
      * render_chart → simpan input ke chartConfig, return { ok: true }.
    - Break kalau chartConfig && chartData sudah ada.
  - Return { chartConfig, chartData } atau { error: "..." } kalau gagal.

CONTEXT:
- Model: claude-haiku-4-5-20251001.
- Supabase via createClient() dari @/lib/supabase/server.
- Aggregate di sisi app (bukan SQL GROUP BY) supaya fleksibel.

GUARDRAIL:
- JANGAN sentuh file lain selain chart-generator.ts.
- Loop harus punya MAX_ITER = 5 untuk safety.
- Return type harus konsisten: { chartConfig, chartData, error? }.
- Ekspor ChartConfig dan ChartRow sebagai named types.
```

</details>

**Verifikasi:**

1. `npx tsc --noEmit` clean.
2. `generateChart("pie chart pengeluaran bulan ini")` di script → return `{ chartConfig: {...}, chartData: [...] }`.

---

## Prompt 2 — Client Component `ChartGenerator` + `DynamicChart`

### Walkthrough Manual

Prompt ini membuat dua komponen React:
1. `ChartGenerator` — input field + tombol generate + state management
2. `DynamicChart` — render chart yang tepat berdasarkan `chartConfig`

📂 **File baru**: `src/components/ChartGenerator.tsx`

**1. Komponen `DynamicChart`**

Menerima `config` (dari `render_chart` tool) dan `data` (dari Supabase), merender chart Recharts yang sesuai.

```tsx
import {
  PieChart, Pie, Cell, Tooltip, Legend,
  BarChart, Bar, XAxis, YAxis, CartesianGrid,
  LineChart, Line,
  AreaChart, Area,
  ResponsiveContainer,
} from "recharts";

const COLORS = ["#6366f1", "#f59e0b", "#10b981", "#ef4444", "#3b82f6", "#8b5cf6"];

function DynamicChart({ config, data }: { config: ChartConfig; data: ChartRow[] }) {
  const { chart_type, title, data_key, label_key } = config;

  return (
    <div className="mt-4">
      <h3 className="text-sm font-semibold text-gray-700 mb-3">{title}</h3>
      <ResponsiveContainer width="100%" height={300}>
        {chart_type === "pie" ? (
          <PieChart>
            <Pie data={data} dataKey={data_key} nameKey={label_key} cx="50%" cy="50%" outerRadius={100}>
              {data.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
            </Pie>
            <Tooltip formatter={(v: number) => `Rp ${v.toLocaleString("id-ID")}`} />
            <Legend />
          </PieChart>
        ) : chart_type === "bar" ? (
          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey={label_key} />
            <YAxis tickFormatter={(v) => `Rp ${(v / 1000).toFixed(0)}k`} />
            <Tooltip formatter={(v: number) => `Rp ${v.toLocaleString("id-ID")}`} />
            <Bar dataKey={data_key} fill="#6366f1" />
          </BarChart>
        ) : chart_type === "line" ? (
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey={label_key} />
            <YAxis tickFormatter={(v) => `Rp ${(v / 1000).toFixed(0)}k`} />
            <Tooltip formatter={(v: number) => `Rp ${v.toLocaleString("id-ID")}`} />
            <Line type="monotone" dataKey={data_key} stroke="#6366f1" dot={false} />
          </LineChart>
        ) : (
          <AreaChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey={label_key} />
            <YAxis tickFormatter={(v) => `Rp ${(v / 1000).toFixed(0)}k`} />
            <Tooltip formatter={(v: number) => `Rp ${v.toLocaleString("id-ID")}`} />
            <Area type="monotone" dataKey={data_key} stroke="#6366f1" fill="#e0e7ff" />
          </AreaChart>
        )}
      </ResponsiveContainer>
    </div>
  );
}
```

**2. Komponen `ChartGenerator`**

```tsx
"use client";

import { useState } from "react";
import { generateChart, type ChartConfig, type ChartRow } from "@/features/chart-generator";

const SUGGESTIONS = [
  "Pie chart pengeluaran bulan ini per kategori",
  "Bar chart income vs expense bulan ini",
  "Tren pengeluaran harian bulan ini",
  "Area chart pengeluaran tahun ini per bulan",
];

export function ChartGenerator() {
  const [instruction, setInstruction] = useState("");
  const [chart, setChart] = useState<{ config: ChartConfig; data: ChartRow[] } | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleGenerate() {
    if (!instruction.trim()) return;
    setLoading(true);
    setError(null);
    setChart(null);

    const result = await generateChart(instruction);

    if (result.error || !result.chartConfig || !result.chartData) {
      setError(result.error ?? "Gagal menghasilkan chart.");
    } else {
      setChart({ config: result.chartConfig, data: result.chartData });
    }

    setLoading(false);
  }

  return (
    <div className="rounded-xl border border-gray-200 bg-white p-5 shadow-sm">
      <h2 className="text-base font-semibold text-gray-800 mb-3">
        Generate Chart
      </h2>

      {/* Input */}
      <div className="flex gap-2">
        <input
          value={instruction}
          onChange={(e) => setInstruction(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleGenerate()}
          placeholder="Cth: pie chart pengeluaran bulan ini..."
          disabled={loading}
          className="flex-1 rounded-lg border border-gray-300 px-3 py-2 text-sm
                     focus:outline-none focus:ring-2 focus:ring-indigo-400 disabled:opacity-50"
        />
        <button
          onClick={handleGenerate}
          disabled={loading || !instruction.trim()}
          className="rounded-lg bg-indigo-600 px-4 py-2 text-sm font-medium text-white
                     hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? "..." : "Generate"}
        </button>
      </div>

      {/* Suggestions */}
      <div className="mt-2 flex flex-wrap gap-1">
        {SUGGESTIONS.map((s) => (
          <button
            key={s}
            onClick={() => setInstruction(s)}
            className="rounded-full border border-gray-200 px-2 py-0.5 text-xs
                       text-gray-500 hover:border-indigo-300 hover:text-indigo-600"
          >
            {s}
          </button>
        ))}
      </div>

      {/* Error */}
      {error && (
        <p className="mt-3 text-sm text-red-500">{error}</p>
      )}

      {/* Chart */}
      {chart && <DynamicChart config={chart.config} data={chart.data} />}
    </div>
  );
}
```

### Hasil yang Diharapkan

```tsx
// src/components/ChartGenerator.tsx — struktur file

"use client";
import { useState } from "react";
import { PieChart, BarChart, LineChart, AreaChart, ... } from "recharts";
import { generateChart, type ChartConfig, type ChartRow } from "@/features/chart-generator";

// Komponen internal (tidak diekspor)
function DynamicChart({ config, data }) { /* render recharts */ }

// Komponen utama (diekspor)
export function ChartGenerator() {
  // state: instruction, chart, loading, error
  // handleGenerate() → panggil generateChart server action
  // render: input + suggestions + DynamicChart
}
```

### Verifikasi setelah file dibuat

1. `npx tsc --noEmit` clean.
2. Tidak ada error import Recharts (pastikan `npm install recharts` sudah dijalankan).
3. Komponen `ChartGenerator` bisa diimport dari file lain.

---

<details>
<summary>Salin prompt berikut</summary>

```
Buat komponen React src/components/ChartGenerator.tsx untuk
fitur Natural Language → Chart.

GOAL:
Buat satu file berisi dua komponen:

1. function DynamicChart({ config, data }) — TIDAK diekspor:
   - Terima ChartConfig + ChartRow[] dari Prompt 1.
   - Render Recharts berdasarkan config.chart_type:
     * "pie"  → PieChart + Pie + Cell per entry (warna dari
                 array COLORS) + Tooltip + Legend.
     * "bar"  → BarChart + Bar + XAxis(dataKey=label_key) +
                 YAxis + CartesianGrid + Tooltip.
     * "line" → LineChart + Line(type=monotone, dot=false) +
                 XAxis + YAxis + CartesianGrid + Tooltip.
     * "area" → AreaChart + Area(type=monotone) + XAxis +
                 YAxis + CartesianGrid + Tooltip.
   - Semua dibungkus ResponsiveContainer width="100%" height={300}.
   - Tooltip formatter: "Rp " + value.toLocaleString("id-ID").
   - YAxis tickFormatter: "Rp ${(v/1000).toFixed(0)}k" (kecuali pie).
   - Tampilkan config.title sebagai heading <h3> di atas chart.
   - COLORS = ["#6366f1","#f59e0b","#10b981","#ef4444","#3b82f6","#8b5cf6"].

2. export function ChartGenerator() — "use client":
   - State: instruction (string), chart ({ config, data } | null),
     loading (boolean), error (string | null).
   - handleGenerate(): panggil generateChart(instruction) dari
     @/features/chart-generator. Set chart atau error dari result.
   - Enter key pada input → trigger handleGenerate.
   - UI:
     * Judul "Generate Chart".
     * Input text + tombol "Generate" (disabled saat loading/empty).
     * Loading state: tombol teks "...".
     * Chip suggestions (4 contoh instruksi, klik → isi input):
       - "Pie chart pengeluaran bulan ini per kategori"
       - "Bar chart income vs expense bulan ini"
       - "Tren pengeluaran harian bulan ini"
       - "Area chart pengeluaran tahun ini per bulan"
     * Error: tampilkan teks merah kalau result.error ada.
     * Chart: render DynamicChart kalau chart state tidak null.

CONTEXT:
- Import ChartConfig, ChartRow, generateChart dari
  @/features/chart-generator.
- npm install recharts sudah/akan dijalankan.
- Styling dengan Tailwind CSS.

GUARDRAIL:
- JANGAN buat file terpisah untuk DynamicChart.
- JANGAN hardcode tipe chart — selalu baca dari config.chart_type.
- JANGAN lupa "use client" di baris pertama.
- JANGAN simpan chartData di localStorage atau state global.
```

</details>

**Verifikasi:**

1. `npx tsc --noEmit` clean.
2. Komponen `ChartGenerator` bisa diimport tanpa error.
3. `npm run build` tidak ada error Recharts.

---

## Prompt 3 — Wire ke Halaman Dashboard + Test End-to-End

### Walkthrough Manual

Prompt terakhir — pasang `ChartGenerator` ke halaman Dashboard dan test semua skenario.

📂 **File yang dimodifikasi**: `src/app/dashboard/page.tsx`

```tsx
// src/app/dashboard/page.tsx
import { ChartGenerator } from "@/components/ChartGenerator";

export default function DashboardPage() {
  return (
    <main className="p-6 space-y-6">
      {/* ... komponen dashboard yang sudah ada ... */}

      {/* Tambahan */}
      <ChartGenerator />
    </main>
  );
}
```

### Hasil yang Diharapkan

```tsx
// src/app/dashboard/page.tsx — hanya bagian yang berubah

import { ChartGenerator } from "@/components/ChartGenerator"; // ← tambah import

export default function DashboardPage() {
  return (
    <main ...>
      {/* komponen lama tetap ada */}
      <ChartGenerator />  {/* ← tambah di bagian bawah */}
    </main>
  );
}
```

### Verifikasi setelah file diubah

1. `npm run dev` → buka `http://localhost:3000/dashboard`.
2. Komponen ChartGenerator muncul dengan input field + 4 suggestion chips.
3. Klik suggestion "Pie chart pengeluaran bulan ini per kategori" → input terisi.
4. Klik Generate → loading muncul → pie chart muncul dengan data kategori.
5. Ketik manual "bar chart income vs expense bulan ini" → bar chart muncul.
6. Test error: ketik "halo apa kabar" → error message muncul dengan elegan.

---

<details>
<summary>Salin prompt berikut</summary>

```
Pasang komponen ChartGenerator ke halaman Dashboard.

GOAL:
- Modifikasi src/app/dashboard/page.tsx:
  - Tambah import ChartGenerator dari @/components/ChartGenerator.
  - Render <ChartGenerator /> di bagian bawah halaman,
    di luar komponen yang sudah ada.

GUARDRAIL:
- JANGAN hapus atau ubah komponen dashboard yang sudah ada.
- JANGAN pindahkan ChartGenerator ke posisi tengah layout
  kalau itu merusak tampilan existing.
- Cukup tambah import + satu baris render.
```

</details>

**Verifikasi:**

1. Dashboard render tanpa error.
2. Ketik "pie chart pengeluaran bulan ini" → chart muncul.
3. Tidak ada regresi pada komponen dashboard lainnya.

---

## Validasi Akhir Module 09a

- [ ] `src/features/chart-generator.ts` punya `generateChart` + 2 tools + helper `queryTransactions`.
- [ ] `src/components/ChartGenerator.tsx` punya `ChartGenerator` + `DynamicChart`.
- [ ] Halaman Dashboard menampilkan komponen ChartGenerator.
- [ ] Pie chart muncul dari instruksi "pie chart pengeluaran bulan ini".
- [ ] Bar chart muncul dari instruksi "bar chart income vs expense bulan ini".
- [ ] Line/Area chart muncul dari instruksi tren waktu.
- [ ] Instruksi tidak relevan menampilkan error yang informatif.
- [ ] `npx tsc --noEmit` clean.
- [ ] `npm run build` sukses.
- [ ] Tidak ada regresi fitur lain (chatbot, quick-add, RAG).

## Refleksi Module 09a

1. Claude memilih `chart_type` berdasarkan instruksi user — seberapa akurat pilihannya? Instruksi apa yang paling sering menghasilkan tipe chart yang tidak tepat?
2. Saat ini data di-aggregate di sisi app (bukan SQL `GROUP BY`). Apa trade-off-nya kalau tabel `transactions` punya 100.000+ row?
3. Kalau user instruksi "bandingkan pengeluaran 3 bulan terakhir", tool `query_transactions` perlu dipanggil 3 kali. Bagaimana Anda akan extend schema tool untuk support multi-period dalam satu request?
4. Saat ini chart tidak bisa di-refresh otomatis saat data baru masuk (quick-add). Bagaimana cara membuat chart realtime tanpa polling setiap detik?
5. Bagaimana cara menambah `export_chart` tool agar user bisa download chart sebagai PNG?

---

⬅️ Kembali: **[Module 09 — Multimodal](../Module-09-Multimodal/latihan.md)** · 🏠 Index: **[Day 4 — AI Agent & Tools](../README.md)**
