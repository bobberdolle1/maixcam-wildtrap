
# MaixCAM WildTrap 🎯

**AI-Powered Camera Trap for Wildlife Monitoring**

Production-ready application for MaixCAM with automatic detection, capture, and notifications.

---

## Features

### Detection Modes
- **Motion Detection** - Energy-efficient frame differencing
- **AI Detection** - YOLOv8 object recognition (animals, people, vehicles)
- **Hybrid Mode** ⭐ - Motion trigger → AI verification (recommended)
- **Scheduled Mode** - Timelapse capture at intervals

### Capture Modes
- **Photo** - Single high-quality image
- **Burst** - Series of 3/5/10 photos
- **Video** - Record 5/10/15/30 second clips
- **Timelapse** - Periodic capture during detection

### Smart Features
- 🎯 **Object Filtering** - Target specific animals/people
- 🌙 **Night Mode** - Automatic brightness/contrast enhancement
- 📊 **Metadata Logging** - JSON + CSV detection history
- 🔔 **Notifications** - Telegram Bot + HTTP Webhook
- 💾 **Auto-Cleanup** - Manage storage limits automatically
- ⚡ **Energy Saving** - Optimized detection pipeline
- 📱 **Touchscreen UI** - Easy configuration and monitoring

---

## Quick Start

### 1. Installation

```bash
# Copy files to MaixCAM
scp wildtrap_app.py wildtrap_config.json root@maixcam:/root/

# SSH into MaixCAM
ssh root@maixcam

# Create directories
mkdir -p /root/wildtrap/{captures,logs,temp}
```

### 2. Configuration

Edit `wildtrap_config.json`:

```json
{
  "detection_mode": "hybrid",
  "capture_mode": "burst",
  "target_objects": ["dog", "cat", "bird", "person"],
  "confidence_threshold": 0.6,
  "cooldown_seconds": 30,
  "telegram_enabled": true,
  "telegram_bot_token": "YOUR_BOT_TOKEN",
  "telegram_chat_id": "YOUR_CHAT_ID"
}
```

### 3. Run

```bash
python3 wildtrap_app.py
```

---

## Configuration Guide

### Detection Settings

| Parameter | Values | Description |
|-----------|--------|-------------|
| `detection_mode` | motion / ai / hybrid / scheduled | Detection method |
| `motion_sensitivity` | 20-100 | Motion detection threshold |
| `confidence_threshold` | 0.3-0.9 | AI confidence minimum |
| `min_object_size` | pixels | Filter small detections |
| `cooldown_seconds` | seconds | Delay between captures |

### Target Objects

Available COCO classes:
- **Animals**: dog, cat, bird, horse, cow, sheep, bear, elephant, zebra, giraffe
- **People**: person
- **Vehicles**: car, truck, motorcycle, bus

### Camera Settings

| Parameter | Values | Description |
|-----------|--------|-------------|
| `camera_width` | 320/640/1280/1920 | Resolution width |
| `camera_height` | 240/480/720/1080 | Resolution height |
| `night_mode` | true/false | Auto brightness boost |
| `jpeg_quality` | 1-100 | Compression quality |

### Capture Settings

| Parameter | Values | Description |
|-----------|--------|-------------|
| `capture_mode` | photo/burst/video/timelapse | Capture type |
| `burst_count` | 3/5/10 | Photos per burst |
| `video_duration` | 5/10/15/30 | Video length (seconds) |
| `timelapse_interval` | seconds | Interval for scheduled mode |

### Telegram Notifications

1. Create bot with [@BotFather](https://t.me/botfather)
2. Get bot token
3. Get your chat ID from [@userinfobot](https://t.me/userinfobot)
4. Configure:

```json
{
  "telegram_enabled": true,
  "telegram_bot_token": "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11",
  "telegram_chat_id": "123456789",
  "telegram_throttle_minutes": 5
}
```

### Storage Management

| Parameter | Values | Description |
|-----------|--------|-------------|
| `storage_max_gb` | GB | Maximum storage usage |
| `storage_keep_days` | days | Auto-delete older files |
| `auto_cleanup` | true/false | Enable automatic cleanup |

---

## File Structure

```
/root/wildtrap/
├── captures/              # Saved photos/videos
│   ├── 20260510_143022_dog_0.87.jpg
│   ├── 20260510_143022_dog_0.87.json
│   └── ...
├── logs/
│   └── detections.csv    # Detection history
└── temp/                 # Temporary files
```

### Metadata Format

Each capture includes a JSON file:

```json
{
  "timestamp": "20260510_143022",
  "detection_mode": "hybrid",
  "capture_mode": "burst",
  "detected_objects": [
    {
      "label": "dog",
      "confidence": 0.87,
      "bbox": [120, 80, 450, 380]
    }
  ],
  "camera_settings": {
    "width": 1280,
    "height": 720,
    "night_mode": true,
    "quality": 90
  },
  "files": ["20260510_143022_dog_0.87_burst1.jpg", ...]
}
```

---

## Usage Tips

### Recommended Settings

**Wildlife Monitoring (Day)**
```json
{
  "detection_mode": "hybrid",
  "capture_mode": "burst",
  "burst_count": 5,
  "target_objects": ["dog", "cat", "bird", "deer", "bear"],
  "confidence_threshold": 0.7,
  "cooldown_seconds": 60,
  "night_mode": false
}
```

**Security (24/7)**
```json
{
  "detection_mode": "hybrid",
  "capture_mode": "video",
  "video_duration": 15,
  "target_objects": ["person", "car"],
  "confidence_threshold": 0.8,
  "cooldown_seconds": 30,
  "night_mode": true
}
```

**Bird Watching**
```json
{
  "detection_mode": "ai",
  "capture_mode": "burst",
  "burst_count": 10,
  "target_objects": ["bird"],
  "confidence_threshold": 0.6,
  "cooldown_seconds": 10
}
```

### Energy Optimization

- Use **hybrid mode** for best battery life
- Increase `cooldown_seconds` to reduce captures
- Lower resolution for longer operation
- Disable notifications when not needed

### Night Vision

The software night mode enhances images by:
1. Increasing exposure/brightness (1.5x multiplier)
2. Histogram equalization for contrast
3. Automatic adjustment per frame

For best results:
- Enable `night_mode: true`
- Use lower resolution (640x480)
- Increase `confidence_threshold` to 0.7+

---

## Troubleshooting

### Camera Not Initializing
```bash
# Check camera module
ls /dev/video*

# Restart camera service
systemctl restart camera
```

### AI Model Not Found
```bash
# Download YOLOv8 model
cd /root/models
wget https://github.com/sipeed/MaixPy/releases/download/v4.0.0/yolov8n.mud
```

### Storage Full
```bash
# Manual cleanup
rm -rf /root/wildtrap/captures/*

# Or enable auto_cleanup in config
```

### Telegram Not Working
- Verify bot token and chat ID
- Check internet connection
- Test with curl:
```bash
curl "https://api.telegram.org/bot<TOKEN>/getMe"
```

---

## API Reference

### AppState
- `can_capture()` - Check cooldown status
- `record_detection(objects)` - Log detection event
- `save()` - Persist configuration

### CameraController
- `initialize()` - Setup camera and display
- `capture_frame()` - Get single frame
- `capture_photo(filename)` - Save photo
- `capture_burst(base, count)` - Burst mode
- `capture_video(filename, duration)` - Video recording

### Detectors
- `MotionDetector.detect(img)` - Frame differencing
- `AIDetector.detect(img)` - YOLOv8 inference
- `HybridDetector.detect(img)` - Combined pipeline

### CaptureManager
- `save_capture(img, objects, camera)` - Save with metadata
- `cleanup_old_files()` - Storage management

### NotificationManager
- `send_notification(image_path, objects)` - Multi-channel alerts

---

## Performance

| Mode | FPS | Power | Accuracy |
|------|-----|-------|----------|
| Motion | ~30 | Low | Medium |
| AI | ~20 | High | High |
| Hybrid | ~25 | Medium | High |
| Scheduled | Variable | Very Low | N/A |

---

## License

MIT License - Free for personal and commercial use

---

## Support

- GitHub Issues: [Report bugs](https://github.com/yourusername/wildtrap)
- MaixPy Docs: https://wiki.sipeed.com/maixpy
- Community: https://maixhub.com

---

## Credits

Built with:
- [MaixPy](https://github.com/sipeed/MaixPy) - Python framework for MaixCAM
- [YOLOv8](https://github.com/ultralytics/ultralytics) - Object detection
- Architecture inspired by advanced_servo_app.py

---

**Made with ❤️ for wildlife enthusiasts and makers**
