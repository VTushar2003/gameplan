# Chats Pod Implementation Plan

## Context & Overview
Based on the existing project structure, Gameplan uses a **pod-based architecture** where each Space can have multiple pods of different types: Discussions, Tasks, and Documents. The system uses the `GP Pod` doctype to define pods, and each pod type has its own dedicated components and routing.

Now we need to add **Chats** as a new pod type that enables real-time messaging within spaces.

## Current Architecture Understanding
- **Pods**: Defined in `GP Pod` doctype with types: "Discussions", "Tasks", "Documents"
- **Pod Components**: `PodDiscussions.vue`, `PodTasks.vue`, `PodDocuments.vue` show previews in space overview
- **Pod Pages**: `SpaceDiscussions.vue`, `SpaceTasks.vue`, `SpaceDocuments.vue` show full pod content
- **Routing**: Each pod type has dedicated routes (e.g., `/space/:spaceId/discussions/:podId`)
- **Data Layer**: Uses frappe-ui's `useList`, `useDoc` composables for data fetching

## Implementation Plan

### Phase 1: Backend Infrastructure

#### 1.1 New Doctype: `GP Chat Message`
- [ ] Create `gameplan/gameplan/doctype/gp_chat_message/gp_chat_message.json`
- [ ] Add required fields:
  - [ ] `content` (Text Editor, required)
  - [ ] `project` (Link to GP Project, required)
  - [ ] `pod` (Link to GP Pod, required)
  - [ ] `message_type` (Select: text/file/image, default: text)

  - [ ] `reactions` (Table, GP Reaction)
  - [ ] `tags` (Table, GP Tag Link)
  - [ ] `deleted_at` (Datetime)
  - [ ] `edited_at` (Datetime)

#### 1.2 Update `GP Pod` Doctype
- [ ] Update `gameplan/gameplan/doctype/gp_pod/gp_pod.json`
- [ ] Add "Chats" to the "type" field options: "Discussions\nDocuments\nTasks\nChats"

#### 1.3 Backend Python Class
- [ ] Create `gameplan/gameplan/doctype/gp_chat_message/gp_chat_message.py`
- [ ] Implement `GPChatMessage` class extending `Document` and `HasMentions`
- [ ] Add validation methods:
  - [ ] `validate()` - prevent reply to self
  - [ ] `after_insert()` - update pod activity, notify mentions
  - [ ] `after_delete()` - update pod activity
  - [ ] `update_project_tool_activity()` - update last modified time
- [ ] Add whitelisted methods:
  - [ ] `edit_message(content)` - edit message content

#### 1.4 Data Fetching
- **Using `useList` directly** with built-in filters and pagination

### Phase 2: Frontend Infrastructure

#### 2.1 Update Pod Type Configuration
- [ ] Update `frontend/src/pages/SpaceOverview/SpaceCustomize.vue`
- [ ] Add "Chats" to `podTypeOptions` array
- [ ] Add `LucideMessageCircle` icon for Chats in `getPodIcon()`
- [ ] Add chat description in `getPodSummary()`

#### 2.2 Data Composable for Chat Messages
- [ ] Create `frontend/src/data/chatMessages.ts`
- [ ] Define `ChatMessage` interface with all required fields
- [ ] Implement `useChatMessages()` composable:
  - [ ] Use `useList` directly with GP Chat Message doctype
  - [ ] Support filtering by pod using filters
  - [ ] Default order: creation asc (oldest first)
  - [ ] Include caching and immediate loading
  - [ ] Use existing frappe-ui patterns for error/loading states
- [ ] Implement `useChatMessage()` for individual message operations:
  - [ ] Use `useDoc` for individual message operations
  - [ ] Support editing messages via setValue
  - [ ] Support deleting messages via delete method
  - [ ] Cache individual messages
  - [ ] Follow existing frappe-ui patterns

#### 2.3 Pod Preview Component
- [ ] Create `frontend/src/pages/SpaceOverview/PodChats.vue`
- [ ] **Use existing Gameplan components** (Avatar, TextEditor for rendering)
- [ ] **Follow existing pod styling patterns** from PodDiscussions/PodTasks
- [ ] Display recent messages (last 3)
- [ ] Show user avatars and timestamps
- [ ] Show message content preview (stripped HTML)
- [ ] Handle empty state with existing patterns
- [ ] Use consistent spacing values from other pod components

#### 2.4 Full Chat Pod Page (Start with blank component)
- [ ] Create `frontend/src/pages/SpaceChats.vue` **as a blank component first**
- [ ] **Use existing Gameplan layout patterns** (PageContainer, etc.)
- [ ] **Use frappe-ui components** wherever possible (Button, TextEditor, etc.)
- [ ] **Follow existing spacing patterns** from other Space pages
- [ ] Then implement features:
  - [ ] Clean, centered layout using existing container patterns
  - [ ] Header with pod title using existing header components
  - [ ] Scrollable messages container with standard padding values
  - [ ] Fixed input area at bottom using existing input patterns
  - [ ] Date separators using existing text styling
  - [ ] Auto-scroll to bottom on new messages

#### 2.5 Chat Components

##### ChatMessageList Component
- [ ] Create `frontend/src/components/Chat/ChatMessageList.vue`
- [ ] **Use existing Gameplan/frappe-ui components**:
  - [ ] Button component for "Load more"
  - [ ] Use existing list patterns and spacing
  - [ ] Follow existing loading/error state patterns
- [ ] Features:
  - [ ] Display list of messages with existing spacing patterns
  - [ ] "Load more" button styled with existing Button component
  - [ ] Message grouping by user and time (15+ minute intervals)
  - [ ] Smart avatar/timestamp display logic
  - [ ] Empty state using existing patterns with appropriate messaging

##### ChatMessage Component
- [ ] Create `frontend/src/components/Chat/ChatMessage.vue`
- [ ] **Use existing Gameplan/frappe-ui components**:
  - [ ] Avatar component from frappe-ui
  - [ ] Dropdown component for message actions
  - [ ] UserMention component for @mentions
  - [ ] Follow existing button/icon patterns
  - [ ] Use existing spacing/padding values
- [ ] Features:
  - [ ] User avatar using existing Avatar component
  - [ ] User name and timestamp with existing text styles
  - [ ] Message content rendering with proper typography
  - [ ] Reactions support using existing patterns
  - [ ] @mentions support using existing UserMention component
  - [ ] Inline editing mode with existing TextEditor
  - [ ] Message actions dropdown using existing Dropdown component

##### ChatMessageInput Component
- [ ] Create `frontend/src/components/Chat/ChatMessageInput.vue`
- [ ] **Use existing Gameplan/frappe-ui components**:
  - [ ] TextEditor component for message composition
  - [ ] Button component for send button
  - [ ] Follow existing form patterns and spacing
  - [ ] Use existing input styling patterns
- [ ] Features:
  - [ ] TextEditor component for message composition
  - [ ] Send button using existing Button component
  - [ ] Keyboard shortcuts (Ctrl/Cmd + Enter)
  - [ ] @mentions support in TextEditor
  - [ ] Follow existing form submission patterns
  - [ ] Auto-resize following existing input patterns

### Phase 3: Routing & Integration (Start with routing first)

#### 3.1 Add Chat Routes (PRIORITY: Do this first)
- [ ] Update `frontend/src/router.ts`
- [ ] Add `SpaceChats` route to Space children:
  - [ ] Path: `chats/:podId?`
  - [ ] Component: SpaceChats.vue (blank component initially)
  - [ ] Props: true
- [ ] Test route navigation works before building components

#### 3.2 Update Space Overview (Do this second)
- [ ] Update `frontend/src/pages/SpaceOverview/SpaceOverview.vue`
- [ ] Add router-link for Chat pods:
  - [ ] Condition: `pod.type === 'Chats'`
  - [ ] Route to: `SpaceChats` with spaceId and podId params
  - [ ] Render: `PodChats` component (create after routing works)
- [ ] Import `PodChats` component
- [ ] Test pod navigation works in space overview

### Phase 4: TypeScript Types

#### 4.1 Update Doctype Types
- [ ] Update `frontend/src/types/doctypes.ts`
- [ ] Add 'Chats' to `GPPod['type']` union type
- [ ] Create `GPChatMessage` interface:
  - [ ] All required fields with proper types
  - [ ] Optional fields (deleted_at, edited_at, etc.)
  - [ ] Nested types for reactions and mentions
  - [ ] No reply_to fields (linear messaging)

## Implementation Order (Updated for Progressive Development)

### **Step 1: Basic Backend Setup**
1. Create GP Chat Message doctype with essential fields
2. Update GP Pod to include "Chats" type
3. Basic Python class (minimal validation)

### **Step 2: Route Integration (Start here for frontend)**
1. Create blank `SpaceChats.vue` component
2. Add chat route to router.ts

### **Step 3: Space Overview Integration**
1. Update SpaceCustomize.vue with Chats option
2. Update SpaceOverview.vue to handle Chat pods
3. Create basic `PodChats.vue` preview component

### **Step 4: Chat Components Development**
1. Create data composable (`chatMessages.ts`)
2. Build ChatMessageInput component
3. Build ChatMessage component
4. Build ChatMessageList component
5. Integrate all components into SpaceChats.vue

### **Step 5: Polish & Features**
1. Add message operations (edit, delete)
2. Improve styling and spacing
3. Add reactions and mentions integration
4. Optimize performance and UX

## Implementation Decisions
- ✅ **Message Loading**: Load more button (no infinite scroll initially)
- ✅ **Timestamp Display**: Grouped by time intervals (15+ minutes apart)
- ✅ **Message Threading**: Linear messaging (no threaded replies)

### 2. **Message Features**
- ✅ **File Uploads**: Not implemented initially
- ✅ **Emoji Reactions**: Yes, using existing reaction system
- ✅ **@Mentions**: Yes, using existing mentions system
- ✅ **Message Input**: Use existing TextEditor component

### 3. **Permissions & Access**
- ✅ **Permission Model**: All space members can see all messages
- ✅ **Message Editing**: Yes, users can edit their own messages
- ✅ **Message Deletion**: Yes, users can delete their own messages
- ✅ **Retention Policies**: No special retention policies

### 4. **Integration Points**
- ✅ **Global Search**: Not included initially
- ✅ **Activity System**: Not included initially
- ✅ **Pinned Messages**: Not supported initially

### 5. **Technical Preferences**
- ✅ **Component Structure**: Approved (ChatMessageList, ChatMessage, ChatMessageInput)
- ✅ **Optimistic Updates**: Yes, show messages immediately before server confirmation
- ✅ **Message Input**: Use TextEditor component

## Design Inspiration & UI Requirements

### Chat Interface Design (Based on Reference)
The chat interface should follow these key design elements from the reference image:

#### Layout Structure
- **Clean, centered layout** with ample white space
- **Messages area** with comfortable padding and spacing
- **Date separators** (e.g., "Today") centered with subtle styling
- **Fixed input area** at bottom with rounded input field

#### Message Design Patterns
- **Right-aligned user messages** with darker background bubbles
- **Left-aligned responses** with user avatars and lighter backgrounds
- **Message bubbles** with proper border radius and subtle shadows
- **Consistent spacing** between message groups

#### Input Area Features
- **Rounded input field** with placeholder text ("Ask me anything...")
- **Icon buttons** on the left (attachment, mic, etc.)
- **Send button** on the right with accent color
- **Subtle border/shadow** around input container

#### Visual Elements
- **User avatars** (circular, consistent sizing)
- **Message actions** (copy, regenerate icons) appearing on hover
- **Date/time stamps** with muted text color
- **Clean typography** with good contrast ratios

## Implementation Notes

1. **No Real-time Initially**: Messages will only refresh when the user manually refreshes or navigates.

2. **Modern Chat UI**: Clean bubble-style design with proper message alignment and spacing.

3. **Follows Existing Patterns**: The implementation closely follows existing patterns used for Discussions, Tasks, and Documents pods.

4. **Scalable Architecture**: The structure allows for easy addition of real-time features and advanced chat features in future phases.

5. **Consistent UI**: Uses the same design system and component patterns as the rest of the application.

6. **Optimistic Updates**: Messages appear immediately for better UX, then sync with server.

7. **Linear Threading**: Simple linear message flow without complex reply threads.

8. **Existing Integrations**: Leverages existing @mentions and reactions systems from discussions.

## Technical Implementation Details

### Backend Files Structure
```
gameplan/gameplan/doctype/gp_chat_message/
├── __init__.py
├── gp_chat_message.json
├── gp_chat_message.py
└── api.py
```

### Frontend Files Structure
```
frontend/src/
├── data/chatMessages.ts
├── components/Chat/
│   ├── ChatMessageList.vue
│   ├── ChatMessage.vue
│   └── ChatMessageInput.vue
├── pages/
│   ├── SpaceChats.vue
│   └── SpaceOverview/PodChats.vue
└── types/doctypes.ts (updated)
```

### Database Schema (GP Chat Message)
```sql
CREATE TABLE `tabGP Chat Message` (
  `name` varchar(140) PRIMARY KEY,
  `content` longtext,
  `project` varchar(140),
  `pod` varchar(140),
  `message_type` varchar(140) DEFAULT 'text',
  `deleted_at` datetime,
  `edited_at` datetime,
  `owner` varchar(140),
  `creation` datetime,
  `modified` datetime,
  -- Standard Frappe fields
  KEY `project` (`project`),
  KEY `pod` (`pod`),
  KEY `owner` (`owner`),
  KEY `creation` (`creation`)
);
```

### Key Features Summary
- **Modern Chat UI**: Clean bubble-style interface with proper message alignment
- **Linear Messaging**: No reply threads, simple chronological order with date separators
- **Time Grouping**: Messages grouped by 15+ minute intervals with smart avatar display
- **Message Bubbles**: Right-aligned for current user, left-aligned for others with avatars
- **User Permissions**: Edit/delete own messages only
- **Existing Integrations**: @mentions and reactions using existing systems
- **Optimistic Updates**: Immediate UI feedback with server sync
- **Load More**: Button-based pagination instead of infinite scroll
- **Responsive Design**: Clean layout that works well in pod containers
- **Hover Interactions**: Message actions appear on hover for clean interface

This comprehensive plan provides a complete roadmap for implementing the Chats pod feature while maintaining consistency with Gameplan's existing architecture and patterns.