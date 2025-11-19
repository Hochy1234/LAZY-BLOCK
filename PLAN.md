# Lazy Block Development Plan

## Guiding Principles
- Build iteratively with a working UI at the end of every phase so we can evaluate usability early.
- Keep the block model, storage, and transformation engine isolated from tkinter widgets to simplify future Rust/C++ integrations.
- Prefer ttkbootstrap-first styling but keep a tkinter fallback so automated checks can run without native theme dependencies.

## Phase 1 – UI Skeleton & Demo Flow (In Progress)
- Implement the top toolbar with two stacked rows (categories + tools) and a fixed 「創建」 button, matching the layout in the requirements.
- Build panels A/B/C: block browser with folder selector, editor input area, conversion output area.
- Wire demo data so clicking a block injects its templates into the editor/output areas, demonstrating the intended conversion loop.
- Provide callbacks for category change, folder change, and block creation so later phases can attach real behaviors.
- Acceptance: running `python -m lazy_block_app` shows the described layout, buttons react, and selecting a sample block updates the B/C panels.

## Phase 2 – Block Storage & Template Runtime
- Implement filesystem-backed block folders (`blocks/<folder>/<block>/block.json`) and expose create/list/delete APIs.
- Expand `Block` model with validation helpers (template placeholders detection, missing inputs warning).
- Connect `BlocksPanel` folder picker to `core.blocks_storage.list_blocks_in_folder` and refresh UI when folders change.
- Acceptance: selecting a folder filled with JSON block definitions populates the A panel, and clicking a block renders text using live input values.

## Phase 3 – Block Creation & Editing Workflow
- Build the 「創建」 dialog that collects folder/name/display/input/output definitions plus embedded tools (e.g., `{輸入文字()}` directives).
- Validate user input (unique folder, mandatory fields, placeholder detection) before saving the new block folder.
- Add the ability to delete/rename blocks and refresh the list automatically after operations.
- Acceptance: designers can create, edit, and delete blocks purely through the UI without touching JSON manually.

## Phase 4 – Live Editing & Transformation Enhancements
- Allow dragging/dropping block tokens into the editor, keeping metadata for later substitution.
- Implement live syncing between B and C areas: typing text or inserting tokens in B re-renders C in real time.
- Introduce tool palette customization per category (e.g., theme switcher under 美術) with relevant callbacks.
- Acceptance: users experience the interactive workflow described (drag/drop or click-to-insert), and C updates instantly as B changes.

## Phase 5 – Theming, Packaging & Testing
- Surface ttkbootstrap theme selector in the 美術 category and persist the chosen theme.
- Package the project (entry point script, README updates) and add automated tests for the core engine/storage.
- Prepare release artifacts and document how to add new tools/blocks.
- Acceptance: repository ships with tests covering the core logic, CI passes, theming works, and packaging instructions are available.

