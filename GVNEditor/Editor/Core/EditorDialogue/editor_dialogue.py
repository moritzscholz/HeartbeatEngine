"""
    This file is part of GVNEditor.

    GVNEditor is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    GVNEditor is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with GVNEditor.  If not, see <https://www.gnu.org/licenses/>.
"""
from Editor.Core.BaseClasses.base_editor import EditorBase
from Editor.Interface.EditorDialogue.editor_dialogue import EditorDialogueUI
from PyQt5 import QtWidgets

class EditorDialogue(EditorBase):
    def __init__(self, settings, logger):
        super().__init__(settings, logger)
        self.editor_type = self.editor_types[0] # Dialogue

        # Build the Dialogue Editor UI
        self.ed_ui = EditorDialogueUI(self)

        # Initialize a main branch
        self.ed_ui.branches.CreateBranch(
            ("main", "This is the default, main branch\nConsider this the root of your dialogue tree")
        )

    def UpdateActiveEntry(self):
        """ Makes the selected entry the active one, refreshing the details panel """
        print("Changing active entry")

        selection = self.ed_ui.dialogue_sequence.GetSelectedEntry()

        # Refresh the details panel to reflect the newly chosen row
        self.UpdateDetails(selection)

    def UpdateDetails(self, selected_entry):
        """ Refreshes the details panel with the details from the selected dialogue entry """
        if selected_entry:
            self.ed_ui.details.PopulateDetails(selected_entry)

        # No entries left to select. Wipe remaining details
        else:
            self.ed_ui.details.Clear()

    # @TODO: How to support the initial switch when 'main' is created?
    def SwitchBranches(self, cur_branch, new_branch):
        """ Switches the active branch, storing all existing dialogue sequence entries in the old branch """
        # If there is no source branch, then there is nothing to store
        if cur_branch:

            self.UpdateBranchData(cur_branch)
            self.ed_ui.dialogue_sequence.Clear()

        # Load any entries in the new branch (if applicable)
        if new_branch.branch_data:
            for entry in new_branch.branch_data:
                self.ed_ui.dialogue_sequence.AddEntry(entry, None, True)

    def UpdateBranchData(self, cur_branch):
        """ Updates the active branch with all active dialogue entries """
        # Clear the contents of the current branch since we're forcefully updating whats stored
        cur_branch.branch_data.clear()

        # Store the data from each entry in the branch
        num_of_entries = self.ed_ui.dialogue_sequence.dialogue_table.rowCount()
        for entry_index in range(num_of_entries):

            # Store the data held by the entry
            dialogue_entry = self.ed_ui.dialogue_sequence.dialogue_table.cellWidget(entry_index, 0)
            cur_branch.branch_data.append(dialogue_entry.action_data)
