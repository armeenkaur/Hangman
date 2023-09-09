import pygame as pg
import string

class GUI:
    BACKGROUND = "back_color"
    FOREGROUND = "text_color"
    FONT = "font"
    BORDER_COLOR = "border_color"
    BORDER_SIZE = "border_size"
    HOVERED_BACKGROUND = "hover_color"
    PRESSED_BACKGROUND = "press_color"
    TOGGLED_BACKGROUND = "toggle_color"

    default_options = None
    default_font = None

    @staticmethod
    def create_defaults():
        font = GUI.default_font or pg.font.SysFont("Comic Sans MS", 20)

        GUI.default_options = {
            Label.__name__: {
                GUI.BACKGROUND: (255, 255, 255),
                GUI.FOREGROUND: (0, 0, 0),
                GUI.FONT: font,
                GUI.BORDER_COLOR: (0, 0, 0),
                GUI.BORDER_SIZE: 4
            },
            Button.__name__: {
                GUI.BACKGROUND: (255, 255, 255),
                GUI.FOREGROUND: (0, 0, 0),
                GUI.FONT: font,
                GUI.BORDER_COLOR: (0, 0, 0),
                GUI.BORDER_SIZE: 4,
                GUI.HOVERED_BACKGROUND: (200, 200, 200),
                GUI.PRESSED_BACKGROUND: (100, 100, 100),
            },
            ToggleButton.__name__: {
                GUI.BACKGROUND: (255, 255, 255),
                GUI.FOREGROUND: (0, 0, 0),
                GUI.FONT: font,
                GUI.BORDER_COLOR: (0, 0, 0),
                GUI.BORDER_SIZE: 4,
                GUI.HOVERED_BACKGROUND: (200, 200, 200),
                GUI.PRESSED_BACKGROUND: (100, 100, 100),
                GUI.TOGGLED_BACKGROUND: (150, 150, 150)
            },
            Textbox.__name__: {
                GUI.BACKGROUND: (255, 255, 255),
                GUI.FOREGROUND: (0, 0, 0),
                GUI.FONT: font,
                GUI.BORDER_COLOR: (0, 0, 0),
                GUI.BORDER_SIZE: 4,
                GUI.HOVERED_BACKGROUND: (200, 200, 200),
                GUI.PRESSED_BACKGROUND: (100, 100, 100),
            }
        }

    def with_defaults(self, options):
        if not GUI.default_options:
            GUI.create_defaults()

        defaults = GUI.default_options[self.__class__.__name__]

        for key in defaults:
            if key not in options:
                options[key] = defaults[key]
        
        return options

class Label(GUI):
    def __init__(self, rect, text, **kwargs):
        self.rect = rect
        self.text = text

        self.rendered_text = None
        self.rendered_text_rect = None
        
        self.options = self.with_defaults(kwargs)

        self.recreate()

    def update(self, event):
        return

    def render(self, screen):
        border = self.options[GUI.BORDER_SIZE]
        if border > 0:
            pg.draw.rect(screen, self.options[GUI.BORDER_COLOR], self.rect.inflate(border, border))

        pg.draw.rect(screen, self.options[GUI.BACKGROUND], self.rect)

        screen.blit(self.rendered_text, self.rendered_text_rect)

    def set_text(self, text):
        self.text = text
        self.recreate()

    def recreate(self):
        self.rendered_text = self.options[GUI.FONT].render(self.text, True, self.options[GUI.FOREGROUND])
        self.rendered_text_rect = self.rendered_text.get_rect(center=self.rect.center)

class Textbox(GUI):
    valid_text = (string.ascii_letters + string.digits + string.punctuation + " ")

    def __init__(self, rect, text, **kwargs):
        self.rect = rect
        
        self.text = None
        self.text_changed = False
        self.buffer = list(text)
        
        self.focused = False
        self.draw_cursor = True
        self.blink_counter = 0
        self.blink_time = 500
        
        self.rendered_text = None
        self.rendered_text_rect = None
        self.visible_area = None
        
        self.options = self.with_defaults(kwargs)

        self.recreate()

    def render(self, screen):
        border = self.options[GUI.BORDER_SIZE]
        if border > 0:
            pg.draw.rect(screen, self.options[GUI.BORDER_COLOR], self.rect.inflate(border, border))

        pg.draw.rect(screen, self.options[GUI.BACKGROUND], self.rect)

        screen.blit(self.rendered_text, self.rendered_text_rect, self.visible_area)

        ticks = pg.time.get_ticks()
        if ticks - self.blink_counter > self.blink_time:
            self.draw_cursor = not self.draw_cursor
            self.blink_counter = ticks
        if self.draw_cursor and self.focused:
            cursor_start = (self.rendered_text_rect.left + self.visible_area.width, self.rendered_text_rect.top)
            cursor_end = (self.rendered_text_rect.left + self.visible_area.width, self.rendered_text_rect.bottom)
            pg.draw.line(screen, (0, 0, 0), cursor_start, cursor_end, 2)

    def update(self, event):
        if self.focused and event.type == pg.KEYDOWN:
            if event.key in [pg.K_LEFT, pg.K_RIGHT, pg.K_UP, pg.K_DOWN]:
                return
            elif event.key == pg.K_BACKSPACE and len(self.buffer) > 0:
                self.buffer.pop()
                self.recreate()
            elif event.unicode in self.valid_text:
                self.buffer.append(event.unicode)
                self.recreate()
        elif event.type == pg.MOUSEBUTTONDOWN:
            self.focused = self.rect.collidepoint(event.pos)

    def set_text(self, text):
        self.buffer = list(text)
        self.recreate()

    def recreate(self):
        new_text = "".join(self.buffer)
        self.text_changed = new_text != self.text

        self.text = new_text
        self.rendered_text = self.options[GUI.FONT].render(self.text, True, self.options[GUI.FOREGROUND])
        self.rendered_text_rect = self.rendered_text.get_rect(x=self.rect.left + 5, centery=self.rect.centery)

        if self.rendered_text_rect.width > self.rect.width - 10:
            offset = self.rendered_text_rect.width - (self.rect.width - 10)
            self.visible_area = pg.Rect(offset, 0, self.rect.width - 10, self.rendered_text_rect.height)
        else:
            self.visible_area = self.rendered_text.get_rect()

class Button(GUI):
    def __init__(self, rect, text, **kwargs):
        self.rect = rect
        self.text = text

        self.enabled = True

        self.hovered = False
        self.pressed = False
        self.clicked = False
        
        self.rendered_text = None
        self.rendered_text_rect = None
        
        self.options = self.with_defaults(kwargs)

        self.recreate()

    def render(self, screen):
        border = self.options[GUI.BORDER_SIZE]
        if border > 0:
            pg.draw.rect(screen, self.options[GUI.BORDER_COLOR], self.rect.inflate(border, border))

        bg_color = self.options[(GUI.PRESSED_BACKGROUND if self.pressed else (
            GUI.HOVERED_BACKGROUND if self.hovered else GUI.BACKGROUND))]
        pg.draw.rect(screen, bg_color, self.rect)

        if not self.enabled:
            pg.draw.rect(screen, (100, 100, 100), self.rect)

        screen.blit(self.rendered_text, self.rendered_text_rect)

    def update(self, event):
        if self.enabled:
            if event.type == pg.MOUSEMOTION:
                self.hovered = self.rect.collidepoint(event.pos)
            elif event.type == pg.MOUSEBUTTONDOWN:
                self.pressed = self.hovered
                self.clicked = False
            elif event.type == pg.MOUSEBUTTONUP:
                self.clicked = self.hovered and self.pressed
                self.pressed = False

    def click_handled(self):
        self.clicked = False

    def set_enabled(self, enabled):
        self.enabled = enabled

    def set_text(self, text):
        self.text = text
        self.recreate()
        
    def recreate(self):
        self.rendered_text = self.options[GUI.FONT].render(self.text, True, self.options[GUI.FOREGROUND])
        self.rendered_text_rect = self.rendered_text.get_rect(center=self.rect.center)

class ToggleButton(Button):
    def __init__(self, rect, text, **kwargs):
        super().__init__(rect, text, **kwargs)
        self.toggled = False

    def update(self, event):
        super().update(event)
        if self.clicked:
            self.toggled = not self.toggled
            self.click_handled()

    def render(self, screen):
        border = self.options[GUI.BORDER_SIZE]
        if border > 0:
            pg.draw.rect(screen, self.options[GUI.BORDER_COLOR], self.rect.inflate(border, border))

        bg_color = self.options[GUI.PRESSED_BACKGROUND if self.pressed else (
            (GUI.TOGGLED_BACKGROUND if self.toggled else (
                GUI.HOVERED_BACKGROUND if self.hovered else GUI.BACKGROUND)))]
        pg.draw.rect(screen, bg_color, self.rect)

        if not self.enabled:
            pg.draw.rect(screen, (100, 100, 100), self.rect)
        
        screen.blit(self.rendered_text, self.rendered_text_rect)
