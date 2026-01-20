import pytesseract
from PIL import Image, ImageGrab, ImageEnhance
import pyautogui
import time
import random

# Путь к tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def click_center_screen():
    """Кликает по центру экрана"""
    screen_width, screen_height = pyautogui.size()
    center_x = screen_width // 2
    center_y = screen_height // 2
    print(f"Кликаю по центру: ({center_x}, {center_y})")
    pyautogui.click(center_x, center_y)
    time.sleep(1)  # Задержка после клика


def improve_image_quality(image):
    """Улучшает качество изображения для распознавания"""
    # Конвертируем в grayscale
    image = image.convert('L')

    # Увеличиваем контрастность
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2.0)

    return image


def get_text_from_region(x1, y1, x2, y2):
    """Распознает текст с правильными настройками для русского"""
    try:
        # Делаем скриншот
        screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        print(f"Размер скриншота: {screenshot.size}")

        # Улучшаем изображение
        improved = improve_image_quality(screenshot)
        improved.save("debug_russian.png")
        print("Скриншот для распознавания сохранен как 'debug_russian.png'")

        # Настройки для русского текста
        custom_config = r'--oem 3 --psm 6'

        # Распознаем на русском
        text = pytesseract.image_to_string(improved, lang='rus', config=custom_config)
        text = text.strip()

        print(f"Сырой распознанный текст: '{text}'")
        return text

    except Exception as e:
        print(f"Ошибка при распознавании: {e}")
        return ""


def type_like_human(text, min_delay=0.03, max_delay=0.12):
    """Печатает текст как человек"""
    print(f"Начинаю печатать: '{text}'")

    for char in text:
        pyautogui.write(char)
        time.sleep(random.uniform(min_delay, max_delay))


def main():
    # Ваши координаты
    region_coords = (169, 431, 1708, 639)

    print("=== АВТОМАТИЧЕСКИЙ ВВОД ТЕКСТА ===")
    print(f"Область распознавания: {region_coords}")

    # Подготовка
    print("Начинаю через 5 секунд...")
    for i in range(5, 0, -1):
        print(f"{i}...")
        time.sleep(1)

    try:
        # 1. Кликаем по центру экрана
        print("1. Кликаю по центру экрана...")
        click_center_screen()

        # 2. Задержка 2 секунды перед распознаванием
        print("2. Жду 2 секунды...")
        time.sleep(2)

        # 3. Распознаем текст
        print("3. Распознаю текст...")
        text = get_text_from_region(*region_coords)

        # 4. Проверяем результат и печатаем
        if text and len(text) > 5:  # Если распознано больше 5 символов
            print(f"✅ Успешно распознано: '{text}'")
            print("4. Печатаю распознанный текст...")
            type_like_human(text)
        else:
            print("❌ Текст не распознан, использую текст по умолчанию")
            default_text = "видеть лишь за белый а показаться тот дом потом"
            print(f"4. Печатаю текст по умолчанию: '{default_text}'")
            type_like_human(default_text)

        print("✅ Текст успешно введен!")

    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")


if __name__ == "__main__":
    main()