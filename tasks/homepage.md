# Homepage Implementation Plan

## Context
Gameplan is a work collaboration tool centered around **Spaces**. Each Space represents a team, project, or company-level workspace that users can join. Spaces contain **Pods** of three types: Discussions, Tasks, and Documents. Multiple pods of the same type can exist with different titles (e.g., "Work Updates" and "Announcements" discussion pods).

The Space overview page with customizable pod layouts is already built. Now we need to create a personalized homepage where users can pin and manage their favorite spaces, plus see their assigned tasks.

## Current State Analysis
- `MySpaces.vue` component exists but is empty (`frontend/src/pages/MySpaces/MySpaces.vue`)
- Route `/spaces` already configured to use `MySpaces.vue`
- `SpaceList.vue` exists for browsing all spaces with join/leave functionality
- Backend has `GP Pinned Project` doctype with `project`, `user`, `team`, and `order` fields
- API method `recent_projects()` excludes pinned projects
- Existing components: `SpaceOptions.vue`, `TaskList.vue`, `MyTasks.vue`
- Data composables: `useSpace()`, `useGroupedSpaces()`, `hasJoined()`, `useTask()`

## Implementation Plan

### Phase 1: Core MySpaces Component Structure
**Files to create/modify:**
- [ ] `frontend/src/pages/MySpaces/MySpaces.vue` - Main component
- [ ] `frontend/src/pages/MySpaces/SpaceCard.vue` - Individual space card component
- [ ] `frontend/src/pages/MySpaces/MyTasksSection.vue` - Tasks section component
- [ ] `frontend/src/data/pinnedSpaces.ts` - Data composable for pinned spaces

**MySpaces.vue Layout:**
```
┌─────────────────────────────────┐
│ Header: "My Spaces" + Customize │
├─────────────────────────────────┤
│ My Spaces Section               │
│ - Pinned space cards (grid)     │
│ - Empty state if no pins        │
│ - "Browse all spaces" link      │
├─────────────────────────────────┤
│ My Tasks Section                │
│ - Recent assigned tasks         │
│ - "View all tasks" link         │
└─────────────────────────────────┘
```

### Phase 2: Data Layer Implementation
**No new backend APIs needed!** Use existing `useList` composable pattern.

**Frontend data composable (`data/pinnedSpaces.ts`):**
- [ ] Create `usePinnedSpaces()` composable with useList for GP Pinned Project
- [ ] Implement `pinSpace()` method using insert.submit
- [ ] Implement `unpinSpace()` method using delete.submit
- [ ] Implement `reorderSpaces()` method using setValue.submit
- [ ] Implement `isPinned()` helper method
- [ ] Add proper TypeScript types for GPPinnedProject
```typescript
export function usePinnedSpaces() {
  const pinnedSpaces = useList<GPPinnedProject>({
    doctype: 'GP Pinned Project',
    fields: ['name', 'project', 'user', 'order'],
    filters: { user: useUser('sessionUser').name },
    orderBy: 'order asc',
    cacheKey: 'pinnedSpaces',
    immediate: true,
  })

  const pinSpace = (spaceId: string) => {
    return pinnedSpaces.insert.submit({
      project: spaceId,
      user: useUser('sessionUser').name,
      order: (pinnedSpaces.data?.length || 0) + 1
    })
  }

  const unpinSpace = (spaceId: string) => {
    const pinnedSpace = pinnedSpaces.data?.find(p => p.project === spaceId)
    if (pinnedSpace) {
      return pinnedSpaces.delete.submit({ name: pinnedSpace.name })
    }
  }

  const reorderSpaces = (orderedSpaceIds: string[]) => {
    const updatePromises = orderedSpaceIds.map((spaceId, index) => {
      const pinnedSpace = pinnedSpaces.data?.find(p => p.project === spaceId)
      if (pinnedSpace) {
        return pinnedSpaces.setValue.submit({
          name: pinnedSpace.name,
          order: index + 1
        })
      }
    }).filter(Boolean)

    return Promise.all(updatePromises)
  }

  const isPinned = (spaceId: string) => {
    return pinnedSpaces.data?.some(p => p.project === spaceId) || false
  }

  return {
    pinnedSpaces,
    pinSpace,
    unpinSpace,
    reorderSpaces,
    isPinned
  }
}
```

### Phase 3: Space Cards with Pin/Unpin
**SpaceCard.vue features:**
- [ ] Display space icon, title, description
- [ ] Show member avatars (max 5)
- [ ] Unread count indicator
- [ ] Click to navigate to SpaceOverview
- [ ] Drag handle for reordering (in customize mode)
- [ ] Pin/unpin via `SpaceOptions` context menu

**Design pattern:** Similar to existing `PodDiscussions.vue` cards but for spaces

**SpaceOptions integration:**
- [ ] Add "Pin space" / "Unpin space" option to existing `SpaceOptions.vue` menu
- [ ] Use `usePinnedSpaces()` composable to check current pin state
- [ ] Toggle pin/unpin functionality integrated into existing options

### Phase 4: Customize Mode
**Customize functionality:**
- [ ] Toggle between view/edit modes
- [ ] Drag and drop to reorder pinned spaces with minimal animations
- [ ] Save changes button
- [ ] Cancel changes

**Implementation approach:** Similar to `SpaceCustomize.vue` drag-and-drop pattern

**Animation style:** Minimal transitions - simple opacity and transform changes during drag operations

### Phase 5: My Tasks Integration
**MyTasksSection.vue:**
- [ ] Show recent tasks assigned to current user (limit 5-7)
- [ ] Task status indicators
- [ ] Due date highlights
- [ ] Link to full MyTasks page
- [ ] Reuse existing `TaskList.vue` component logic

## Technical Implementation Details

### Key Components Structure
- [ ] Create `MySpaces/` directory structure
- [ ] Set up component files and imports
- [ ] Establish component communication patterns

### Data Flow
- [ ] Implement `MySpaces.vue` loads pinned spaces using `usePinnedSpaces()` composable
- [ ] Set up `pinnedSpaces` uses `useList` with `GP Pinned Project` doctype filtered by current user
- [ ] Configure Space cards show real-time data from `useSpace()` composable for each pinned project
- [ ] Implement Pin/unpin actions use `pinnedSpaces.insert.submit()` and `pinnedSpaces.delete.submit()`
- [ ] Set up Reordering uses `pinnedSpaces.setValue.submit()` to update order field on each record
- [ ] Configure Tasks section uses filtered `TaskList` component logic

### Styling Approach
- [ ] Use existing Tailwind semantic classes (`bg-surface-*`, `text-ink-*`)
- [ ] Implement Grid layout for space cards (responsive: 1-3 columns)
- [ ] Match existing design patterns from `SpaceOverview` and pod components
- [ ] Ensure consistent with current UI patterns

### Integration Points
- [ ] Link to `SpaceList.vue` for browsing all spaces
- [ ] Link to `MyTasks.vue` for full task management
- [ ] Extend existing `SpaceOptions.vue` with pin/unpin functionality
- [ ] Maintain consistent breadcrumb pattern

## Implementation Notes
Based on clarifications:
1. **No maximum limit** on pinned spaces - users can pin as many as needed
2. **Space card previews** - not implemented initially, can be added later
3. **Pin/Unpin location** - integrated into existing `SpaceOptions` context menu
4. **Animation style** - minimal transitions for drag-and-drop operations

## Additional Implementation Details

### SpaceOptions.vue Extension
Add pin/unpin option to the existing options computed array:
- [ ] Import `usePinnedSpaces()` composable in SpaceOptions.vue
- [ ] Add pin/unpin option to options computed array
- [ ] Implement pin/unpin click handlers
- [ ] Add appropriate icons (LucidePin/LucidePinOff)
```typescript
// In SpaceOptions.vue
const { isPinned, pinSpace, unpinSpace } = usePinnedSpaces()

// Add to options array
{
  label: isPinned(props.spaceId) ? 'Unpin space' : 'Pin space',
  icon: LucidePin, // or LucidePinOff
  onClick: () => {
    if (isPinned(props.spaceId)) {
      unpinSpace(props.spaceId)
    } else {
      pinSpace(props.spaceId)
    }
  }
}
```
