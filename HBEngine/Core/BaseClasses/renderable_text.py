"""
    The Heartbeat Engine is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    The Heartbeat Engine is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with the Heartbeat Engine. If not, see <https://www.gnu.org/licenses/>.
"""
import pygame
from HBEngine.Core.BaseClasses.renderable import Renderable


class TextRenderable(Renderable):
    """
    The Text Renderable class is the base class for renderable text elements in the HBEngine. This includes:
        - Titles
        - Sub-titles
        - Actions text
        - Pop-up text
        - etc
    """
    def __init__(self, scene, renderable_data):
        super().__init__(scene, renderable_data)

        font = self.scene.settings.ConvertPartialToAbsolutePath(self.renderable_data['font'])
        self.text = self.renderable_data["text"]
        self.text_color = self.renderable_data["text_color"]
        text_size = self.renderable_data["text_size"]
        self.font_obj = pygame.font.Font(font, text_size)

        # If a size was passed (expected as screen space values), then use it for the wrap bounds
        if "size" not in self.renderable_data:
            assert "wrap_bounds" in self.renderable_data, print(
                f"No 'wrap_bounds' value assigned to {self}, and no 'size' "
                f"value provided. This makes for an impossible action!")
            self.renderable_data["size"] = self.ConvertNormToScreen(self.renderable_data["wrap_bounds"])

        # Build a surface using the wrap bounds as the containing area. If text spills outside these bounds, it's
        # automatically wrapped until the maximum Y
        self.surface = pygame.Surface((
                int(self.renderable_data["size"][0]),
                int(self.renderable_data["size"][1])),
            pygame.SRCALPHA
        )

        self.WrapText(self.surface)
        self.rect = self.surface.get_rect()

        # For new objects, resize initially in case we're already using a scaled resolution
        self.RecalculateSize(self.scene.resolution_multiplier)

    def WrapText(self, surface):
        rect = surface.get_rect()
        base_top = rect.top
        line_spacing = -2
        font_height = self.font_obj.size("Tg")[1]

        # Pre-split the text based on any specified newlines
        text_to_process = self.text.split("\n")
        print(text_to_process)

        # Process each line, applying wrapping where necessary
        for line in text_to_process:

            processing_complete = False
            while not processing_complete:
                i = 1

                # Determine if the text will exceed the bounds height
                if base_top + font_height > rect.bottom:
                    break

                # Parse the text until we've exceeded horizontal bounds, or we reached the end of the string
                while self.font_obj.size(line[:i])[0] < rect.width and i < len(line):
                    i += 1

                # If we didn't reach the end of the string, grab the last occurence of a whitespace
                if i < len(line):
                    i = line.rfind(" ", 0, i) + 1

                # Render the line and blit it to the surface
                image = self.font_obj.render(line[:i], True, self.text_color)
                surface.blit(image, (rect.left, base_top))
                base_top += font_height + line_spacing

                # Remove the text we just blitted
                line = line[i:]

                # Exit if we're finished processing everything in this line
                if not line:
                    processing_complete = True


