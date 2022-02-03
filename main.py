
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.lang.builder import Builder
from datetime import datetime
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.card import MDCardSwipe
from kivymd.uix.picker import MDDatePicker,MDTimePicker, MDThemePicker
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivymd.uix.list import OneLineListItem
from kivymd.uix.textfield import MDTextField
from kivymd.uix.list import IRightBodyTouch
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.dialog import MDDialog
from store import add_task,delete_task,update_task,view,status
import plyer

Window.size = (320,600)
Builder.load_file('main.kv')


class RightCheckbox(IRightBodyTouch,MDCheckbox):
    pass


class Edit_content(BoxLayout):
    pass


class SwipeToDeleteItem(MDCardSwipe):
    text = StringProperty()
    secondary_text = StringProperty()

    def __init__(self,check = False, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.ids.check.active = check


    def delete_task_dialog(self):
        self.dialog = MDDialog(
            title='Delete Task',
            type= 'confirmation',
            text='Are you sure you want to delete this task?',
            buttons=[
                MDFlatButton(text='Cancel', on_release=self.cancel,md_bg_color= (1, 0, 1, 1) ),
                MDRaisedButton(text='Delete', on_release=self.delete)


            ]
        )
        self.dialog.open()





    def delete(self,*args):
        print('cancel')
        print(args)
        Snackbar(
            text= 'Task deleted',
            snackbar_x="10dp",
            snackbar_y="10dp",
            size_hint_x=.9,
            pos_hint={'center_y':0.2 }
        )


    def cancel(self,*args):
        global dialog
        self.dialog.dismiss()

    

class Mainwindow(BoxLayout):
    current_date =str(datetime.now().strftime('%A %d %B %Y'))
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
     


    def palette(self):
        theme_picker = MDThemePicker()
        theme_picker.open()

    def date_selecter(self):
        date = MDDatePicker()
        date.bind(on_save = self.date_selected)
        date.open()

    def date_selected(self,instance,value,date_range):

        self.ids.date_text.text = str(value.strftime('%A %d %B %Y'))




    def add_tasks(self):
        task = self.ids.task.text
        date = self.ids.date_text.text

        add_task(task,date)

        if date ==self.current_date:
            self.ids.today_task.add_widget(SwipeToDeleteItem(text=task,secondary_text=date))
            self.ids.task_list.add_widget(SwipeToDeleteItem(text=task,secondary_text=date))
        else:
            self.ids.task_list.add_widget(SwipeToDeleteItem(text=task,secondary_text=date))
        Snackbar(
            text='Task has been added',
            snackbar_x="10dp",
            snackbar_y="10dp",
            size_hint_x=.9,
            pos_hint={'center_y':0.2 }
        ).open()
        self.ids.task.text = ''

        


    def edit_task(self):
        pass




class TodoApp(MDApp):

    
    def build(self):
        self.main = Mainwindow()
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'Green'
        return self.main


##### this loads the tasks when application starts ######
    def on_start(self):
        
        for task, date, completed in view():
            if completed == 'True':
                self.main.ids.completed_list.add_widget(SwipeToDeleteItem(text=task,secondary_text= date, check= True))
            elif completed == "False":
                self.main.ids.task_list.add_widget(SwipeToDeleteItem(text=task,secondary_text=date, check= False))
                if date ==self.main.current_date:
                    self.main.ids.today_task.add_widget(SwipeToDeleteItem(text=task,secondary_text=date))



# ####### this method is been executed when a list is checked #####
    def mark(self,check, instance):
        print(check)
        item = instance.text
      
# add to completed list and remove from all and today task
        if check.active == True:
            print('true')

            self.main.ids.task_list.remove_widget(instance)
            self.main.ids.today_task.remove_widget(instance)
            self.main.ids.completed_list.add_widget(instance)

            Snackbar(text= "Task completed",
            snackbar_x="10dp",
            snackbar_y="10dp",
            size_hint_x=.9,
            pos_hint={'center_y':0.2 }
            ).open()
            # saving status to database
            status(item,'True')

        if check.active == False:
            self.main.ids.completed_list.remove_widget(instance)
            self.main.ids.task_list.add_widget(instance)
            # saving status to database
            status(item,'False')

            # if instance.secondary_text == self.main.current_date:
            #     self.main.ids.today_task.add_widget(instance)
            #     # Snackbar(text= "Task unmarked").open()
            #     # # saving status to database
            #     # status(item,'False')
            #     print('current date')

            Snackbar(text= "Task unmarked",
            snackbar_x="10dp",
            snackbar_y="10dp",
            size_hint_x=.9,
            pos_hint={'center_y':0.2 }
            
            
            
            ).open()
            




    def remove_task(self, instance):

        print(instance)


        self.task_to_delete = instance


        
        self.dialog = MDDialog(
            title='Delete Task',
            type= 'confirmation',
            text='Are you sure you want to delete this task?',
            buttons=[
                MDFlatButton(text='Cancel', on_release=self.cancel,md_bg_color= (1, 0, 1, 1) ),
                MDRaisedButton(text='Delete', on_release=self.delete)


            ]
        )
        self.dialog.open()





    def delete(self,*args):
        print('delete')
        print(self.task_to_delete)

        self.main.ids.task_list.remove_widget(self.task_to_delete)
        self.main.ids.today_task.remove_widget(self.task_to_delete)
        self.main.ids.completed_list.remove_widget(self.task_to_delete)
        delete_task(self.task_to_delete.text)
        Snackbar(
            text= 'Task deleted',
            snackbar_x="10dp",
            snackbar_y="10dp",
            size_hint_x=.9,
            pos_hint={'center_y':0.2 }
        ).open()

        self.dialog.dismiss()


    def cancel(self,*args):
        global dialog
        self.dialog.dismiss()

    def edit_task_dialog(self, instance):
        self.edit_content = Edit_content()
        self.edit_content.ids.edit_task = instance.text
        print(instance.text)

        self.edit = MDDialog(
            title='Edit Task',
            type='custom',
            content_cls = Edit_content(),
            buttons=[
            MDFlatButton(
            text="Cancel",
            on_release= self.cancel_edit),
            
            MDRaisedButton(
            text="Save",
            on_release= self.save_edit
            ),]
        )
        self.edit.open()




    def cancel_edit(self, *args):
        self.edit.dismiss()


    def save_edit(self,*args):
        print('save edit')
        pass

        
   
if __name__ == "__main__":
    app = TodoApp()
    app.run()