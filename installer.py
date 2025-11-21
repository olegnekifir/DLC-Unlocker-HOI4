import os
import shutil
import sys
from colorama import init, Fore, Style

# Инициализация Colorama для поддержки цветного вывода в Windows
init()

def get_script_directory():
    """
    Определяет правильную директорию скрипта, учитывая компиляцию в exe
    """
    if getattr(sys, 'frozen', False):
        # Если скрипт скомпилирован в exe
        return os.path.dirname(sys.executable)
    else:
        # Если скрипт запущен как .py файл
        return os.path.dirname(os.path.abspath(__file__))

def find_hoi4_directory():
    """
    Функция выполняет поиск директории Hearts of Iron IV в стандартных расположениях,
    в текущей директории или запрашивает путь у пользователя.
    """
    # Стандартные пути установки HOI4 для разных платформ
    common_paths = [
        # Windows (Steam)
        os.path.expandvars("%PROGRAMFILES(X86)%\\Steam\\steamapps\\common\\Hearts of Iron IV"),
        # Windows (Steam альтернативный)
        os.path.expandvars("%PROGRAMFILES%\\Steam\\steamapps\\common\\Hearts of Iron IV"),
        # Linux (Steam)
        os.path.expanduser("~/.steam/steam/steamapps/common/Hearts of Iron IV"),
        # macOS (Steam)
        os.path.expanduser("~/Library/Application Support/Steam/steamapps/common/Hearts of Iron IV")
    ]
    
    # Проверка стандартных путей
    for path in common_paths:
        if os.path.exists(path):
            print(Fore.GREEN + f"Найдена стандартная директория: {path}" + Style.RESET_ALL)
            return path
    
    # Проверка текущей директории на наличие папки dlc
    current_dir = os.getcwd()
    if os.path.exists(os.path.join(current_dir, "dlc")):
        print(Fore.GREEN + "Обнаружена папка dlc в текущей директории" + Style.RESET_ALL)
        return current_dir
    
    # Ручной ввод пути
    print(Fore.YELLOW + "Автоматический поиск не дал результатов." + Style.RESET_ALL)
    while True:
        user_path = input("Введите путь к директории Hearts of Iron IV: ").strip()
        # Удаляем кавычки если они есть
        user_path = user_path.strip('"')
        if os.path.exists(user_path):
            return user_path
        else:
            print(Fore.RED + "Ошибка: Указанная директория не существует!" + Style.RESET_ALL)

def main():
    """
    Основная логика скрипта:
    1. Поиск директории игры
    2. Удаление папки dlc
    3. Копирование файлов
    """
    script_dir = get_script_directory()
    print(Fore.CYAN + f"Директория скрипта: {script_dir}" + Style.RESET_ALL)
    
    print(Fore.CYAN + "Поиск директории Hearts of Iron IV..." + Style.RESET_ALL)
    game_dir = find_hoi4_directory()
    
    # Определение путей для операций
    dlc_path = os.path.join(game_dir, "dlc")
    files_src = os.path.join(script_dir, "Files")
    
    print(Fore.CYAN + f"Поиск папки Files: {files_src}" + Style.RESET_ALL)
    
    # Проверка существования исходной папки Files
    if not os.path.exists(files_src):
        print(Fore.RED + f"Ошибка: Папка 'Files' не найдена по пути: {files_src}" + Style.RESET_ALL)
        print(Fore.YELLOW + "Убедитесь, что папка 'Files' находится в той же директории, что и скрипт!" + Style.RESET_ALL)
        
        # Показываем содержимое директории скрипта для отладки
        print(Fore.CYAN + "Содержимое директории скрипта:" + Style.RESET_ALL)
        for item in os.listdir(script_dir):
            item_path = os.path.join(script_dir, item)
            if os.path.isdir(item_path):
                print(Fore.BLUE + f"[DIR] {item}" + Style.RESET_ALL)
            else:
                print(Fore.WHITE + f"[FILE] {item}" + Style.RESET_ALL)
        
        input("Нажмите Enter для выхода...")
        sys.exit(1)
    
    try:
        # Удаление папки dlc
        if os.path.exists(dlc_path):
            print(Fore.YELLOW + f"Удаление существующей папки dlc: {dlc_path}" + Style.RESET_ALL)
            shutil.rmtree(dlc_path)
        else:
            print(Fore.YELLOW + "Папка dlc не найдена, создание новой..." + Style.RESET_ALL)
        
        # Копирование новых файлов
        print(Fore.YELLOW + f"Копирование файлов из {files_src} в {game_dir}..." + Style.RESET_ALL)
        
        # Создаем папку dlc если она не существует
        os.makedirs(os.path.dirname(dlc_path), exist_ok=True)
        
        # Копируем все содержимое папки Files
        for item in os.listdir(files_src):
            src = os.path.join(files_src, item)
            dst = os.path.join(game_dir, item)
            
            print(Fore.WHITE + f"Копирование: {item}" + Style.RESET_ALL)
            
            if os.path.isdir(src):
                shutil.copytree(src, dst, dirs_exist_ok=True)
            else:
                # Создаем директорию для файла если нужно
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copy2(src, dst)
                
        print(Fore.GREEN + "Установка успешно завершена!" + Style.RESET_ALL)
        
    except Exception as e:
        print(Fore.RED + f"Критическая ошибка: {str(e)}" + Style.RESET_ALL)
        import traceback
        traceback.print_exc()
        input("Нажмите Enter для выхода...")
        sys.exit(1)

if __name__ == "__main__":
    main()