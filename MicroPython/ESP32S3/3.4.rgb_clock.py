from machine import Pin
import neopixel

class RGBClock:
    def __init__(self, pin, num_leds=12):
        self.num_leds = num_leds
        self.np = neopixel.NeoPixel(Pin(pin), num_leds)

    def clear(self):
        for i in range(self.num_leds):
            self.np[i] = (0, 0, 0)
        self.np.write()

    def show_time(self, hour, minute, second):
        """
        Display time on 12-LED ring: Hours   -> Green - Minutes -> Blue - Seconds -> Red
        """
        self.clear()
        # Map time to 0..11
        h_pos = hour % 12 ; m_pos = minute // 5 ; s_pos = second // 5
        # Colors (R, G, B)
        HOUR_COLOR   = (0, 50, 0)   # Green
        MIN_COLOR    = (0, 0, 50)   # Blue
        SEC_COLOR    = (50, 0, 0)   # Red
        # Draw (add colors if overlapping)
        self._add_color(h_pos, HOUR_COLOR)
        self._add_color(m_pos, MIN_COLOR)
        self._add_color(s_pos, SEC_COLOR)
        self.np.write()

    def _add_color(self, pos, color):
        r, g, b = self.np[pos]
        cr, cg, cb = color
        self.np[pos] = (r + cr, g + cg, b + cb)
        