# Variant: Calm Editorial

## Design stance
Luftig, textdriven layout — som Linear möter en dark-mode editor. Fokus på chattflödet. Sidebar är sekundär navigation.

## Key choices
- Layout: Sidebar (280px) + chat (flex)
- Typography: Inter för allt, JetBrains Mono för code/data
- Color: Mörk #0a0a12 bakgrund, Bone White #e3e3e4 text, cyan #00d4ff accent
- Interaction: Minimal — agent-klick växlar vy, textinput är primär handling

## Trade-offs
- Strong at: Lugn känsla, läsbar chatt, tydlig hierarki
- Weak at: GPU-data syns bara i sidebar-footer, agent-översikt tar mycket plats utan att visa mycket info

## Best for
Användare som chattar mycket — vill ha rent, fokuserat gränssnitt med agenter som sekundär vy.
