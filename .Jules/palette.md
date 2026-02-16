## 2026-02-09 - Accessible Form Labels Pattern
**Learning:** In complex search interfaces, manual label management often leads to disconnected or missing programmatic associations between labels and inputs. Internalizing label and ID management within core UI components (Input, Select, RangeInput) using React's `useId` hook ensures that every input is always correctly associated with a `<label>` or `<legend>`, improving screen reader support without increasing developer friction.
**Action:** Use the enhanced `Input`, `Select`, and `RangeInput` components which now handle their own unique IDs and label associations. Prefer `RangeInput` for numeric ranges as it now correctly uses semantic `<fieldset>` and `<legend>` elements.

## 2026-02-10 - UI Component Styling Convention
**Learning:** In this project, UI components (Button, Badge) use a specific naming convention for CSS module classes: `[componentName][Variant/Size]` (e.g., `buttonPrimary`, `badgeSm`). Standard dynamic access like `styles[variant]` fails because the variant name is not enough; it must be prefixed and capitalized to match the CSS module's exported keys.
**Action:** When adding or modifying UI components with variants or sizes, ensure the class mapping logic correctly matches the CSS module naming convention (e.g., `styles['button' + variant.charAt(0).toUpperCase() + variant.slice(1)]`).

## 2026-02-12 - Stable State Initialization
**Learning:** Initializing state from props in a `useEffect` with the prop as a dependency (e.g., `initialFilters`) causes infinite re-render loops if the parent passes a literal object (e.g., `initialFilters={{}}`). Objects in JS have different identities on every render even if their content is identical.
**Action:** Initialize state once using the functional initializer in `useState`. If prop-to-state synchronization is required, ensure the parent memoizes the prop or use a deep equality check before updating state in `useEffect`.

## 2026-02-14 - Keyboard Parity for Hover-Only Content
**Learning:** Interactive components that reveal content only on hover (such as movie titles in `MovieCard`) are inaccessible to keyboard and screen reader users. Using Framer Motion's `whileFocus` (or `whileFocusWithin`) in conjunction with `whileHover` and shared variants ensures visual parity. For non-link interactives, adding `tabIndex={0}`, `role="button"`, and handling `Enter`/`Space` keys is essential for a complete accessible experience.
**Action:** Always ensure hover-triggered overlays also respond to focus. Implement proper keyboard handlers and ARIA roles for any custom interactive elements that aren't natively focusable.

## 2026-02-15 - Minimalist Accessibility with focus-within
**Learning:** For components that already have established CSS-based hover transitions (like `GenreCard`), adding accessibility for keyboard users can be achieved with minimal overhead by using the CSS `:focus-within` pseudo-class. This provides a lightweight alternative to full Framer Motion refactoring when only simple visibility toggling is needed, while still fulfilling accessibility requirements.
**Action:** Use `:focus-within` on parent link/button containers to reveal absolute-positioned children that are otherwise only visible on hover.
