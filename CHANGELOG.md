# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] - 2026-06-20

### Features
- **overwatch**: Add planning master files, webapp prototype layout options, and sketches `004` (Solo System), `005` (Solo HUD), and `006` (Shadow Commander) (`013fc64`, `35e3f03`)
- **api**: Add FastAPI server skeleton with authentication, health check, live WebSocket broker, and endpoints for agents, GPU management, and chat proxy (`35e3f03`)
- **web**: Add dark-themed, glassmorphism Solo Leveling style frontend dashboard under `igris/web` supporting terminal streaming, agent army view, and telemetry charts (`35e3f03`)
- **orchestrator**: Integrate direct chat console in Python with ANSI colors, interactive keyboard commands (`s`, `t`, `a`, `h`, `q`), and simulated router flow (`a789d09`, `c07de22`, `af5ad20`, `8173c18`)

### Bug Fixes
- **core**: Correct auto-revert of training status in orchestrator and prevent showing blocked agents (`bd61e2f`)
