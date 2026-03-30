import mss
import mss.tools
from Xlib import display, X
from Xlib.error import BadWindow
from typing import Optional, Tuple
from src.ui import AssistantUI

ui = AssistantUI()

class WindowCapturer:
    def __init__(self):
        try:
            self.d = display.Display()  # xlib jest pod X11 na linuxach
            self.root = self.d.screen().root
        except Exception as e:
            ui.display_error(f"[Error] {e}")
            raise e

    def _get_active_window_geometry(self) -> Optional[Tuple[int, int, int, int]]:
        """
        Pobiera współrzędne (x, y, width, height) aktywnego okna.
        Zwraca None, jeśli nie uda się pobrać okna.
        """
        try:
            window_id_property = self.root.get_full_property(
                self.d.intern_atom('_NET_ACTIVE_WINDOW'),
                X.AnyPropertyType
            )
            if not window_id_property or window_id_property.value[0] == 0:
                return None

            window_id = window_id_property.value[0]
            window = self.d.create_resource_object('window', window_id)
            geom = window.get_geometry()
            trans = window.translate_coords(self.root, 0, 0)

            return trans.x, trans.y, geom.width, geom.height

        except BadWindow:
            return None

        except Exception as e:
            ui.display_request(f"[!] {e}")
            return None

    def capture_active_window(self, output_path: str = "screenshot.png") -> Optional[str]:
        geo = self._get_active_window_geometry()  # Pobiera (x, y, w, h) z Xlib
        if not geo:
            return None

        x, y, w, h = geo

        try:
            with mss.mss() as sct:
                root_screen = sct.monitors[0]
                left = max(x, root_screen["left"])
                top = max(y, root_screen["top"])

                max_possible_width = root_screen["width"] - (left - root_screen["left"])
                max_possible_height = root_screen["height"] - (top - root_screen["top"])

                width = min(w, max_possible_width)
                height = min(h, max_possible_height)

                if width <= 0 or height <= 0:
                    ui.display_error("Okno jest poza obszarem widocznym.")
                    return None

                capture_region = {
                    "top": int(top),
                    "left": int(left),
                    "width": int(width),
                    "height": int(height)
                }

                sct_img = sct.grab(capture_region)
                mss.tools.to_png(sct_img.rgb, sct_img.size, output=output_path)

            ui.display_good(f"[Capture Image] Screenshoted ({width}x{height})")
            return output_path

        except Exception as e:
            ui.display_error(f"XGetImage failed: {e}")
            return None