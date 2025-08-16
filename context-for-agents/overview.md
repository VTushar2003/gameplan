### **Gameplan Improvement Task List**

---

#### **Phase 1: Core User Experience & Structure**

**Homepage Revamp**

- [x] **Pinned Spaces Section**
    - [x] Implement a "Pinned Spaces" default view.
    - [x] Add a user preference setting to choose their default home view.
    - [x] Develop the customizable grid layout for spaces.
    - [x] Enable drag-and-drop reordering for spaces on the grid.

- [ ] **All Spaces Section**
    - [ ] Implement the "Show All" spaces view with a search bar.

- [x] **Todos / Schedule Section**
    - [ ] Create the "My Assigned Todos" widget for the homepage.
    - [ ] Add filtering to the Todos widget (by due date, project, priority).
    - [ ] Add sorting options to the Todos widget.
    - [ ] Implement Google Calendar integration to show events.
    - [ ] Implement Frappe Calendar integration.
    - [ ] Scope out Outlook Calendar integration.

**Sidebar Navigation**
- [ ] Implement a "Shortcuts/Bookmarks" section.

**Space Configuration**
- [x] Implement the concept of "Tools" within a Space (Discussions, Tasks, Docs, etc.).
- [x] The Space page should show a grid of tools enabled on that space.
- [x] Develop the customizable grid for arranging tools within a Space.
- [x] Ability to enable/disable tools in a space.
- [ ] Allow users to customize notification settings for each tool within a Space.

---

#### **Phase 2: Feature Enhancement**

**Discussions**
- [ ] Implement categories for discussions (e.g., Announcements, Questions).
- [ ] Add filtering capabilities based on categories, author, date, etc.
- [ ] Add a "Mark as Unread" option for discussion posts.
- [ ] Add a "Remind me later" feature for discussion notifications.

**Documents**
- [ ] Add a comment section under the document.
- [ ] Allow adding external links as "documents"
- [ ] Folders for organization
- [ ] Implement version history for documents, with the ability to view and revert changes.

**Tasks**
- [ ] Allow the creation of subtasks under a parent task.
- [ ] Enable file attachments on tasks.
- [ ] Open task detail view in a dialog

**Chat**
- [ ] Chat as a tool for every space
- [ ] Basic chat features like @mention, reactions, etc

**User Groups & Permissions**
- [ ] Build the User Groups creation and management interface.
- [ ] Integrate User Groups into the Space access control settings.
- [ ] Allow Space admins to set group-level permissions (e.g., Viewer, Editor).
- [ ] Implement group `@mentions` (e.g., `@engineering`) in discussions and comments.

---

#### **Phase 3: Onboarding & Gamification**

**Signup Flow**
- [ ] Implement one-click signup/login via Google.
- [ ] Implement one-click signup/login via Microsoft.
- [ ] Develop logic to detect workspace email domains upon signup.
- [ ] Automate the creation of an "Organization" account based on a workspace email.
- [ ] Auto-suggest joining the Organization for subsequent signups from the same domain.
- [ ] Set up the `gameplan.so/signup` page.
- [ ] Implement unique workspace URLs (e.g., `gameplan.so/acme`).

**"Make Your Own Room" (The Game)**
- [ ] Design the 2D RPG-style canvas UI for the personal room.
- [ ] Develop the drag-and-drop interface for room customization (furniture, etc.).
- [ ] Design and implement a gamification/point system.
- [ ] Define the actions that earn points (e.g., completing tasks, creating docs).
- [ ] Create a store or system for unlocking decorative items with points.
- [ ] Implement the ability for users to "visit" each other's rooms.
- [ ] Add a feature to leave messages or reactions in another user's room.