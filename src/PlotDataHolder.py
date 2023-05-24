import matplotlib
matplotlib.use('TkAgg')  # Set animation backend before import matplotlib.animation
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def hexstr_to_dec_int(hexstr, reverse_flag=False):
    target_hexstr = hexstr[::-1] if reverse_flag else hexstr
    hex_bytes_list = [target_hexstr[i - 1:i + 1] for i in range(1, len(target_hexstr) + 1, 2)]
    final_decimal_list = [int(hex_byte, 16) for hex_byte in hex_bytes_list if int(hex_byte, 16) != 0]
    return final_decimal_list[-1] if final_decimal_list else 0


class PlotDataHolder:
    def __init__(self, num):
        self.data_set_holder = dict()
        self.holder_len = num
        self.figure, self.axs = plt.subplots(self.holder_len)
        for i in range(0, num):
            self.data_set_holder[f'array{i + 1}'] = list()

    def add_value_to_set(self, set_name, value):
        self.data_set_holder[set_name].append(value)

    def get_data_sets(self):
        return self.data_set_holder, len(self.data_set_holder)

    def plot_data(self, axis, x, y, title="Default title", y_title="Y title", line="r-"):
        y[:] = y[-50:]  # Fix the list size so that the animation plot 'window' is x number of points
        axis.clear()  # Clear last data frame
        axis.set_ylim([0, 5])  # Set Y axis limit of plot
        axis.set_title(title)  # Set title of figure
        axis.set_ylabel(y_title)  # Set title of y-axis
        axis.plot(x, y, line)  # Plot new data frame

    def animate(self, i, axs, ser, counter):
        counter.append(i)
        counter[:] = counter[-50:]

        for i in range(0, self.holder_len):
            data = hexstr_to_dec_int(ser.read().hex())
            data *= 3.3
            data /= 265
            print(data)
            self.add_value_to_set(f'array{i + 1}', data)

        data_sets, num = self.get_data_sets()
        dataList_list = [data_sets[f'array{i + 1}'][-50:] for i in range(0, num)]

        if self.holder_len == 1:
            self.plot_data(axs, counter, dataList_list[0], title=f'AX{i + 1}', y_title=f'Voltage {i + 1}')
        else:
            for i in range(0, self.holder_len):
                self.plot_data(axs[i], counter, dataList_list[i], title=f'AX{i+1}', y_title=f'Voltage {i+1}')

    def start_animate(self, serial_inst):
        counter = list()
        # fig, axs = plt.subplots(self.holder_len)
        ani = animation.FuncAnimation(self.figure, self.animate, frames=1000, fargs=(self.axs, serial_inst, counter),
                                      interval=300)
        plt.tight_layout()
        plt.show()


if __name__ == '__main__':
    holder = PlotDataHolder(3)
    data_sets, num = holder.get_data_sets()
    print(f'Holder len is {holder.get_data_sets()[1]}')
