import time
import logging

# Налаштування логування
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def check_new_contracts():
    """
    Тимчасова функція для перевірки нових контрактів.
    Пізніше тут буде логіка підключення до BNB ноди.
    """
    logging.info("Перевірка нових контрактів...")
    # TODO: додати перевірку контрактів
    time.sleep(2)  # Затримка для імітації роботи

def main():
    logging.info("Старт бота для моніторингу контрактів...")
    try:
        while True:
            check_new_contracts()
    except KeyboardInterrupt:
        logging.info("Бот зупинений вручну.")

if __name__ == "__main__":
    main()
