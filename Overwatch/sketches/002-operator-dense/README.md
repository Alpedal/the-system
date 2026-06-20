# Variant: Operator Dense

## Design stance
Kompakt, informationsrik dashboard — all data synlig samtidigt. Som Grafana möter en terminal-multiplexer. Power-user-verktyg.

## Key choices
- Layout: CSS Grid 3x2 — agenter (2 kol), telemetri, chatt, rutt-logg
- Typography: JetBrains Mono för all data, Inter för chatt
- Color: Samma mörka palett, men mer färgkodad data
- Interaction: Kort-klick växlar agent-fokus, chatt alltid synlig, rutt-logg streamar

## Trade-offs
- Strong at: All information synlig direkt, telemetri live, routing transparent
- Weak at: Kan kännas överväldigande för nya användare, liten chattruta

## Best for
Power users som vill övervaka hela systemet — ser agenter, GPU, chatt, och routing samtidigt.
