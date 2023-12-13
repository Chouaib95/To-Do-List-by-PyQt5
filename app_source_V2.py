# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from pathlib import Path
import sys, json
from datetime import datetime, timedelta
import re

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.path_0 = (Path(__file__).parent.resolve()) / "my_to_do_list.json"
        self.start_time = datetime.now()
        self.add_item_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.add_item_pushButton.setGeometry(QtCore.QRect(40, 60, 211, 51))
        font = QtGui.QFont()
        font.setFamily("Chiller")
        font.setPointSize(16)
        self.add_item_pushButton.setFont(font)
        self.add_item_pushButton.setObjectName("add_item_pushButton")
        self.delete_item_pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.delete_item_pushButton_2.setGeometry(QtCore.QRect(270, 60, 231, 51))
        font = QtGui.QFont()
        font.setFamily("Chiller")
        font.setPointSize(16)
        self.delete_item_pushButton_2.setFont(font)
        self.delete_item_pushButton_2.setObjectName("delete_item_pushButton_2")
        self.clear_list_pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.clear_list_pushButton_3.setGeometry(QtCore.QRect(520, 60, 231, 51))
        font = QtGui.QFont()
        font.setFamily("Chiller")
        font.setPointSize(16)
        self.clear_list_pushButton_3.setFont(font)
        self.clear_list_pushButton_3.setObjectName("clear_list_pushButton_3")
        self.my_list_listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.my_list_listWidget.setGeometry(QtCore.QRect(40, 131, 711, 411))
        font = QtGui.QFont()
        font.setFamily("Chiller")
        font.setPointSize(16)
        self.my_list_listWidget.setFont(font)
        self.my_list_listWidget.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.my_list_listWidget.setObjectName("my_list_listWidget")
        self.zone_text_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.zone_text_lineEdit.setGeometry(QtCore.QRect(40, 10, 481, 41))
        font = QtGui.QFont()
        font.setFamily("Chiller")
        font.setPointSize(14)
        self.zone_text_lineEdit.setFont(font)
        self.zone_text_lineEdit.setObjectName("zone_text_lineEdit")
        self.duration_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.duration_lineEdit.setGeometry(QtCore.QRect(680, 10, 71, 41))
        font = QtGui.QFont()
        font.setFamily("Chiller")
        font.setPointSize(14)
        self.duration_lineEdit.setFont(font)
        self.duration_lineEdit.setObjectName("duration_lineEdit")
        self.duration_label = QtWidgets.QLabel(self.centralwidget)
        self.duration_label.setGeometry(QtCore.QRect(550, 10, 121, 41))
        font = QtGui.QFont()
        font.setFamily("Chiller")
        font.setPointSize(14)
        self.duration_label.setFont(font)
        self.duration_label.setObjectName("duration_label")

        # Modifier le type d'entrée pour accepter des nombres flottants
        # self.duration_lineEdit.setInputMask("999.99")


        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.set_connections()
        # Ajouter ces lignes pour configurer la mise en page
        
        self.style()
        self.animations()
        self.load_from_json()
        self.duration_lineEdit.setText("")

        # Ajoutez ces lignes pour configurer la minuterie
        self.auto_save_timer = QtCore.QTimer(MainWindow)
        self.auto_save_timer.timeout.connect(self.auto_save)
        self.auto_save_timer.start(700)  # Enregistre chaque 900 milliseconde
        

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "To Do List"))
        self.add_item_pushButton.setText(_translate("MainWindow", "Add item to the list"))
        self.delete_item_pushButton_2.setText(_translate("MainWindow", "Delete item from the list"))
        self.clear_list_pushButton_3.setText(_translate("MainWindow", "Clear the list"))
        self.duration_label.setText(_translate("MainWindow", "Duration (days)"))

    def extract_substring_until_tab_regex(self,input_string):
        match = re.search(r'^([^\t]*)', input_string)
        if match:
            return match.group(1)
        else:
            return ""

    def save_to_json(self):
        items = [
            {
                "text": self.extract_substring_until_tab_regex(self.my_list_listWidget.item(i).text()),
                "checked": self.my_list_listWidget.item(i).checkState() == QtCore.Qt.Checked,
                "duration": self.my_list_listWidget.item(i).data(QtCore.Qt.UserRole + 1),
                "start_time": self.my_list_listWidget.item(i).data(QtCore.Qt.UserRole)
            }
            for i in range(self.my_list_listWidget.count())
        ]
        with open(self.path_0, "w") as json_file:
            json.dump(items, json_file, indent=4, ensure_ascii=True)

    def auto_save(self):
        self.save_to_json()
        self.load_from_json()
    
    def time_difference_to_string(self, difference:datetime)->str:
        days, seconds = difference.days, difference.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        return f"{days} d - {hours} h - {minutes} min - {seconds} s"
    

    def load_from_json(self):
        try:
            with open(self.path_0, "r") as json_file:
                items = json.load(json_file)
                #print("Loaded items from JSON:", items)

                # Effacer tous les éléments de la liste avant d'ajouter les nouveaux
                self.my_list_listWidget.clear()

                for item in items:
                    list_item = QtWidgets.QListWidgetItem("")
                    list_item.setFlags(list_item.flags() | QtCore.Qt.ItemIsUserCheckable)
                    list_item.setCheckState(
                        QtCore.Qt.Checked if item.get('checked') else QtCore.Qt.Unchecked
                    )

                    # Ajouter la date et l'heure de début
                    list_item.setData(QtCore.Qt.UserRole, item.get('start_time', self.start_time.isoformat()))

                    # Ajouter la durée
                    list_item.setData(QtCore.Qt.UserRole + 1, float(item.get('duration', 0)))

                    # Calculer le temps restant
                    remaining_time = datetime.fromisoformat(item.get('start_time', self.start_time.isoformat())) + timedelta(days=float(item.get('duration', 0))) - datetime.now()

                    # Afficher le temps restant dans la liste
                    remaining_time_str = self.time_difference_to_string(remaining_time)
                    text_to_treat = item.get('text', '')
                    list_item.setText(f"{self.extract_substring_until_tab_regex(text_to_treat)}\t-\tRemaining Time: {remaining_time_str}")

                    self.my_list_listWidget.addItem(list_item)

                #print("Items added to the list widget.")
                #MainWindow.show()#au cas où la fenetre ne s'ouvre pas

        except FileNotFoundError:
            print("File not found:", self.path_0)
        except Exception as e:
            print("Error loading from JSON:", type(e), str(e))

    def add_item(self):
        contenu = self.zone_text_lineEdit.text()
        duration_days = self.duration_lineEdit.text().strip()
        list_item = QtWidgets.QListWidgetItem(contenu)
        list_item.setFlags(list_item.flags() | QtCore.Qt.ItemIsUserCheckable)
        list_item.setCheckState(QtCore.Qt.Unchecked)

        # Ajouter la date et l'heure de début
        list_item.setData(QtCore.Qt.UserRole, self.start_time.isoformat())

        # Ajouter la durée
        list_item.setData(QtCore.Qt.UserRole + 1, float(duration_days))
        
        # Calculer le temps restant
        remaining_time = self.start_time + timedelta(days=float(duration_days)) - datetime.now()

        # Afficher le temps restant dans la liste
        remaining_time_str = self.time_difference_to_string(remaining_time)
        
        # Afficher le temps restant dans la liste
        list_item.setText(f"{contenu}\t-\tRemaining Time: {remaining_time_str}")

        self.my_list_listWidget.addItem(list_item)
        self.zone_text_lineEdit.setText("")
        self.duration_lineEdit.setText("")
        self.animation.start()
        self.save_to_json()

    def delete_item(self):
        row = self.my_list_listWidget.currentRow()
        if row != -1:
            self.my_list_listWidget.takeItem(row)
            self.save_to_json()

    def clear_list(self):
        self.my_list_listWidget.clear()
        self.save_to_json()

    def set_connections(self):
        self.add_item_pushButton.clicked.connect(self.add_item)
        self.delete_item_pushButton_2.clicked.connect(self.delete_item)
        self.clear_list_pushButton_3.clicked.connect(self.clear_list)

     # Ajout de styles sophistiqués
    def style(self):
        self.add_item_pushButton.setStyleSheet("QPushButton {"
                                               "background-color: #4CAF50;"
                                               "color: white;"
                                               "border: 2px solid #4CAF50;"
                                               "border-radius: 5px;"
                                               "padding: 5px 10px;"
                                               "font-size: 26px;"
                                               "}"
                                               "QPushButton:hover {"
                                               "background-color: #45a049;"
                                               "}")

        self.delete_item_pushButton_2.setStyleSheet("QPushButton {"
                                                    "background-color: #f44336;"
                                                    "color: white;"
                                                    "border: 2px solid #f44336;"
                                                    "border-radius: 5px;"
                                                    "padding: 5px 10px;"
                                                    "font-size: 26px;"
                                                    "}"
                                                    "QPushButton:hover {"
                                                    "background-color: #d32f2f;"
                                                    "}")

        self.clear_list_pushButton_3.setStyleSheet("QPushButton {"
                                                   "background-color: #008CBA;"
                                                   "color: white;"
                                                   "border: 2px solid #008CBA;"
                                                   "border-radius: 5px;"
                                                   "padding: 5px 10px;"
                                                   "font-size: 26px;"
                                                   "}"
                                                   "QPushButton:hover {"
                                                   "background-color: #0077A8;"
                                                   "}")
        self.duration_label.setStyleSheet("QLabel {"
                                  "font-family: 'Chiller';"
                                  "font-size: 22px;"
                                  "color: #333;"
                                  "border: 2px dashed #FFA07A;"  # Couleur saumon en pointillé
                                  "border-radius: 5px;"
                                  "padding: 5px;"
                                  "background-color: #FFDAB9;"  # Couleur de fond saumon
                                  "}")

    def animations(self):
        # Ajout d'animations
        self.animation = QtCore.QPropertyAnimation(self.add_item_pushButton, b"geometry")
        self.animation.setDuration(500)
        self.animation.setStartValue(QtCore.QRect(40, 60, 211, 51))
        self.animation.setEndValue(QtCore.QRect(40, 60, 250, 51))
        self.animation.setEasingCurve(QtCore.QEasingCurve.OutBounce)

        #img_path = str(Path(r"C:\Users\choua\Desktop\Projet To_do_list\pics\img1.jpg"))
        img_path = (Path(__file__).parent.resolve()) / "pics" / "img1.jpg"
        pixmap = QtGui.QPixmap(str(img_path))

        # Définir l'arrière-plan avec l'image chargée
        palette = QtGui.QPalette()
        palette.setBrush(QtGui.QPalette.Window, QtGui.QBrush(pixmap))
        MainWindow.setPalette(palette)

        # Ajout d'un QGraphicsOpacityEffect pour le fond
        self.background_effect = QtWidgets.QGraphicsOpacityEffect()
        self.centralwidget.setGraphicsEffect(self.background_effect)

        # Animation pour le fond
        self.background_animation = QtCore.QPropertyAnimation(self.background_effect, b"opacity")
        self.background_animation.setDuration(1000)
        self.background_animation.setStartValue(0.0)
        self.background_animation.setEndValue(1.0)
        self.background_animation.setEasingCurve(QtCore.QEasingCurve.OutQuad)
        self.background_animation.start()

        # Rendre l'arrière-plan de la fenêtre principale légèrement transparent
        MainWindow.setWindowOpacity(0.95)  # Ajustez la valeur selon vos besoins (0.0 à 1.0)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())