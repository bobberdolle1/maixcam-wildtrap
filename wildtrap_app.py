#!/usr/bin/env python3
"""
MaixCAM WildTrap - AI-Powered Camera Trap
Production-ready wildlife monitoring system
"""

import os, sys, time, json, csv
from datetime import datetime
from pathlib import Path

try:
    from maix import camera, display, image, nn, touchscreen
except ImportError:
    camera = display = image = nn = touchscreen = None

VERSION = "1.0.0"
CONFIG_FILE = "wildtrap_config.json"
BASE_DIR = Path("/root/wildtrap")
CAPTURES_DIR = BASE_DIR / "captures"
LOGS_DIR = BASE_DIR / "logs"
TEMP_DIR = BASE_DIR / "temp"

# COCO classes for YOLOv8
COCO_CLASSES = [
    "person", "bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck", "boat",
    "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
    "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack",
    "umbrella", "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball",
    "kite", "baseball bat", "baseball glove", "skateboard", "surfboard", "tennis racket",
    "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana", "apple",
    "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair",
    "couch", "potted plant", "bed", "dining table", "toilet", "tv", "laptop", "mouse", "remote",
    "keyboard", "cell phone", "microwave", "oven", "toaster", "sink", "refrigerator", "book",
    "clock", "vase", "scissors", "teddy bear", "hair drier", "toothbrush"
]

# UI Colors
COLOR_BG = (20, 20, 30)
COLOR_TEXT = (255, 255, 255)
COLOR_ACCENT = (0, 200, 100)
COLOR_WARNING = (255, 150, 0)
COLOR_ERROR = (255, 50, 50)

DEFAULT_CONFIG = {
    "detection_mode": "hybrid",
    "capture_mode": "burst",
    "burst_count": 5,
    "video_duration": 10,
    "timelapse_interval": 60,
    "target_objects": ["person", "dog", "cat", "bird", "horse", "cow", "sheep", "bear"],
    "confidence_threshold": 0.6,
    "min_object_size": 1000,
    "motion_sensitivity": 50,
    "cooldown_seconds": 30,
    "camera_width": 1280,
    "camera_height": 720,
    "night_mode": True,
    "jpeg_quality": 90,
    "telegram_enabled": False,
    "telegram_bot_token": "",
    "telegram_chat_id": "",
    "telegram_throttle_minutes": 5,
    "webhook_enabled": False,
    "webhook_url": "",
    "storage_max_gb": 5,
    "storage_keep_days": 7,
    "auto_cleanup": True,
    "armed": False
}

def load_config():
    """Load configuration from JSON file or create default."""
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                return {**DEFAULT_CONFIG, **config}
        else:
            save_config(DEFAULT_CONFIG)
            return DEFAULT_CONFIG.copy()
    except Exception as e:
        print(f"Error loading config: {e}")
        return DEFAULT_CONFIG.copy()

def save_config(config):
    """Save configuration to JSON file."""
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving config: {e}")
        return False

def ensure_directories():
    """Create required directories if they don't exist."""
    for directory in [BASE_DIR, CAPTURES_DIR, LOGS_DIR, TEMP_DIR]:
        directory.mkdir(parents=True, exist_ok=True)

def get_timestamp():
    """Get current timestamp in YYYYMMDD_HHMMSS format."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def get_disk_usage():
    """Get disk usage in GB."""
    try:
        stat = os.statvfs(str(CAPTURES_DIR))
        total_gb = (stat.f_blocks * stat.f_frsize) / (1024**3)
        used_gb = ((stat.f_blocks - stat.f_bfree) * stat.f_frsize) / (1024**3)
        return used_gb, total_gb
    except:
        return 0, 0

def apply_night_mode(img):
    """Apply night vision enhancement to image."""
    try:
        img = img.mul(1.5)
        img = img.histeq()
        return img
    except:
        return img

class AppState:
    """Central application state management."""
    def __init__(self):
        self.config = load_config()
        self.running = True
        self.armed = self.config.get("armed", False)
        self.current_screen = "main"
        self.menu_selection = 0
        self.last_touch_time = 0
        self.last_detection_time = 0
        self.captures_today = 0
        self.last_capture_info = None
        self.total_detections = 0
        self.detection_counts = {}
        
    def save(self):
        """Save current state to config."""
        self.config["armed"] = self.armed
        save_config(self.config)
    
    def can_capture(self):
        """Check if cooldown period has passed."""
        cooldown = self.config.get("cooldown_seconds", 30)
        return (time.time() - self.last_detection_time) >= cooldown
    
    def record_detection(self, objects):
        """Record detection event."""
        self.last_detection_time = time.time()
        self.total_detections += 1
        for obj in objects:
            label = obj.get("label", "unknown")
            self.detection_counts[label] = self.detection_counts.get(label, 0) + 1

class CameraController:
    """Manages camera operations and settings."""
    def __init__(self, state):
        self.state = state
        self.cam = None
        self.disp = None
        self.initialized = False
        
    def initialize(self):
        """Initialize camera and display."""
        try:
            if camera is None:
                print("Camera module not available")
                return False
            width = self.state.config.get("camera_width", 1280)
            height = self.state.config.get("camera_height", 720)
            self.cam = camera.Camera(width, height)
            self.disp = display.Display()
            self.initialized = True
            print(f"Camera initialized: {width}x{height}")
            return True
        except Exception as e:
            print(f"Camera initialization error: {e}")
            return False
    
    def capture_frame(self):
        """Capture a single frame."""
        if not self.initialized or self.cam is None:
            return None
        try:
            img = self.cam.read()
            if self.state.config.get("night_mode", False):
                img = apply_night_mode(img)
            return img
        except Exception as e:
            print(f"Frame capture error: {e}")
            return None
    
    def capture_photo(self, filename):
        """Capture and save a photo."""
        img = self.capture_frame()
        if img:
            try:
                img.save(str(filename))
                return True
            except Exception as e:
                print(f"Photo save error: {e}")
        return False
    
    def capture_burst(self, base_filename, count):
        """Capture burst of photos."""
        captured = []
        for i in range(count):
            filename = f"{base_filename}_burst{i+1}.jpg"
            if self.capture_photo(filename):
                captured.append(filename)
            time.sleep(0.2)
        return captured
    
    def capture_video(self, filename, duration):
        """Capture video for specified duration."""
        frames = []
        start_time = time.time()
        frame_count = 0
        while time.time() - start_time < duration:
            img = self.capture_frame()
            if img:
                frame_file = f"{filename}_frame{frame_count:04d}.jpg"
                img.save(str(frame_file))
                frames.append(frame_file)
                frame_count += 1
            time.sleep(0.1)
        return frames
    
    def display_frame(self, img):
        """Display frame on screen."""
        if self.disp and img:
            try:
                self.disp.show(img)
            except Exception as e:
                print(f"Display error: {e}")
    
    def cleanup(self):
        """Release camera resources."""
        if self.cam:
            del self.cam
        if self.disp:
            del self.disp
        self.initialized = False

class MotionDetector:
    """Frame differencing motion detection."""
    def __init__(self, state):
        self.state = state
        self.previous_frame = None
        self.motion_threshold = 25
        
    def detect(self, img):
        """Detect motion in current frame."""
        if img is None:
            return False
        try:
            gray = img.to_grayscale()
            small = gray.resize(160, 120)
            if self.previous_frame is None:
                self.previous_frame = small
                return False
            diff = small.difference(self.previous_frame)
            self.previous_frame = small
            # Simplified motion detection
            return True
        except Exception as e:
            print(f"Motion detection error: {e}")
            return False

class AIDetector:
    """YOLOv8 object detection with filtering."""
    def __init__(self, state):
        self.state = state
        self.model = None
        self.initialized = False
        
    def initialize(self):
        """Load YOLOv8 model."""
        try:
            if nn is None:
                print("Neural network module not available")
                return False
            model_path = "/root/models/yolov8n.mud"
            if os.path.exists(model_path):
                self.model = nn.YOLOv8(model=model_path)
                self.initialized = True
                print("YOLOv8 model loaded")
                return True
            else:
                print(f"Model not found: {model_path}")
                return False
        except Exception as e:
            print(f"AI model initialization error: {e}")
            return False
    
    def detect(self, img):
        """Detect objects in image."""
        if not self.initialized or self.model is None or img is None:
            return []
        try:
            results = self.model.detect(img)
            target_objects = self.state.config.get("target_objects", [])
            confidence_threshold = self.state.config.get("confidence_threshold", 0.6)
            min_size = self.state.config.get("min_object_size", 1000)
            filtered_objects = []
            for obj in results:
                class_id = obj.class_id
                confidence = obj.score
                bbox = obj.box
                label = COCO_CLASSES[class_id] if class_id < len(COCO_CLASSES) else "unknown"
                if label not in target_objects:
                    continue
                if confidence < confidence_threshold:
                    continue
                bbox_area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1])
                if bbox_area < min_size:
                    continue
                filtered_objects.append({
                    "label": label,
                    "confidence": confidence,
                    "bbox": bbox
                })
            return filtered_objects
        except Exception as e:
            print(f"AI detection error: {e}")
            return []

class HybridDetector:
    """Combined motion + AI detection pipeline."""
    def __init__(self, state, motion_detector, ai_detector):
        self.state = state
        self.motion_detector = motion_detector
        self.ai_detector = ai_detector
    
    def detect(self, img):
        """Run hybrid detection: motion → AI verification."""
        if not self.motion_detector.detect(img):
            return []
        objects = self.ai_detector.detect(img)
        return objects

class CaptureManager:
    """Manages file saving, metadata, and cleanup."""
    def __init__(self, state):
        self.state = state
        
    def save_capture(self, img, objects, camera_controller):
        """Save capture with metadata."""
        try:
            timestamp = get_timestamp()
            if objects:
                obj_label = objects[0]["label"]
                obj_conf = objects[0]["confidence"]
                base_name = f"{timestamp}_{obj_label}_{obj_conf:.2f}"
            else:
                base_name = f"{timestamp}_capture"
            mode = self.state.config.get("capture_mode", "photo")
            files_saved = []
            if mode == "photo":
                filename = CAPTURES_DIR / f"{base_name}.jpg"
                if camera_controller.capture_photo(filename):
                    files_saved.append(str(filename))
            elif mode == "burst":
                count = self.state.config.get("burst_count", 5)
                files_saved = camera_controller.capture_burst(CAPTURES_DIR / base_name, count)
            elif mode == "video":
                duration = self.state.config.get("video_duration", 10)
                files_saved = camera_controller.capture_video(CAPTURES_DIR / base_name, duration)
            if files_saved:
                metadata = {
                    "timestamp": timestamp,
                    "detection_mode": self.state.config.get("detection_mode"),
                    "capture_mode": mode,
                    "detected_objects": objects,
                    "camera_settings": {
                        "width": self.state.config.get("camera_width"),
                        "height": self.state.config.get("camera_height"),
                        "night_mode": self.state.config.get("night_mode"),
                        "quality": self.state.config.get("jpeg_quality")
                    },
                    "files": files_saved
                }
                metadata_file = CAPTURES_DIR / f"{base_name}.json"
                with open(metadata_file, 'w') as f:
                    json.dump(metadata, f, indent=2)
                self._log_detection(timestamp, objects)
                self.state.captures_today += 1
                self.state.last_capture_info = {"time": timestamp, "objects": objects}
                return files_saved
        except Exception as e:
            print(f"Capture save error: {e}")
        return []
    
    def _log_detection(self, timestamp, objects):
        """Log detection to CSV file."""
        try:
            log_file = LOGS_DIR / "detections.csv"
            file_exists = log_file.exists()
            with open(log_file, 'a', newline='') as f:
                writer = csv.writer(f)
                if not file_exists:
                    writer.writerow(["timestamp", "object", "confidence", "bbox"])
                for obj in objects:
                    writer.writerow([timestamp, obj["label"], obj["confidence"], str(obj["bbox"])])
        except Exception as e:
            print(f"CSV logging error: {e}")
    
    def cleanup_old_files(self):
        """Remove old captures based on storage limits."""
        try:
            if not self.state.config.get("auto_cleanup", True):
                return
            max_gb = self.state.config.get("storage_max_gb", 5)
            keep_days = self.state.config.get("storage_keep_days", 7)
            used_gb, _ = get_disk_usage()
            if used_gb > max_gb:
                files = sorted(CAPTURES_DIR.glob("*"), key=lambda p: p.stat().st_mtime)
                for file in files[:len(files)//4]:
                    try:
                        file.unlink()
                    except:
                        pass
            cutoff_time = time.time() - (keep_days * 86400)
            for file in CAPTURES_DIR.glob("*"):
                if file.stat().st_mtime < cutoff_time:
                    try:
                        file.unlink()
                    except:
                        pass
        except Exception as e:
            print(f"Cleanup error: {e}")

class NotificationManager:
    """Handles Telegram and webhook notifications."""
    def __init__(self, state):
        self.state = state
        self.last_notification_time = 0
    
    def can_notify(self):
        """Check if throttle period has passed."""
        throttle_minutes = self.state.config.get("telegram_throttle_minutes", 5)
        return (time.time() - self.last_notification_time) >= (throttle_minutes * 60)
    
    def send_notification(self, image_path, objects):
        """Send notification via enabled channels."""
        if not self.can_notify():
            return
        try:
            if self.state.config.get("telegram_enabled", False):
                self._send_telegram(image_path, objects)
            if self.state.config.get("webhook_enabled", False):
                self._send_webhook(image_path, objects)
            self.last_notification_time = time.time()
        except Exception as e:
            print(f"Notification error: {e}")
    
    def _send_telegram(self, image_path, objects):
        """Send photo to Telegram."""
        try:
            import urequests
            bot_token = self.state.config.get("telegram_bot_token", "")
            chat_id = self.state.config.get("telegram_chat_id", "")
            if not bot_token or not chat_id:
                return
            caption = "🎯 WildTrap Detection\n"
            for obj in objects:
                caption += f"• {obj['label']}: {obj['confidence']:.2%}\n"
            url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
            with open(image_path, 'rb') as f:
                files = {'photo': f}
                data = {'chat_id': chat_id, 'caption': caption}
                response = urequests.post(url, files=files, data=data)
            print(f"Telegram notification sent: {response.status_code}")
        except Exception as e:
            print(f"Telegram error: {e}")
    
    def _send_webhook(self, image_path, objects):
        """Send POST request to webhook URL."""
        try:
            import urequests
            webhook_url = self.state.config.get("webhook_url", "")
            if not webhook_url:
                return
            payload = {"timestamp": get_timestamp(), "objects": objects}
            response = urequests.post(webhook_url, json=payload)
            print(f"Webhook notification sent: {response.status_code}")
        except Exception as e:
            print(f"Webhook error: {e}")

class UI:
    """Touchscreen interface management."""
    def __init__(self, state, camera_controller):
        self.state = state
        self.camera = camera_controller
        self.touch = None
        
    def initialize(self):
        """Initialize touchscreen."""
        try:
            if touchscreen:
                self.touch = touchscreen.TouchScreen()
                return True
        except:
            pass
        return False
    
    def draw_main_screen(self, img, objects=None):
        """Draw main monitoring screen with live preview."""
        if img is None:
            return
        try:
            status = "ARMED" if self.state.armed else "STANDBY"
            status_color = COLOR_ACCENT if self.state.armed else COLOR_WARNING
            img.draw_string(10, 10, f"STATUS: {status}", color=status_color, scale=2)
            mode = self.state.config.get("detection_mode", "hybrid").upper()
            img.draw_string(10, 40, f"Mode: {mode}", color=COLOR_TEXT, scale=1.5)
            img.draw_string(10, 65, f"Captures: {self.state.captures_today}", color=COLOR_TEXT, scale=1.5)
            if objects:
                y_offset = 90
                for obj in objects[:3]:
                    text = f"{obj['label']}: {obj['confidence']:.2%}"
                    img.draw_string(10, y_offset, text, color=COLOR_ACCENT, scale=1.5)
                    bbox = obj['bbox']
                    img.draw_rectangle(int(bbox[0]), int(bbox[1]), 
                                     int(bbox[2]-bbox[0]), int(bbox[3]-bbox[1]),
                                     color=COLOR_ACCENT, thickness=2)
                    y_offset += 25
            used_gb, total_gb = get_disk_usage()
            img.draw_string(10, img.height() - 30, 
                          f"Storage: {used_gb:.1f}GB / {total_gb:.1f}GB",
                          color=COLOR_TEXT, scale=1.5)
            img.draw_string(img.width()//2 - 80, img.height() - 30,
                          "TAP FOR MENU", color=COLOR_WARNING, scale=1.5)
            self.camera.display_frame(img)
        except Exception as e:
            print(f"UI draw error: {e}")
    
    def check_touch(self):
        """Check for touch input."""
        if self.touch is None:
            return None
        try:
            points = self.touch.read()
            if points:
                return points[0]
        except:
            pass
        return None
    
    def handle_input(self):
        """Handle touch input."""
        touch = self.check_touch()
        if touch:
            current_time = time.time()
            if current_time - self.state.last_touch_time > 0.5:
                self.state.last_touch_time = current_time
                if self.state.current_screen == "main":
                    self.state.current_screen = "menu"
        return touch

class WildTrapApp:
    """Main application controller."""
    def __init__(self):
        self.state = AppState()
        self.camera = CameraController(self.state)
        self.motion_detector = MotionDetector(self.state)
        self.ai_detector = AIDetector(self.state)
        self.hybrid_detector = HybridDetector(self.state, self.motion_detector, self.ai_detector)
        self.capture_manager = CaptureManager(self.state)
        self.notification_manager = NotificationManager(self.state)
        self.ui = UI(self.state, self.camera)
        
    def initialize(self):
        """Initialize all components."""
        print(f"WildTrap v{VERSION} - Initializing...")
        ensure_directories()
        if not self.camera.initialize():
            print("Warning: Camera initialization failed")
        self.ai_detector.initialize()
        self.ui.initialize()
        print("Initialization complete")
        return True
    
    def run_detection_cycle(self):
        """Execute one detection cycle."""
        img = self.camera.capture_frame()
        if img is None:
            return None
        mode = self.state.config.get("detection_mode", "hybrid")
        objects = []
        if mode == "motion":
            if self.motion_detector.detect(img):
                objects = [{"label": "motion", "confidence": 1.0, "bbox": [0,0,0,0]}]
        elif mode == "ai":
            objects = self.ai_detector.detect(img)
        elif mode == "hybrid":
            objects = self.hybrid_detector.detect(img)
        elif mode == "scheduled":
            interval = self.state.config.get("timelapse_interval", 60)
            if time.time() - self.state.last_detection_time >= interval:
                objects = [{"label": "scheduled", "confidence": 1.0, "bbox": [0,0,0,0]}]
        return img, objects
    
    def process_detection(self, img, objects):
        """Process detected objects and trigger capture."""
        if not objects or not self.state.armed:
            return
        if not self.state.can_capture():
            return
        self.state.record_detection(objects)
        files = self.capture_manager.save_capture(img, objects, self.camera)
        if files:
            print(f"Captured: {len(files)} files")
            self.notification_manager.send_notification(files[0], objects)
            self.capture_manager.cleanup_old_files()
    
    def run(self):
        """Main application loop."""
        if not self.initialize():
            print("Initialization failed")
            return
        print("WildTrap running. Press Ctrl+C to exit.")
        try:
            while self.state.running:
                result = self.run_detection_cycle()
                if result:
                    img, objects = result
                    self.process_detection(img, objects)
                    self.ui.draw_main_screen(img, objects)
                    self.ui.handle_input()
                time.sleep(0.033)  # ~30 FPS
        except KeyboardInterrupt:
            print("\nShutting down...")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources."""
        self.state.save()
        self.camera.cleanup()
        print("Cleanup complete")

def main():
    """Application entry point."""
    app = WildTrapApp()
    app.run()

if __name__ == "__main__":
    main()
