# 🎯 MaixCAM WildTrap - START HERE

**AI-Powered Camera Trap for MaixCAM**

---

## 📁 What's Included

| File | Size | Description |
|------|------|-------------|
| **wildtrap_app.py** | 24KB | Main production application |
| **simple_wildtrap.py** | 7.2KB | Educational simplified version |
| **wildtrap_config.json** | 716B | Configuration file |
| **README.md** | 7.6KB | Full documentation (English) |
| **README_RU.md** | 6.2KB | Full documentation (Russian) |
| **QUICKSTART.md** | 4.5KB | 5-minute setup guide |
| **EXAMPLES.md** | 8KB | Real-world configurations |
| **PROJECT_INFO.md** | 11KB | Technical architecture |
| **DELIVERY_SUMMARY.md** | 9.6KB | Project completion report |

**Total**: 9 files, 88KB

---

## 🚀 Quick Start (3 Steps)

### 1. Copy to MaixCAM
```bash
scp wildtrap_app.py wildtrap_config.json root@<MAIXCAM_IP>:/root/
```

### 2. Setup Directories
```bash
ssh root@<MAIXCAM_IP>
mkdir -p /root/wildtrap/{captures,logs,temp}
```

### 3. Run
```bash
python3 wildtrap_app.py
```

**Done!** Camera trap is now running.

---

## 📖 Documentation Guide

### New Users
1. **Read**: [QUICKSTART.md](QUICKSTART.md) - 5-minute setup
2. **Try**: Run `simple_wildtrap.py` to understand basics
3. **Configure**: Edit `wildtrap_config.json` for your needs

### Experienced Users
1. **Read**: [README.md](README.md) - Full feature documentation
2. **Configure**: Use [EXAMPLES.md](EXAMPLES.md) for your use case
3. **Deploy**: Run `wildtrap_app.py` in production

### Developers
1. **Read**: [PROJECT_INFO.md](PROJECT_INFO.md) - Architecture
2. **Study**: Review `wildtrap_app.py` source code
3. **Extend**: Modify and customize

### Russian Speakers
1. **Читать**: [README_RU.md](README_RU.md) - Полная документация
2. **Настроить**: Редактировать `wildtrap_config.json`
3. **Запустить**: `python3 wildtrap_app.py`

---

## ⚡ Features at a Glance

### Detection
- ✅ Motion Detection (fast, energy-efficient)
- ✅ AI Detection (YOLOv8, 80 object classes)
- ✅ Hybrid Mode (motion → AI verification)
- ✅ Scheduled Mode (timelapse)

### Capture
- ✅ Photo (single shot)
- ✅ Burst (3/5/10 photos)
- ✅ Video (5/10/15/30 seconds)
- ✅ Timelapse (scheduled intervals)

### Smart Features
- ✅ Object filtering (target specific animals/people)
- ✅ Night mode (auto brightness enhancement)
- ✅ Metadata logging (JSON + CSV)
- ✅ Telegram notifications
- ✅ HTTP webhooks
- ✅ Auto-cleanup (storage management)
- ✅ Touchscreen UI
- ✅ Energy saving

---

## 🎯 Common Use Cases

### Wildlife Monitoring
```json
{
  "detection_mode": "hybrid",
  "capture_mode": "burst",
  "target_objects": ["dog", "cat", "bird", "deer", "bear"]
}
```

### Security Camera
```json
{
  "detection_mode": "hybrid",
  "capture_mode": "video",
  "target_objects": ["person", "car"],
  "night_mode": true
}
```

### Bird Watching
```json
{
  "detection_mode": "ai",
  "capture_mode": "burst",
  "target_objects": ["bird"],
  "burst_count": 10
}
```

**More examples**: See [EXAMPLES.md](EXAMPLES.md)

---

## 🔧 Basic Configuration

Edit `wildtrap_config.json`:

```json
{
  "detection_mode": "hybrid",        // motion, ai, hybrid, scheduled
  "capture_mode": "burst",           // photo, burst, video, timelapse
  "target_objects": ["person", "dog", "cat"],
  "confidence_threshold": 0.6,       // 0.3-0.9
  "cooldown_seconds": 30,            // delay between captures
  "armed": true                      // enable/disable detection
}
```

---

## 📱 Telegram Notifications

1. Create bot: [@BotFather](https://t.me/botfather)
2. Get chat ID: [@userinfobot](https://t.me/userinfobot)
3. Configure:

```json
{
  "telegram_enabled": true,
  "telegram_bot_token": "YOUR_BOT_TOKEN",
  "telegram_chat_id": "YOUR_CHAT_ID"
}
```

---

## 🐛 Troubleshooting

### Camera not working
```bash
ls /dev/video*
systemctl restart camera
```

### AI model missing
```bash
cd /root/models
wget https://github.com/sipeed/MaixPy/releases/download/v4.0.0/yolov8n.mud
```

### No detections
- Check `"armed": true` in config
- Lower `confidence_threshold` to 0.5
- Verify `target_objects` includes what you're testing

**More help**: See [README.md](README.md) troubleshooting section

---

## 📊 Project Status

- ✅ **Production Ready** - Fully tested and documented
- ✅ **Complete** - All features implemented
- ✅ **Documented** - English + Russian docs
- ✅ **Examples** - 8 real-world configurations
- ✅ **Educational** - Simplified version included

---

## 🎓 Learning Path

1. **Beginner**: Read QUICKSTART.md → Run simple_wildtrap.py
2. **Intermediate**: Read README.md → Deploy wildtrap_app.py
3. **Advanced**: Read PROJECT_INFO.md → Customize code

---

## 📞 Support

- **Documentation**: README.md, QUICKSTART.md, EXAMPLES.md
- **MaixPy Wiki**: https://wiki.sipeed.com/maixpy
- **Community**: https://maixhub.com

---

## 📄 License

MIT License - Free for personal and commercial use

---

## 🎉 Ready to Start?

### Option 1: Quick Deploy (5 minutes)
→ Follow [QUICKSTART.md](QUICKSTART.md)

### Option 2: Learn First (15 minutes)
→ Read [README.md](README.md)

### Option 3: Explore Examples (10 minutes)
→ Browse [EXAMPLES.md](EXAMPLES.md)

---

**Choose your path and start trapping! 🎯**

**Version**: 1.0.0  
**Status**: Production Ready ✅  
**License**: MIT
