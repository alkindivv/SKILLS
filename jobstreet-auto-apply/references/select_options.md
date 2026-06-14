# JobStreet Select Option ID Mappings

JobStreet uses cryptic option IDs for questionnaire selects. Here are the mapped values.

## Salary (select[name*="2588"])

| Option ID | Text |
|-----------|------|
| ID_Q_2588_V_2_A_2589 | Rp 1 million |
| ID_Q_2588_V_2_A_2590 | Rp 1.5 million |
| ID_Q_2588_V_2_A_2591 | Rp 2 million |
| ID_Q_2588_V_2_A_2592 | Rp 2.5 million |
| ID_Q_2588_V_2_A_2593 | Rp 3 million |
| ID_Q_2588_V_2_A_2594 | Rp 3.5 million |
| ID_Q_2588_V_2_A_2595 | Rp 4 million |
| ID_Q_2588_V_2_A_2596 | Rp 4.5 million |
| ID_Q_2588_V_2_A_2597 | Rp 5 million |
| ID_Q_2588_V_2_A_2598 | Rp 5.5 million |
| ID_Q_2588_V_2_A_2599 | Rp 6 million |
| ID_Q_2588_V_2_A_2600 | Rp 7 million |
| ID_Q_2588_V_2_A_2601 | Rp 8 million |
| ID_Q_2588_V_2_A_2602 | Rp 9 million |
| ID_Q_2588_V_2_A_2603 | Rp 10 million |
| ID_Q_2588_V_2_A_2604 | Rp 15 million |
| ID_Q_2588_V_2_A_2605 | Rp 20 million |
| ID_Q_2588_V_2_A_2606 | Rp 25 million |
| ID_Q_2588_V_2_A_2607 | Rp 30 million |
| ID_Q_2588_V_2_A_2608 | Rp 40 million |
| ID_Q_2588_V_2_A_2609 | Rp 60 million |
| ID_Q_2588_V_2_A_2610 | Rp 80 million |
| ID_Q_2588_V_2_A_2611 | Rp 100 million or more |

## Legal Counsel Experience (select[name*="9ABA"])

| Option ID | Text |
|-----------|------|
| ID_Q_9ABA..._1 | No experience |
| ID_Q_9ABA..._2 | Less than 1 year |
| ID_Q_9ABA..._3 | 1 year |
| ID_Q_9ABA..._4 | 2 years |
| ID_Q_9ABA..._5 | 3 years |
| ID_Q_9ABA..._6 | 4 years |
| ID_Q_9ABA..._7 | 5 years |
| ID_Q_9ABA..._8 | More than 5 years |

## Corporate & Commercial Law Experience (select[name*="124"])

| Option ID | Text |
|-----------|------|
| ID_Q_124_V_2_A_664 | No experience |
| ID_Q_124_V_2_A_665 | Less than 1 year |
| ID_Q_124_V_2_A_666 | 1 year |
| ID_Q_124_V_2_A_667 | 2 years |
| ID_Q_124_V_2_A_668 | 3 years |
| ID_Q_124_V_2_A_669 | 4 years |
| ID_Q_124_V_2_A_670 | 5 years |
| ID_Q_124_V_2_A_671 | More than 5 years |

## Notice Period (input[name*="385"])

| Option ID | Text |
|-----------|------|
| ID_Q_385_V_2_A_2535 | None, I'm ready to go now |
| ID_Q_385_V_2_A_2536 | Less than 1 month |
| ID_Q_385_V_2_A_2537 | 1 month |
| ID_Q_385_V_2_A_2538 | 2 months |
| ID_Q_385_V_2_A_2539 | More than 2 months |

## Languages (input[name*="180"])

| Option ID | Language |
|-----------|----------|
| ID_Q_180_V_1_A_1032 | English |
| ID_Q_180_V_1_A_1033 | Bahasa Indonesia |
| ID_Q_180_V_1_A_1034 | Mandarin |
| ID_Q_180_V_1_A_1035 | Japanese |
| ID_Q_180_V_1_A_1036 | French |
| ID_Q_180_V_1_A_1037 | German |
| ID_Q_180_V_1_A_1038 | Korean |
| ID_Q_180_V_1_A_1039 | Other (language not listed) |

## Language Proficiency (input[name*="119"])

| Option ID | Proficiency |
|-----------|-------------|
| ID_Q_119_V_1_A_635 | Speaks proficiently in a professional setting |
| ID_Q_119_V_1_A_636 | Writes proficiently in a professional setting |
| ID_Q_119_V_1_A_637 | Limited proficiency |

## How to Discover New Options

When encountering a new job with different questions, run:

```javascript
agent-browser eval "JSON.stringify({
  selects: [...document.querySelectorAll('select')].map(s => ({
    name: s.name,
    options: [...s.options].map(o => ({value: o.value, text: o.textContent}))
  })),
  radios: [...document.querySelectorAll('input[type=radio]')].map(r => ({
    name: r.name, value: r.value, label: r.labels?.[0]?.textContent
  })),
  checkboxes: [...document.querySelectorAll('input[type=checkbox]')].map(c => ({
    name: c.name, id: c.id, label: c.labels?.[0]?.textContent
  }))
})"
```
