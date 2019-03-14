# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ask_new_product.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AskNewProduct(object):
    def setupUi(self, AskNewProduct):
        AskNewProduct.setObjectName("AskNewProduct")
        AskNewProduct.resize(360, 100)
        AskNewProduct.setSizeGripEnabled(False)
        self.btn_cancel = QtWidgets.QPushButton(AskNewProduct)
        self.btn_cancel.setGeometry(QtCore.QRect(20, 30, 150, 40))
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(20)
        self.btn_cancel.setFont(font)
        self.btn_cancel.setObjectName("btn_cancel")
        self.btn_new = QtWidgets.QPushButton(AskNewProduct)
        self.btn_new.setGeometry(QtCore.QRect(190, 30, 150, 40))
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(20)
        self.btn_new.setFont(font)
        self.btn_new.setDefault(True)
        self.btn_new.setObjectName("btn_new")

        self.retranslateUi(AskNewProduct)
        QtCore.QMetaObject.connectSlotsByName(AskNewProduct)

    def retranslateUi(self, AskNewProduct):
        _translate = QtCore.QCoreApplication.translate
        AskNewProduct.setWindowTitle(_translate("AskNewProduct", "Dialog"))
        self.btn_cancel.setText(_translate("AskNewProduct", "取消"))
        self.btn_new.setText(_translate("AskNewProduct", "新增商品"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    AskNewProduct = QtWidgets.QDialog()
    ui = Ui_AskNewProduct()
    ui.setupUi(AskNewProduct)
    AskNewProduct.show()
    sys.exit(app.exec_())
