from os import get_terminal_size as _terminal_size

#Credit to billythegoat356 - PyStyle
class _MakeColors:
    def _makeansi(col: str, text: str) -> str:
        return f"\033[38;2;{col}m{text}\033[38;2;255;255;255m"

    def _rmansi(col: str) -> str:
        return col.replace('\033[38;2;', '').replace('m','').replace('50m', '').replace('\x1b[38', '')

    def _start(color: str) -> str:
        return f"\033[38;2;{color}m"

    def _end() -> str:
        return "\033[38;2;255;255;255m"

    def _maketext(color: str, text: str, end: bool = False) -> str:
        end = _MakeColors._end() if end else ""
        return color+text+end

    def _getspaces(text: str) -> int:
        return len(text) - len(text.lstrip())

class Colors:
    def StaticMIX(colors: list, _start: bool = True) -> str:
        rgb = []
        for col in colors:
            col = _MakeColors._rmansi(col=col)
            col = col.split(';')
            r = int(int(col[0]))
            g = int(int(col[1]))
            b = int(int(col[2]))
            rgb.append([r, g, b])
        r = round(sum(rgb[0] for rgb in rgb) / len(rgb))
        g = round(sum(rgb[1] for rgb in rgb) / len(rgb))
        b = round(sum(rgb[2] for rgb in rgb) / len(rgb))
        rgb = f'{r};{g};{b}'
        return _MakeColors._start(rgb) if _start else rgb

    red_to_purple = ["255;0;m"]
    blue_to_purple = ["0;0;255"]  # Start with blue (0,0,255)
    instagram_gradient = [
            (188, 45, 130),   # Deep pink
            (214, 41, 118),   # Vibrant pink
            (250, 126, 30),   # Warm orange
            (255, 201, 95)    # Golden yellow
        ]  # Start with deep pinkish-purple
    col = (list, str)

    dynamic_colors = [
        red_to_purple,
        blue_to_purple,
        instagram_gradient,
    ]

    for color in dynamic_colors:
        content = color[0]
        color.pop(0)

        # Define key colors in the gradient
        colors = [
            (134, 0, 175),  # Deep pinkish-purple
            (225, 48, 108),  # Vibrant pink
            (245, 96, 64),   # Warm orange
            (255, 220, 128)  # Golden yellow
        ]

        # Generate a smooth gradient between these colors
        for i in range(len(colors) - 1):
            start_color = colors[i]
            end_color = colors[i + 1]
            
            for step in range(8):  # 8 steps between each key color
                r = int(start_color[0] + (end_color[0] - start_color[0]) * step / 7)
                g = int(start_color[1] + (end_color[1] - start_color[1]) * step / 7)
                b = int(start_color[2] + (end_color[2] - start_color[2]) * step / 7)
                
                result = f"{r};{g};{b}"
                color.append(result)

    all_colors = [color for color in dynamic_colors]

class Colorate:

    def Color(color: str, text: str, end: bool = True) -> str:
        return _MakeColors._maketext(color=color, text=text, end=end)

    def Diagonal(color: list, text: str, speed: int = 1, cut: int = 0) -> str:
        color = color[cut:]
        lines = text.splitlines()
        result = ""
        color_n = 0
        for lin in lines:
            carac = list(lin)
            for car in carac:
                colorR = color[color_n]
                result += " " * \
                    _MakeColors._getspaces(
                        car) + _MakeColors._makeansi(colorR, car.strip())
                if color_n + speed < len(color):
                    color_n += speed
                else:
                    color_n = 1
            result += "\n"

        return result.rstrip()

class Center:
    def XCenter(text: str, spaces: int = None, icon: str = " "):
        if spaces is None:
            spaces = Center._xspaces(text=text)
        return "\n".join((icon * spaces) + text for text in text.splitlines())

    def _xspaces(text: str):
        try:
            col = _terminal_size().columns
        except OSError:
            return 0
        textl = text.splitlines()
        ntextl = max((len(v) for v in textl if v.strip()), default = 0)
        return int((col - ntextl) / 2)

    def _yspaces(text: str):
        try:
            lin = _terminal_size().lines
        except OSError:
            return 0
        textl = text.splitlines()
        ntextl = len(textl)
        return int((lin - ntextl) / 2)