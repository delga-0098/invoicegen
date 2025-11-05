# invoicegen
[![ci](https://github.com/delga-0098/invoicegen/actions/workflows/main.yml/badge.svg)](https://github.com/delga-0098/invoicegen/actions/workflows/main.yml)

## CSV Contract (Maintenance Job Lines)

This defines the structure and validation rules for the job line CSV files used by **InvoiceGen**.

### Required Columns

| Column Name | Example | Description |
|--------------|----------|--------------|
| **Date** | `10/02/2025` | Date work was done (MM/DD/YYYY). Must be a valid calendar date. |
| **Address** | `123 Elm St` | The property where the job was performed. |
| **Unit** | `A` | The unit in chich the work was performed. |
| **Description** | `Fix leaking sink (P-trap)` | Description of work performed. Category can be embedded in this text if desired. |
| **Quantity** | `1.5` | Amount of work done (hours, units, etc.). Must be a non-negative number. |
| **Unit Price** | `65` | Rate per unit. Must be a non-negative number. |
| **Total** | `97.50` | Optional — ignored by the system. Computed internally as `Quantity * Unit Price`. Mismatches produce a warning. |
| **Paid** | `TRUE` | Determines if the work was paid for already. |

---

### Validation Rules

- **Date:** Must follow the `MM/DD/YYYY` format and represent a valid date (e.g., `10/32/2025` is invalid).  
- **Address:** Cannot be empty.
- **Unit:** Cannot be empty.
- **Description:** Cannot be empty and must be less than 2000 characters.  
- **Quantity / Unit Price:**  
  - Must be valid decimal numbers (`1.5`, `45`, `0.25`).  
  - No `$`, commas, or text allowed.  
  - Must be ≥ 0.  
- **Total:** Ignored for math. If it differs from the computed total, a warning is reported.  
- **Paid:** Must be a bool operation.
- **Extra Columns:** Ignored with a notice (e.g., “Unknown column: Technician”).  
- **Blank Lines:** Ignored automatically.

---

### Example CSV

```csv
Date,Address,Unit,Description,Unit Price,Quantity,Total,Paid
11/1/2024,Elderwood,A,Repair leaking toilet.,100,1,100,TRUE
11/8/2024,Elderwood,Single,Change doorknob.,100,1,100,FALSE
11/10/2024,Elderwood,Single,Paint everything.,1000,1,1000,TRUE
11/10/2024,Elderwood,Single,Clean bathroom and floor. Trow out trash.,150,1,150,FALSE
11/15/2024,Elizabeth,C,Unclog sink.,80,1,80,FALSE
11/16/2014,Elizabeth,D,Repair hole in wall.,80,1,80,TRUE
11/29/2024,Elizabeth,C,Connect filter.,75,1,75,FALSE
12/13/2024,Elizabeth,B,Repair leaking sink.,80,1,80,FALSE
2/19/2025,Elizabeth,G,Unclog sink.,80,1,80,TRUE
11/16/2024,Hill,A,Repair leaking toilet.,80,1,80,FALSE
11/16/2024,Hill,A,Repair toilet floater.,75,1,75,FALSE
11/15/2024,Hill,A,Change sink faucet.,150,1,150,TRUE
12/29/2021,Hill,Front,Repair leak.,100,1,100,FALSE
```