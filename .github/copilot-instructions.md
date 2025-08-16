---
description: 'VueJS 3 development standards and best practices with Composition API and TypeScript'
applyTo: 'frontend/**/*.vue, frontend/**/*.ts, frontend/**/*.js, gameplan/**/*.py'
---

# Project Name: Gameplan

Gameplan is an open-source work collaboration tool for modern teams. It encourages thoughtful
communication and deep-thinking.

Spaces is how you can organize information. A Space has a title, icon, description and cover image.
People can join a space.

It contains something called Pods. A pod is of multiple types: Discussions, Tasks, Documents, Chats.
A space can have one or more pods. It can have multiple pods of the same type as well. However, two
pods of the same type cannot have the same title. The title of the pod gives it semantic meaning.

For e.g., in a space called Engineering we can have various pods:
1. Discussions (type: Discussions) - for general discussions about engineering
2. Work Updates (type: Discussions) - to add work updates
3. Onboarding (type: Documents) - onboarding documents for new engineers
4. Chats (type: Chats) - general chit chat for engineers
5. GitHub Notifications (type: Chats) - a bot adds important notifications from github (new prs, new releases, etc)

Spaces and Pods are the building blocks of how you can organize information in your team.

A space can be created for global context (Company level), team context (Engineering), or a specific
project (Conference 2025).

# Gameplan: Tech Stack

- Backend: Frappe Framework
- Frontend Vue 3 App with Vite dev server


# Frontend: VueJS 3 Development Instructions

Instructions for building high-quality VueJS 3 applications with the Composition API, TypeScript, and modern best practices.

## Project Context
- `./frontend/` is the main directory for VueJS frontend code
- Vue 3.x with Composition API as default
- TypeScript for type safety
- Single File Components (`.vue`) with `<script setup lang="ts">` syntax
- Vite as the build tool
- We don't use any state management libraries
- Official Vue style guide and best practices
- frappe-ui for UI components and data fetching utilities
- The folder `./frappe-ui/` is a local copy of the frappe-ui library, you can look through it to check what components are available to use.

## Project Structure
- `./frontend/src/` contains the main source code
- `./frontend/src/components/` for reusable components
- `./frontend/src/pages/` for page components
- `./frontend/src/data/` for data fetching composables
- `./frontend/src/utils/` for utility functions and helpers
- `./frontend/src/directives/` for custom directives

## Development Standards

### Architecture
- Favor the Composition API (`setup` functions and composables) over the Options API
- Organize components and composables by feature or domain for scalability
- Separate UI-focused components (presentational) from logic-focused components (containers)
- Put page components in a `./frontend/src/pages/` directory
- Use a `./frontend/src/components/` directory for shared UI components
- For small components, just put them in one file `pages/Page.vue` or `./frontend/src/components/Component.vue`
- For larger components, split it into smaller components and composables and put them in a folder named after the component and include an `index.ts` (e.g., `./frontend/src/components/MyComponent/index.ts`, `pages/MyPage/index.ts`)

### TypeScript Integration
- Enable `strict` mode in `tsconfig.json` for maximum type safety
- Use `defineComponent` or `<script setup lang="ts">` with `defineProps` and `defineEmits`
- Leverage `PropType<T>` for typed props and default values
- Use interfaces or type aliases for complex prop and state shapes
- Define types for event handlers, refs, and `useRoute`/`useRouter` hooks
- Implement generic components and composables where applicable

### Component Design
- Adhere to the single responsibility principle for components
- Use PascalCase for component names and for file names
- Keep components small and focused on one concern
- Use `<script setup lang="ts">` syntax for brevity and performance
- Validate props with TypeScript; use runtime checks only when necessary
- Favor slots and scoped slots for flexible composition
- Prefer `useTemplateRef` for accessing DOM elements instead of `ref` or `querySelector` in `setup`

### State Management
- Don't use any state management libraries like Vuex or Pinia
- For simple local state, use `ref` and `reactive` within `setup`
- Use `computed` for derived state
- Keep state normalized for complex structures

### Composition API Patterns
- Create reusable composables for shared logic, e.g., `useFetch`, `useAuth`
- Use `watch` and `watchEffect` with precise dependency lists
- Cleanup side effects in `onUnmounted` or `watch` cleanup callbacks
- Use `provide`/`inject` sparingly for deep dependency injection

### Styling
- Always prefer tailwindcss for styling
- Use utility classes for layout and spacing
- Use semantic class names wherever possible:
  - Background classes: `bg-surface-white`, `bg-surface-gray-1`, `bg-surface-gray-2`, ..., `bg-surface-gray-9`, `bg-surface-black`
  - Text classes: `text-ink-white`, `text-ink-gray-1`, `text-ink-gray-2`, ..., `text-ink-gray-9`, `text-ink-black`
  - Fill classes: `fill-ink-*`
  - Placeholder classes: `placeholder-ink-*`
  - Border classes: `border-outline-white`, `border-outline-gray-1`, `border-outline-gray-2`, ..., `border-outline-gray-5`, `border-outline-black`
  - Ring classes: `ring-outline-*`
  - Divide classes: `divide-ink-gray-*`
  - Font size classes: `text-xs`, `text-sm`, `text-base`, `text-lg`, `text-xl`, `text-2xl`, `text-3xl`
  - Font size for multiline text: `text-p-xs`, `text-p-sm`, `text-p-base`, `text-p-lg`, `text-p-xl`, `text-p-2xl`
- Always use gray shades for everything, never use color shades even for primary states
- Other than these, use standard Tailwind CSS classes for everything else
- Sparingly use `<style scoped>` when necessary
- Implement mobile-first, responsive design with CSS Grid and Flexbox
- Ensure styles are accessible (contrast, focus states)

### Performance Optimization
- Apply `v-once` and `v-memo` for static or infrequently changing elements
- Avoid unnecessary watchers; prefer `computed` where possible
- Tree-shake unused code and leverage Vite’s optimization features

### Data Fetching
- Use `useDoc`, `useList`, and `useCall` from frappe-ui for data fetching
- Look at `./frontend/src/data/` for examples of data fetching composables
- Handle loading, error, and success states explicitly

When working with a list of documents, use the `useList` composable:
```ts
const items = useList<Doctype>({
  doctype: 'My Doctype',
  filters: () => ({ field: 'value' }),
  fields: ['name', 'title', 'modified'],
  limit: 10,
  cacheKey: 'my-doctype-list',
  immediate: true,
})
// update fields in a single row based on its name
items.setValue.submit({ name: '<id>', title: 'Item Title' }) // items.setValue.loading, items.setValue.error
// add a new item
items.insert.submit({ title: 'New Item' })
// delete an item
items.delete.submit({ name: '<id>' })
```

When working with a single document, use the `useDoc` composable:
```ts
const item = useDoc<Doctype>({
  doctype: 'My Doctype',
  name: '<id>',
  methods: {
    customMethod: 'custom_method', // custom_method is a server-side whitelisted class method in my_doctype.py
  }
})

item.doc.title // access fields
item.setValue.submit({ title: 'Updated Title' }) // update fields
item.delete.submit() // delete the document
item.customMethod.submit({ param: 'value' }) // call custom method
```

### Icons

- Always use lucide icons for consistency
- Never use FeatherIcon component
- To use a lucide icon, directly add the component in the template, no need to import it in the script section:
  ```vue
  <template>
    <LucideIconName class="size-4" />
  </template>
  ```
- To use a lucide icon in the script section, import it like this, ignore any typescript errors related to lucide icons:
  ```ts
  import LucideIconName from '~icons/lucide/icon-name'
  ```

## Utilities and Composables

- @vueuse/core is installed in this project
- If there is a scenario where a vueuse composable can simplify the code, prefer using it over custom implementations
- common composables include `useLocalStorage`, and `useDebounce`
- dont use `useFetch` because we use `useList`, `useDoc`, `useCall` for data fetching from frappe-ui

### Error Handling
- Use global error handler (`app.config.errorHandler`) for uncaught errors
- Wrap risky logic in `try/catch`; provide user-friendly messages
- Use `errorCaptured` hook in components for local boundaries
- Display fallback UI or error alerts gracefully

### Forms and Validation
- Build forms with controlled `v-model` bindings
- Validate on blur or input with debouncing for performance
- Handle file uploads and complex multi-step forms in composables
- Ensure accessible labeling, error announcements, and focus management

### Routing
- Use Vue Router 4 with `createRouter` and `createWebHistory`
- Implement nested routes and route-level code splitting
- Protect routes with navigation guards (`beforeEnter`, `beforeEach`)
- Use `useRoute` and `useRouter` in `setup` for programmatic navigation
- Manage query params and dynamic segments properly


### Security
- Avoid using `v-html`; sanitize any HTML inputs rigorously
- Use CSP headers to mitigate XSS and injection attacks
- Validate and escape data in templates and directives
- Store sensitive tokens in HTTP-only cookies, not `localStorage`

### Accessibility
- Use semantic HTML elements and ARIA attributes
- Manage focus for modals and dynamic content
- Provide keyboard navigation for interactive components
- Add meaningful `alt` text for images and icons
- Ensure color contrast meets WCAG AA standards

## Implementation Process
1. Plan component and composable architecture
3. Create core UI components and layout
5. Implement data fetching and state logic
10. Ensure accessibility compliance

## Additional Guidelines
- Follow Vue’s official style guide (vuejs.org/style-guide)
- Use ESLint (with `plugin:vue/vue3-recommended`) and Prettier for code consistency
- Write meaningful commit messages and maintain clean git history
- Keep dependencies up to date and audit for vulnerabilities
- Document complex logic with JSDoc/TSDoc
- Use Vue DevTools for debugging and profiling

## Common Patterns
- Renderless components and scoped slots for flexible UI
- Compound components using provide/inject
- Custom directives for cross-cutting concerns

# Backend: Gameplan is a Frappe Framework App

## Backend project structure
- `./gameplan/` is the main directory for backend code
- `./gameplan/gameplan/` contains the main doctypes and business logic
- `./gameplan/gameplan/doctype/` contains individual doctype definitions
- `./gameplan/api.py` contains some API endpoints and logic

## Bench commands

- Always run bench commands from the `frappe-bench` directory
- Always run bench commands with the `--site` flag to specify the site
- Assume `gameplan.frappe.test` local site already exists in the bench setup
- Run any site commands with `bench --site gameplan.frappe.test <command>`

## Server side code debugging
- If there is a need to print debug information, create a python file inside the `gameplan` directory, e.g., `./gameplan/debug.py`
- Create a function in that file, e.g., `def execute():`
- Use `print()` statements in that file to log debug information
- Run the debug file with `bench --site gameplan.frappe.test execute gameplan.debug.execute`
- This will execute the file and print the output to the console

## Vite dev server
- Assume the Vite dev server is already running on port 8080
- Use `http://gameplan.frappe.test:8080/g` to access the frontend during development

## Miscellaneous

- Ignore newline errors in all files

## Code Comments

- Only add comments that explain why something is done, not what is done
- Use JSDoc/TSDoc for documenting complex functions, components, and composables
- Don't add unnecessary comments for simple code
- Use inline comments sparingly, only when the code is not self-explanatory
