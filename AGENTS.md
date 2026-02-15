# AGENTS.md --- Agent Execution Guide

This document defines the operational rules, architecture constraints,
and coding standards for AI agents working in this repository.

Agents must prioritize correctness, minimal changes, and adherence to
the existing architecture.

------------------------------------------------------------------------

# 🔴 Agent Operating Rules (READ FIRST)

When modifying this repository:

1.  Prefer modifying existing files over creating new ones.
2.  Do NOT introduce new architectural patterns unless explicitly
    requested.
3.  Follow the established layered architecture strictly.
4.  Match existing naming conventions exactly.
5.  Do not add dependencies without justification.
6.  Write production-quality code --- avoid placeholders, stubs, or TODO
    comments.
7.  Keep functions small and single-purpose.
8.  Never duplicate logic that already exists.
9.  Search the repository for similar implementations before writing
    code.
10. Favor clarity over cleverness.
11. Ask clarifying questions if requirements are ambiguous.
12. Do not perform large refactors unless explicitly instructed.

Failure to follow these rules results in lower-quality contributions.

------------------------------------------------------------------------

# 🔴 Before Writing Code (MANDATORY)

Agents MUST:

✅ Search the repository for existing patterns\
✅ Identify which architectural layer is affected\
✅ Confirm whether tests must be updated\
✅ Reuse utilities whenever possible\
✅ Avoid parallel abstractions

Do NOT immediately generate code.

Reason first.

------------------------------------------------------------------------

# 🔴 Architecture Authority (STRICT)

This project enforces layered architecture:

    API → Service → Repository → Database

Agents must NEVER:

-   Access repositories directly from API routes\
-   Perform database queries inside services\
-   Embed business logic inside routes\
-   Bypass dependency injection

If a task appears to require this --- the design is likely wrong.

Follow the layers.

------------------------------------------------------------------------

# 🔴 Code Modification Style

When updating code:

-   Prefer **minimal diffs**
-   Preserve formatting
-   Do not reorder imports unnecessarily
-   Do not refactor unrelated code
-   Only change what is required
-   Keep files under 500 lines when possible. If logic can be cleanly split
    into separate files while maintaining relevance, prefer smaller files
    for better maintainability. However, do not artificially split logic
    that belongs together.

Large rewrites are discouraged unless explicitly requested.

------------------------------------------------------------------------

# 🔴 Prohibited Practices

Agents must NOT:

-   Rewrite large files without need\
-   Rename public functions silently\
-   Change API contracts without instruction\
-   Introduce global state\
-   Convert async code to sync\
-   Add unnecessary abstractions\
-   Create duplicate services or repositories

When unsure --- choose the simpler solution.

------------------------------------------------------------------------

# 🔴 Dependency Policy

Do NOT add dependencies unless:

✅ The feature cannot be implemented with the current stack\
✅ The dependency is widely adopted and production-safe\
✅ Justification is provided

Prefer the standard library and existing tools.

------------------------------------------------------------------------

# 🔴 Testing Requirements (MANDATORY)

Backend logic changes MUST include:

-   Unit tests for success cases\
-   Unit tests for failure cases

Agents should not consider a task complete without tests.

------------------------------------------------------------------------

# 🔴 Definition of Good Code

Good code in this repository is:

-   Typed\
-   Tested\
-   Async-safe\
-   Architecturally correct\
-   Readable within 30 seconds

Optimize for maintainability.

------------------------------------------------------------------------

# Project Overview

FastAPI MongoDB Movies is a clean architecture application with:

-   **Backend:** FastAPI + Motor (async MongoDB)
-   **Frontend:** React + TypeScript + CSS Modules
-   **Database:** MongoDB (sample_mflix)
-   **Architecture:** Service--Repository pattern with dependency
    injection
-   **Styling:** Design system + responsive breakpoints

------------------------------------------------------------------------

# Development Commands

## Environment Setup

``` bash
uv sync
uv sync --group test
```

## Run Application

Backend:

``` bash
uv run python main.py -b
```

Frontend:

``` bash
cd frontend && pnpm start
```

Both:

``` bash
uv run python main.py -b
uv run python main.py -f
```

## Package Manager

Use **pnpm** for all frontend operations:

```bash
pnpm install
pnpm add <package>
pnpm remove <package>
pnpm start
pnpm test
pnpm typecheck
```

------------------------------------------------------------------------

# Code Style Guidelines

## Type Hints (REQUIRED)

Always use type hints.

``` python
async def get_movie_by_id(movie_id: str) -> Dict[str, Any]:
```

Avoid untyped functions.

------------------------------------------------------------------------

## Naming Conventions

  Element     Convention
  ----------- ------------------
  Classes     PascalCase
  Functions   snake_case
  Variables   snake_case
  Constants   UPPER_SNAKE_CASE

Match existing naming patterns.

------------------------------------------------------------------------

## Import Order

1.  Standard library\
2.  Third-party\
3.  Local (relative within app)

Do not reorder unless necessary.

------------------------------------------------------------------------

# Backend Rules

Agents must:

✅ Use async/await for database operations\
✅ Validate inputs in the service layer\
✅ Raise custom exceptions\
✅ Use dependency injection\
✅ Document public methods\
✅ Follow existing patterns

------------------------------------------------------------------------

## Error Handling Pattern

Services raise domain exceptions.

API routes translate them into HTTP responses.

Never leak raw database errors.

------------------------------------------------------------------------

# Repository Pattern

Repositories handle ONLY data access.

No business logic allowed.

------------------------------------------------------------------------

# Service Pattern

Services contain business logic and validation.

They orchestrate repositories --- never the reverse.

------------------------------------------------------------------------

# Database Rules

-   Use Motor async driver\
-   Manage connections correctly\
-   Never block the event loop\
-   Prefer indexed queries

------------------------------------------------------------------------

# Frontend Agent Rules

Agents must:

✅ Prefer functional components\
✅ Use TypeScript interfaces\
✅ Follow CSS Modules\
✅ Reuse hooks when possible\
✅ Handle loading + error states\
✅ Follow accessibility best practices\
✅ Create granular, reusable components\
✅ Separate concerns between styling and animations\
✅ Use barrel exports for clean imports

Do NOT introduce state libraries unless explicitly requested.

------------------------------------------------------------------------

## Framer Motion

Use **Framer Motion** for all animations and interactions.

### Animation Responsibilities
- **Framer Motion**: Hover effects, tap animations, transitions, transforms
- **CSS**: Base styling, layout, disabled states, visual effects

### Performance Guidelines
- Prefer transform-based animations (`x`, `y`, `scale`, `opacity`)
- Avoid animating layout-heavy properties (width, height, left, top)
- Use `transition` prop for smooth animations
- Implement staggered animations for lists

### Animation Patterns
- Use animation variants for reusable animation logic
- Implement proper `whileHover`, `whileTap`, and `transition` props
- Create shared animation utilities in `/src/utils/animationVariants.ts`
- Follow existing animation patterns in components

------------------------------------------------------------------------

# File Creation Rules

Before creating a new file:

1.  Confirm similar functionality does not exist\
2.  Follow current folder structure\
3.  Use consistent naming\
4.  Create separate files for granular components\
5.  Co-locate CSS modules in `/src/styles/components/`\
6.  Add barrel exports for component groups

## Component File Structure
```
Component.tsx          # Component implementation
Component.module.css   # Component styles (in /src/styles/components/)
index.ts              # Barrel export (for component groups)
```

New files should be rare, but granular component separation is encouraged.

# Frontend Component Organization

## Component Structure

### UI Components (`/src/components/ui/`)
- **Flat structure**: Single components as individual files (Button.tsx, Image.tsx)
- **Grouped structure**: Subdirectories only when multiple variants needed (buttons/, inputs/)
- **Barrel exports**: Use `index.ts` files for clean import paths

### Domain Components (`/src/components/movies/`, `/src/components/genres/`)
- **Feature-based organization**: Group by domain responsibility
- **Granular components**: Create focused, single-purpose components
- **Composition patterns**: Use UI components as building blocks

## CSS Modules Organization

### Styling Structure (`/src/styles/components/`)
- **Mirror component structure**: CSS files follow same organization as components
- **UI components**: `/src/styles/components/ui/`
- **Domain components**: `/src/styles/components/movies/`, `/src/styles/components/genres/`

### Styling Responsibilities
- **Base styling**: Layout, colors, typography, spacing
- **State styling**: Disabled, loading, error states
- **No animations**: All animations handled by Framer Motion

## Component Design Principles

### Granularity
- **Single responsibility**: Each component has one clear purpose
- **Composable**: Components can be combined to create complex UI
- **Reusable**: Design for use across multiple contexts

### Props Interface
- **TypeScript interfaces**: Strong typing for all component props
- **Default values**: Provide sensible defaults for optional props
- **Consistent naming**: Follow established prop naming conventions

### Style Overrides
- **CSS Modules**: Allow style customization through className prop
- **Design system**: Use CSS custom properties for consistent theming
- **Responsive design**: Mobile-first approach with breakpoint utilities

# Frontend Import/Export Patterns

## Component Imports
```typescript
// Individual component imports
import { Button, Image, Badge } from "../ui";

// Domain component imports
import MovieCard from "../movies/MovieCard";
import GenreCard from "../genres/GenreCard";
```

## Style Imports
```typescript
// CSS module imports (relative to component)
import styles from "../../styles/components/ui/Button.module.css";
```

## Barrel Exports
```typescript
// Component group index.ts
export { default as Button } from './Button';
export { default as Image } from './Image';
export type { ButtonProps, ImageProps } from './Button';
```

## Utility Imports
```typescript
// Animation utilities
import { AnimationVariants } from "../../utils/animationVariants";

// Type definitions
import { Movie, Genre } from "../../types";
```

# Logging

Use the project logger.

Avoid prints.

Keep logs structured and professional.

No emojis in backend code.

------------------------------------------------------------------------

# Caching Implementation

Use **React Query (TanStack Query)** for frontend API caching.

## Query Hooks

Create typed query hooks in `frontend/src/hooks/useQueries.ts`:

- `useMovies(params)` - stale time: 5 minutes
- `useMovieById(id)` - stale time: 10 minutes
- `useMovieGenres()` - stale time: 24 hours
- `useMovieTypes()` - stale time: 24 hours
- `useMovieComments(movieId)` - stale time: 2 minutes

## Cache Strategy by Endpoint

| Endpoint | Cache Duration | Rationale |
|----------|---------------|-----------|
| `/movies/genres` | 24 hours | Rarely changes |
| `/movies/types` | 24 hours | Rarely changes |
| `/movies/` | 5 minutes | Paginated, filterable |
| `/movies/{id}` | 10 minutes | Individual movie |
| `/comments/movie/{id}` | 2 minutes | Can change |

## Provider Setup

Wrap app in `QueryClientProvider` in `App.tsx` with client-side cache config.

------------------------------------------------------------------------

# Environment Variables

Required:

    DB_USER=
    DB_PASS=
    DB_HOST=
    MONGODB_TLS=true

Optional:

    LOG_LEVEL=INFO
    LOG_TO_CONSOLE=true
    LOG_TO_FILE=true

------------------------------------------------------------------------

# If Uncertain

Agents should ask clarifying questions rather than guessing architecture
decisions.
