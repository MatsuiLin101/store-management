# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'message.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Message(object):
    def setupUi(self, Message):
        Message.setObjectName("Message")
        Message.resize(600, 125)
        self.btn_confirm = QtWidgets.QPushButton(Message)
        self.btn_confirm.setGeometry(QtCore.QRect(250, 60, 100, 40))
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(20)
        self.btn_confirm.setFont(font)
        self.btn_confirm.setDefault(True)
        self.btn_confirm.setObjectName("btn_confirm")
        self.message = QtWidgets.QLabel(Message)
        self.message.setGeometry(QtCore.QRect(25, 10, 550, 40))
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(20)
        self.message.setFont(font)
        self.message.setAlignment(QtCore.Qt.AlignCenter)
        self.message.setObjectName("message")

        self.retranslateUi(Message)
        QtCore.QMetaObject.connectSlotsByName(Message)

    def retranslateUi(self, Message):
        _translate = QtCore.QCoreApplication.translate
        Message.setWindowTitle(_translate("Message", "Dialog"))
        self.btn_confirm.setText(_translate("Message", "確認"))
        self.message.setText(_translate("Message", "產生10頁價格牌，總共999樣商品。"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Message = QtWidgets.QDialog()
    ui = Ui_Message()
    ui.setupUi(Message)
    Message.show()
    sys.exit(app.exec_())
