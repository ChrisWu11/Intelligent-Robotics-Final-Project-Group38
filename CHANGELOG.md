# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2025-11-30
### Added
- Indoor cleaning robot simulation built in Webots with camera-based perception, obstacle-aware navigation, and a finite state machine to manage EXPLORE and CLEAN modes. The controller detects red zones, drives forward for cleaning, pauses, and resumes exploration with cooldown handling.
- Supervisor controller that streams robot position updates and cleaning events to downstream services via WebSocket-friendly JSON messages.
- FastAPI backend that manages WebSocket connections for both the supervisor and frontend clients, relaying robot positions and aggregating cleaned-zone coordinates for visualization.
- React frontend that renders the apartment boundaries, robot trajectory, cleaned zones, and orientation triangle in real time while reflecting the current robot state.
- Project documentation describing the overall architecture, runtime steps, and component layout for the simulation, backend, and frontend layers.
