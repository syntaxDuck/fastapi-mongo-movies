## 2026-02-09 - Accessible Form Labels Pattern
**Learning:** In complex search interfaces, manual label management often leads to disconnected or missing programmatic associations between labels and inputs. Internalizing label and ID management within core UI components (Input, Select, RangeInput) using React's `useId` hook ensures that every input is always correctly associated with a `<label>` or `<legend>`, improving screen reader support without increasing developer friction.
**Action:** Use the enhanced `Input`, `Select`, and `RangeInput` components which now handle their own unique IDs and label associations. Prefer `RangeInput` for numeric ranges as it now correctly uses semantic `<fieldset>` and `<legend>` elements.

## 2026-02-10 - Inline Form Action Layout
**Learning:** Absolute positioning of elements within a form field (like a search icon or clear button) can lead to "pointer-event interception" where one element blocks clicks on another if they overlap. Using compact icons instead of text labels for these inline actions reduces the hit area conflict while maintaining visual clarity.
**Action:** Use compact icons for inline form actions (like "Clear" or "Search") and ensure they have descriptive `aria-label` attributes. Maintain adequate padding on the input to prevent text from overlapping the icons.
