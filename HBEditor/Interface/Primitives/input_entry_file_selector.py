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
from PyQt5 import QtWidgets, QtGui
from HBEditor.Core.settings import Settings
from HBEditor.Interface.Primitives.input_entry_base import InputEntryBase
from HBEditor.Interface.Prompts.file_system_prompt import FileSystemPrompt


class InputEntryFileSelector(InputEntryBase):
    def __init__(self, logger, details_panel, type_filter, refresh_func=None):
        super().__init__(refresh_func)

        # This type requires the logger and a direct ref to the owning QWidget for filesystem operations
        self.logger = logger
        self.details_panel = details_panel

        # Store a type filter to restrict what files can be chosen in the browser
        self.type_filter = type_filter

        self.input_widget = QtWidgets.QLineEdit()
        self.input_widget.setFont(Settings.getInstance().paragraph_font)
        self.input_widget.setStyleSheet(Settings.getInstance().paragraph_color)
        self.input_widget.setText("None")
        self.input_widget.textChanged.connect(self.InputValueUpdated)
        self.input_widget.setEnabled(True)

        # Create the file selector button, and style it accordingly
        self.file_select_button = QtWidgets.QToolButton()
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(Settings.getInstance().ConvertPartialToAbsolutePath("Content/Icons/Open_Folder.png")),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off
        )
        self.file_select_button.setIcon(icon)

        # Add input elements to the layout
        self.main_layout.addWidget(self.input_widget)
        self.main_layout.addWidget(self.file_select_button)

        # Connect Signals
        self.file_select_button.clicked.connect(self.OpenFilePrompt)

    def Get(self):
        return self.input_widget.text()

    def Set(self, data) -> None:
        # Disconnect the input change signal to allow us to perform the change without flipping the global toggle
        self.input_widget.disconnect()

        # Change the data without causing any signal calls
        self.input_widget.setText(data)

        # Now that the input is changed, reconnect
        self.input_widget.textChanged.connect(self.InputValueUpdated)

    def MakeUneditable(self):
        self.file_select_button.setEnabled(False)
        self.input_widget.setStyleSheet(Settings.getInstance().read_only_background_color)

    def MakeEditable(self):
        self.file_select_button.setEnabled(True)
        self.input_widget.setStyleSheet("")

    def OpenFilePrompt(self) -> str:
        #@TODO: Replace file browser will popup list of files available in the project
        """ Prompts the user with a filedialog, accepting an existing file """
        prompt = FileSystemPrompt(self.logger, self.details_panel)
        existing_file = prompt.GetFile(
            Settings.getInstance().GetProjectContentDirectory(),
            self.type_filter,
            "Choose a File to Open"
        )

        # Did the user choose a value?
        if existing_file:
            selected_dir = existing_file

            # Remove the project dir from the path, so that the selected dir only contains a relative path
            selected_dir = selected_dir.replace(Settings.getInstance().user_project_dir + "/", "")
            self.input_widget.setText(selected_dir)





