# UI Design — Beach Generator

A Week-10 design suggestion for putting a Maya window around your beach
geometry builders in `beach_geometry.py`. This is a **suggestion**, not a
constraint. Use it as a starting point; deviate freely as long as you keep
the three-layer separation.

## Where your project stands today

You already have the geometry pieces and the start of a data-driven setup:

- `beach_geometry.py` — the builders:
  `create_sand(width, length, position)`,
  `create_water(width, length, position)`,
  `create_palmtree(width, height, scale, length, position, axis)`,
  `create_seashells(width, height, scale, position, axis)`.
- `beach_materials.py` — `_make_sg`, `assign_material`,
  `create_ocean_material`, `create_ocean_material_builtin`.
- `Main.py` — a `config` dict of per-element parameters, a `create_element()`
  dispatcher, and a `build_beach(config=None)` driver.

What's missing for Week 10 is a Maya window. Everything below is about
*producing* the inputs to your geometry builders from UI controls instead of
hand-editing `config` at the top of `Main.py`.

## A note about wiring (important)

The starter in this PR (`beach_ui_starter.py`) calls your **geometry
builders directly** — `beach_geometry.create_sand`, `create_water`,
`create_palmtree`, `create_seashells` — via a small *local* config list
inside `do_the_work()`. It deliberately does **not** call
`Main.build_beach()` yet, because `Main.py` currently references some
names that aren't defined in the file (`BUILDERS`, `BEACH_CONFIG`,
`MATERIAL_PALETTE`, `SAND_LENGTH` / `SAND_LENGHT`, `TYPE_MATERIALS`), and
the module-level `config` is a `dict` rather than the `list` the driver
iterates over.

That's a separate bug-fix pass (your open PR #1 fixes the `mport` typo on
line 1 of `beach_geometry.py`; it still needs to land for the import in this
starter to resolve, and the runtime issues in `Main.build_beach` are
follow-ups). Once those are sorted, switching `do_the_work()` over to call
`Main.build_beach(config_list)` is a one-line change — the UI never has to
care.

## The shape you're building toward (recap)

```
UI  →  DATA  →  LOGIC
```

See `demo_ui_and_polish.py` (sections 1, 4, 5) and the `scene_builder/`
package on Notion for the pattern. Copy `tool_skeleton.py` and fill it in
with the keys below, or use `beach_ui_starter.py` (in this PR) — it's
pre-wired to your geometry builders.

## Suggested settings dict shape

```python
{
    "beach_size":   60.0,   # float — sand + water plane size (world units)
    "palm_count":      3,   # int   — how many palm trees to scatter
    "shell_patches":   2,   # int   — how many seashell scatter patches
    "palm_scale":   15.0,   # float — passed to create_palmtree(scale=...)
    "spread":       25.0,   # float — XZ scatter radius for palms / shells
    "seed":           42,   # int   — for deterministic placement
    "group_name":  "beach_grp",  # str — top-level Maya group name
}
```

Every key here corresponds to exactly one control in `build_ui()` and one
query in `read_settings()`.

## Suggested UI layout (top to bottom)

| Setting          | Control                            | Range / options  |
|------------------|------------------------------------|------------------|
| `beach_size`     | `cmds.floatSliderGrp`              | 20.0 – 120.0     |
| `palm_count`     | `cmds.intSliderGrp`                | 0 – 10           |
| `shell_patches`  | `cmds.intSliderGrp`                | 0 – 6            |
| `palm_scale`     | `cmds.floatSliderGrp`              | 5.0 – 25.0       |
| `spread`         | `cmds.floatSliderGrp`              | 5.0 – 50.0       |
| `seed`           | `cmds.intFieldGrp`                 | any              |
| `group_name`     | `cmds.textFieldGrp`                | any valid name   |
|                  | `cmds.button("Build beach")`       | calls `on_run()` |

Window size around `380 × 360` is comfortable. Keep one
`columnLayout(adjustableColumn=True, rowSpacing=6, columnOffset=("both", 14))`
as the parent; that gives consistent margins and stacked controls.

## How the layers map to your existing code

- **LOGIC — `do_the_work(settings)`**: seed `random.Random(settings["seed"])`,
  build a local `config_list` (sand entry, water entry, N palm entries,
  M seashell entries), then call your geometry builders one entry at a time.
  Group the created nodes under `settings["group_name"]` at the end.

- **DATA — `read_settings()`**: query each control with `query=True` and
  return the dict shape above. Nothing else.

- **UI — `build_ui()`**: window → `columnLayout` → controls → button → show.
  No logic in here, not even reading the controls — that lives in
  `read_settings()`.

- **BRIDGE — `on_run()`**: 4 lines.
  `settings = read_settings(); try: do_the_work(settings) except ValueError as e: cmds.warning(e)`.

## Must-have vs. nice-to-have

**Must-have** (for the grading rubric):
- All three layers separated; no scene-building code inside the callback.
- At least 4 working controls (a couple of sliders, a text field, a checkbox
  or int field).
- A "Build" button that calls the geometry builders via a settings dict.
- The `default_settings()` dict matches what `build_ui()` produces.
- Friendly error path: `cmds.warning(...)` on `ValueError`, no raw traceback
  in the Script Editor for normal bad input.

**Nice-to-have** (extra polish):
- **Fix `Main.py`** so `build_beach(config_list)` actually runs: define a
  `BUILDERS = {"sand": geo.create_sand, "water": geo.create_water, ...}`
  table, change the module-level `config` from a `dict` to a `list` of
  typed entries, and replace the undefined `BEACH_CONFIG` / `SAND_LENGHT` /
  `MATERIAL_PALETTE` / `TYPE_MATERIALS` references with values that
  actually exist. Then change one line in the starter's `do_the_work()`
  to `Main.build_beach(config_list)`.
- A "Clear scene" button next to "Build" (`cmds.file(new=True, force=True)`).
- A shelf-button installer following Section 8 of the demo.
- Hook up `beach_materials.create_ocean_material_builtin` to the water plane
  so the water plane actually looks like water on first build.

## How to use the starter file in this PR

`beach_ui_starter.py` is the lightweight scaffold:

- `default_settings()` and `do_the_work()` are **written** and already wire
  to your geometry builders. You shouldn't need to change them.
- `build_ui()` and `read_settings()` are **stubbed** with TODO comments in
  the right shape. Fill in the controls listed above, query them in
  `read_settings()`, and you're done.

You can copy it next to your other modules and `import` it from there, or
restructure into the `scene_builder/`-style package (see Section 1B of the
demo) — both options are graded equally.

## Resources

- **`tool_skeleton.py`** — the blank version of this pattern. Copy it.
- **`demo_ui_and_polish.py`** — read sections 1, 4, 5 first; section 8 for
  the shelf-button finish.
- **`scene_builder/` package** — the recommended multi-file layout if you
  want to split UI and logic across files.

Questions? Comment on this PR or message me.
