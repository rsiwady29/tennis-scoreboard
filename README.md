# Tennis Scoreboard with Bluetooth Remote Input

A real-time tennis scoring system designed for Raspberry Pi 2W with Bluetooth remote control support.

## Features

- **Standard Tennis Scoring**: Tracks points, games, sets, and matches with proper tennis rules
- **Bluetooth Remote Input**: Hands-free scoring via HID keyboard devices
- **Persistent Storage**: Auto-saves match state with complete history
- **Modular UI System**: Console interface with extensible observer pattern
- **Real-time Updates**: <50ms latency for scoring input

## Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Scoreboard**:
   ```bash
   python tennis_scoreboard.py
   ```

3. **Connect Bluetooth Remote**: Pair your Bluetooth HID device (keyboard/remote)

4. **Start Scoring**:
   - **UP Arrow**: Home player scores a point
   - **DOWN Arrow**: Away player scores a point
   - **S**: Swap server
   - **R**: Reset current match
   - **N**: Start new match
   - **L**: Load latest saved match

## Input Controls

### Phase 1 (Hardcoded)
- UP/DOWN arrows for point scoring
- S for server swap
- R for reset
- N for new match
- L for load latest

### Phase 2 (Configurable)
- JSON-based input mapping
- Multiple device support
- Device discovery via `/dev/input/event*`

## File Structure

```
tennis_scoreboard/
├── tennis_scoreboard.py      # Main entry point
├── core/
│   ├── match.py              # Match logic & scoring rules
│   ├── persistence.py        # JSON save/load
│   ├── input.py              # Input device handling
│   └── observer.py           # Observer interface
├── ui/
│   ├── console_ui.py         # Console renderer
│   └── led_ui.py             # Future: HUB75 LED support
├── matches/                  # Match history storage
└── input_config.json         # Input mapping config
```

## Tennis Scoring Rules

- **Points**: 0 → 15 → 30 → 40 → Advantage → Game
- **Games**: First to 6 with 2-game margin
- **Sets**: Best of 3 (configurable)
- **Deuce**: At 40-40, must win by 2 points
- **Advantage**: Win next point after deuce to win game

## Persistence

- Auto-saves after every scoring action
- Match files: `YYYY-MM-DD-N.json`
- `latest.json` always points to most recent match
- Survives crashes and power loss

## Hardware Support

- **Primary**: Raspberry Pi 2W
- **Input**: Bluetooth HID devices, USB keyboards
- **Future**: HUB75 LED matrix panels

## Development

### Phase 1 (MVP)
- [x] Core match logic
- [x] Console UI
- [x] Basic input handling
- [x] JSON persistence

### Phase 2 (Enhancements)
- [ ] Configurable input mapping
- [ ] LED matrix UI
- [ ] Web dashboard
- [ ] systemd service

## License

MIT License - see LICENSE file for details
