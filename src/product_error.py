# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'product_error.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Error(object):
    def setupUi(self, Error):
        Error.setObjectName("Error")
        Error.resize(600, 300)
        self.message = QtWidgets.QLabel(Error)
        self.message.setGeometry(QtCore.QRect(0, 90, 600, 130))
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(20)
        self.message.setFont(font)
        self.message.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.message.setMidLineWidth(0)
        self.message.setText("")
        self.message.setAlignment(QtCore.Qt.AlignCenter)
        self.message.setObjectName("message")
        self.btn_confirm = QtWidgets.QPushButton(Error)
        self.btn_confirm.setGeometry(QtCore.QRect(225, 235, 150, 40))
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(20)
        self.btn_confirm.setFont(font)
        self.btn_confirm.setDefault(True)
        self.btn_confirm.setObjectName("btn_confirm")
        self.label = QtWidgets.QLabel(Error)
        self.label.setGeometry(QtCore.QRect(0, 30, 600, 40))
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")

        self.retranslateUi(Error)
        QtCore.QMetaObject.connectSlotsByName(Error)

    def retranslateUi(self, Error):
        _translate = QtCore.QCoreApplication.translate
        Error.setWindowTitle(_translate("Error", "Dialog"))
        self.btn_confirm.setText(_translate("Error", "確認"))
        self.label.setText(_translate("Error", "商品輸入錯誤"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Error = QtWidgets.QDialog()
    ui = Ui_Error()
    ui.setupUi(Error)
    Error.show()
    sys.exit(app.exec_())
