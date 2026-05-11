# Changelog

All notable changes to MaixCAM WildTrap will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2026-05-11

### 🎉 Initial Release - Production Ready

First production-ready release of MaixCAM WildTrap - AI-powered camera trap for wildlife monitoring and security.

### ✨ Added

#### Detection System
- Motion detection using frame differencing algorithm
- AI object detection with YOLOv8 (80 COCO classes)
- Hybrid detection mode (Motion → AI verification)
- Scheduled/timelapse detection mode
- Configurable motion sensitivity (20-100)
- Confidence threshold filtering (0.3-0.9)
- Minimum object size filtering
- Cooldown system to prevent spam captures

#### Capture System
- Photo mode (single high-quality image)
- Burst mode (3/5/10 sequential photos)
- Video mode (5/10/15/30 second recordings)
- Timelapse mode (scheduled intervals)
- Configurable resolution (320x240 to 1920x1080)
- JPEG quality settings (1-100)
- Night mode with brightness/contrast enhancement

#### Storage & Metadata
- Structured file storage (/root/wildtrap/captures/)
- Filename format: YYYYMMDD_HHMMSS_object_confidence.jpg
- JSON metadata for each capture (timestamp, objects, settings)
- CSV logging for detection history
- Auto-cleanup based on storage limits
- Configurable retention (days and GB limits)

#### Notifications
- Telegram Bot integration with photo attachments
- HTTP Webhook support with JSON payload
- Notification throttling to prevent spam
- Configurable throttle intervals

#### User Interface
- Touchscreen interface framework
- Live preview with detection overlays
- Status display (ARMED/STANDBY)
- Bounding box visualization
- Storage usage indicator
- Touch input handling

#### Configuration
- JSON-based configuration system
- 20+ configurable parameters
- Runtime configuration updates
- Persistent state management
- Default configuration template

#### Documentation
- Comprehensive README (English + Russian)
- Quick start guide (5-minute setup)
- 8 real-world configuration examples
- Technical architecture documentation
- API reference
- Troubleshooting guide
- Project information and roadmap

#### Code Quality
- Production-ready error handling
- Graceful degradation on failures
- Resource cleanup (camera, display)
- Modular architecture (8 core classes)
- Comprehensive docstrings
- Type hints where applicable
- 650 lines of production code
- 242 lines of educational code

### 📦 Deliverables

- `wildtrap_app.py` - Main production application (24KB)
- `simple_wildtrap.py` - Educational simplified version (7.2KB)
- `wildtrap_config.json` - Configuration template (716B)
- `README.md` - Unified documentation (EN + RU)
- `QUICKSTART.md` - 5-minute setup guide
- `EXAMPLES.md` - 8 real-world configurations
- `PROJECT_INFO.md` - Technical architecture
- `START_HERE.md` - Navigation guide
- `CHANGELOG.md` - This file
- `LICENSE` - MIT License

### 🎯 Supported Use Cases

- Wildlife monitoring and research
- Home and office security
- Bird watching and photography
- Trail cameras for remote locations
- Pet activity monitoring
- Construction site security
- Nature timelapse projects
- Scientific data collection

### 🔧 Technical Stack

- **Platform**: MaixCAM (Sipeed)
- **Language**: Python 3
- **Framework**: MaixPy 4.x
- **AI Model**: YOLOv8n (3.2MB)
- **Libraries**: maix.camera, maix.display, maix.image, maix.nn, maix.touchscreen

### 📊 Performance

- Motion Detection: ~30 FPS, low power
- AI Detection: ~20 FPS, high accuracy
- Hybrid Mode: ~25 FPS, balanced
- Detection latency: ~150ms per cycle

### 🐛 Known Limitations

- Touchscreen menu system is framework-only (not fully implemented)
- Video mode saves frames as images (no native H.264 encoding)
- Motion detection is simplified (no advanced algorithms)
- Single camera support only
- Battery monitoring depends on hardware support

### 🔮 Future Plans

See [PROJECT_INFO.md](PROJECT_INFO.md) for detailed roadmap.

---

## [Unreleased]

### Planned for v1.1.0
- Full touchscreen menu implementation
- Gallery viewer with swipe navigation
- Statistics dashboard with charts
- Species counter and identification
- Advanced scheduling (sunrise/sunset triggers)

### Planned for v2.0.0
- Native video encoding (H.264)
- Multi-camera support
- Web interface for remote access
- Cloud storage integration
- Audio detection (optional microphone)
- Advanced motion algorithms

---

## Release Links

- **v1.0.0**: https://github.com/bobberdolle1/maixcam-wildtrap/releases/tag/v1.0.0

---

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

See [PROJECT_INFO.md](PROJECT_INFO.md) for architecture details.

---

## Support

- **Issues**: https://github.com/bobberdolle1/maixcam-wildtrap/issues
- **Discussions**: https://github.com/bobberdolle1/maixcam-wildtrap/discussions
- **MaixPy Wiki**: https://wiki.sipeed.com/maixpy
- **Community**: https://maixhub.com

---

**Legend**:
- ✨ Added - New features
- 🔧 Changed - Changes in existing functionality
- 🐛 Fixed - Bug fixes
- 🗑️ Deprecated - Soon-to-be removed features
- ❌ Removed - Removed features
- 🔒 Security - Security fixes
