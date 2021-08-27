from kivymd.uix.label import MDIcon

class ActionCheckBox():
    def __init__(self, app):
        # Icon to show when the checkbox is not checked
        self.notCheckIcon = "checkbox-blank-outline"

        # Icon to show when the checkbox is checked
        self.onCheckIcon = "checkbox-marked-outline"

        self.notCheckIconLs = [self.notCheckIcon, lambda x:self.check()]

        self.onCheckIconLs = [self.onCheckIcon, lambda x:self.uncheck()]

        self.app = app

        self.appToolbar = self.app.root.ids.AppToolbar

        self.checked = False

    def show(self):
        if len(self.appToolbar.right_action_items) != 2:
            self.appToolbar.right_action_items.insert(0, self.notCheckIconLs)


    def hide(self):
        if len(self.appToolbar.right_action_items) != 0:
            self.appToolbar.right_action_items.remove(self.notCheckIconLs)


    def check(self):
        if len(self.appToolbar.right_action_items) != 0:
            self.appToolbar.right_action_items = [self.onCheckIconLs, ["trash-can-outline", lambda x: self.app.onToolbarTrashCanClick(x)]]
            self.checked = True

            myfilesscreen = self.app.myfilesscreen

            myfilesscreen.selectedFiles = []

            for checkbox in myfilesscreen.cardCheckboxes:
                checkbox.state = "down"
                myfilesscreen.selectedFiles.append(checkbox)
                

    def uncheck(self, changeMyFilesCheckboxState=True):
        if len(self.appToolbar.right_action_items) != 0:
            self.appToolbar.right_action_items = [self.notCheckIconLs]
            self.checked = False



            self.app.myfilesscreen.selectedFiles = []

            if changeMyFilesCheckboxState == True:
                for checkbox in self.app.myfilesscreen.cardCheckboxes:
                    checkbox.state = "normal"
