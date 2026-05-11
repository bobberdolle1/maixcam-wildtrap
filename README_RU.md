# MaixCAM WildTrap 🎯

**AI-фотоловушка для мониторинга дикой природы**

Готовое к использованию приложение для MaixCAM с автоматической детекцией, съемкой и уведомлениями.

---

## Возможности

### Режимы детекции
- **Motion Detection** - Энергоэффективное определение движения
- **AI Detection** - Распознавание объектов YOLOv8 (животные, люди, транспорт)
- **Hybrid Mode** ⭐ - Движение → AI проверка (рекомендуется)
- **Scheduled Mode** - Таймлапс съемка по расписанию

### Режимы съемки
- **Photo** - Одиночное фото высокого качества
- **Burst** - Серия из 3/5/10 фотографий
- **Video** - Запись видео 5/10/15/30 секунд
- **Timelapse** - Периодическая съемка при детекции

### Умные функции
- 🎯 **Фильтрация объектов** - Выбор конкретных животных/людей
- 🌙 **Ночной режим** - Автоматическое улучшение яркости/контраста
- 📊 **Логирование метаданных** - JSON + CSV история детекций
- 🔔 **Уведомления** - Telegram Bot + HTTP Webhook
- 💾 **Авто-очистка** - Автоматическое управление хранилищем
- ⚡ **Энергосбережение** - Оптимизированный pipeline детекции
- 📱 **Сенсорный UI** - Простая настройка и мониторинг

---

## Быстрый старт

### 1. Установка

```bash
# Копируем файлы на MaixCAM
scp wildtrap_app.py wildtrap_config.json root@maixcam:/root/

# Подключаемся по SSH
ssh root@maixcam

# Создаем директории
mkdir -p /root/wildtrap/{captures,logs,temp}
```

### 2. Настройка

Редактируем `wildtrap_config.json`:

```json
{
  "detection_mode": "hybrid",
  "capture_mode": "burst",
  "target_objects": ["dog", "cat", "bird", "person"],
  "confidence_threshold": 0.6,
  "cooldown_seconds": 30,
  "telegram_enabled": true,
  "telegram_bot_token": "ВАШ_ТОКЕН_БОТА",
  "telegram_chat_id": "ВАШ_CHAT_ID"
}
```

### 3. Запуск

```bash
python3 wildtrap_app.py
```

---

## Руководство по настройке

### Параметры детекции

| Параметр | Значения | Описание |
|----------|----------|----------|
| `detection_mode` | motion / ai / hybrid / scheduled | Метод детекции |
| `motion_sensitivity` | 20-100 | Порог чувствительности движения |
| `confidence_threshold` | 0.3-0.9 | Минимальная уверенность AI |
| `min_object_size` | пиксели | Фильтр мелких объектов |
| `cooldown_seconds` | секунды | Задержка между съемками |

### Целевые объекты

Доступные COCO классы:
- **Животные**: dog, cat, bird, horse, cow, sheep, bear, elephant, zebra, giraffe
- **Люди**: person
- **Транспорт**: car, truck, motorcycle, bus

### Настройки камеры

| Параметр | Значения | Описание |
|----------|----------|----------|
| `camera_width` | 320/640/1280/1920 | Ширина разрешения |
| `camera_height` | 240/480/720/1080 | Высота разрешения |
| `night_mode` | true/false | Авто-усиление яркости |
| `jpeg_quality` | 1-100 | Качество сжатия |

### Уведомления Telegram

1. Создайте бота через [@BotFather](https://t.me/botfather)
2. Получите токен бота
3. Узнайте свой chat ID через [@userinfobot](https://t.me/userinfobot)
4. Настройте:

```json
{
  "telegram_enabled": true,
  "telegram_bot_token": "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11",
  "telegram_chat_id": "123456789",
  "telegram_throttle_minutes": 5
}
```

---

## Структура файлов

```
/root/wildtrap/
├── captures/              # Сохраненные фото/видео
│   ├── 20260510_143022_dog_0.87.jpg
│   ├── 20260510_143022_dog_0.87.json
│   └── ...
├── logs/
│   └── detections.csv    # История детекций
└── temp/                 # Временные файлы
```

---

## Рекомендуемые настройки

### Мониторинг дикой природы (день)
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

### Охранная камера (24/7)
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

### Наблюдение за птицами
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

---

## Производительность

| Режим | FPS | Энергия | Точность |
|-------|-----|---------|----------|
| Motion | ~30 | Низкая | Средняя |
| AI | ~20 | Высокая | Высокая |
| Hybrid | ~25 | Средняя | Высокая |
| Scheduled | Переменная | Очень низкая | N/A |

---

## Лицензия

MIT License - Свободно для личного и коммерческого использования

---

## Поддержка

- GitHub Issues: [Сообщить об ошибке](https://github.com/yourusername/wildtrap)
- MaixPy Docs: https://wiki.sipeed.com/maixpy
- Сообщество: https://maixhub.com

---

**Сделано с ❤️ для любителей дикой природы и мейкеров**
