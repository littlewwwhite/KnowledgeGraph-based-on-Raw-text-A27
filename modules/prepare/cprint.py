def red(text):
    return "\033[31m" + str(text) + "\033[0m"


def green(text):
    return "\033[32m" + str(text) + "\033[0m"


def yellow(text):
    return "\033[33m" + str(text) + "\033[0m"


def blue(text):
    return "\033[34m" + str(text) + "\033[0m"

# 打印紫色字体


def purple(text):
    return "\033[35m" + str(text) + "\033[0m"


def cyan(text):
    return "\033[36m" + str(text) + "\033[0m"


def white(text):
    return "\033[37m" + str(text) + "\033[0m"


def bold(text):
    return "\033[1m" + str(text) + "\033[0m"


def underline(text):
    return "\033[4m" + str(text) + "\033[0m"


def blink(text):
    return "\033[5m" + str(text) + "\033[0m"


def reverse(text):
    return "\033[7m" + str(text) + "\033[0m"


def conceal(text):
    return "\033[8m" + str(text) + "\033[0m"


def strikethrough(text):
    return "\033[9m" + str(text) + "\033[0m"


def black_background(text):
    return "\033[40m" + str(text) + "\033[0m"


def red_background(text):
    return "\033[41m" + str(text) + "\033[0m"


def green_background(text):
    return "\033[42m" + str(text) + "\033[0m"


def yellow_background(text):
    return "\033[43m" + str(text) + "\033[0m"


def blue_background(text):
    return "\033[44m" + str(text) + "\033[0m"


def purple_background(text):
    return "\033[45m" + str(text) + "\033[0m"


def cyan_background(text):
    return "\033[46m" + str(text) + "\033[0m"


def white_background(text):
    return "\033[47m" + str(text) + "\033[0m"


def default_color(text):
    return "\033[39m" + str(text) + "\033[0m"


def default_background(text):
    return "\033[49m" + str(text) + "\033[0m"


def gray(text):
    return "\033[90m" + str(text) + "\033[0m"


def light_red(text):
    return "\033[91m" + str(text) + "\033[0m"


def light_green(text):
    return "\033[92m" + str(text) + "\033[0m"


def light_yellow(text):
    return "\033[93m" + str(text) + "\033[0m"


def light_blue(text):
    return "\033[94m" + str(text) + "\033[0m"


def light_purple(text):
    return "\033[95m" + str(text) + "\033[0m"


def light_cyan(text):
    return "\033[96m" + str(text) + "\033[0m"


if __name__ == "__main__":
    print(red("red"))
    print(green("green"))
    print(yellow("yellow"))
    print(blue("blue"))
    print(purple("purple"))
    print(cyan("cyan"))
    print(white("white"))
    print(bold("bold"))
    print(underline("underline"))
    print(blink("blink"))
    print(reverse("reverse"))
    print(conceal("conceal"))
    print(strikethrough("strikethrough"))
    print(black_background("black_background"))
    print(red_background("red_background"))
    print(green_background("green_background"))
    print(yellow_background("yellow_background"))
    print(blue_background("blue_background"))
    print(purple_background("purple_background"))
    print(cyan_background("cyan_background"))
    print(white_background("white_background"))
    print(default_color("default_color"))
    print(default_background("default_background"))
    print(gray("gray"))
    print(light_red("light_red"))
    print(light_green("light_green"))
    print(light_yellow("light_yellow"))
    print(light_blue("light_blue"))
    print(light_purple("light_purple"))
    print(light_cyan("light_cyan"))
