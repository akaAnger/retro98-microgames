# Retro'98 Microgames

[![Static checks](https://github.com/akaAnger/retro98-microgames/actions/workflows/static-checks.yml/badge.svg)](https://github.com/akaAnger/retro98-microgames/actions/workflows/static-checks.yml)

**Retro'98 Microgames** is a collection of small browser games built in the visual language of Windows 98. The project is fully static and intentionally dependency-free: every game is written with plain HTML, CSS, and JavaScript.

The goal is to keep the games easy to open, easy to inspect, and easy to extend, while still showing attention to UI details, local state, accessibility, and browser performance.

## Highlights

- A growing set of self-contained microgames in one retro desktop-style launcher.
- No build step, framework, external assets, CDN, tracking, or backend.
- Each game lives as an isolated HTML file in `game/`.
- Local progress is stored only in `localStorage`.
- Retro UI built with CSS: window chrome, system-like buttons, progress bars, and pixel-style interaction patterns.
- Keyboard shortcuts, visible focus states, ARIA labels, and clear action feedback.

## Included games

| Game | Description |
| --- | --- |
| `Password Game 98` | A rule-based password puzzle with escalating constraints and retro hints. |
| `Do Not Press 98` | A clicker/troll microgame with moving buttons, clones, overlays, and staged effects. |
| `Dancing Folder` | A playful cursor-following folder interaction with random window behavior. |
| `Glazyaka 98` | Canvas-based animated eyes with tracking, blinking, micro-movements, and PNG export. |
| `Stimulation Clicker 98` | A larger clicker with economy tiers, upgrades, synergies, autosave, offline income, prestige, and achievements. |

## Tech stack

- HTML5
- CSS3
- Vanilla JavaScript / ES6+
- Canvas API for visual effects
- WebAudio API for generated UI sounds
- `localStorage` for local-only saves

## Project structure

```text
.
├── index.html
├── game/
│   ├── password98.html
│   ├── dontpress98.html
│   ├── dancingfolder98.html
│   ├── eye98.html
│   └── stimclicker98.html
├── tests/
│   └── test_static.py
├── CONTRIBUTING.md
└── README.md
```

## Local development

Start any static server from the repository root:

```bash
python -m http.server 8080
```

Then open:

```text
http://localhost:8080
```

The project can also be deployed to any static host, including GitHub Pages.

Run the dependency-free smoke checks before changing launcher entries or game files:

```bash
python -m unittest discover -s tests -v
```

The checks verify that every launcher target exists, all HTML entry points contain the required document metadata, and the launcher keeps its small-screen responsive layout. GitHub Actions runs them for every pull request and push to `main`.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the extension rules, accessibility expectations, storage isolation, and browser checks for new microgames.

## Architecture notes

- The main page loads games inside the same browser window through an iframe-based launcher.
- Each game is designed as a standalone file with isolated logic.
- UI sounds are generated in the browser and start only after user interaction.
- Saves stay on the user's device and are never sent to a server.
- The project avoids external resources so it can be reviewed and hosted easily.

## Privacy and security

- No analytics.
- No third-party scripts.
- No network requests from gameplay.
- No account system.
- No server-side storage.
- Clipboard access is used only after explicit user action.

## Roadmap

- Add a shared retro UI component layer.
- Add a high-score/statistics panel to the launcher.

## License

MIT
