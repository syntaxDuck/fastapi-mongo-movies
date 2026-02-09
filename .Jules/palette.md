# Palette's Journal

## 2026-02-09 - Accessible Form Labels and ARIA Attributes
**Learning:** In a custom design system without Tailwind-like utility classes, explicit labels with proper `htmlFor` and `id` associations are critical for accessibility. While placeholders provide some visual guidance, they are not a replacement for labels, especially for screen readers and during field focus.
**Action:** Always ensure every form input has a corresponding `<label>` element. Use `aria-label` for icon-only buttons or when a visible label is not desired but context is needed for accessibility.
