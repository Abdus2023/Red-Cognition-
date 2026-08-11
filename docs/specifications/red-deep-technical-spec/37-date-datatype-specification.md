# XLIV. The `date!` Datatype — Complete Arithmetic and Navigation

```red
; ══════════════════════════════════════════════════════════════════
; DATE! DATATYPE — COMPLETE ARITHMETIC REFERENCE
; ══════════════════════════════════════════════════════════════════

; ── Construction ─────────────────────────────────────────────────────
d1: 2026-07-29             ; ISO format YYYY-MM-DD
d2: 29-Jul-2026            ; DD-Mmm-YYYY
d3: now                    ; current date+time
d4: now/date               ; date part only
d5: 2026-07-29/14:30:00    ; date+time
d6: 2026-07-29/14:30:00+02:00  ; with timezone

; ── Component access ─────────────────────────────────────────────────
print d1/year              ; → 2026
print d1/month             ; → 7
print d1/day               ; → 29
print d1/weekday           ; → 3 (1=Mon, 7=Sun)
print d1/yearday           ; → day of year (1-366)
print d1/week              ; → ISO week number
print d1/time              ; → none (no time component)
print d1/zone              ; → timezone offset pair

; ── Date arithmetic ──────────────────────────────────────────────────
tomorrow:    d1 + 1                   ; → 2026-07-30
next-week:   d1 + 7                   ; → 2026-08-05
next-month:  d1 + 31                  ; → 2026-08-29
last-year:   d1 - 365                 ; → 2025-07-29

; Difference between dates (in days as integer!)
days-between: d1 - 2026-01-01        ; → 209

; ── Component mutation ───────────────────────────────────────────────
d: copy d1
d/month: 12                           ; → 2026-12-29
d/day: 1                              ; → 2026-12-01

; ── Comparison ───────────────────────────────────────────────────────
print d1 < 2027-01-01   ; → true
print d1 = 2026-07-29   ; → true
sort dates: [2026-03-15  2026-01-01  2026-12-25]

; ── Time component operations ────────────────────────────────────────
dt: 2026-07-29/09:00:00
dt/time: dt/time + 3:30:00         ; add 3.5 hours
dt/hour: dt/hour + 1               ; increment hour

; ── Date formatting ──────────────────────────────────────────────────
; mold produces ISO format
mold 2026-07-29                    ; → "2026-07-29"

; form produces localised format
form 2026-07-29                    ; → "29-Jul-2026"

; Custom formatting
format-date: func [d [date!] fmt [string!]][
    replace/all replace/all replace/all replace/all
        copy fmt
        "YYYY" to-string d/year
        "MM"   to-string d/month
        "DD"   to-string d/day
        "Day"  pick system/locale/days d/weekday
]

print format-date 2026-07-29 "DD/MM/YYYY"      ; → 29/07/2026
print format-date 2026-07-29 "Day, YYYY-MM-DD" ; → Wednesday, 2026-07-29

; ── Calendar utilities ───────────────────────────────────────────────
days-in-month: func [year [integer!] month [integer!]][
    d: to-date reduce [1 month year]
    d/month: d/month + 1
    d/day: 0                   ; day 0 = last day of prev month
    d/day
]

leap-year?: func [year [integer!]][
    any [
        all [0 = mod year 4   not zero? mod year 100]
        0 = mod year 400
    ]
]

; Days remaining in year
days-remaining: func [d [date!]][
    (to-date reduce [31 12 d/year]) - d
]
```