import os
import subprocess
import re

# Функція для розрізання відео на частини
def split_video(input_file, output_folder, segments):
    """Розбиває відео на частини"""
    for idx, segment in enumerate(segments):
        start_time, end_time = segment
        output_file = os.path.join(output_folder, f"part_{idx + 1}.mp4")
        command = f"ffmpeg -i \"{input_file}\" -ss {start_time} -to {end_time} -c copy \"{output_file}\""
        subprocess.run(command, shell=True)
        print(f"Частина {idx + 1} збережена як {output_file}")

# Функція для об'єднання відео з папки у один файл
def combine_videos(input_folder, output_file):
    """Об'єднує відео у один файл"""
    # Отримуємо список всіх mp4 файлів у папці та сортуємо їх
    files = sorted(
        [f for f in os.listdir(input_folder) if f.endswith('.mp4')],
        key=lambda x: int(re.search(r'\d+', x).group())
    )

    # Створюємо тимчасовий текстовий файл зі списком файлів для об'єднання
    with open("file_list.txt", "w") as f:
        for file in files:
            f.write(f"file '{os.path.join(input_folder, file)}'\n")

    # Виконуємо об'єднання файлів за допомогою ffmpeg
    ffmpeg_command = ["ffmpeg", "-f", "concat", "-safe", "0", "-i", "file_list.txt", "-c", "copy", output_file]
    subprocess.run(ffmpeg_command)

    # Видаляємо тимчасовий файл зі списком
    os.remove("file_list.txt")
    print(f"Сборка завершена: {output_file}")

# Головна програма з вибором дії
if __name__ == '__main__':
    action = input("Виберіть дію: 'розрізати' або 'об'єднати': ").strip().lower()

    if action == 'розрізати':
        # Папка з відео для порізки
        split_folder = '!split'  # Папка з відео для порізки

        # Перевірка наявності папки для відео порізки
        if not os.path.exists(split_folder):
            print(f"Папка {split_folder} не знайдена.")
            exit()

        # Показуємо файли в папці
        files = [f for f in os.listdir(split_folder) if os.path.isfile(os.path.join(split_folder, f))]
        print("Доступні файли для порізки:")
        for i, file in enumerate(files):
            print(f"{i + 1}: {file}")

        # Вибір файлу для порізки
        file_index = int(input("Введіть номер файлу для порізки: ").strip()) - 1
        if file_index < 0 or file_index >= len(files):
            print("Неправильний вибір файлу.")
            exit()

        input_file = os.path.join(split_folder, files[file_index])

        # Питання про розбиття відео на частини
        num_segments = int(input("Скільки частин потрібно? Введіть число: ").strip())
        segments = []
        for i in range(num_segments):
            start_time = input(f"Час початку для частини {i + 1} (у форматі hh:mm:ss): ").strip()
            end_time = input(f"Час завершення для частини {i + 1} (у форматі hh:mm:ss): ").strip()
            segments.append((start_time, end_time))

        # Створення папки для збереження порізаних частин
        output_folder = '!split_parts'
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Виконуємо розрізання
        split_video(input_file, output_folder, segments)
        print("Порізка файлу завершена!")

        # Пропонуємо користувачу об'єднати щойно створені частини
        combine_now = input("Чи потрібно об'єднати щойно створені частини у один файл? (y/n): ").strip().lower()
        if combine_now == 'y':
            output_file = os.path.join(output_folder, "output.mp4")
            combine_videos(output_folder, output_file)
            print("Об'єднання відео завершено!")

    elif action == 'об\'єднати':
        # Папка з частинами відео для об'єднання
        input_folder = '!split_parts'
        output_file = os.path.join(input_folder, "output.mp4")

        # Перевірка наявності папки для об'єднання частин
        if not os.path.exists(input_folder):
            print(f"Папка {input_folder} не знайдена.")
            exit()

        # Виконуємо об'єднання відео
        combine_videos(input_folder, output_file)
        print("Об'єднання відео завершено!")

    else:
        print("Неправильний вибір дії. Спробуйте ще раз.")