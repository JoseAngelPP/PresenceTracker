import sys
from datetime import datetime, timedelta

MINIMUM_PRESENCE_MINUTES = 0
DETENTION_TIME_FORMAT = "%H:%M"


class PresenceTracker:
    def __init__(self):
        self.students = {}

    def validate_datetime_format(self, value, format):
        # Validar que una fecha/hora tenga un formato
        try:
            return datetime.strptime(value, format)
        except ValueError:
            # Si no tiene el formato regresar error
            raise Exception(f"Formato de fecha incorrecto para {value}")

    def process_presence(self, student_name, start_time, end_time):
        # Validar las horas de inicio de de fin
        start_time = self.validate_datetime_format(start_time, DETENTION_TIME_FORMAT)
        end_time = self.validate_datetime_format(end_time, DETENTION_TIME_FORMAT)

        # Validar que la hora de fin sea posterior a la de inicio
        if end_time < start_time:
            raise Exception(
                f"La hora de entrada debe ser previa a la de salida para {student_name}"
            )

        duration = end_time - start_time

        if student_name not in self.students:
            self.students[student_name] = {"time": timedelta(), "days": 0}

        # Guardar el tiempo y días en la sala
        self.students[student_name]["time"] += duration
        self.students[student_name]["days"] += 1

    def calculate_total_minutes(self, duration):
        # Obtener el tiempo en minutos
        total_minutes = duration.total_seconds() // 60
        return int(total_minutes)

    def read_file(self, input_data):
        """
        Los tests usan StringIO para simular el archivo,
        si la función recibe un string significa que es un archivo
        Caso contrario es un objeto StringIO y se evalua directamente.
        """
        if isinstance(input_data, str):
            file = open(input_data, "r")
        else:
            file = input_data
        with file:
            # Evaluar solo las líneas con información
            lines = list(line for line in (l.strip() for l in file) if line)
            for line in lines:
                line = line.strip().split()
                command = line[0]

                """
                Si el comando es un estudiante agregarlo a la lista
                Si es una lista de información validarla y guardarla
                """
                if command == "Student":
                    student_name = line[1]
                    self.students[student_name] = {"time": timedelta(), "days": 0}
                elif command == "Presence":
                    student_name = line[1]
                    weekday = int(line[2])
                    if weekday < 1 or weekday > 7:
                        raise Exception("El número de día debe ser entre el 1 y 7")

                    start_time = line[3]
                    end_time = line[4]

                    self.process_presence(student_name, start_time, end_time)

    def get_attendance(self):
        try:
            # Leer el archivo de la línea de comandos
            console_input = sys.argv
            if len(console_input) < 2:
                raise Exception("No se recibió un archivo con información")

            self.read_file(console_input[1])
            # Order por tiempo de presencia a los estudiantes
            sorted_students = dict(
                sorted(
                    self.students.items(),
                    key=lambda item: item[1].get("time"),
                    reverse=True,
                )
            )
            # Imprimir la información de cada estudiante
            for student, estudent_info in sorted_students.items():
                duration = estudent_info.get("time", timedelta())
                num_days = estudent_info.get("days", 0)
                total_minutes = self.calculate_total_minutes(duration)

                # Si el tiempo de presencia es menor que un mínimo omitir su registro
                if total_minutes > MINIMUM_PRESENCE_MINUTES:
                    print(f"{student}: {total_minutes} minutes in {num_days} days")
                else:
                    print(f"{student}: {total_minutes} minutes")
        except Exception as e:
            print(e)


tracker = PresenceTracker()
tracker.get_attendance()
