import re
from FileManager import FileManager
import filecmp
import os

class Optimizer:
    @staticmethod
    def optimize_intermediate_code(input_path):
        output_path = "output/optimized_{0}.txt"
        
        # Leer el código intermedio original
        with open(input_path, 'r') as file:
            original_code = file.read()
        
        # Realizar la primera optimizacion
        optimized_code = Optimizer._apply_optimizations(original_code)

        # Guardar la primera optimizacion en un archivo
        with FileManager(output_path.format(1)) as file:
            file.truncate(0)
            file.write(optimized_code)
            
        if(Optimizer._equal_codes(output_path.format(1), input_path)) or not Optimizer._is_valid_code(output_path.format(1)):
            print("Optimization completed in 1 iteration.")
            with FileManager(output_path.format(1)) as file:
                file.truncate(0)
                file.write(original_code)
            return
            
        iteration = 2
        
        # Generar las siguientes optimizaciones y guardados en archivos.
        while iteration < 5:
            # Aplicar las optimizaciones
            optimized_code = Optimizer._apply_optimizations(optimized_code)

            # Guardar el código optimizado en un archivo
            with FileManager(output_path.format(iteration)) as file:
                file.truncate(0)
                file.write(optimized_code)
                
            if Optimizer._equal_codes(output_path.format(iteration), output_path.format(iteration - 1)) or not Optimizer._is_valid_code(output_path.format(iteration)): 
                os.remove(output_path.format(iteration))
                iteration -= 1
                break 
            
            iteration += 1
       
        print(f"Optimization completed in {iteration} iterations.")

        
    @staticmethod
    def _equal_codes(new_path, previous_path):
        return filecmp.cmp(new_path, previous_path)
    
    @staticmethod
    def _is_valid_code(path):
        with open(path, 'r') as file:
            code = file.read()

        lines = code.split('\n')

        for line in lines:
            if '=' in line:
                parts = line.split('=')
                variable = parts[0].strip()
                value = parts[1].strip()

                if re.match(r'^-?\d+$', value):
                    # Verifica si el valor es una constante numérica
                    if variable.isdigit() and variable != value:
                        return False
                elif re.match(r'^-?\d+([<>=!]=?)\S*$', value):
                    # Verifica si hay un número junto a un operador de comparación
                    return False

        return True

    @staticmethod
    def _apply_optimizations(code):
        # Propagar constantes, quitar sentences sin sentido y duplicadas.
        code = Optimizer._propagate_constants(code)
        code = Optimizer._delete_no_sense_instructions(code)
        code = Optimizer._eliminate_duplicate_lines(code)

        return code

    @staticmethod
    def _propagate_constants(code):
        lines = code.split('\n')
        variables = {}

        for line in lines:
            if '=' in line:
                parts = line.split('=')
                variable = parts[0].strip()
                value = parts[1].strip()

                # Verifica si el valor es una constante
                if re.match(r'^-?\d+$', value):
                    # Verifica si la variable tiene la concatenación de 't' y un número
                    if not re.match(r'^t\d+$', variable):
                        continue  # No reemplazar si la variable no sigue el formato t + número

                    # Guarda la variable y su valor constante
                    variables[variable] = value

        # Reemplaza las ocurrencias de variables por sus valores constantes
        for variable, value in variables.items():
            code = re.sub(r'\b' + re.escape(variable) + r'\b', value, code)

        return code

    @staticmethod
    def _delete_no_sense_instructions(code):
        lines = code.split('\n')
        optimized_lines = []

        for line in lines:
            if '=' in line:
                parts = line.split('=')
                variable = parts[0].strip()
                value = parts[1].strip()

                # Verifica si la variable es igual al valor (no tiene sentido)
                if variable == value:
                    continue  # Saltar la línea

            optimized_lines.append(line)

        return '\n'.join(optimized_lines)
    
    @staticmethod
    def _eliminate_duplicate_lines(code):
        lines = code.split('\n')
        unique_lines = list(dict.fromkeys(lines))  # Elimina duplicados preservando el orden

        return '\n'.join(unique_lines)
