# Contributing to Retro'98 Microgames

Retro'98 Microgames is intentionally static and dependency-free. Changes should keep every game easy to open, inspect, and host without a build step.

## Add a microgame

1. Create one self-contained HTML file under `game/`.
2. Give the document a `<!doctype html>`, `lang="ru"`, UTF-8 charset, viewport metadata, and a descriptive `<title>`.
3. Keep gameplay assets local. Do not add CDN scripts, analytics, trackers, or network-dependent runtime assets.
4. Add exactly one launcher entry in `index.html` that points to the new `game/*.html` file.
5. Preserve keyboard access and visible focus for interactive controls. Add accessible names when the visual label alone is not enough.
6. Store optional progress locally only when the game needs persistence; use a game-specific `localStorage` key so games do not overwrite each other.

## Change an existing game

Keep changes isolated to the game whenever possible. Avoid introducing shared global state through the launcher, and do not make one game depend on another game's DOM, storage, or scripts.

For interaction changes, check the main path with both pointer and keyboard input. For saved-state changes, verify both a fresh profile and an existing save when applicable.

## Validate before opening a PR

Run the dependency-free smoke checks from the repository root:

```bash
python -m unittest discover -s tests -v
```

The checks ensure that launcher entries are unique, every launcher target exists, every `game/*.html` file is represented in the launcher, and HTML entry points keep required document metadata.

For gameplay changes, also serve the repository locally:

```bash
python -m http.server 8080
```

Then open `http://localhost:8080` and verify the changed game in a browser. GitHub Actions repeats the static checks on every pull request.

## Pull request scope

Prefer one focused gameplay fix, new microgame, documentation update, or infrastructure change per pull request. Avoid unrelated formatting churn or generated files so the actual behavior change stays reviewable.
