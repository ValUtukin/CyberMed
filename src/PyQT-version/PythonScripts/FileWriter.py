import datetime


class FileWriter:
    def __init__(self):
        self.file_directory = r"C:\\PyCharmProjects\TestADCFileWriting"
        self.current_processing_file = None

    def prepare_file_name(self, part: str, motor_number: int, pwm: int, time: float, delay: float):
        file_name = ""
        if part == "Upper":
            file_name += "U"
            file_name += f"PWM{pwm}"
            file_name += f"M{motor_number}"
            file_name += "MASS0"
        elif part == "Lower":
            file_name += "L"
            file_name += f"PWM{pwm}"
            file_name += f"M{motor_number}"
            file_name += "MASS1000"
        else:
            print(f"FileWriter/prepare_file_name - incorrect part: {part}")
        print(f"FileWriter/prepare_file_name - file name: {file_name}")
        self.write_settings(file_name, pwm, time, delay)

    def write_settings(self, file_name: str, pwm: int, time: float, delay: float):
        full_file_path = self.file_directory + '\\' + file_name + ".txt"
        date = datetime.datetime.today()
        with open(full_file_path, "w") as f:
            f.write(date.strftime("%d %b %Y") + "\n")
            first_string = f"PWM: {pwm}\nTime: {time}\nDelay: {delay}\n"
            f.write(first_string + "\n")
        self.current_processing_file = full_file_path

    def write_data(self, data_dict):
        y_data = data_dict.get('0')
        x_data = [i for i in range(len(y_data))]
        with open(self.current_processing_file, 'a') as f:
            f.write(f"i\tx\ty\n")
            for i in range(len(x_data)):
                target_str = f'{i + 1}\t{x_data[i]}\t{round(y_data[i], 3)}'
                f.write(target_str + '\n')