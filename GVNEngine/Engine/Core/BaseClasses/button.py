from Engine.Core.BaseClasses.interactable import Interactable
from Engine.Core.BaseClasses.renderable_text import TextRenderable

class Button(Interactable):
    """
    The Button class extends the 'Interactable' class, and adds an additional child 'TextRenderable'
    """
    def __init__(self, scene, renderable_data):
        super().__init__(scene, renderable_data)

        # Initialize text renderable
        button_text_renderable = TextRenderable(
            self.scene,
            self.renderable_data
        )
        self.children.append(button_text_renderable)
        self.scene.renderables_group.Add(button_text_renderable)

    def GetText(self):
        pass

    def SetText(self):
        pass
