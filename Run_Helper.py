"""
#=========================================================================================================
#: DESCRIPTION    : To help with DnD, basically DnD for poor
#: DOCUMENTATION : None
#---------------------------------------------------------------------------------------------------------
#: USAGE       : Just run in terminal: python3 <name of script>
#: EXAMPLES    :
#---------------------------------------------------------------------------------------------------------
#: AUTHOR      : wollwo
#: NAME        : Charlie_DnD_Helper
#: VERSION     : 1.00  - 2021.07.02 - 
#=========================================================================================================
"""

#: ToDo : Add list of items that you have on self + possibility to check box for attunment. Name of item will be written into Label on main window in attunments section?
#: ToDo : possibility to scroll main window

#: ----------------------------------------------- IMPORTS -----------------------------------------------
import json

from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Rectangle, Color #, Canvas
from kivy.config import Config

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView

#: ----------------------------------------------- IMPORTS - CUSTOM --------------------------------------
#: ----------------------------------------------- VARIABLES ---------------------------------------------
project_version = '1.00'
character_json_file = 'Character.json'
CharacterData = {}
CurrentHP = 0


#: ----------------------------------------------- CLASSES -----------------------------------------------
class MyGui(App):
    def build(self):
        self.title = '"Charliho DnD Helper" app'
        return MyMainWindow()


#: Tag_Class : Label class
class MyFancyLabel(Label):
    def __init__(self, size_x=100, size_y=100, pos_x=100, pos_y=100, show_border=True, **kwargs):
        super(MyFancyLabel, self).__init__(**kwargs)

        #: Default Position
        x_coll = 0
        y_coll = Window.size[1]

        #: draw borders for Label
        if show_border:
            with self.canvas.before:
                Color(71 / 255, 121 / 255, 152 / 255)
                self.rec = Rectangle(pos=(x_coll + pos_x, y_coll - size_y - pos_y),
                                     size=(size_x, size_y)
                                     )
                Color(75 / 255, 75 / 255, 75 / 255)
                border_x = 3
                border_y = 3
                self.rec = Rectangle(pos=(x_coll + pos_x + border_x, y_coll - size_y - pos_y + border_y),
                                     size=(size_x - (2 * border_x), size_y - (2 * border_y))
                                     )
        #: Label arguments
        self.size_hint = (None, None)
        self.pos = (x_coll + pos_x, y_coll - size_y - pos_y)
        self.size = (size_x, size_y)


#: Tag_Class : TextInput class
#: ToDo : add scrolling
class MyFancyTextInput(TextInput):
    def __init__(self, size_x=100, size_y=100, pos_x=100, pos_y=100, override_multiline=False, **kwargs):
        super(MyFancyTextInput, self).__init__(**kwargs)

        #: Default Position
        x_coll = 0
        y_coll = Window.size[1]

        #: TextInput arguments
        self.size_hint = (None, None)
        self.pos = (x_coll + pos_x, y_coll - size_y - pos_y)
        self.size = (size_x, size_y)

        if override_multiline:
            self.multiline = True
        else:
            self.multiline = False


#: Tag_Class : Checkbox class
class MyFancyCheckBox(CheckBox):
    def __init__(self, on_off, size_x=100, size_y=100, pos_x=100, pos_y=100, used_key='False', overwrite_disable='False', **kwargs):
        super(MyFancyCheckBox, self).__init__(**kwargs)

        #: Default Position
        x_coll = 0
        y_coll = Window.size[1]

        #: image of checkbox
        self.background_checkbox_disabled_down = 'img/Disabled_Checked_01.png'
        self.background_checkbox_disabled_normal = 'img/Disabled_Blank_01.png'
        self.background_checkbox_down = 'img/Enabled_Checked_01.png'
        self.background_checkbox_normal = 'img/Enabled_Blank_01.png'

        self.on_off = on_off
        if self.on_off == 1:
            self.active = True

        if used_key != 'False':
            self.used_key = used_key

        if overwrite_disable == 1:
            self.disabled = True

        self.size_hint = (None, None)
        self.pos = (x_coll + pos_x, y_coll - size_y - pos_y)
        self.size = (size_x, size_y)


#: Tag_Class : Button class
class MyFancyButton(Button):
    def __init__(self, size_x=100, size_y=100, pos_x=100, pos_y=100, overwrite_disable=False, **kwargs):
        super(MyFancyButton, self).__init__(**kwargs)

        #: Default Position
        x_coll = 0
        y_coll = Window.size[1]

        if overwrite_disable:
            self.disabled = True

        self.size_hint = (None, None)
        self.pos = (x_coll + pos_x, y_coll - size_y - pos_y)
        self.size = (size_x, size_y)


#: Tag_Class : Layout class
class MyMainWindow(FloatLayout):
    def __init__(self, **kwargs):
        super(MyMainWindow, self).__init__(**kwargs)

        #: Tag :  Set background color
        with self.canvas.before:
            Color(75 / 255, 75 / 255, 75 / 255, 255 / 255)
            Rectangle(size=Window.size)

        #: DEFAULT FONT SIZES
        self.defaultFontSize = 25

        ###################################
        #: Tag : Positions of collections #
        ###################################
        minimum_width = 400
        pos01 = (20, 20)     #: HP
        pos02 = (20, 150)    #: Saving Throws
        pos03 = (20, 330)    #: Skills
        pos04 = (20, 750)    #: Exhaustion
        pos05 = (20, 930)    #: Death Saves
        pos06 = (440, 20)    #: Spell Saves
        pos07 = (440, 110)   #: Sorcerer Points
        pos08 = (440, 240)   #: Spell Slots
        pos09 = (440, 670)   #: Other Proficiencies
        pos10 = (440, 810)   #: Race Traits
        pos11 = (860, 500)   #: Class Abilities            #tmp (860, 20)
        pos12 = (860, 750)   #: Feats                      #tmp (860, 270)
        pos13 = (860, 830)   #: Background Feature         #tmp (860, 350)
        pos14 = (860, 950)   #: Metamagic                  #tmp (860, 480)
        pos15 = (860, 20)    #: Aditional Info Textbox     #tmp (860, 570)
        pos16 = (1280, 500)  #: Stats                      #tmp (1280, 20)
        pos17 = (1280, 660)  #: Proficiency_Bonus + Passives + initiative + ACs   #tmp (1280, 160)
        pos18 = (1280, 800)   #: Attunements               #tmp (1280, 300)

        #############################
        #: Tag :  Health Point Bars #
        #############################
        first_row_size_y = 40
        self.health_point_label = MyFancyLabel(font_size=self.defaultFontSize,
                                               text='HEALTH  POINTS',
                                               size_x=minimum_width,
                                               size_y=first_row_size_y,
                                               pos_x=pos01[0],
                                               pos_y=pos01[1],
                                               show_border=True
                                               )
        self.add_widget(self.health_point_label)

        self.health_point_bonus_checkbox = MyFancyCheckBox(on_off=0,
                                                           size_x=40,
                                                           size_y=first_row_size_y,
                                                           pos_x=pos01[0],
                                                           pos_y=pos01[1],
                                                           )
        self.add_widget(self.health_point_bonus_checkbox)

        #: SECOND ROW "Health Point Bars"
        remove_from_font_size_01 = 12
        second_row_position_from_top = first_row_size_y + 0
        second_row_size_y = 20
        self.health_point_label_max = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                   text='MAX',
                                                   size_x=40,
                                                   size_y=second_row_size_y,
                                                   pos_x=pos01[0],
                                                   pos_y=pos01[1] + second_row_position_from_top,
                                                   show_border=False
                                                   )
        self.add_widget(self.health_point_label_max)

        self.health_point_label_bonus = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                     text='BONUS',
                                                     size_x=60,
                                                     size_y=second_row_size_y,
                                                     pos_x=pos01[0] + 100,
                                                     pos_y=pos01[1] + second_row_position_from_top,
                                                     show_border=False
                                                     )
        self.add_widget(self.health_point_label_bonus)

        self.health_point_label_tmp = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                   text='TMP',
                                                   size_x=40,
                                                   size_y=second_row_size_y,
                                                   pos_x=pos01[0] + 200,
                                                   pos_y=pos01[1] + second_row_position_from_top,
                                                   show_border=False
                                                   )
        self.add_widget(self.health_point_label_tmp)

        self.health_point_label_total = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                     text='TOTAL',
                                                     size_x=50,
                                                     size_y=second_row_size_y,
                                                     pos_x=pos01[0] + 300,
                                                     pos_y=pos01[1] + second_row_position_from_top,
                                                     show_border=False
                                                     )
        self.add_widget(self.health_point_label_total)

        #: THIRD ROW "Health Point Bars"
        remove_from_font_size_02 = 0
        third_row_position_from_top = second_row_position_from_top + second_row_size_y + 0
        third_row_size_y = 50
        self.health_point_input_max = MyFancyTextInput(font_size=self.defaultFontSize - remove_from_font_size_02,
                                                       text=str(CharacterData['HP']['MAX']),
                                                       size_x=80,
                                                       size_y=third_row_size_y,
                                                       pos_x=pos01[0],
                                                       pos_y=pos01[1] + third_row_position_from_top,
                                                       disabled=True
                                                       )
        self.add_widget(self.health_point_input_max)

        self.health_point_input_bonus = MyFancyTextInput(font_size=self.defaultFontSize - remove_from_font_size_02,
                                                         text=str(CharacterData['HP']['BONUS']),
                                                         size_x=80,
                                                         size_y=third_row_size_y,
                                                         pos_x=pos01[0] + 100,
                                                         pos_y=pos01[1] + third_row_position_from_top,
                                                         disabled=True
                                                         )
        self.add_widget(self.health_point_input_bonus)

        self.health_point_input_tmp = MyFancyTextInput(font_size=self.defaultFontSize - remove_from_font_size_02,
                                                       text=str(CharacterData['HP']['TMP']),
                                                       size_x=80,
                                                       size_y=third_row_size_y,
                                                       pos_x=pos01[0] + 200,
                                                       pos_y=pos01[1] + third_row_position_from_top,
                                                       disabled=False
                                                       )
        self.add_widget(self.health_point_input_tmp)

        self.health_point_label_total = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_02,
                                                     text=str(CurrentHP),
                                                     size_x=80,
                                                     size_y=third_row_size_y,
                                                     pos_x=pos01[0] + 300,
                                                     pos_y=pos01[1] + third_row_position_from_top,
                                                     show_border=True
                                                     )
        self.add_widget(self.health_point_label_total)

        #: Labels for + and = characters
        self.health_point_label_plus1 = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_02,
                                                     text='+',
                                                     size_x=20,
                                                     size_y=third_row_size_y,
                                                     pos_x=pos01[0] + 80,
                                                     pos_y=pos01[1] + third_row_position_from_top,
                                                     show_border=False
                                                     )
        self.add_widget(self.health_point_label_plus1)

        self.health_point_label_plus2 = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_02,
                                                     text='+',
                                                     size_x=20,
                                                     size_y=third_row_size_y,
                                                     pos_x=pos01[0] + 180,
                                                     pos_y=pos01[1] + third_row_position_from_top,
                                                     show_border=False
                                                     )
        self.add_widget(self.health_point_label_plus2)

        self.health_point_label_equal = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_02,
                                                     text='=',
                                                     size_x=20,
                                                     size_y=third_row_size_y,
                                                     pos_x=pos01[0] + 280,
                                                     pos_y=pos01[1] + third_row_position_from_top,
                                                     show_border=False
                                                     )
        self.add_widget(self.health_point_label_equal)

        #: Tag :  Health Point Bars # Check Box & TextInput Logic
        #: Logic for checkbox
        def on_bonus_checkbox_active(checkbox, value):
            if value:
                print(f'INFO DEBUG: The checkbox {checkbox} is active, value {value}')
                self.health_point_input_max.disabled = False
                self.health_point_input_bonus.disabled = False
            else:
                print(f'INFO DEBUG: The checkbox {checkbox} is inactive, value {value}')
                self.health_point_input_max.disabled = True
                self.health_point_input_bonus.disabled = True
                save_character_data(character_json_file, CharacterData)

        self.health_point_bonus_checkbox.bind(active=on_bonus_checkbox_active)

        #: Logic for InputBox
        def on_enter(instance):
            self.health_point_input_max.do_cursor_movement(action='cursor_home')
            self.health_point_input_bonus.do_cursor_movement(action='cursor_home')
            self.health_point_input_tmp.do_cursor_movement(action='cursor_home')

            try:
                int(eval(self.health_point_input_max.text))
                self.health_point_input_max.text = str(eval(self.health_point_input_max.text))
            except:
                self.health_point_input_max.text = '0'

            CharacterData['HP']['MAX'] = int(self.health_point_input_max.text)

            try:
                int(eval(self.health_point_input_bonus.text))
                self.health_point_input_bonus.text = str(eval(self.health_point_input_bonus.text))
            except:
                self.health_point_input_bonus.text = '0'

            CharacterData['HP']['BONUS'] = int(self.health_point_input_bonus.text)

            try:
                int(eval(self.health_point_input_tmp.text))
                self.health_point_input_tmp.text = str(eval(self.health_point_input_tmp.text))
            except:
                self.health_point_input_tmp.text = '0'

            CharacterData['HP']['TMP'] = int(self.health_point_input_tmp.text)

            #: Update Label with CurrentHP
            calculate_current_hp([CharacterData['HP']['MAX'], CharacterData['HP']['BONUS'], CharacterData['HP']['TMP']])
            self.health_point_label_total.text = str(CurrentHP)

            save_character_data(character_json_file, CharacterData)
            print(f'INFO DEBUG: hp_sum = {CurrentHP}, {instance}')

        self.health_point_input_max.bind(on_text_validate=on_enter)
        self.health_point_input_bonus.bind(on_text_validate=on_enter)
        self.health_point_input_tmp.bind(on_text_validate=on_enter)

        #########################
        #: Tag :  Saving Throws #
        #########################
        first_row_size_y = 40
        self.saving_throws_label = MyFancyLabel(font_size=self.defaultFontSize,
                                                text='SAVING  THROWS',
                                                size_x=minimum_width,
                                                size_y=first_row_size_y,
                                                pos_x=pos02[0],
                                                pos_y=pos02[1],
                                                show_border=True
                                                )
        self.add_widget(self.saving_throws_label)

        #: STR
        remove_from_font_size_01 = 10
        second_row_position_from_top = first_row_size_y + 0
        second_row_size_y = 40
        second_row_size_x = 80
        my_key = 'STR'
        self.saving_throws_str_checkbox = MyFancyCheckBox(on_off=CharacterData['Saving_Throws'][my_key][0],
                                                          size_x=second_row_size_y,
                                                          size_y=second_row_size_y,
                                                          pos_x=pos02[0],
                                                          pos_y=pos02[1] + second_row_position_from_top,
                                                          disabled=True
                                                          )
        self.add_widget(self.saving_throws_str_checkbox)

        self.saving_throws_str_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                    text=my_key,
                                                    size_x=second_row_size_x,
                                                    size_y=second_row_size_y,
                                                    pos_x=pos02[0] + second_row_size_y,
                                                    pos_y=pos02[1] + second_row_position_from_top,
                                                    show_border=False
                                                    )
        self.add_widget(self.saving_throws_str_label)

        self.saving_throws_str_value_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                          text=str(CharacterData['Saving_Throws'][my_key][1]),
                                                          size_x=second_row_size_y,
                                                          size_y=second_row_size_y,
                                                          pos_x=pos02[0] + second_row_size_y + second_row_size_x,
                                                          pos_y=pos02[1] + second_row_position_from_top,
                                                          show_border=True
                                                          )
        self.add_widget(self.saving_throws_str_value_label)

        #: DEX
        second_row_position_from_top = second_row_position_from_top + second_row_size_y + 0
        my_key = 'DEX'
        self.saving_throws_dex_checkbox = MyFancyCheckBox(on_off=CharacterData['Saving_Throws'][my_key][0],
                                                          size_x=second_row_size_y,
                                                          size_y=second_row_size_y,
                                                          pos_x=pos02[0],
                                                          pos_y=pos02[1] + second_row_position_from_top,
                                                          disabled=True
                                                          )
        self.add_widget(self.saving_throws_dex_checkbox)

        self.saving_throws_dex_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                    text=my_key,
                                                    size_x=second_row_size_x,
                                                    size_y=second_row_size_y,
                                                    pos_x=pos02[0] + second_row_size_y,
                                                    pos_y=pos02[1] + second_row_position_from_top,
                                                    show_border=False
                                                    )
        self.add_widget(self.saving_throws_dex_label)

        self.saving_throws_dex_value_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                          text=str(CharacterData['Saving_Throws'][my_key][1]),
                                                          size_x=second_row_size_y,
                                                          size_y=second_row_size_y,
                                                          pos_x=pos02[0] + second_row_size_y + second_row_size_x,
                                                          pos_y=pos02[1] + second_row_position_from_top,
                                                          show_border=True
                                                          )
        self.add_widget(self.saving_throws_dex_value_label)

        #: CON
        second_row_position_from_top = second_row_position_from_top + second_row_size_y + 0
        my_key = 'CON'
        self.saving_throws_con_checkbox = MyFancyCheckBox(on_off=CharacterData['Saving_Throws'][my_key][0],
                                                          size_x=second_row_size_y,
                                                          size_y=second_row_size_y,
                                                          pos_x=pos02[0],
                                                          pos_y=pos02[1] + second_row_position_from_top,
                                                          disabled=True
                                                          )
        self.add_widget(self.saving_throws_con_checkbox)

        self.saving_throws_con_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                    text=my_key,
                                                    size_x=second_row_size_x,
                                                    size_y=second_row_size_y,
                                                    pos_x=pos02[0] + second_row_size_y,
                                                    pos_y=pos02[1] + second_row_position_from_top,
                                                    show_border=False
                                                    )
        self.add_widget(self.saving_throws_con_label)

        self.saving_throws_con_value_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                          text=str(CharacterData['Saving_Throws'][my_key][1]),
                                                          size_x=second_row_size_y,
                                                          size_y=second_row_size_y,
                                                          pos_x=pos02[0] + second_row_size_y + second_row_size_x,
                                                          pos_y=pos02[1] + second_row_position_from_top,
                                                          show_border=True
                                                          )
        self.add_widget(self.saving_throws_con_value_label)

        #: INT
        second_row_position_from_top = first_row_size_y + 0
        second_column_position = 210
        my_key = 'INT'
        self.saving_throws_int_checkbox = MyFancyCheckBox(on_off=CharacterData['Saving_Throws'][my_key][0],
                                                          size_x=second_row_size_y,
                                                          size_y=second_row_size_y,
                                                          pos_x=pos02[0] + second_column_position,
                                                          pos_y=pos02[1] + second_row_position_from_top,
                                                          disabled=True
                                                          )
        self.add_widget(self.saving_throws_int_checkbox)

        self.saving_throws_int_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                    text=my_key,
                                                    size_x=second_row_size_x,
                                                    size_y=second_row_size_y,
                                                    pos_x=pos02[0] + second_column_position + second_row_size_y,
                                                    pos_y=pos02[1] + second_row_position_from_top,
                                                    show_border=False
                                                    )
        self.add_widget(self.saving_throws_int_label)

        self.saving_throws_int_value_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                          text=str(CharacterData['Saving_Throws'][my_key][1]),
                                                          size_x=second_row_size_y,
                                                          size_y=second_row_size_y,
                                                          pos_x=pos02[0] + second_column_position + second_row_size_y + second_row_size_x,
                                                          pos_y=pos02[1] + second_row_position_from_top,
                                                          show_border=True
                                                          )
        self.add_widget(self.saving_throws_int_value_label)

        #: WIS
        second_row_position_from_top = second_row_position_from_top + second_row_size_y + 0
        my_key = 'WIS'
        self.saving_throws_wis_checkbox = MyFancyCheckBox(on_off=CharacterData['Saving_Throws'][my_key][0],
                                                          size_x=second_row_size_y,
                                                          size_y=second_row_size_y,
                                                          pos_x=pos02[0] + second_column_position,
                                                          pos_y=pos02[1] + second_row_position_from_top,
                                                          disabled=True
                                                          )
        self.add_widget(self.saving_throws_wis_checkbox)

        self.saving_throws_wis_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                    text=my_key,
                                                    size_x=second_row_size_x,
                                                    size_y=second_row_size_y,
                                                    pos_x=pos02[0] + second_column_position + second_row_size_y,
                                                    pos_y=pos02[1] + second_row_position_from_top,
                                                    show_border=False
                                                    )
        self.add_widget(self.saving_throws_wis_label)

        self.saving_throws_wis_value_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                          text=str(CharacterData['Saving_Throws'][my_key][1]),
                                                          size_x=second_row_size_y,
                                                          size_y=second_row_size_y,
                                                          pos_x=pos02[0] + second_column_position + second_row_size_y + second_row_size_x,
                                                          pos_y=pos02[1] + second_row_position_from_top,
                                                          show_border=True
                                                          )
        self.add_widget(self.saving_throws_wis_value_label)

        #: CHA
        second_row_position_from_top = second_row_position_from_top + second_row_size_y + 0
        my_key = 'CHA'
        self.saving_throws_cha_checkbox = MyFancyCheckBox(on_off=CharacterData['Saving_Throws'][my_key][0],
                                                          size_x=second_row_size_y,
                                                          size_y=second_row_size_y,
                                                          pos_x=pos02[0] + second_column_position,
                                                          pos_y=pos02[1] + second_row_position_from_top,
                                                          disabled=True
                                                          )
        self.add_widget(self.saving_throws_cha_checkbox)

        self.saving_throws_cha_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                    text=my_key,
                                                    size_x=second_row_size_x,
                                                    size_y=second_row_size_y,
                                                    pos_x=pos02[0] + second_column_position + second_row_size_y,
                                                    pos_y=pos02[1] + second_row_position_from_top,
                                                    show_border=False
                                                    )
        self.add_widget(self.saving_throws_cha_label)

        self.saving_throws_cha_value_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                          text=str(CharacterData['Saving_Throws'][my_key][1]),
                                                          size_x=second_row_size_y,
                                                          size_y=second_row_size_y,
                                                          pos_x=pos02[0] + second_column_position + second_row_size_y + second_row_size_x,
                                                          pos_y=pos02[1] + second_row_position_from_top,
                                                          show_border=True
                                                          )
        self.add_widget(self.saving_throws_cha_value_label)

        ##################
        #: Tag :  Skills #
        ##################
        #: skill[0/1 - proficiency, from ability, score, bonus]
        first_row_size_y = 40
        self.saving_throws_label = MyFancyLabel(font_size=self.defaultFontSize,
                                                text='SKILLS',
                                                size_x=minimum_width,
                                                size_y=first_row_size_y,
                                                pos_x=pos03[0],
                                                pos_y=pos03[1],
                                                show_border=True
                                                )
        self.add_widget(self.saving_throws_label)

        #: Acrobatics
        remove_from_font_size_01 = 10
        second_row_position_from_top = first_row_size_y + 0
        second_row_size_y = 40
        second_row_size_x = 110
        my_key = 'Acrobatics'
        self.saving_throws_str_checkbox = MyFancyCheckBox(on_off=CharacterData['Skills'][my_key][0],
                                                          size_x=second_row_size_y,
                                                          size_y=second_row_size_y,
                                                          pos_x=pos03[0],
                                                          pos_y=pos03[1] + second_row_position_from_top,
                                                          disabled=True
                                                          )
        self.add_widget(self.saving_throws_str_checkbox)

        self.saving_throws_str_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                    text=my_key,
                                                    size_x=second_row_size_x,
                                                    size_y=second_row_size_y,
                                                    pos_x=pos03[0] + second_row_size_y,
                                                    pos_y=pos03[1] + second_row_position_from_top,
                                                    show_border=False
                                                    )
        self.add_widget(self.saving_throws_str_label)

        self.saving_throws_str_value_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                          text=str(CharacterData['Skills'][my_key][2]),
                                                          size_x=second_row_size_y,
                                                          size_y=second_row_size_y,
                                                          pos_x=pos03[0] + second_row_size_y + second_row_size_x,
                                                          pos_y=pos03[1] + second_row_position_from_top,
                                                          show_border=True
                                                          )
        self.add_widget(self.saving_throws_str_value_label)

        #: Animal_Handling
        second_row_position_from_top = second_row_position_from_top + second_row_size_y + 0
        my_key = 'Animal_Handling'
        self.saving_throws_dex_checkbox = MyFancyCheckBox(on_off=CharacterData['Skills'][my_key][0],
                                                          size_x=second_row_size_y,
                                                          size_y=second_row_size_y,
                                                          pos_x=pos03[0],
                                                          pos_y=pos03[1] + second_row_position_from_top,
                                                          disabled=True
                                                          )
        self.add_widget(self.saving_throws_dex_checkbox)

        self.saving_throws_dex_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                    text=my_key,
                                                    size_x=second_row_size_x,
                                                    size_y=second_row_size_y,
                                                    pos_x=pos03[0] + second_row_size_y,
                                                    pos_y=pos03[1] + second_row_position_from_top,
                                                    show_border=False
                                                    )
        self.add_widget(self.saving_throws_dex_label)

        self.saving_throws_dex_value_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                          text=str(CharacterData['Skills'][my_key][2]),
                                                          size_x=second_row_size_y,
                                                          size_y=second_row_size_y,
                                                          pos_x=pos03[0] + second_row_size_y + second_row_size_x,
                                                          pos_y=pos03[1] + second_row_position_from_top,
                                                          show_border=True
                                                          )
        self.add_widget(self.saving_throws_dex_value_label)

        #: Arcana
        second_row_position_from_top = second_row_position_from_top + second_row_size_y + 0
        my_key = 'Arcana'
        self.saving_throws_dex_checkbox = MyFancyCheckBox(on_off=CharacterData['Skills'][my_key][0],
                                                          size_x=second_row_size_y,
                                                          size_y=second_row_size_y,
                                                          pos_x=pos03[0],
                                                          pos_y=pos03[1] + second_row_position_from_top,
                                                          disabled=True
                                                          )
        self.add_widget(self.saving_throws_dex_checkbox)

        self.saving_throws_dex_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                    text=my_key,
                                                    size_x=second_row_size_x,
                                                    size_y=second_row_size_y,
                                                    pos_x=pos03[0] + second_row_size_y,
                                                    pos_y=pos03[1] + second_row_position_from_top,
                                                    show_border=False
                                                    )
        self.add_widget(self.saving_throws_dex_label)

        self.saving_throws_dex_value_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                          text=str(CharacterData['Skills'][my_key][2]),
                                                          size_x=second_row_size_y,
                                                          size_y=second_row_size_y,
                                                          pos_x=pos03[0] + second_row_size_y + second_row_size_x,
                                                          pos_y=pos03[1] + second_row_position_from_top,
                                                          show_border=True
                                                          )
        self.add_widget(self.saving_throws_dex_value_label)

        #: Athletics
        second_row_position_from_top = second_row_position_from_top + second_row_size_y + 0
        my_key = 'Athletics'
        self.saving_throws_dex_checkbox = MyFancyCheckBox(on_off=CharacterData['Skills'][my_key][0],
                                                          size_x=second_row_size_y,
                                                          size_y=second_row_size_y,
                                                          pos_x=pos03[0],
                                                          pos_y=pos03[1] + second_row_position_from_top,
                                                          disabled=True
                                                          )
        self.add_widget(self.saving_throws_dex_checkbox)

        self.saving_throws_dex_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                    text=my_key,
                                                    size_x=second_row_size_x,
                                                    size_y=second_row_size_y,
                                                    pos_x=pos03[0] + second_row_size_y,
                                                    pos_y=pos03[1] + second_row_position_from_top,
                                                    show_border=False
                                                    )
        self.add_widget(self.saving_throws_dex_label)

        self.saving_throws_dex_value_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                          text=str(CharacterData['Skills'][my_key][2]),
                                                          size_x=second_row_size_y,
                                                          size_y=second_row_size_y,
                                                          pos_x=pos03[0] + second_row_size_y + second_row_size_x,
                                                          pos_y=pos03[1] + second_row_position_from_top,
                                                          show_border=True
                                                          )
        self.add_widget(self.saving_throws_dex_value_label)

        #: Deception
        second_row_position_from_top = second_row_position_from_top + second_row_size_y + 0
        my_key = 'Deception'
        self.saving_throws_dex_checkbox = MyFancyCheckBox(on_off=CharacterData['Skills'][my_key][0],
                                                          size_x=second_row_size_y,
                                                          size_y=second_row_size_y,
                                                          pos_x=pos03[0],
                                                          pos_y=pos03[1] + second_row_position_from_top,
                                                          disabled=True
                                                          )
        self.add_widget(self.saving_throws_dex_checkbox)

        self.saving_throws_dex_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                    text=my_key,
                                                    size_x=second_row_size_x,
                                                    size_y=second_row_size_y,
                                                    pos_x=pos03[0] + second_row_size_y,
                                                    pos_y=pos03[1] + second_row_position_from_top,
                                                    show_border=False
                                                    )
        self.add_widget(self.saving_throws_dex_label)

        self.saving_throws_dex_value_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                          text=str(CharacterData['Skills'][my_key][2]),
                                                          size_x=second_row_size_y,
                                                          size_y=second_row_size_y,
                                                          pos_x=pos03[0] + second_row_size_y + second_row_size_x,
                                                          pos_y=pos03[1] + second_row_position_from_top,
                                                          show_border=True
                                                          )
        self.add_widget(self.saving_throws_dex_value_label)

        #: History
        second_row_position_from_top = second_row_position_from_top + second_row_size_y + 0
        my_key = 'History'
        self.saving_throws_dex_checkbox = MyFancyCheckBox(on_off=CharacterData['Skills'][my_key][0],
                                                          size_x=second_row_size_y,
                                                          size_y=second_row_size_y,
                                                          pos_x=pos03[0],
                                                          pos_y=pos03[1] + second_row_position_from_top,
                                                          disabled=True
                                                          )
        self.add_widget(self.saving_throws_dex_checkbox)

        self.saving_throws_dex_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                    text=my_key,
                                                    size_x=second_row_size_x,
                                                    size_y=second_row_size_y,
                                                    pos_x=pos03[0] + second_row_size_y,
                                                    pos_y=pos03[1] + second_row_position_from_top,
                                                    show_border=False
                                                    )
        self.add_widget(self.saving_throws_dex_label)

        self.saving_throws_dex_value_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                          text=str(CharacterData['Skills'][my_key][2]),
                                                          size_x=second_row_size_y,
                                                          size_y=second_row_size_y,
                                                          pos_x=pos03[0] + second_row_size_y + second_row_size_x,
                                                          pos_y=pos03[1] + second_row_position_from_top,
                                                          show_border=True
                                                          )
        self.add_widget(self.saving_throws_dex_value_label)

        #: Insight
        second_row_position_from_top = second_row_position_from_top + second_row_size_y + 0
        my_key = 'Insight'
        self.saving_throws_dex_checkbox = MyFancyCheckBox(on_off=CharacterData['Skills'][my_key][0],
                                                          size_x=second_row_size_y,
                                                          size_y=second_row_size_y,
                                                          pos_x=pos03[0],
                                                          pos_y=pos03[1] + second_row_position_from_top,
                                                          disabled=True
                                                          )
        self.add_widget(self.saving_throws_dex_checkbox)

        self.saving_throws_dex_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                    text=my_key,
                                                    size_x=second_row_size_x,
                                                    size_y=second_row_size_y,
                                                    pos_x=pos03[0] + second_row_size_y,
                                                    pos_y=pos03[1] + second_row_position_from_top,
                                                    show_border=False
                                                    )
        self.add_widget(self.saving_throws_dex_label)

        self.saving_throws_dex_value_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                          text=str(CharacterData['Skills'][my_key][2]),
                                                          size_x=second_row_size_y,
                                                          size_y=second_row_size_y,
                                                          pos_x=pos03[0] + second_row_size_y + second_row_size_x,
                                                          pos_y=pos03[1] + second_row_position_from_top,
                                                          show_border=True
                                                          )
        self.add_widget(self.saving_throws_dex_value_label)

        #: Intimidation
        second_row_position_from_top = second_row_position_from_top + second_row_size_y + 0
        my_key = 'Intimidation'
        self.saving_throws_dex_checkbox = MyFancyCheckBox(on_off=CharacterData['Skills'][my_key][0],
                                                          size_x=second_row_size_y,
                                                          size_y=second_row_size_y,
                                                          pos_x=pos03[0],
                                                          pos_y=pos03[1] + second_row_position_from_top,
                                                          disabled=True
                                                          )
        self.add_widget(self.saving_throws_dex_checkbox)

        self.saving_throws_dex_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                    text=my_key,
                                                    size_x=second_row_size_x,
                                                    size_y=second_row_size_y,
                                                    pos_x=pos03[0] + second_row_size_y,
                                                    pos_y=pos03[1] + second_row_position_from_top,
                                                    show_border=False
                                                    )
        self.add_widget(self.saving_throws_dex_label)

        self.saving_throws_dex_value_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                          text=str(CharacterData['Skills'][my_key][2]),
                                                          size_x=second_row_size_y,
                                                          size_y=second_row_size_y,
                                                          pos_x=pos03[0] + second_row_size_y + second_row_size_x,
                                                          pos_y=pos03[1] + second_row_position_from_top,
                                                          show_border=True
                                                          )
        self.add_widget(self.saving_throws_dex_value_label)

        #: Investigation
        second_row_position_from_top = second_row_position_from_top + second_row_size_y + 0
        my_key = 'Investigation'
        self.saving_throws_con_checkbox = MyFancyCheckBox(on_off=CharacterData['Skills'][my_key][0],
                                                          size_x=second_row_size_y,
                                                          size_y=second_row_size_y,
                                                          pos_x=pos03[0],
                                                          pos_y=pos03[1] + second_row_position_from_top,
                                                          disabled=True
                                                          )
        self.add_widget(self.saving_throws_con_checkbox)

        self.saving_throws_con_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                    text=my_key,
                                                    size_x=second_row_size_x,
                                                    size_y=second_row_size_y,
                                                    pos_x=pos03[0] + second_row_size_y,
                                                    pos_y=pos03[1] + second_row_position_from_top,
                                                    show_border=False
                                                    )
        self.add_widget(self.saving_throws_con_label)

        self.saving_throws_con_value_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                          text=str(CharacterData['Skills'][my_key][2]),
                                                          size_x=second_row_size_y,
                                                          size_y=second_row_size_y,
                                                          pos_x=pos03[0] + second_row_size_y + second_row_size_x,
                                                          pos_y=pos03[1] + second_row_position_from_top,
                                                          show_border=True
                                                          )
        self.add_widget(self.saving_throws_con_value_label)

        #: Tag :  Skills # Secon Columns
        #: Medicine
        second_row_position_from_top = first_row_size_y + 0
        second_column_position = 190
        my_key = 'Medicine'
        self.saving_throws_int_checkbox = MyFancyCheckBox(on_off=CharacterData['Skills'][my_key][0],
                                                          size_x=second_row_size_y,
                                                          size_y=second_row_size_y,
                                                          pos_x=pos03[0] + second_column_position,
                                                          pos_y=pos03[1] + second_row_position_from_top,
                                                          disabled=True
                                                          )
        self.add_widget(self.saving_throws_int_checkbox)

        self.saving_throws_int_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                    text=my_key,
                                                    size_x=second_row_size_x,
                                                    size_y=second_row_size_y,
                                                    pos_x=pos03[0] + second_column_position + second_row_size_y,
                                                    pos_y=pos03[1] + second_row_position_from_top,
                                                    show_border=False
                                                    )
        self.add_widget(self.saving_throws_int_label)

        self.saving_throws_int_value_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                          text=str(CharacterData['Skills'][my_key][2]),
                                                          size_x=second_row_size_y,
                                                          size_y=second_row_size_y,
                                                          pos_x=pos03[0] + second_column_position + second_row_size_y + second_row_size_x,
                                                          pos_y=pos03[1] + second_row_position_from_top,
                                                          show_border=True
                                                          )
        self.add_widget(self.saving_throws_int_value_label)

        #: Nature
        second_row_position_from_top = second_row_position_from_top + second_row_size_y + 0
        my_key = 'Nature'
        self.saving_throws_wis_checkbox = MyFancyCheckBox(on_off=CharacterData['Skills'][my_key][0],
                                                          size_x=second_row_size_y,
                                                          size_y=second_row_size_y,
                                                          pos_x=pos03[0] + second_column_position,
                                                          pos_y=pos03[1] + second_row_position_from_top,
                                                          disabled=True
                                                          )
        self.add_widget(self.saving_throws_wis_checkbox)

        self.saving_throws_wis_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                    text=my_key,
                                                    size_x=second_row_size_x,
                                                    size_y=second_row_size_y,
                                                    pos_x=pos03[0] + second_column_position + second_row_size_y,
                                                    pos_y=pos03[1] + second_row_position_from_top,
                                                    show_border=False
                                                    )
        self.add_widget(self.saving_throws_wis_label)

        self.saving_throws_wis_value_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                          text=str(CharacterData['Skills'][my_key][2]),
                                                          size_x=second_row_size_y,
                                                          size_y=second_row_size_y,
                                                          pos_x=pos03[0] + second_column_position + second_row_size_y + second_row_size_x,
                                                          pos_y=pos03[1] + second_row_position_from_top,
                                                          show_border=True
                                                          )
        self.add_widget(self.saving_throws_wis_value_label)

        #: Perception
        second_row_position_from_top = second_row_position_from_top + second_row_size_y + 0
        my_key = 'Perception'
        self.saving_throws_wis_checkbox = MyFancyCheckBox(on_off=CharacterData['Skills'][my_key][0],
                                                          size_x=second_row_size_y,
                                                          size_y=second_row_size_y,
                                                          pos_x=pos03[0] + second_column_position,
                                                          pos_y=pos03[1] + second_row_position_from_top,
                                                          disabled=True
                                                          )
        self.add_widget(self.saving_throws_wis_checkbox)

        self.saving_throws_wis_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                    text=my_key,
                                                    size_x=second_row_size_x,
                                                    size_y=second_row_size_y,
                                                    pos_x=pos03[0] + second_column_position + second_row_size_y,
                                                    pos_y=pos03[1] + second_row_position_from_top,
                                                    show_border=False
                                                    )
        self.add_widget(self.saving_throws_wis_label)

        self.saving_throws_wis_value_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                          text=str(CharacterData['Skills'][my_key][2]),
                                                          size_x=second_row_size_y,
                                                          size_y=second_row_size_y,
                                                          pos_x=pos03[0] + second_column_position + second_row_size_y + second_row_size_x,
                                                          pos_y=pos03[1] + second_row_position_from_top,
                                                          show_border=True
                                                          )
        self.add_widget(self.saving_throws_wis_value_label)

        #: Performance
        second_row_position_from_top = second_row_position_from_top + second_row_size_y + 0
        my_key = 'Performance'
        self.saving_throws_wis_checkbox = MyFancyCheckBox(on_off=CharacterData['Skills'][my_key][0],
                                                          size_x=second_row_size_y,
                                                          size_y=second_row_size_y,
                                                          pos_x=pos03[0] + second_column_position,
                                                          pos_y=pos03[1] + second_row_position_from_top,
                                                          disabled=True
                                                          )
        self.add_widget(self.saving_throws_wis_checkbox)

        self.saving_throws_wis_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                    text=my_key,
                                                    size_x=second_row_size_x,
                                                    size_y=second_row_size_y,
                                                    pos_x=pos03[0] + second_column_position + second_row_size_y,
                                                    pos_y=pos03[1] + second_row_position_from_top,
                                                    show_border=False
                                                    )
        self.add_widget(self.saving_throws_wis_label)

        self.saving_throws_wis_value_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                          text=str(CharacterData['Skills'][my_key][2]),
                                                          size_x=second_row_size_y,
                                                          size_y=second_row_size_y,
                                                          pos_x=pos03[0] + second_column_position + second_row_size_y + second_row_size_x,
                                                          pos_y=pos03[1] + second_row_position_from_top,
                                                          show_border=True
                                                          )
        self.add_widget(self.saving_throws_wis_value_label)

        #: Persuasion
        second_row_position_from_top = second_row_position_from_top + second_row_size_y + 0
        my_key = 'Persuasion'
        self.saving_throws_wis_checkbox = MyFancyCheckBox(on_off=CharacterData['Skills'][my_key][0],
                                                          size_x=second_row_size_y,
                                                          size_y=second_row_size_y,
                                                          pos_x=pos03[0] + second_column_position,
                                                          pos_y=pos03[1] + second_row_position_from_top,
                                                          disabled=True
                                                          )
        self.add_widget(self.saving_throws_wis_checkbox)

        self.saving_throws_wis_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                    text=my_key,
                                                    size_x=second_row_size_x,
                                                    size_y=second_row_size_y,
                                                    pos_x=pos03[0] + second_column_position + second_row_size_y,
                                                    pos_y=pos03[1] + second_row_position_from_top,
                                                    show_border=False
                                                    )
        self.add_widget(self.saving_throws_wis_label)

        self.saving_throws_wis_value_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                          text=str(CharacterData['Skills'][my_key][2]),
                                                          size_x=second_row_size_y,
                                                          size_y=second_row_size_y,
                                                          pos_x=pos03[0] + second_column_position + second_row_size_y + second_row_size_x,
                                                          pos_y=pos03[1] + second_row_position_from_top,
                                                          show_border=True
                                                          )
        self.add_widget(self.saving_throws_wis_value_label)

        #: Religion
        second_row_position_from_top = second_row_position_from_top + second_row_size_y + 0
        my_key = 'Religion'
        self.saving_throws_wis_checkbox = MyFancyCheckBox(on_off=CharacterData['Skills'][my_key][0],
                                                          size_x=second_row_size_y,
                                                          size_y=second_row_size_y,
                                                          pos_x=pos03[0] + second_column_position,
                                                          pos_y=pos03[1] + second_row_position_from_top,
                                                          disabled=True
                                                          )
        self.add_widget(self.saving_throws_wis_checkbox)

        self.saving_throws_wis_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                    text=my_key,
                                                    size_x=second_row_size_x,
                                                    size_y=second_row_size_y,
                                                    pos_x=pos03[0] + second_column_position + second_row_size_y,
                                                    pos_y=pos03[1] + second_row_position_from_top,
                                                    show_border=False
                                                    )
        self.add_widget(self.saving_throws_wis_label)

        self.saving_throws_wis_value_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                          text=str(CharacterData['Skills'][my_key][2]),
                                                          size_x=second_row_size_y,
                                                          size_y=second_row_size_y,
                                                          pos_x=pos03[0] + second_column_position + second_row_size_y + second_row_size_x,
                                                          pos_y=pos03[1] + second_row_position_from_top,
                                                          show_border=True
                                                          )
        self.add_widget(self.saving_throws_wis_value_label)

        #: Sleight_of_Hand
        second_row_position_from_top = second_row_position_from_top + second_row_size_y + 0
        my_key = 'Sleight_of_Hand'
        self.saving_throws_wis_checkbox = MyFancyCheckBox(on_off=CharacterData['Skills'][my_key][0],
                                                          size_x=second_row_size_y,
                                                          size_y=second_row_size_y,
                                                          pos_x=pos03[0] + second_column_position,
                                                          pos_y=pos03[1] + second_row_position_from_top,
                                                          disabled=True
                                                          )
        self.add_widget(self.saving_throws_wis_checkbox)

        self.saving_throws_wis_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                    text=my_key,
                                                    size_x=second_row_size_x,
                                                    size_y=second_row_size_y,
                                                    pos_x=pos03[0] + second_column_position + second_row_size_y,
                                                    pos_y=pos03[1] + second_row_position_from_top,
                                                    show_border=False
                                                    )
        self.add_widget(self.saving_throws_wis_label)

        self.saving_throws_wis_value_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                          text=str(CharacterData['Skills'][my_key][2]),
                                                          size_x=second_row_size_y,
                                                          size_y=second_row_size_y,
                                                          pos_x=pos03[0] + second_column_position + second_row_size_y + second_row_size_x,
                                                          pos_y=pos03[1] + second_row_position_from_top,
                                                          show_border=True
                                                          )
        self.add_widget(self.saving_throws_wis_value_label)

        #: Stealth
        second_row_position_from_top = second_row_position_from_top + second_row_size_y + 0
        my_key = 'Stealth'
        self.saving_throws_wis_checkbox = MyFancyCheckBox(on_off=CharacterData['Skills'][my_key][0],
                                                          size_x=second_row_size_y,
                                                          size_y=second_row_size_y,
                                                          pos_x=pos03[0] + second_column_position,
                                                          pos_y=pos03[1] + second_row_position_from_top,
                                                          disabled=True
                                                          )
        self.add_widget(self.saving_throws_wis_checkbox)

        self.saving_throws_wis_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                    text=my_key,
                                                    size_x=second_row_size_x,
                                                    size_y=second_row_size_y,
                                                    pos_x=pos03[0] + second_column_position + second_row_size_y,
                                                    pos_y=pos03[1] + second_row_position_from_top,
                                                    show_border=False
                                                    )
        self.add_widget(self.saving_throws_wis_label)

        self.saving_throws_wis_value_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                          text=str(CharacterData['Skills'][my_key][2]),
                                                          size_x=second_row_size_y,
                                                          size_y=second_row_size_y,
                                                          pos_x=pos03[0] + second_column_position + second_row_size_y + second_row_size_x,
                                                          pos_y=pos03[1] + second_row_position_from_top,
                                                          show_border=True
                                                          )
        self.add_widget(self.saving_throws_wis_value_label)

        #: Survival
        second_row_position_from_top = second_row_position_from_top + second_row_size_y + 0
        my_key = 'Survival'
        self.saving_throws_cha_checkbox = MyFancyCheckBox(on_off=CharacterData['Skills'][my_key][0],
                                                          size_x=second_row_size_y,
                                                          size_y=second_row_size_y,
                                                          pos_x=pos03[0] + second_column_position,
                                                          pos_y=pos03[1] + second_row_position_from_top,
                                                          disabled=True
                                                          )
        self.add_widget(self.saving_throws_cha_checkbox)

        self.saving_throws_cha_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                    text=my_key,
                                                    size_x=second_row_size_x,
                                                    size_y=second_row_size_y,
                                                    pos_x=pos03[0] + second_column_position + second_row_size_y,
                                                    pos_y=pos03[1] + second_row_position_from_top,
                                                    show_border=False
                                                    )
        self.add_widget(self.saving_throws_cha_label)

        self.saving_throws_cha_value_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                          text=str(CharacterData['Skills'][my_key][2]),
                                                          size_x=second_row_size_y,
                                                          size_y=second_row_size_y,
                                                          pos_x=pos03[0] + second_column_position + second_row_size_y + second_row_size_x,
                                                          pos_y=pos03[1] + second_row_position_from_top,
                                                          show_border=True
                                                          )
        self.add_widget(self.saving_throws_cha_value_label)

        ######################
        #: Tag :  Exhaustion #
        ######################
        first_row_size_y = 40
        self.saving_throws_label = MyFancyLabel(font_size=self.defaultFontSize,
                                                text='EXHAUSTION',
                                                size_x=minimum_width,
                                                size_y=first_row_size_y,
                                                pos_x=pos04[0],
                                                pos_y=pos04[1],
                                                show_border=True
                                                )
        self.add_widget(self.saving_throws_label)

        #: 1. level Exhaustion
        remove_from_font_size_01 = 10
        second_row_position_from_top = first_row_size_y + 0
        second_row_size_y = 40
        second_row_size_x = 40

        self.exhaustion_label_1 = MyFancyLabel(font_size=self.defaultFontSize,
                                               text='1.',
                                               size_x=second_row_size_x,
                                               size_y=second_row_size_y,
                                               pos_x=pos04[0],
                                               pos_y=pos04[1] + second_row_size_y,
                                               show_border=True
                                               )
        self.add_widget(self.exhaustion_label_1)

        self.exhaustion_1_checkbox = MyFancyCheckBox(on_off=CharacterData['Exhaustion'][0][0],
                                                     size_x=second_row_size_y,
                                                     size_y=second_row_size_y,
                                                     pos_x=pos04[0] + second_row_size_y,
                                                     pos_y=pos04[1] + second_row_position_from_top,
                                                     disabled=False,
                                                     used_key=0
                                                     )
        self.add_widget(self.exhaustion_1_checkbox)

        self.exhaustion_label_1_desc = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                    text=CharacterData['Exhaustion'][0][1],
                                                    size_x=70,
                                                    size_y=second_row_size_y,
                                                    pos_x=pos04[0] + (second_row_size_y * 2),
                                                    pos_y=pos04[1] + second_row_size_y,
                                                    show_border=False
                                               )
        self.add_widget(self.exhaustion_label_1_desc)

        #: 2. level Exhaustion
        second_row_position_from_top = second_row_position_from_top + second_row_size_y + 0

        self.exhaustion_label_2 = MyFancyLabel(font_size=self.defaultFontSize,
                                               text='2.',
                                               size_x=second_row_size_x,
                                               size_y=second_row_size_y,
                                               pos_x=pos04[0],
                                               pos_y=pos04[1] + second_row_position_from_top,
                                               show_border=True
                                               )
        self.add_widget(self.exhaustion_label_2)

        self.exhaustion_2_checkbox = MyFancyCheckBox(on_off=CharacterData['Exhaustion'][1][0],
                                                     size_x=second_row_size_y,
                                                     size_y=second_row_size_y,
                                                     pos_x=pos04[0] + second_row_size_y,
                                                     pos_y=pos04[1] + second_row_position_from_top,
                                                     disabled=False,
                                                     used_key=1
                                                     )
        self.add_widget(self.exhaustion_2_checkbox)

        self.exhaustion_label_2_desc = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                    text=CharacterData['Exhaustion'][1][1],
                                                    size_x=90,
                                                    size_y=second_row_size_y,
                                                    pos_x=pos04[0] + (second_row_size_y * 2),
                                                    pos_y=pos04[1] + second_row_position_from_top,
                                                    show_border=False
                                                    )
        self.add_widget(self.exhaustion_label_2_desc)

        #: 3. level Exhaustion
        second_row_position_from_top = second_row_position_from_top + second_row_size_y + 0

        self.exhaustion_label_3 = MyFancyLabel(font_size=self.defaultFontSize,
                                               text='3.',
                                               size_x=second_row_size_x,
                                               size_y=second_row_size_y,
                                               pos_x=pos04[0],
                                               pos_y=pos04[1] + second_row_position_from_top,
                                               show_border=True
                                               )
        self.add_widget(self.exhaustion_label_3)

        self.exhaustion_3_checkbox = MyFancyCheckBox(on_off=CharacterData['Exhaustion'][2][0],
                                                     size_x=second_row_size_y,
                                                     size_y=second_row_size_y,
                                                     pos_x=pos04[0] + second_row_size_y,
                                                     pos_y=pos04[1] + second_row_position_from_top,
                                                     disabled=False,
                                                     used_key=2
                                                     )
        self.add_widget(self.exhaustion_3_checkbox)

        self.exhaustion_label_3_desc = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                    text=CharacterData['Exhaustion'][2][1],
                                                    size_x=130,
                                                    size_y=second_row_size_y,
                                                    pos_x=pos04[0] + (second_row_size_y * 2),
                                                    pos_y=pos04[1] + second_row_position_from_top,
                                                    show_border=False
                                                    )
        self.add_widget(self.exhaustion_label_3_desc)

        #: 4. level Exhaustion
        second_row_position_from_top = first_row_size_y + 0
        second_column_position = 210

        self.exhaustion_label_4 = MyFancyLabel(font_size=self.defaultFontSize,
                                               text='4.',
                                               size_x=second_row_size_x,
                                               size_y=second_row_size_y,
                                               pos_x=pos04[0] + second_column_position,
                                               pos_y=pos04[1] + second_row_position_from_top,
                                               show_border=True
                                               )
        self.add_widget(self.exhaustion_label_4)

        self.exhaustion_4_checkbox = MyFancyCheckBox(on_off=CharacterData['Exhaustion'][3][0],
                                                     size_x=second_row_size_y,
                                                     size_y=second_row_size_y,
                                                     pos_x=pos04[0] + second_column_position + second_row_size_y,
                                                     pos_y=pos04[1] + second_row_position_from_top,
                                                     disabled=False,
                                                     used_key=3
                                                     )
        self.add_widget(self.exhaustion_4_checkbox)

        self.exhaustion_label_4_desc = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                    text=CharacterData['Exhaustion'][3][1],
                                                    size_x=90,
                                                    size_y=second_row_size_y,
                                                    pos_x=pos04[0] + second_column_position + (second_row_size_y * 2),
                                                    pos_y=pos04[1] + second_row_position_from_top,
                                                    show_border=False
                                                    )
        self.add_widget(self.exhaustion_label_4_desc)

        #: 5. level Exhaustion
        second_row_position_from_top = second_row_position_from_top + second_row_size_y + 0

        self.exhaustion_label_5 = MyFancyLabel(font_size=self.defaultFontSize,
                                               text='5.',
                                               size_x=second_row_size_x,
                                               size_y=second_row_size_y,
                                               pos_x=pos04[0] + second_column_position,
                                               pos_y=pos04[1] + second_row_position_from_top,
                                               show_border=True
                                               )
        self.add_widget(self.exhaustion_label_5)

        self.exhaustion_5_checkbox = MyFancyCheckBox(on_off=CharacterData['Exhaustion'][4][0],
                                                     size_x=second_row_size_y,
                                                     size_y=second_row_size_y,
                                                     pos_x=pos04[0] + second_column_position + second_row_size_y,
                                                     pos_y=pos04[1] + second_row_position_from_top,
                                                     disabled=False,
                                                     used_key=4
                                                     )
        self.add_widget(self.exhaustion_5_checkbox)

        self.exhaustion_label_5_desc = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                    text=CharacterData['Exhaustion'][4][1],
                                                    size_x=70,
                                                    size_y=second_row_size_y,
                                                    pos_x=pos04[0] + second_column_position + (second_row_size_y * 2),
                                                    pos_y=pos04[1] + second_row_position_from_top,
                                                    show_border=False
                                                    )
        self.add_widget(self.exhaustion_label_5_desc)

        #: 6. level Exhaustion
        second_row_position_from_top = second_row_position_from_top + second_row_size_y + 0

        self.exhaustion_label_6 = MyFancyLabel(font_size=self.defaultFontSize,
                                               text='5.',
                                               size_x=second_row_size_x,
                                               size_y=second_row_size_y,
                                               pos_x=pos04[0] + second_column_position,
                                               pos_y=pos04[1] + second_row_position_from_top,
                                               show_border=True
                                               )
        self.add_widget(self.exhaustion_label_6)

        self.exhaustion_6_checkbox = MyFancyCheckBox(on_off=CharacterData['Exhaustion'][5][0],
                                                     size_x=second_row_size_y,
                                                     size_y=second_row_size_y,
                                                     pos_x=pos04[0] + second_column_position + second_row_size_y,
                                                     pos_y=pos04[1] + second_row_position_from_top,
                                                     disabled=False,
                                                     used_key=5
                                                     )
        self.add_widget(self.exhaustion_6_checkbox)

        self.exhaustion_label_6_desc = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                    text=CharacterData['Exhaustion'][5][1],
                                                    size_x=40,
                                                    size_y=second_row_size_y,
                                                    pos_x=pos04[0] + second_column_position + (second_row_size_y * 2),
                                                    pos_y=pos04[1] + second_row_position_from_top,
                                                    show_border=False
                                                    )
        self.add_widget(self.exhaustion_label_6_desc)

        #: Tag :  Exhaustion # Check Box Logic
        #: Logic for checkbox
        def exhaustion_on_checkbox_active(checkbox, value):
            if value:
                CharacterData['Exhaustion'][checkbox.used_key][0] = 1
                print(f'INFO DEBUG: The checkbox {checkbox} is active, value={value}, key={checkbox.used_key}, ' +
                      f'key_value={CharacterData["Exhaustion"][checkbox.used_key]}')
            else:
                CharacterData['Exhaustion'][checkbox.used_key][0] = 0
                print(f'INFO DEBUG: The checkbox {checkbox} is inactive, value={value}, key={checkbox.used_key}, ' +
                      f'key_value={CharacterData["Exhaustion"][checkbox.used_key]}')

            save_character_data(character_json_file, CharacterData)

        self.exhaustion_1_checkbox.bind(active=exhaustion_on_checkbox_active)
        self.exhaustion_2_checkbox.bind(active=exhaustion_on_checkbox_active)
        self.exhaustion_3_checkbox.bind(active=exhaustion_on_checkbox_active)
        self.exhaustion_4_checkbox.bind(active=exhaustion_on_checkbox_active)
        self.exhaustion_5_checkbox.bind(active=exhaustion_on_checkbox_active)
        self.exhaustion_6_checkbox.bind(active=exhaustion_on_checkbox_active)

        ###############################
        #: Tag :  Death Saving Throws #
        ###############################
        first_row_size_y = 40
        self.saving_throws_label = MyFancyLabel(font_size=self.defaultFontSize,
                                                text='DEATH SAVES',
                                                size_x=minimum_width,
                                                size_y=first_row_size_y,
                                                pos_x=pos05[0],
                                                pos_y=pos05[1],
                                                show_border=True
                                                )
        self.add_widget(self.saving_throws_label)

        #: Live
        second_row_position_from_top = first_row_size_y + 0
        second_row_size_y = 40

        self.death_save_label_l = MyFancyLabel(font_size=self.defaultFontSize,
                                               text='L=',
                                               size_x=second_row_size_y,
                                               size_y=second_row_size_y,
                                               pos_x=pos05[0],
                                               pos_y=pos05[1] + second_row_size_y,
                                               show_border=True
                                               )
        self.add_widget(self.death_save_label_l)

        self.death_save_l1_checkbox = MyFancyCheckBox(on_off=CharacterData['Death_Save']['Lx1'],
                                                      size_x=second_row_size_y,
                                                      size_y=second_row_size_y,
                                                      pos_x=pos05[0] + second_row_size_y,
                                                      pos_y=pos05[1] + second_row_position_from_top,
                                                      disabled=False,
                                                      used_key='Lx1'
                                                      )
        self.add_widget(self.death_save_l1_checkbox)

        self.death_save_l2_checkbox = MyFancyCheckBox(on_off=CharacterData['Death_Save']['Lx2'],
                                                      size_x=second_row_size_y,
                                                      size_y=second_row_size_y,
                                                      pos_x=pos05[0] + second_row_size_y * 2,
                                                      pos_y=pos05[1] + second_row_position_from_top,
                                                      disabled=False,
                                                      used_key='Lx2'
                                                      )
        self.add_widget(self.death_save_l2_checkbox)

        self.death_save_l3_checkbox = MyFancyCheckBox(on_off=CharacterData['Death_Save']['Lx3'],
                                                      size_x=second_row_size_y,
                                                      size_y=second_row_size_y,
                                                      pos_x=pos05[0] + second_row_size_y * 3,
                                                      pos_y=pos05[1] + second_row_position_from_top,
                                                      disabled=False,
                                                      used_key='Lx3'
                                                      )
        self.add_widget(self.death_save_l3_checkbox)

        #: Death
        self.death_save_label_d = MyFancyLabel(font_size=self.defaultFontSize,
                                               text='D=',
                                               size_x=second_row_size_y,
                                               size_y=second_row_size_y,
                                               pos_x=pos05[0] + second_row_size_y * 5,
                                               pos_y=pos05[1] + second_row_size_y,
                                               show_border=True
                                               )
        self.add_widget(self.death_save_label_d)

        self.death_save_d1_checkbox = MyFancyCheckBox(on_off=CharacterData['Death_Save']['Dx1'],
                                                      size_x=second_row_size_y,
                                                      size_y=second_row_size_y,
                                                      pos_x=pos05[0] + second_row_size_y * 6,
                                                      pos_y=pos05[1] + second_row_position_from_top,
                                                      disabled=False,
                                                      used_key='Dx1'
                                                      )
        self.add_widget(self.death_save_d1_checkbox)

        self.death_save_d2_checkbox = MyFancyCheckBox(on_off=CharacterData['Death_Save']['Dx2'],
                                                      size_x=second_row_size_y,
                                                      size_y=second_row_size_y,
                                                      pos_x=pos05[0] + second_row_size_y * 7,
                                                      pos_y=pos05[1] + second_row_position_from_top,
                                                      disabled=False,
                                                      used_key='Dx2'
                                                      )
        self.add_widget(self.death_save_d2_checkbox)

        self.death_save_d3_checkbox = MyFancyCheckBox(on_off=CharacterData['Death_Save']['Dx3'],
                                                      size_x=second_row_size_y,
                                                      size_y=second_row_size_y,
                                                      pos_x=pos05[0] + second_row_size_y * 8,
                                                      pos_y=pos05[1] + second_row_position_from_top,
                                                      disabled=False,
                                                      used_key='Dx3'
                                                      )
        self.add_widget(self.death_save_d3_checkbox)

        #: Tag :  Death Saving Throws # Check Box Logic
        #: Logic for checkbox
        def death_save_on_checkbox_active(checkbox, value):
            if value:
                CharacterData['Death_Save'][checkbox.used_key] = 1
                print(f'INFO DEBUG: The checkbox {checkbox} is active, value={value}, key={checkbox.used_key}, ' +
                      f'key_value={CharacterData["Death_Save"][checkbox.used_key]}')
            else:
                CharacterData['Death_Save'][checkbox.used_key] = 0
                print(f'INFO DEBUG: The checkbox {checkbox} is inactive, value={value}, key={checkbox.used_key}, ' +
                      f'key_value={CharacterData["Death_Save"][checkbox.used_key]}')

            save_character_data(character_json_file, CharacterData)

        self.death_save_l1_checkbox.bind(active=death_save_on_checkbox_active)
        self.death_save_l2_checkbox.bind(active=death_save_on_checkbox_active)
        self.death_save_l3_checkbox.bind(active=death_save_on_checkbox_active)
        self.death_save_d1_checkbox.bind(active=death_save_on_checkbox_active)
        self.death_save_d2_checkbox.bind(active=death_save_on_checkbox_active)
        self.death_save_d3_checkbox.bind(active=death_save_on_checkbox_active)

        ##########################
        #: Tag :  Spell Save DCs #
        ##########################
        first_row_size_y = 40
        self.spell_save_label = MyFancyLabel(font_size=self.defaultFontSize,
                                             text='SPELL SAVES',
                                             size_x=minimum_width,
                                             size_y=first_row_size_y,
                                             pos_x=pos06[0],
                                             pos_y=pos06[1],
                                             show_border=True
                                             )
        self.add_widget(self.spell_save_label)

        #: second row 1. Spell Save  (add more if necessary)
        remove_from_font_size_01 = 7
        second_row_size_y = 40

        self.spell_save_label_dc0 = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                 text='DC:   ' + str(CharacterData["Spell_Save_DC"][0]),
                                                 size_x=120,
                                                 size_y=second_row_size_y,
                                                 pos_x=pos06[0],
                                                 pos_y=pos06[1] + second_row_size_y,
                                                 show_border=False
                                                 )
        self.add_widget(self.spell_save_label_dc0)

        self.spell_save_label_spell_ability0 = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                            text=CharacterData["Spellcasting_Ability"][0],
                                                            size_x=110,
                                                            size_y=second_row_size_y,
                                                            pos_x=pos06[0] + 120,
                                                            pos_y=pos06[1] + second_row_size_y,
                                                            show_border=False
                                                            )
        self.add_widget(self.spell_save_label_spell_ability0)

        self.spell_save_label_atk0 = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                  text='Spell ATK:   ' + str(CharacterData["Spell_Attack_Bonus"][0]),
                                                  size_x=150,
                                                  size_y=second_row_size_y,
                                                  pos_x=pos06[0] + 230,
                                                  pos_y=pos06[1] + second_row_size_y,
                                                  show_border=False
                                                  )
        self.add_widget(self.spell_save_label_atk0)

        #: second row 2. Spell Save  (add more if necessary)

        ##################################
        #: Tag :  Sorcerer Point (or Ki) #
        ##################################
        first_row_size_y = 40
        self.spell_save_label = MyFancyLabel(font_size=self.defaultFontSize,
                                             text='SORCERER POINT',
                                             size_x=minimum_width,
                                             size_y=first_row_size_y,
                                             pos_x=pos07[0],
                                             pos_y=pos07[1],
                                             show_border=True
                                             )
        self.add_widget(self.spell_save_label)

        #: start with checkbox
        second_row_position_from_top = first_row_size_y + 0
        second_row_size_y = 40
        my_key = 'Sx1'
        self.Sorcerer_Points_Sx1_checkbox = MyFancyCheckBox(on_off=CharacterData['Sorcerer_Points (or Ki)'][my_key][0],
                                                            size_x=second_row_size_y,
                                                            size_y=second_row_size_y,
                                                            pos_x=pos07[0],
                                                            pos_y=pos07[1] + second_row_position_from_top,
                                                            disabled=False,
                                                            used_key=my_key,
                                                            overwrite_disable=CharacterData['Sorcerer_Points (or Ki)'][my_key][1]
                                                            )
        self.add_widget(self.Sorcerer_Points_Sx1_checkbox)

        my_key = 'Sx2'
        self.Sorcerer_Points_Sx2_checkbox = MyFancyCheckBox(on_off=CharacterData['Sorcerer_Points (or Ki)'][my_key][0],
                                                            size_x=second_row_size_y,
                                                            size_y=second_row_size_y,
                                                            pos_x=pos07[0] + second_row_size_y,
                                                            pos_y=pos07[1] + second_row_position_from_top,
                                                            disabled=False,
                                                            used_key=my_key,
                                                            overwrite_disable=CharacterData['Sorcerer_Points (or Ki)'][my_key][1]
                                                            )
        self.add_widget(self.Sorcerer_Points_Sx2_checkbox)

        my_key = 'Sx3'
        self.Sorcerer_Points_Sx3_checkbox = MyFancyCheckBox(on_off=CharacterData['Sorcerer_Points (or Ki)'][my_key][0],
                                                            size_x=second_row_size_y,
                                                            size_y=second_row_size_y,
                                                            pos_x=pos07[0] + second_row_size_y * 2,
                                                            pos_y=pos07[1] + second_row_position_from_top,
                                                            disabled=False,
                                                            used_key=my_key,
                                                            overwrite_disable=CharacterData['Sorcerer_Points (or Ki)'][my_key][1]
                                                            )
        self.add_widget(self.Sorcerer_Points_Sx3_checkbox)

        my_key = 'Sx4'
        self.Sorcerer_Points_Sx4_checkbox = MyFancyCheckBox(on_off=CharacterData['Sorcerer_Points (or Ki)'][my_key][0],
                                                            size_x=second_row_size_y,
                                                            size_y=second_row_size_y,
                                                            pos_x=pos07[0] + second_row_size_y * 3,
                                                            pos_y=pos07[1] + second_row_position_from_top,
                                                            disabled=False,
                                                            used_key=my_key,
                                                            overwrite_disable=CharacterData['Sorcerer_Points (or Ki)'][my_key][1]
                                                            )
        self.add_widget(self.Sorcerer_Points_Sx4_checkbox)

        my_key = 'Sx5'
        self.Sorcerer_Points_Sx5_checkbox = MyFancyCheckBox(on_off=CharacterData['Sorcerer_Points (or Ki)'][my_key][0],
                                                            size_x=second_row_size_y,
                                                            size_y=second_row_size_y,
                                                            pos_x=pos07[0] + second_row_size_y * 4,
                                                            pos_y=pos07[1] + second_row_position_from_top,
                                                            disabled=False,
                                                            used_key=my_key,
                                                            overwrite_disable=CharacterData['Sorcerer_Points (or Ki)'][my_key][1]
                                                            )
        self.add_widget(self.Sorcerer_Points_Sx5_checkbox)

        my_key = 'Sx6'
        self.Sorcerer_Points_Sx6_checkbox = MyFancyCheckBox(on_off=CharacterData['Sorcerer_Points (or Ki)'][my_key][0],
                                                            size_x=second_row_size_y,
                                                            size_y=second_row_size_y,
                                                            pos_x=pos07[0] + second_row_size_y * 5,
                                                            pos_y=pos07[1] + second_row_position_from_top,
                                                            disabled=False,
                                                            used_key=my_key,
                                                            overwrite_disable=CharacterData['Sorcerer_Points (or Ki)'][my_key][1]
                                                            )
        self.add_widget(self.Sorcerer_Points_Sx6_checkbox)

        my_key = 'Sx7'
        self.Sorcerer_Points_Sx7_checkbox = MyFancyCheckBox(on_off=CharacterData['Sorcerer_Points (or Ki)'][my_key][0],
                                                            size_x=second_row_size_y,
                                                            size_y=second_row_size_y,
                                                            pos_x=pos07[0] + second_row_size_y * 6,
                                                            pos_y=pos07[1] + second_row_position_from_top,
                                                            disabled=False,
                                                            used_key=my_key,
                                                            overwrite_disable=CharacterData['Sorcerer_Points (or Ki)'][my_key][1]
                                                            )
        self.add_widget(self.Sorcerer_Points_Sx7_checkbox)

        my_key = 'Sx8'
        self.Sorcerer_Points_Sx8_checkbox = MyFancyCheckBox(on_off=CharacterData['Sorcerer_Points (or Ki)'][my_key][0],
                                                            size_x=second_row_size_y,
                                                            size_y=second_row_size_y,
                                                            pos_x=pos07[0] + second_row_size_y * 7,
                                                            pos_y=pos07[1] + second_row_position_from_top,
                                                            disabled=False,
                                                            used_key=my_key,
                                                            overwrite_disable=CharacterData['Sorcerer_Points (or Ki)'][my_key][1]
                                                            )
        self.add_widget(self.Sorcerer_Points_Sx8_checkbox)

        my_key = 'Sx9'
        self.Sorcerer_Points_Sx9_checkbox = MyFancyCheckBox(on_off=CharacterData['Sorcerer_Points (or Ki)'][my_key][0],
                                                            size_x=second_row_size_y,
                                                            size_y=second_row_size_y,
                                                            pos_x=pos07[0] + second_row_size_y * 8,
                                                            pos_y=pos07[1] + second_row_position_from_top,
                                                            disabled=False,
                                                            used_key=my_key,
                                                            overwrite_disable=CharacterData['Sorcerer_Points (or Ki)'][my_key][1]
                                                            )
        self.add_widget(self.Sorcerer_Points_Sx9_checkbox)

        my_key = 'Sx10'
        self.Sorcerer_Points_Sx10_checkbox = MyFancyCheckBox(on_off=CharacterData['Sorcerer_Points (or Ki)'][my_key][0],
                                                             size_x=second_row_size_y,
                                                             size_y=second_row_size_y,
                                                             pos_x=pos07[0] + second_row_size_y * 9,
                                                             pos_y=pos07[1] + second_row_position_from_top,
                                                             disabled=False,
                                                             used_key=my_key,
                                                             overwrite_disable=CharacterData['Sorcerer_Points (or Ki)'][my_key][1]
                                                             )
        self.add_widget(self.Sorcerer_Points_Sx10_checkbox)

        #: second row of Sorcery Points
        #: Tag :  Sorcerer Point (or Ki) # halfway point, second row
        second_row_position_from_top = first_row_size_y + second_row_size_y + 0
        my_key = 'Sx11'
        self.Sorcerer_Points_Sx11_checkbox = MyFancyCheckBox(on_off=CharacterData['Sorcerer_Points (or Ki)'][my_key][0],
                                                             size_x=second_row_size_y,
                                                             size_y=second_row_size_y,
                                                             pos_x=pos07[0],
                                                             pos_y=pos07[1] + second_row_position_from_top,
                                                             disabled=False,
                                                             used_key=my_key,
                                                             overwrite_disable=CharacterData['Sorcerer_Points (or Ki)'][my_key][1]
                                                             )
        self.add_widget(self.Sorcerer_Points_Sx11_checkbox)

        my_key = 'Sx12'
        self.Sorcerer_Points_Sx12_checkbox = MyFancyCheckBox(on_off=CharacterData['Sorcerer_Points (or Ki)'][my_key][0],
                                                             size_x=second_row_size_y,
                                                             size_y=second_row_size_y,
                                                             pos_x=pos07[0] + second_row_size_y,
                                                             pos_y=pos07[1] + second_row_position_from_top,
                                                             disabled=False,
                                                             used_key=my_key,
                                                             overwrite_disable=CharacterData['Sorcerer_Points (or Ki)'][my_key][1]
                                                             )
        self.add_widget(self.Sorcerer_Points_Sx12_checkbox)

        my_key = 'Sx13'
        self.Sorcerer_Points_Sx13_checkbox = MyFancyCheckBox(on_off=CharacterData['Sorcerer_Points (or Ki)'][my_key][0],
                                                             size_x=second_row_size_y,
                                                             size_y=second_row_size_y,
                                                             pos_x=pos07[0] + second_row_size_y * 2,
                                                             pos_y=pos07[1] + second_row_position_from_top,
                                                             disabled=False,
                                                             used_key=my_key,
                                                             overwrite_disable=CharacterData['Sorcerer_Points (or Ki)'][my_key][1]
                                                             )
        self.add_widget(self.Sorcerer_Points_Sx13_checkbox)

        my_key = 'Sx14'
        self.Sorcerer_Points_Sx14_checkbox = MyFancyCheckBox(on_off=CharacterData['Sorcerer_Points (or Ki)'][my_key][0],
                                                             size_x=second_row_size_y,
                                                             size_y=second_row_size_y,
                                                             pos_x=pos07[0] + second_row_size_y * 3,
                                                             pos_y=pos07[1] + second_row_position_from_top,
                                                             disabled=False,
                                                             used_key=my_key,
                                                             overwrite_disable=CharacterData['Sorcerer_Points (or Ki)'][my_key][1]
                                                             )
        self.add_widget(self.Sorcerer_Points_Sx14_checkbox)

        my_key = 'Sx15'
        self.Sorcerer_Points_Sx15_checkbox = MyFancyCheckBox(on_off=CharacterData['Sorcerer_Points (or Ki)'][my_key][0],
                                                             size_x=second_row_size_y,
                                                             size_y=second_row_size_y,
                                                             pos_x=pos07[0] + second_row_size_y * 4,
                                                             pos_y=pos07[1] + second_row_position_from_top,
                                                             disabled=False,
                                                             used_key=my_key,
                                                             overwrite_disable=CharacterData['Sorcerer_Points (or Ki)'][my_key][1]
                                                             )
        self.add_widget(self.Sorcerer_Points_Sx15_checkbox)

        my_key = 'Sx16'
        self.Sorcerer_Points_Sx16_checkbox = MyFancyCheckBox(on_off=CharacterData['Sorcerer_Points (or Ki)'][my_key][0],
                                                             size_x=second_row_size_y,
                                                             size_y=second_row_size_y,
                                                             pos_x=pos07[0] + second_row_size_y * 5,
                                                             pos_y=pos07[1] + second_row_position_from_top,
                                                             disabled=False,
                                                             used_key=my_key,
                                                             overwrite_disable=CharacterData['Sorcerer_Points (or Ki)'][my_key][1]
                                                             )
        self.add_widget(self.Sorcerer_Points_Sx16_checkbox)

        my_key = 'Sx17'
        self.Sorcerer_Points_Sx17_checkbox = MyFancyCheckBox(on_off=CharacterData['Sorcerer_Points (or Ki)'][my_key][0],
                                                             size_x=second_row_size_y,
                                                             size_y=second_row_size_y,
                                                             pos_x=pos07[0] + second_row_size_y * 6,
                                                             pos_y=pos07[1] + second_row_position_from_top,
                                                             disabled=False,
                                                             used_key=my_key,
                                                             overwrite_disable=CharacterData['Sorcerer_Points (or Ki)'][my_key][1]
                                                             )
        self.add_widget(self.Sorcerer_Points_Sx17_checkbox)

        my_key = 'Sx18'
        self.Sorcerer_Points_Sx18_checkbox = MyFancyCheckBox(on_off=CharacterData['Sorcerer_Points (or Ki)'][my_key][0],
                                                             size_x=second_row_size_y,
                                                             size_y=second_row_size_y,
                                                             pos_x=pos07[0] + second_row_size_y * 7,
                                                             pos_y=pos07[1] + second_row_position_from_top,
                                                             disabled=False,
                                                             used_key=my_key,
                                                             overwrite_disable=CharacterData['Sorcerer_Points (or Ki)'][my_key][1]
                                                             )
        self.add_widget(self.Sorcerer_Points_Sx18_checkbox)

        my_key = 'Sx19'
        self.Sorcerer_Points_Sx19_checkbox = MyFancyCheckBox(on_off=CharacterData['Sorcerer_Points (or Ki)'][my_key][0],
                                                             size_x=second_row_size_y,
                                                             size_y=second_row_size_y,
                                                             pos_x=pos07[0] + second_row_size_y * 8,
                                                             pos_y=pos07[1] + second_row_position_from_top,
                                                             disabled=False,
                                                             used_key=my_key,
                                                             overwrite_disable=CharacterData['Sorcerer_Points (or Ki)'][my_key][1]
                                                             )
        self.add_widget(self.Sorcerer_Points_Sx19_checkbox)

        my_key = 'Sx20'
        self.Sorcerer_Points_Sx20_checkbox = MyFancyCheckBox(on_off=CharacterData['Sorcerer_Points (or Ki)'][my_key][0],
                                                             size_x=second_row_size_y,
                                                             size_y=second_row_size_y,
                                                             pos_x=pos07[0] + second_row_size_y * 9,
                                                             pos_y=pos07[1] + second_row_position_from_top,
                                                             disabled=False,
                                                             used_key=my_key,
                                                             overwrite_disable=CharacterData['Sorcerer_Points (or Ki)'][my_key][1]
                                                             )
        self.add_widget(self.Sorcerer_Points_Sx20_checkbox)

        #: Tag :  Sorcerer Point (or Ki) # Check Box Logic
        #: Logic for checkbox
        def sorc_point_on_checkbox_active(checkbox, value):
            if value:
                CharacterData['Sorcerer_Points (or Ki)'][checkbox.used_key][0] = 1
                print(f'INFO DEBUG: The checkbox {checkbox} is active, value={value}, key={checkbox.used_key}, ' +
                      f'key_value={CharacterData["Sorcerer_Points (or Ki)"][checkbox.used_key]}')
            else:
                CharacterData['Sorcerer_Points (or Ki)'][checkbox.used_key][0] = 0
                print(f'INFO DEBUG: The checkbox {checkbox} is inactive, value={value}, key={checkbox.used_key}, ' +
                      f'key_value={CharacterData["Sorcerer_Points (or Ki)"][checkbox.used_key]}')

            save_character_data(character_json_file, CharacterData)

        self.Sorcerer_Points_Sx1_checkbox.bind(active=sorc_point_on_checkbox_active)
        self.Sorcerer_Points_Sx2_checkbox.bind(active=sorc_point_on_checkbox_active)
        self.Sorcerer_Points_Sx3_checkbox.bind(active=sorc_point_on_checkbox_active)
        self.Sorcerer_Points_Sx4_checkbox.bind(active=sorc_point_on_checkbox_active)
        self.Sorcerer_Points_Sx5_checkbox.bind(active=sorc_point_on_checkbox_active)
        self.Sorcerer_Points_Sx6_checkbox.bind(active=sorc_point_on_checkbox_active)
        self.Sorcerer_Points_Sx7_checkbox.bind(active=sorc_point_on_checkbox_active)
        self.Sorcerer_Points_Sx8_checkbox.bind(active=sorc_point_on_checkbox_active)
        self.Sorcerer_Points_Sx9_checkbox.bind(active=sorc_point_on_checkbox_active)
        self.Sorcerer_Points_Sx10_checkbox.bind(active=sorc_point_on_checkbox_active)
        self.Sorcerer_Points_Sx11_checkbox.bind(active=sorc_point_on_checkbox_active)
        self.Sorcerer_Points_Sx12_checkbox.bind(active=sorc_point_on_checkbox_active)
        self.Sorcerer_Points_Sx13_checkbox.bind(active=sorc_point_on_checkbox_active)
        self.Sorcerer_Points_Sx14_checkbox.bind(active=sorc_point_on_checkbox_active)
        self.Sorcerer_Points_Sx15_checkbox.bind(active=sorc_point_on_checkbox_active)
        self.Sorcerer_Points_Sx16_checkbox.bind(active=sorc_point_on_checkbox_active)
        self.Sorcerer_Points_Sx17_checkbox.bind(active=sorc_point_on_checkbox_active)
        self.Sorcerer_Points_Sx18_checkbox.bind(active=sorc_point_on_checkbox_active)
        self.Sorcerer_Points_Sx19_checkbox.bind(active=sorc_point_on_checkbox_active)
        self.Sorcerer_Points_Sx20_checkbox.bind(active=sorc_point_on_checkbox_active)

        #######################
        #: Tag :  Spell Slots #
        #######################
        first_row_size_y = 40
        self.spell_save_label = MyFancyLabel(font_size=self.defaultFontSize,
                                             text='SPELL SLOTS',
                                             size_x=minimum_width,
                                             size_y=first_row_size_y,
                                             pos_x=pos08[0],
                                             pos_y=pos08[1],
                                             show_border=True
                                             )
        self.add_widget(self.spell_save_label)

        #: Level 1 Spell Slots
        remove_from_font_size_01 = 5
        second_row_position_from_top = first_row_size_y + 0
        second_row_size_y = 40
        second_row_size_x = 130

        self.Spell_Slots_1_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                text='1. Level',
                                                size_x=second_row_size_x,
                                                size_y=second_row_size_y,
                                                pos_x=pos08[0],
                                                pos_y=pos08[1] + second_row_size_y,
                                                show_border=False
                                                )
        self.add_widget(self.Spell_Slots_1_label)

        my_key = '1x1'
        shift_x = second_row_size_y * 0
        self.Spell_Slots_1x1_checkbox = MyFancyCheckBox(on_off=CharacterData['Spell_Slots'][my_key][0],
                                                        size_x=second_row_size_y,
                                                        size_y=second_row_size_y,
                                                        pos_x=pos08[0] + second_row_size_x + shift_x,
                                                        pos_y=pos08[1] + second_row_position_from_top,
                                                        disabled=False,
                                                        used_key=my_key,
                                                        overwrite_disable=CharacterData['Spell_Slots'][my_key][1]
                                                        )
        self.add_widget(self.Spell_Slots_1x1_checkbox)

        my_key = '1x2'
        shift_x = second_row_size_y * 1
        self.Spell_Slots_1x2_checkbox = MyFancyCheckBox(on_off=CharacterData['Spell_Slots'][my_key][0],
                                                        size_x=second_row_size_y,
                                                        size_y=second_row_size_y,
                                                        pos_x=pos08[0] + second_row_size_x + shift_x,
                                                        pos_y=pos08[1] + second_row_position_from_top,
                                                        disabled=False,
                                                        used_key=my_key,
                                                        overwrite_disable=CharacterData['Spell_Slots'][my_key][1]
                                                        )
        self.add_widget(self.Spell_Slots_1x2_checkbox)

        my_key = '1x3'
        shift_x = second_row_size_y * 2
        self.Spell_Slots_1x3_checkbox = MyFancyCheckBox(on_off=CharacterData['Spell_Slots'][my_key][0],
                                                        size_x=second_row_size_y,
                                                        size_y=second_row_size_y,
                                                        pos_x=pos08[0] + second_row_size_x + shift_x,
                                                        pos_y=pos08[1] + second_row_position_from_top,
                                                        disabled=False,
                                                        used_key=my_key,
                                                        overwrite_disable=CharacterData['Spell_Slots'][my_key][1]
                                                        )
        self.add_widget(self.Spell_Slots_1x3_checkbox)

        my_key = '1x4'
        shift_x = second_row_size_y * 3
        self.Spell_Slots_1x4_checkbox = MyFancyCheckBox(on_off=CharacterData['Spell_Slots'][my_key][0],
                                                        size_x=second_row_size_y,
                                                        size_y=second_row_size_y,
                                                        pos_x=pos08[0] + second_row_size_x + shift_x,
                                                        pos_y=pos08[1] + second_row_position_from_top,
                                                        disabled=False,
                                                        used_key=my_key,
                                                        overwrite_disable=CharacterData['Spell_Slots'][my_key][1]
                                                        )
        self.add_widget(self.Spell_Slots_1x4_checkbox)

        #: Level 2 Spell Slots
        second_row_position_from_top = second_row_position_from_top + first_row_size_y + 0
        self.Spell_Slots_2_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                text='2. Level',
                                                size_x=second_row_size_x,
                                                size_y=second_row_size_y,
                                                pos_x=pos08[0],
                                                pos_y=pos08[1] + second_row_position_from_top,
                                                show_border=False
                                                )
        self.add_widget(self.Spell_Slots_2_label)

        my_key = '2x1'
        shift_x = second_row_size_y * 0
        self.Spell_Slots_2x1_checkbox = MyFancyCheckBox(on_off=CharacterData['Spell_Slots'][my_key][0],
                                                        size_x=second_row_size_y,
                                                        size_y=second_row_size_y,
                                                        pos_x=pos08[0] + second_row_size_x + shift_x,
                                                        pos_y=pos08[1] + second_row_position_from_top,
                                                        disabled=False,
                                                        used_key=my_key,
                                                        overwrite_disable=CharacterData['Spell_Slots'][my_key][1]
                                                        )
        self.add_widget(self.Spell_Slots_2x1_checkbox)

        my_key = '2x2'
        shift_x = second_row_size_y * 1
        self.Spell_Slots_2x2_checkbox = MyFancyCheckBox(on_off=CharacterData['Spell_Slots'][my_key][0],
                                                        size_x=second_row_size_y,
                                                        size_y=second_row_size_y,
                                                        pos_x=pos08[0] + second_row_size_x + shift_x,
                                                        pos_y=pos08[1] + second_row_position_from_top,
                                                        disabled=False,
                                                        used_key=my_key,
                                                        overwrite_disable=CharacterData['Spell_Slots'][my_key][1]
                                                        )
        self.add_widget(self.Spell_Slots_2x2_checkbox)

        my_key = '2x3'
        shift_x = second_row_size_y * 2
        self.Spell_Slots_2x3_checkbox = MyFancyCheckBox(on_off=CharacterData['Spell_Slots'][my_key][0],
                                                        size_x=second_row_size_y,
                                                        size_y=second_row_size_y,
                                                        pos_x=pos08[0] + second_row_size_x + shift_x,
                                                        pos_y=pos08[1] + second_row_position_from_top,
                                                        disabled=False,
                                                        used_key=my_key,
                                                        overwrite_disable=CharacterData['Spell_Slots'][my_key][1]
                                                        )
        self.add_widget(self.Spell_Slots_2x3_checkbox)

        #: Level 3 Spell Slots
        second_row_position_from_top = second_row_position_from_top + first_row_size_y + 0
        self.Spell_Slots_3_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                text='3. Level',
                                                size_x=second_row_size_x,
                                                size_y=second_row_size_y,
                                                pos_x=pos08[0],
                                                pos_y=pos08[1] + second_row_position_from_top,
                                                show_border=False
                                                )
        self.add_widget(self.Spell_Slots_3_label)

        my_key = '3x1'
        shift_x = second_row_size_y * 0
        self.Spell_Slots_3x1_checkbox = MyFancyCheckBox(on_off=CharacterData['Spell_Slots'][my_key][0],
                                                        size_x=second_row_size_y,
                                                        size_y=second_row_size_y,
                                                        pos_x=pos08[0] + second_row_size_x + shift_x,
                                                        pos_y=pos08[1] + second_row_position_from_top,
                                                        disabled=False,
                                                        used_key=my_key,
                                                        overwrite_disable=CharacterData['Spell_Slots'][my_key][1]
                                                        )
        self.add_widget(self.Spell_Slots_3x1_checkbox)

        my_key = '3x2'
        shift_x = second_row_size_y * 1
        self.Spell_Slots_3x2_checkbox = MyFancyCheckBox(on_off=CharacterData['Spell_Slots'][my_key][0],
                                                        size_x=second_row_size_y,
                                                        size_y=second_row_size_y,
                                                        pos_x=pos08[0] + second_row_size_x + shift_x,
                                                        pos_y=pos08[1] + second_row_position_from_top,
                                                        disabled=False,
                                                        used_key=my_key,
                                                        overwrite_disable=CharacterData['Spell_Slots'][my_key][1]
                                                        )
        self.add_widget(self.Spell_Slots_3x2_checkbox)

        my_key = '3x3'
        shift_x = second_row_size_y * 2
        self.Spell_Slots_3x3_checkbox = MyFancyCheckBox(on_off=CharacterData['Spell_Slots'][my_key][0],
                                                        size_x=second_row_size_y,
                                                        size_y=second_row_size_y,
                                                        pos_x=pos08[0] + second_row_size_x + shift_x,
                                                        pos_y=pos08[1] + second_row_position_from_top,
                                                        disabled=False,
                                                        used_key=my_key,
                                                        overwrite_disable=CharacterData['Spell_Slots'][my_key][1]
                                                        )
        self.add_widget(self.Spell_Slots_3x3_checkbox)

        #: Level 4 Spell Slots
        second_row_position_from_top = second_row_position_from_top + first_row_size_y + 0
        self.Spell_Slots_4_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                text='4. Level',
                                                size_x=second_row_size_x,
                                                size_y=second_row_size_y,
                                                pos_x=pos08[0],
                                                pos_y=pos08[1] + second_row_position_from_top,
                                                show_border=False
                                                )
        self.add_widget(self.Spell_Slots_4_label)

        my_key = '4x1'
        shift_x = second_row_size_y * 0
        self.Spell_Slots_4x1_checkbox = MyFancyCheckBox(on_off=CharacterData['Spell_Slots'][my_key][0],
                                                        size_x=second_row_size_y,
                                                        size_y=second_row_size_y,
                                                        pos_x=pos08[0] + second_row_size_x + shift_x,
                                                        pos_y=pos08[1] + second_row_position_from_top,
                                                        disabled=False,
                                                        used_key=my_key,
                                                        overwrite_disable=CharacterData['Spell_Slots'][my_key][1]
                                                        )
        self.add_widget(self.Spell_Slots_4x1_checkbox)

        my_key = '4x2'
        shift_x = second_row_size_y * 1
        self.Spell_Slots_4x2_checkbox = MyFancyCheckBox(on_off=CharacterData['Spell_Slots'][my_key][0],
                                                        size_x=second_row_size_y,
                                                        size_y=second_row_size_y,
                                                        pos_x=pos08[0] + second_row_size_x + shift_x,
                                                        pos_y=pos08[1] + second_row_position_from_top,
                                                        disabled=False,
                                                        used_key=my_key,
                                                        overwrite_disable=CharacterData['Spell_Slots'][my_key][1]
                                                        )
        self.add_widget(self.Spell_Slots_4x2_checkbox)

        my_key = '4x3'
        shift_x = second_row_size_y * 2
        self.Spell_Slots_4x3_checkbox = MyFancyCheckBox(on_off=CharacterData['Spell_Slots'][my_key][0],
                                                        size_x=second_row_size_y,
                                                        size_y=second_row_size_y,
                                                        pos_x=pos08[0] + second_row_size_x + shift_x,
                                                        pos_y=pos08[1] + second_row_position_from_top,
                                                        disabled=False,
                                                        used_key=my_key,
                                                        overwrite_disable=CharacterData['Spell_Slots'][my_key][1]
                                                        )
        self.add_widget(self.Spell_Slots_4x3_checkbox)

        #: Level 5 Spell Slots
        second_row_position_from_top = second_row_position_from_top + first_row_size_y + 0
        self.Spell_Slots_5_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                text='5. Level',
                                                size_x=second_row_size_x,
                                                size_y=second_row_size_y,
                                                pos_x=pos08[0],
                                                pos_y=pos08[1] + second_row_position_from_top,
                                                show_border=False
                                                )
        self.add_widget(self.Spell_Slots_5_label)

        my_key = '5x1'
        shift_x = second_row_size_y * 0
        self.Spell_Slots_5x1_checkbox = MyFancyCheckBox(on_off=CharacterData['Spell_Slots'][my_key][0],
                                                        size_x=second_row_size_y,
                                                        size_y=second_row_size_y,
                                                        pos_x=pos08[0] + second_row_size_x + shift_x,
                                                        pos_y=pos08[1] + second_row_position_from_top,
                                                        disabled=False,
                                                        used_key=my_key,
                                                        overwrite_disable=CharacterData['Spell_Slots'][my_key][1]
                                                        )
        self.add_widget(self.Spell_Slots_5x1_checkbox)

        my_key = '5x2'
        shift_x = second_row_size_y * 1
        self.Spell_Slots_5x2_checkbox = MyFancyCheckBox(on_off=CharacterData['Spell_Slots'][my_key][0],
                                                        size_x=second_row_size_y,
                                                        size_y=second_row_size_y,
                                                        pos_x=pos08[0] + second_row_size_x + shift_x,
                                                        pos_y=pos08[1] + second_row_position_from_top,
                                                        disabled=False,
                                                        used_key=my_key,
                                                        overwrite_disable=CharacterData['Spell_Slots'][my_key][1]
                                                        )
        self.add_widget(self.Spell_Slots_5x2_checkbox)

        my_key = '5x3'
        shift_x = second_row_size_y * 2
        self.Spell_Slots_5x3_checkbox = MyFancyCheckBox(on_off=CharacterData['Spell_Slots'][my_key][0],
                                                        size_x=second_row_size_y,
                                                        size_y=second_row_size_y,
                                                        pos_x=pos08[0] + second_row_size_x + shift_x,
                                                        pos_y=pos08[1] + second_row_position_from_top,
                                                        disabled=False,
                                                        used_key=my_key,
                                                        overwrite_disable=CharacterData['Spell_Slots'][my_key][1]
                                                        )
        self.add_widget(self.Spell_Slots_5x3_checkbox)

        #: Level 6 Spell Slots
        second_row_position_from_top = second_row_position_from_top + first_row_size_y + 0
        self.Spell_Slots_6_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                text='6. Level',
                                                size_x=second_row_size_x,
                                                size_y=second_row_size_y,
                                                pos_x=pos08[0],
                                                pos_y=pos08[1] + second_row_position_from_top,
                                                show_border=False
                                                )
        self.add_widget(self.Spell_Slots_6_label)

        my_key = '6x1'
        shift_x = second_row_size_y * 0
        self.Spell_Slots_6x1_checkbox = MyFancyCheckBox(on_off=CharacterData['Spell_Slots'][my_key][0],
                                                        size_x=second_row_size_y,
                                                        size_y=second_row_size_y,
                                                        pos_x=pos08[0] + second_row_size_x + shift_x,
                                                        pos_y=pos08[1] + second_row_position_from_top,
                                                        disabled=False,
                                                        used_key=my_key,
                                                        overwrite_disable=CharacterData['Spell_Slots'][my_key][1]
                                                        )
        self.add_widget(self.Spell_Slots_6x1_checkbox)

        my_key = '6x2'
        shift_x = second_row_size_y * 1
        self.Spell_Slots_6x2_checkbox = MyFancyCheckBox(on_off=CharacterData['Spell_Slots'][my_key][0],
                                                        size_x=second_row_size_y,
                                                        size_y=second_row_size_y,
                                                        pos_x=pos08[0] + second_row_size_x + shift_x,
                                                        pos_y=pos08[1] + second_row_position_from_top,
                                                        disabled=False,
                                                        used_key=my_key,
                                                        overwrite_disable=CharacterData['Spell_Slots'][my_key][1]
                                                        )
        self.add_widget(self.Spell_Slots_6x2_checkbox)

        #: Level 7 Spell Slots
        second_row_position_from_top = second_row_position_from_top + first_row_size_y + 0
        self.Spell_Slots_7_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                text='7. Level',
                                                size_x=second_row_size_x,
                                                size_y=second_row_size_y,
                                                pos_x=pos08[0],
                                                pos_y=pos08[1] + second_row_position_from_top,
                                                show_border=False
                                                )
        self.add_widget(self.Spell_Slots_7_label)

        my_key = '7x1'
        shift_x = second_row_size_y * 0
        self.Spell_Slots_7x1_checkbox = MyFancyCheckBox(on_off=CharacterData['Spell_Slots'][my_key][0],
                                                        size_x=second_row_size_y,
                                                        size_y=second_row_size_y,
                                                        pos_x=pos08[0] + second_row_size_x + shift_x,
                                                        pos_y=pos08[1] + second_row_position_from_top,
                                                        disabled=False,
                                                        used_key=my_key,
                                                        overwrite_disable=CharacterData['Spell_Slots'][my_key][1]
                                                        )
        self.add_widget(self.Spell_Slots_7x1_checkbox)

        my_key = '7x2'
        shift_x = second_row_size_y * 1
        self.Spell_Slots_7x2_checkbox = MyFancyCheckBox(on_off=CharacterData['Spell_Slots'][my_key][0],
                                                        size_x=second_row_size_y,
                                                        size_y=second_row_size_y,
                                                        pos_x=pos08[0] + second_row_size_x + shift_x,
                                                        pos_y=pos08[1] + second_row_position_from_top,
                                                        disabled=False,
                                                        used_key=my_key,
                                                        overwrite_disable=CharacterData['Spell_Slots'][my_key][1]
                                                        )
        self.add_widget(self.Spell_Slots_7x2_checkbox)

        #: Level 8 Spell Slots
        second_row_position_from_top = second_row_position_from_top + first_row_size_y + 0
        self.Spell_Slots_8_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                text='8. Level',
                                                size_x=second_row_size_x,
                                                size_y=second_row_size_y,
                                                pos_x=pos08[0],
                                                pos_y=pos08[1] + second_row_position_from_top,
                                                show_border=False
                                                )
        self.add_widget(self.Spell_Slots_8_label)

        my_key = '8x1'
        shift_x = second_row_size_y * 0
        self.Spell_Slots_8x1_checkbox = MyFancyCheckBox(on_off=CharacterData['Spell_Slots'][my_key][0],
                                                        size_x=second_row_size_y,
                                                        size_y=second_row_size_y,
                                                        pos_x=pos08[0] + second_row_size_x + shift_x,
                                                        pos_y=pos08[1] + second_row_position_from_top,
                                                        disabled=False,
                                                        used_key=my_key,
                                                        overwrite_disable=CharacterData['Spell_Slots'][my_key][1]
                                                        )
        self.add_widget(self.Spell_Slots_8x1_checkbox)

        #: Level 9 Spell Slots
        second_row_position_from_top = second_row_position_from_top + first_row_size_y + 0
        self.Spell_Slots_9_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                text='9. Level',
                                                size_x=second_row_size_x,
                                                size_y=second_row_size_y,
                                                pos_x=pos08[0],
                                                pos_y=pos08[1] + second_row_position_from_top,
                                                show_border=False
                                                )
        self.add_widget(self.Spell_Slots_9_label)

        my_key = '9x1'
        shift_x = second_row_size_y * 0
        self.Spell_Slots_9x1_checkbox = MyFancyCheckBox(on_off=CharacterData['Spell_Slots'][my_key][0],
                                                        size_x=second_row_size_y,
                                                        size_y=second_row_size_y,
                                                        pos_x=pos08[0] + second_row_size_x + shift_x,
                                                        pos_y=pos08[1] + second_row_position_from_top,
                                                        disabled=False,
                                                        used_key=my_key,
                                                        overwrite_disable=CharacterData['Spell_Slots'][my_key][1]
                                                        )
        self.add_widget(self.Spell_Slots_9x1_checkbox)

        #: Tag :  Spell Slots # Check Box Logic
        #: Logic for checkbox
        def spell_slot_on_checkbox_active(checkbox, value):
            if value:
                CharacterData['Spell_Slots'][checkbox.used_key][0] = 1
                print(f'INFO DEBUG: The checkbox {checkbox} is active, value={value}, key={checkbox.used_key}, ' +
                      f'key_value={CharacterData["Spell_Slots"][checkbox.used_key]}')
            else:
                CharacterData['Spell_Slots'][checkbox.used_key][0] = 0
                print(f'INFO DEBUG: The checkbox {checkbox} is inactive, value={value}, key={checkbox.used_key}, ' +
                      f'key_value={CharacterData["Spell_Slots"][checkbox.used_key]}')

            save_character_data(character_json_file, CharacterData)

        self.Spell_Slots_1x1_checkbox.bind(active=spell_slot_on_checkbox_active)
        self.Spell_Slots_1x2_checkbox.bind(active=spell_slot_on_checkbox_active)
        self.Spell_Slots_1x3_checkbox.bind(active=spell_slot_on_checkbox_active)
        self.Spell_Slots_1x4_checkbox.bind(active=spell_slot_on_checkbox_active)
        self.Spell_Slots_2x1_checkbox.bind(active=spell_slot_on_checkbox_active)
        self.Spell_Slots_2x2_checkbox.bind(active=spell_slot_on_checkbox_active)
        self.Spell_Slots_2x3_checkbox.bind(active=spell_slot_on_checkbox_active)
        self.Spell_Slots_3x1_checkbox.bind(active=spell_slot_on_checkbox_active)
        self.Spell_Slots_3x2_checkbox.bind(active=spell_slot_on_checkbox_active)
        self.Spell_Slots_3x3_checkbox.bind(active=spell_slot_on_checkbox_active)
        self.Spell_Slots_4x1_checkbox.bind(active=spell_slot_on_checkbox_active)
        self.Spell_Slots_4x2_checkbox.bind(active=spell_slot_on_checkbox_active)
        self.Spell_Slots_4x3_checkbox.bind(active=spell_slot_on_checkbox_active)
        self.Spell_Slots_5x1_checkbox.bind(active=spell_slot_on_checkbox_active)
        self.Spell_Slots_5x2_checkbox.bind(active=spell_slot_on_checkbox_active)
        self.Spell_Slots_5x3_checkbox.bind(active=spell_slot_on_checkbox_active)
        self.Spell_Slots_6x1_checkbox.bind(active=spell_slot_on_checkbox_active)
        self.Spell_Slots_6x2_checkbox.bind(active=spell_slot_on_checkbox_active)
        self.Spell_Slots_7x1_checkbox.bind(active=spell_slot_on_checkbox_active)
        self.Spell_Slots_7x2_checkbox.bind(active=spell_slot_on_checkbox_active)
        self.Spell_Slots_8x1_checkbox.bind(active=spell_slot_on_checkbox_active)
        self.Spell_Slots_9x1_checkbox.bind(active=spell_slot_on_checkbox_active)

        ###############################
        #: Tag :  Other Proficiencies #
        ###############################
        first_row_size_y = 40
        self.Other_Proficiencies_label = MyFancyLabel(font_size=self.defaultFontSize,
                                                      text='OTHER  PROFICIENCIES',
                                                      size_x=minimum_width,
                                                      size_y=first_row_size_y,
                                                      pos_x=pos09[0],
                                                      pos_y=pos09[1],
                                                      show_border=True
                                                      )
        self.add_widget(self.Other_Proficiencies_label)

        remove_from_font_size_01 = 10
        second_row_size_y = 40

        self.Other_Proficiencies_info_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                           text=CharacterData["Other_Proficiencies"],
                                                           size_x=minimum_width,
                                                           size_y=second_row_size_y + 40,
                                                           pos_x=pos09[0],
                                                           pos_y=pos09[1] + second_row_size_y,
                                                           show_border=False
                                                           )
        self.add_widget(self.Other_Proficiencies_info_label)

        #######################
        #: Tag :  Race Traits #
        #######################
        first_row_size_y = 40
        self.Race_Traits_label = MyFancyLabel(font_size=self.defaultFontSize,
                                              text='RACE TRAITS',
                                              size_x=minimum_width,
                                              size_y=first_row_size_y,
                                              pos_x=pos10[0],
                                              pos_y=pos10[1],
                                              show_border=True
                                              )
        self.add_widget(self.Race_Traits_label)

        remove_from_font_size_01 = 10
        second_row_size_y = 40

        self.Race_Traits_info_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                   text=CharacterData["Race_Traits"],
                                                   size_x=minimum_width,
                                                   size_y=second_row_size_y + 90,
                                                   pos_x=pos10[0],
                                                   pos_y=pos10[1] + second_row_size_y,
                                                   show_border=False
                                                   )
        self.add_widget(self.Race_Traits_info_label)

        ###########################
        #: Tag :  Class Abilities #
        ###########################
        first_row_size_y = 40
        self.Class_Abilities_label = MyFancyLabel(font_size=self.defaultFontSize,
                                                  text='CLASS ABILITIES',
                                                  size_x=minimum_width,
                                                  size_y=first_row_size_y,
                                                  pos_x=pos11[0],
                                                  pos_y=pos11[1],
                                                  show_border=True
                                                  )
        self.add_widget(self.Class_Abilities_label)

        remove_from_font_size_01 = 10
        second_row_size_y = 40

        self.Class_Abilities_info_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                       text=CharacterData["Class_Abilities"],
                                                       size_x=minimum_width,
                                                       size_y=second_row_size_y + 150,
                                                       pos_x=pos11[0],
                                                       pos_y=pos11[1] + second_row_size_y,
                                                       show_border=False
                                                       )
        self.add_widget(self.Class_Abilities_info_label)

        my_key = 'STRENGTH_OF_THE_GRAVE'
        self.Class_Abilities_strofgrave_checkbox = MyFancyCheckBox(on_off=CharacterData['Class_Abilities2'][my_key][0],
                                                        size_x=second_row_size_y,
                                                        size_y=second_row_size_y,
                                                        pos_x=pos11[0],
                                                        pos_y=pos11[1] + second_row_size_y + 150,
                                                        disabled=False,
                                                        used_key=my_key,
                                                        overwrite_disable=CharacterData['Class_Abilities2'][my_key][1]
                                                        )
        self.add_widget(self.Class_Abilities_strofgrave_checkbox)

        #: Tag :  Class Abilities # Check Box Logic
        #: Logic for checkbox
        def class_features_on_checkbox_active(checkbox, value):
            if value:
                CharacterData['Class_Abilities2'][checkbox.used_key][0] = 1
                print(f'INFO DEBUG: The checkbox {checkbox} is active, value={value}, key={checkbox.used_key}, ' +
                      f'key_value={CharacterData["Class_Abilities2"][checkbox.used_key]}')
            else:
                CharacterData['Class_Abilities2'][checkbox.used_key][0] = 0
                print(f'INFO DEBUG: The checkbox {checkbox} is inactive, value={value}, key={checkbox.used_key}, ' +
                      f'key_value={CharacterData["Class_Abilities2"][checkbox.used_key]}')

            save_character_data(character_json_file, CharacterData)

        self.Class_Abilities_strofgrave_checkbox.bind(active=class_features_on_checkbox_active)

        #################
        #: Tag :  Feats #
        #################
        first_row_size_y = 40
        self.feats_label = MyFancyLabel(font_size=self.defaultFontSize,
                                        text='FEATS',
                                        size_x=minimum_width,
                                        size_y=first_row_size_y,
                                        pos_x=pos12[0],
                                        pos_y=pos12[1],
                                        show_border=True
                                        )
        self.add_widget(self.feats_label)

        remove_from_font_size_01 = 10
        second_row_size_y = 40

        self.feats_info_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                             text=CharacterData["Feats"],
                                             size_x=minimum_width,
                                             size_y=second_row_size_y,
                                             pos_x=pos12[0],
                                             pos_y=pos12[1] + second_row_size_y,
                                             show_border=False
                                             )
        self.add_widget(self.feats_info_label)

        ######################
        #: Tag :  Background #
        ######################
        first_row_size_y = 40
        self.background_label = MyFancyLabel(font_size=self.defaultFontSize,
                                             text='BACKGROUND FEATURE',
                                             size_x=minimum_width,
                                             size_y=first_row_size_y,
                                             pos_x=pos13[0],
                                             pos_y=pos13[1],
                                             show_border=True
                                             )
        self.add_widget(self.background_label)

        remove_from_font_size_01 = 10
        second_row_size_y = 40

        self.background_info_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                  text=CharacterData["Background"],
                                                  size_x=minimum_width,
                                                  size_y=second_row_size_y,
                                                  pos_x=pos13[0],
                                                  pos_y=pos13[1] + second_row_size_y + 20,
                                                  show_border=False
                                                  )
        self.add_widget(self.background_info_label)

        #####################
        #: Tag :  Metamagic #
        #####################
        first_row_size_y = 40
        self.metamagic_label = MyFancyLabel(font_size=self.defaultFontSize,
                                            text='METAMAGIC',
                                            size_x=minimum_width,
                                            size_y=first_row_size_y,
                                            pos_x=pos14[0],
                                            pos_y=pos14[1],
                                            show_border=True
                                            )
        self.add_widget(self.metamagic_label)

        remove_from_font_size_01 = 10
        second_row_size_y = 40

        self.metamagic_info_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                 text=CharacterData["Metamagic"],
                                                 size_x=minimum_width,
                                                 size_y=second_row_size_y,
                                                 pos_x=pos14[0],
                                                 pos_y=pos14[1] + second_row_size_y,
                                                 show_border=False
                                                 )
        self.add_widget(self.metamagic_info_label)

        #########################
        #: Tag :  Info Text Box #
        #########################
        first_row_size_x = 900
        first_row_size_y = 450

        remove_from_font_size_01 = 7

        #: scrollbar
        # self.scroll = ScrollView(bar_width=20,
        #                          size_hint=(None, None),
        #                          bar_pos_y='right',
        #                          do_scroll_y=True,
        #                          do_scroll_x=False,
        #                          pos=(0 + pos15[0], Window.size[1] - first_row_size_y - pos15[1]),
        #                          size=(first_row_size_x, first_row_size_y),
        #                          scroll_type=['bars', 'content'])
        # self.add_widget(self.scroll)

        #: TextInput
        self.info_input = MyFancyTextInput(font_size=self.defaultFontSize - remove_from_font_size_01,
                                           text=str(CharacterData['Info_Text']),
                                           size_x=first_row_size_x,
                                           size_y=first_row_size_y,
                                           pos_x=pos15[0],
                                           pos_y=pos15[1],
                                           disabled=True,
                                           override_multiline=True
                                           )
        self.add_widget(self.info_input)
        # self.scroll.add_widget(self.info_input)

        self.save_checkbox = MyFancyCheckBox(on_off=0,
                                             size_x=40,
                                             size_y=40,
                                             pos_x=pos15[0] + first_row_size_x + 10,
                                             pos_y=pos15[1],
                                             )
        self.add_widget(self.save_checkbox)

        #: Buttons for resets
        remove_from_font_size_01 = 5
        second_row_size_x = 130
        second_row_size_y = 60
        self.long_reset_button = MyFancyButton(font_size=self.defaultFontSize - remove_from_font_size_01,
                                               text='Long Rest',
                                               size_x=second_row_size_x,
                                               size_y=second_row_size_y,
                                               pos_x=pos15[0] + first_row_size_x + 10,
                                               pos_y=pos15[1] + 20 + second_row_size_y,
                                               disabled=True
                                               )
        self.add_widget(self.long_reset_button)

        self.short_reset_button = MyFancyButton(font_size=self.defaultFontSize - remove_from_font_size_01,
                                                text='Short Rest',
                                                size_x=second_row_size_x,
                                                size_y=second_row_size_y,
                                                pos_x=pos15[0] + first_row_size_x + 10,
                                                pos_y=pos15[1] + 40 + second_row_size_y * 2,
                                                disabled=True
                                                )
        self.add_widget(self.short_reset_button)

        #: Logic for checkbox
        def on_save_checkbox_active(checkbox, value):
            if value:
                print(f'INFO DEBUG: The checkbox {checkbox} is active, value {value}')
                self.info_input.disabled = False
                self.long_reset_button.disabled = False
                self.short_reset_button.disabled = False
            else:
                print(f'INFO DEBUG: The checkbox {checkbox} is inactive, value {value}')
                self.info_input.disabled = True
                self.long_reset_button.disabled = True
                self.short_reset_button.disabled = True
                CharacterData["Info_Text"] = self.info_input.text
                save_character_data(character_json_file, CharacterData)

        self.save_checkbox.bind(active=on_save_checkbox_active)

        #: Logic for Buttons
        def short_rest_button_action(instance):
            print(f'INFO DEBUG: Short Rest Button was pressed')

        self.short_reset_button.bind(on_press=short_rest_button_action)

        def long_rest_button_action(instance):
            print(f'INFO DEBUG: Long Rest Button was pressed')
            short_rest_button_action(instance)

        self.long_reset_button.bind(on_press=long_rest_button_action)

        ##################
        #: Tag :  Stats  #
        ##################
        first_row_size_y = 40

        self.stats_label = MyFancyLabel(font_size=self.defaultFontSize,
                                        text='STATS',
                                        size_x=minimum_width + 200,
                                        size_y=first_row_size_y,
                                        pos_x=pos16[0],
                                        pos_y=pos16[1],
                                        show_border=True
                                        )
        self.add_widget(self.stats_label)

        #: First row
        remove_from_font_size_01 = 5
        second_row_position_from_top = first_row_size_y + 0
        second_row_size_y = 40
        second_row_size_x = 100

        self.stat_str_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                           text='STR',
                                           size_x=second_row_size_x,
                                           size_y=second_row_size_y,
                                           pos_x=pos16[0],
                                           pos_y=pos16[1] + second_row_position_from_top,
                                           show_border=False
                                           )
        self.add_widget(self.stat_str_label)

        self.stat_dex_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                           text='DEX',
                                           size_x=second_row_size_x,
                                           size_y=second_row_size_y,
                                           pos_x=pos16[0] + second_row_size_x,
                                           pos_y=pos16[1] + second_row_position_from_top,
                                           show_border=False
                                           )
        self.add_widget(self.stat_dex_label)

        self.stat_con_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                           text='CON',
                                           size_x=second_row_size_x,
                                           size_y=second_row_size_y,
                                           pos_x=pos16[0] + second_row_size_x * 2,
                                           pos_y=pos16[1] + second_row_position_from_top,
                                           show_border=False
                                           )
        self.add_widget(self.stat_con_label)

        self.stat_int_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                           text='INT',
                                           size_x=second_row_size_x,
                                           size_y=second_row_size_y,
                                           pos_x=pos16[0] + second_row_size_x * 3,
                                           pos_y=pos16[1] + second_row_position_from_top,
                                           show_border=False
                                           )
        self.add_widget(self.stat_int_label)

        self.stat_wis_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                           text='WIS',
                                           size_x=100,
                                           size_y=second_row_size_y,
                                           pos_x=pos16[0] + second_row_size_x * 4,
                                           pos_y=pos16[1] + second_row_position_from_top,
                                           show_border=False
                                           )
        self.add_widget(self.stat_wis_label)

        self.stat_cha_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                           text='CHA',
                                           size_x=second_row_size_x,
                                           size_y=second_row_size_y,
                                           pos_x=pos16[0] + second_row_size_x * 5,
                                           pos_y=pos16[1] + second_row_position_from_top,
                                           show_border=False
                                           )
        self.add_widget(self.stat_cha_label)

        #: Second row 2.1
        second_row_position_from_top = second_row_position_from_top + second_row_size_y + 0
        second_row_size_y = 40
        second_row_size_x = 100

        self.stat_str_as_label = MyFancyLabel(font_size=self.defaultFontSize,
                                              text=str(CharacterData['Ability_Score_Modifiers']['STR']),
                                              size_x=second_row_size_x - 40,
                                              size_y=second_row_size_y,
                                              pos_x=pos16[0],
                                              pos_y=pos16[1] + second_row_position_from_top,
                                              show_border=False
                                              )
        self.add_widget(self.stat_str_as_label)

        self.stat_dex_as_label = MyFancyLabel(font_size=self.defaultFontSize,
                                              text=str(CharacterData['Ability_Score_Modifiers']['DEX']),
                                              size_x=second_row_size_x - 40,
                                              size_y=second_row_size_y,
                                              pos_x=pos16[0] + second_row_size_x,
                                              pos_y=pos16[1] + second_row_position_from_top,
                                              show_border=False
                                              )
        self.add_widget(self.stat_dex_as_label)

        self.stat_con_as_label = MyFancyLabel(font_size=self.defaultFontSize,
                                              text=str(CharacterData['Ability_Score_Modifiers']['CON']),
                                              size_x=second_row_size_x - 40,
                                              size_y=second_row_size_y,
                                              pos_x=pos16[0] + second_row_size_x * 2,
                                              pos_y=pos16[1] + second_row_position_from_top,
                                              show_border=False
                                              )
        self.add_widget(self.stat_con_as_label)

        self.stat_int_as_label = MyFancyLabel(font_size=self.defaultFontSize,
                                              text=str(CharacterData['Ability_Score_Modifiers']['INT']),
                                              size_x=second_row_size_x - 40,
                                              size_y=second_row_size_y,
                                              pos_x=pos16[0] + second_row_size_x * 3,
                                              pos_y=pos16[1] + second_row_position_from_top,
                                              show_border=False
                                              )
        self.add_widget(self.stat_int_as_label)

        self.stat_wis_as_label = MyFancyLabel(font_size=self.defaultFontSize,
                                              text=str(CharacterData['Ability_Score_Modifiers']['WIS']),
                                              size_x=second_row_size_x - 40,
                                              size_y=second_row_size_y,
                                              pos_x=pos16[0] + second_row_size_x * 4,
                                              pos_y=pos16[1] + second_row_position_from_top,
                                              show_border=False
                                              )
        self.add_widget(self.stat_wis_as_label)

        self.stat_cha_as_label = MyFancyLabel(font_size=self.defaultFontSize,
                                              text=str(CharacterData['Ability_Score_Modifiers']['CHA']),
                                              size_x=second_row_size_x - 40,
                                              size_y=second_row_size_y,
                                              pos_x=pos16[0] + second_row_size_x * 5,
                                              pos_y=pos16[1] + second_row_position_from_top,
                                              show_border=False
                                              )
        self.add_widget(self.stat_cha_as_label)

        #: Second row 2.2
        remove_from_font_size_01 = 10
        second_row_position_from_top = second_row_position_from_top + 0
        second_row_size_y = 40
        second_row_size_x = 100

        self.stat_str_bb_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                              text=str(CharacterData['Final_Ability_Scores']['STR']),
                                              size_x=second_row_size_x - 60,
                                              size_y=second_row_size_y,
                                              pos_x=pos16[0] + 60,
                                              pos_y=pos16[1] + second_row_position_from_top,
                                              show_border=True
                                              )
        self.add_widget(self.stat_str_bb_label)

        self.stat_dex_bb_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                              text=str(CharacterData['Final_Ability_Scores']['DEX']),
                                              size_x=second_row_size_x - 60,
                                              size_y=second_row_size_y,
                                              pos_x=pos16[0] + 60 + second_row_size_x,
                                              pos_y=pos16[1] + second_row_position_from_top,
                                              show_border=True
                                              )
        self.add_widget(self.stat_dex_bb_label)

        self.stat_con_bb_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                              text=str(CharacterData['Final_Ability_Scores']['CON']),
                                              size_x=second_row_size_x - 60,
                                              size_y=second_row_size_y,
                                              pos_x=pos16[0] + 60 + second_row_size_x * 2,
                                              pos_y=pos16[1] + second_row_position_from_top,
                                              show_border=True
                                              )
        self.add_widget(self.stat_con_bb_label)

        self.stat_int_bb_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                              text=str(CharacterData['Final_Ability_Scores']['INT']),
                                              size_x=second_row_size_x - 60,
                                              size_y=second_row_size_y,
                                              pos_x=pos16[0] + 60 + second_row_size_x * 3,
                                              pos_y=pos16[1] + second_row_position_from_top,
                                              show_border=True
                                              )
        self.add_widget(self.stat_int_bb_label)

        self.stat_wis_bb_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                              text=str(CharacterData['Final_Ability_Scores']['WIS']),
                                              size_x=second_row_size_x - 60,
                                              size_y=second_row_size_y,
                                              pos_x=pos16[0] + 60 + second_row_size_x * 4,
                                              pos_y=pos16[1] + second_row_position_from_top,
                                              show_border=True
                                              )
        self.add_widget(self.stat_wis_bb_label)

        self.stat_cha_bb_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                              text=str(CharacterData['Final_Ability_Scores']['CHA']),
                                              size_x=second_row_size_x - 60,
                                              size_y=second_row_size_y,
                                              pos_x=pos16[0] + 60 + second_row_size_x * 5,
                                              pos_y=pos16[1] + second_row_position_from_top,
                                              show_border=True
                                              )
        self.add_widget(self.stat_cha_bb_label)

        ###########################################################
        #: Tag :  Proficiency_Bonus + Passives + initiative + ACs #
        ###########################################################
        #: ToDo : add bonus to AC
        first_row_size_y = 40

        self.ac_label = MyFancyLabel(font_size=self.defaultFontSize,
                                     text='Proficiency_Bonus; Passives; initiative; ACs',
                                     size_x=minimum_width + 200,
                                     size_y=first_row_size_y,
                                     pos_x=pos17[0],
                                     pos_y=pos17[1],
                                     show_border=True
                                     )
        self.add_widget(self.ac_label)

        #: second row
        remove_from_font_size_01 = 5
        second_row_position_from_top = first_row_size_y + 0
        second_row_size_y = 30
        second_row_size_x = 300

        self.pr_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                     text='Proficiency:  ' + str(CharacterData['Proficiency_Bonus']),
                                     size_x=second_row_size_x,
                                     size_y=second_row_size_y,
                                     pos_x=pos17[0],
                                     pos_y=pos17[1] + second_row_position_from_top,
                                     show_border=False
                                     )
        self.add_widget(self.pr_label)

        self.in_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                     text='Initiative:  ' + str(CharacterData['initiative_Bonus'] + CharacterData['Ability_Score_Modifiers']['DEX']),
                                     size_x=second_row_size_x,
                                     size_y=second_row_size_y,
                                     pos_x=pos17[0] + second_row_size_x,
                                     pos_y=pos17[1] + second_row_position_from_top,
                                     show_border=False
                                     )
        self.add_widget(self.in_label)

        #: Third row
        second_row_position_from_top = second_row_position_from_top + second_row_size_y + 0

        self.ac_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                     text='AC (No Armor):  ' + str(CharacterData['AC_NoArmor']) + ' + ' + str(CharacterData['AC_Shield']),
                                     size_x=second_row_size_x,
                                     size_y=second_row_size_y,
                                     pos_x=pos17[0],
                                     pos_y=pos17[1] + second_row_position_from_top,
                                     show_border=False
                                     )
        self.add_widget(self.ac_label)

        self.mac_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                      text='AC (Mage Armor):  ' + str(CharacterData['AC_MageArmor']) + ' + ' + str(CharacterData['AC_Shield']),
                                      size_x=second_row_size_x,
                                      size_y=second_row_size_y,
                                      pos_x=pos17[0] + second_row_size_x,
                                      pos_y=pos17[1] + second_row_position_from_top,
                                      show_border=False
                                      )
        self.add_widget(self.mac_label)

        #: Fourth row
        second_row_position_from_top = second_row_position_from_top + second_row_size_y + 0

        self.ac_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                     text='Passive Perception:  ' + str(10 + CharacterData['Passive_Perception_bonus'] + CharacterData['Skills']['Perception'][2]),
                                     size_x=second_row_size_x,
                                     size_y=second_row_size_y,
                                     pos_x=pos17[0],
                                     pos_y=pos17[1] + second_row_position_from_top,
                                     show_border=False
                                     )
        self.add_widget(self.ac_label)

        ######################
        #: Tag :  Attunement #
        ######################
        first_row_size_y = 40

        self.attune_label = MyFancyLabel(font_size=self.defaultFontSize,
                                         text='ATTUNMENTS',
                                         size_x=minimum_width + 200,
                                         size_y=first_row_size_y,
                                         pos_x=pos18[0],
                                         pos_y=pos18[1],
                                         show_border=True
                                         )
        self.add_widget(self.attune_label)

        #: Second Row
        remove_from_font_size_01 = 5
        second_row_position_from_top = first_row_size_y + 0
        second_row_size_y = 40

        self.attune_1_checkbox = MyFancyCheckBox(on_off=CharacterData['Attunments']['Ax1'][0],
                                                 size_x=second_row_size_y,
                                                 size_y=second_row_size_y,
                                                 pos_x=pos18[0] + second_row_size_y,
                                                 pos_y=pos18[1] + second_row_position_from_top,
                                                 disabled=False,
                                                 used_key='Ax1'
                                                 )
        self.add_widget(self.attune_1_checkbox)

        second_row_size_x = 150
        self.attune_1_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                           text=CharacterData['Attunments']['Ax1'][1],
                                           size_x=second_row_size_x,
                                           size_y=second_row_size_y,
                                           pos_x=pos18[0] + second_row_size_y*2,
                                           pos_y=pos18[1] + second_row_position_from_top,
                                           show_border=False
                                           )
        self.add_widget(self.attune_1_label)

        #: Third Row
        second_row_position_from_top = second_row_position_from_top + first_row_size_y + 0
        second_row_size_y = 40

        self.attune_2_checkbox = MyFancyCheckBox(on_off=CharacterData['Attunments']['Ax2'][0],
                                                 size_x=second_row_size_y,
                                                 size_y=second_row_size_y,
                                                 pos_x=pos18[0] + second_row_size_y,
                                                 pos_y=pos18[1] + second_row_position_from_top,
                                                 disabled=False,
                                                 used_key='Ax2'
                                                 )
        self.add_widget(self.attune_2_checkbox)

        second_row_size_x = 150
        self.attune_2_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                           text=CharacterData['Attunments']['Ax2'][1],
                                           size_x=second_row_size_x,
                                           size_y=second_row_size_y,
                                           pos_x=pos18[0] + second_row_size_y * 2,
                                           pos_y=pos18[1] + second_row_position_from_top,
                                           show_border=False
                                           )
        self.add_widget(self.attune_2_label)

        #: Fourth Row
        second_row_position_from_top = second_row_position_from_top + first_row_size_y + 0
        second_row_size_y = 40

        self.attune_3_checkbox = MyFancyCheckBox(on_off=CharacterData['Attunments']['Ax3'][0],
                                                 size_x=second_row_size_y,
                                                 size_y=second_row_size_y,
                                                 pos_x=pos18[0] + second_row_size_y,
                                                 pos_y=pos18[1] + second_row_position_from_top,
                                                 disabled=False,
                                                 used_key='Ax3'
                                                 )
        self.add_widget(self.attune_3_checkbox)

        second_row_size_x = 150
        self.attune_3_label = MyFancyLabel(font_size=self.defaultFontSize - remove_from_font_size_01,
                                           text=CharacterData['Attunments']['Ax3'][1],
                                           size_x=second_row_size_x,
                                           size_y=second_row_size_y,
                                           pos_x=pos18[0] + second_row_size_y * 2,
                                           pos_y=pos18[1] + second_row_position_from_top,
                                           show_border=False
                                           )
        self.add_widget(self.attune_3_label)

        def attune_on_checkbox_active(checkbox, value):
            if value:
                CharacterData['Attunments'][checkbox.used_key][0] = 1
                print(f'INFO DEBUG: The checkbox {checkbox} is active, value={value}, key={checkbox.used_key}, ' +
                      f'key_value={CharacterData["Attunments"][checkbox.used_key][0]}')
            else:
                CharacterData['Attunments'][checkbox.used_key][0] = 0
                print(f'INFO DEBUG: The checkbox {checkbox} is inactive, value={value}, key={checkbox.used_key}, ' +
                      f'key_value={CharacterData["Attunments"][checkbox.used_key][0]}')

            save_character_data(character_json_file, CharacterData)

        self.attune_1_checkbox.bind(active=attune_on_checkbox_active)
        self.attune_2_checkbox.bind(active=attune_on_checkbox_active)
        self.attune_3_checkbox.bind(active=attune_on_checkbox_active)

        #################
        #: Tag :  Melee #
        #################


#: ----------------------------------------------- METHODS -----------------------------------------------
#: Tag_def : calculate_ability_score
def calculate_ability_score(int_):
    if int_ >= 10:
        out_ = (int_ - 10) // 2
    else:
        if ((10 - int_) % 2) != 0:
            out_ = (((10 - int_) // 2) * -1) - 1
        else:
            out_ = (((10 - int_) // 2) * -1)

    return out_


#: Tag_def : calculate_current_hp
def calculate_current_hp(list_):
    global CurrentHP
    CurrentHP = list_[0] + list_[1] + list_[2]


#: Tag_def : calculate_proficiency_bonus
def calculate_proficiency_bonus(int_):
    out_ = ((int_ - 1) // 4) + 2
    return out_


#: Tag_def : load_character_data
def load_character_data(name_):
    with open(name_, 'r') as file:
        out_ = json.load(file)

    file.close()
    return out_


#: Tag_def : save_character_data
def save_character_data(name_, json_):
    with open(name_, 'w') as file:
        json.dump(json_, file, indent=4)

    file.close()


#: ----------------------------------------------- BODY --------------------------------------------------
if __name__ == '__main__':
    CharacterData = load_character_data(character_json_file)

    #: Tag : recalculate HP
    try:
        for hp_type in CharacterData['HP'].keys():
            if not isinstance(CharacterData['HP'][hp_type], int):
                raise ValueError
    except ValueError as e:
        print('ERROR: JSON - "HP" was not integer -> example {"HP": {"MAX": 20}')
        exit(1)

    calculate_current_hp([CharacterData['HP']['MAX'], CharacterData['HP']['BONUS'], CharacterData['HP']['TMP']])

    #: Tag : recalculate "proficiency bonus"
    try:
        if isinstance(CharacterData['Character_Level'], int):
            CharacterData['Proficiency_Bonus'] = calculate_proficiency_bonus(CharacterData['Character_Level'])
            save_character_data(character_json_file, CharacterData)
        else:
            raise ValueError
    except ValueError as e:
        print('ERROR: JSON - "Character_Level" was not integer -> example {"Character_Level": 4}')
        exit(1)

    #: Tag : recalculate "Final Ability Scores"
    try:
        for AS_name in CharacterData['Basic_Ability_Scores'].keys():
            if isinstance(CharacterData['Basic_Ability_Scores'][AS_name], int) and isinstance(CharacterData['Race_Ability_Score_Bonus'][AS_name], int) and isinstance(CharacterData['Ability_Score_Improvement'][AS_name], int):
                CharacterData['Final_Ability_Scores'][AS_name] = CharacterData['Basic_Ability_Scores'][AS_name] + CharacterData['Race_Ability_Score_Bonus'][AS_name] + CharacterData['Ability_Score_Improvement'][AS_name]
                save_character_data(character_json_file, CharacterData)
            else:
                raise ValueError
    except ValueError as e:
        print('ERROR: JSON - "Basic_Ability_Scores" or "Race_Ability_Score_Bonus" or "Ability_Score_Improvement" ' +
              'was not integer -> example {"Basic_Ability_Scores": 10}')
        exit(1)

    #: Tag : recalculate "Ability Scores Modifiers"
    try:
        for AS_name in CharacterData['Ability_Score_Modifiers'].keys():
            if isinstance(CharacterData['Ability_Score_Modifiers_additional_Bonus'][AS_name], int):
                CharacterData['Ability_Score_Modifiers'][AS_name] = CharacterData['Ability_Score_Modifiers_additional_Bonus'][AS_name] + calculate_ability_score(CharacterData['Final_Ability_Scores'][AS_name])
                save_character_data(character_json_file, CharacterData)
            else:
                raise ValueError
    except ValueError as e:
        print('ERROR: JSON - "Ability_Score_Modifiers_additional_Bonus" was not integer -> ' +
              'example {"Ability_Score_Modifiers_additional_Bonus": 0}')
        exit(1)

    #: Tag : recalculate "Spell_Save_DC" and "Spell_Attack_Bonus"
    for index in range(0, len(CharacterData['Spellcasting_Ability'])):
        if len(CharacterData['Spell_Save_DC']) < len(CharacterData['Spellcasting_Ability']):
            CharacterData['Spell_Save_DC'].append(0)
        CharacterData['Spell_Save_DC'][index] = 8 + CharacterData['Proficiency_Bonus'] + CharacterData['Ability_Score_Modifiers'][CharacterData['Spellcasting_Ability'][index]]

        if len(CharacterData['Spell_Attack_Bonus']) < len(CharacterData['Spellcasting_Ability']):
            CharacterData['Spell_Attack_Bonus'].append(0)
        CharacterData['Spell_Attack_Bonus'][index] = CharacterData['Proficiency_Bonus'] + CharacterData['Ability_Score_Modifiers'][CharacterData['Spellcasting_Ability'][index]]

        save_character_data(character_json_file, CharacterData)

    #: Tag : recalculate "Saving Throws"
    try:
        for AS_name in CharacterData['Saving_Throws'].keys():
            if isinstance(CharacterData['Saving_Throws'][AS_name][0], int):
                CharacterData['Saving_Throws'][AS_name][1] = CharacterData['Ability_Score_Modifiers'][AS_name] + (CharacterData['Proficiency_Bonus'] * CharacterData['Saving_Throws'][AS_name][0]) + CharacterData['Saving_Throws'][AS_name][2]
                save_character_data(character_json_file, CharacterData)
    except ValueError as e:
        print('ERROR: JSON - "Saving_Throws" was not integer -> ' +
              'example {"Saving_Throws": {"STR": [0, 0]}}')
        exit(1)

    #: Tag : recalculate "Skills"
    try:
        for skill in CharacterData['Skills'].keys():
            if isinstance(CharacterData['Skills'][skill][0], int):
                CharacterData['Skills'][skill][2] = CharacterData['Ability_Score_Modifiers'][CharacterData['Skills'][skill][1]] + (CharacterData['Proficiency_Bonus'] * CharacterData['Skills'][skill][0]) + CharacterData['Skills'][skill][3]
                save_character_data(character_json_file, CharacterData)
    except ValueError as e:
        print('ERROR: JSON - "Saving_Throws" was not integer -> ' +
              'example {"Skills": {"Acrobatics": [0, DEX, 0]}}')
        exit(1)

    #: Tag : test print
    print(CharacterData)

    #: Tag : Run APP

    Config.set('graphics', 'fullscreen', 'auto')
    Config.write()
    Window.fullscreen = 'auto'
    MyGui().run()
