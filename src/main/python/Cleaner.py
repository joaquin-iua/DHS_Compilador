import re
import os

class Cleaner:

    @staticmethod
    def clean_file(file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Filtrar las líneas que contienen código
        filtered_lines = [line.strip() for line in lines if line.strip()]

        # Eliminar espacios innecesarios entre signos de igual
        cleaned_lines = [re.sub(r'\s*([+=-])\s*', r'\1', line) for line in filtered_lines]

        # Escribir las líneas filtradas y limpiadas en el mismo archivo
        with open(file_path, 'w') as file:
            file.write('\n'.join(cleaned_lines))
            
    @staticmethod
    def clean_folder(folder_path):
        # Obtener la lista de archivos en la carpeta 'input'
        files = os.listdir(folder_path)

        # Eliminar cada archivo en la carpeta 'input'
        for file_name in files:
            file_path = os.path.join(folder_path, file_name)
            os.remove(file_path)