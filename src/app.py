import sys
import barcode
import pickle
import os
from decimal import *
from PyQt5 import QtWidgets, QtCore
from product_manager import Ui_MainWindow
from product_card import Ui_MainWindow as Ui_CardWindow
from product_card_in_list import Ui_MainWindow as Ui_CardInListWindow
from product_error import Ui_Error
from ask_new_product import Ui_AskNewProduct
from add_new_product import Ui_AddNewProduct
from edit_product import Ui_EditProduct
from message import Ui_Message
from card import ProductCard


def func_check_code(code):
    try:
        int(code)
    except:
        return (False, '輸入錯誤，請重新輸入13位數字條碼。\n')

    if len(code) > 13:
        return (False, '條碼超過長度，請重新輸入13位數字條碼。\n')

    EAN = barcode.get_barcode_class('ean13')
    ean = EAN(code)
    if str(ean) != code:
        return (False, f"{code} 編碼錯誤，請將編碼修正為 {ean}。\n")

    return (True, str(ean))


def func_open_product():
    with open('products.pkl', 'rb') as f:
        products = pickle.load(f)
    f.close()
    return products


def func_search_product(code):
    products = func_open_product()
    if products.get(code):
        return (True, products.get(code))
    else:
        return (False, None)


def func_add_edit_product(code, data):
    try:
        products = func_open_product()
        if products.get(code):
            products.get(code).update(data)
        else:
            products[code] = data
        with open('products.pkl', 'wb') as f:
            pickle.dump(products, f, pickle.HIGHEST_PROTOCOL)
        f.close()
        return True
    except:
        return False


def func_add_list(code):
    try:
        products = func_open_product()
        products.get(code).update({
            'in_list': True
        })
        with open('products.pkl', 'wb') as f:
            pickle.dump(products, f, pickle.HIGHEST_PROTOCOL)
        f.close()
        return True
    except:
        return False


def func_remove_list(code):
    try:
        products = func_open_product()
        products.get(code).update({
            'in_list': False
        })
        with open('products.pkl', 'wb') as f:
            pickle.dump(products, f, pickle.HIGHEST_PROTOCOL)
        f.close()
        return True
    except:
        return False


def func_init_barcode(code):
    EAN = barcode.get_barcode_class('ean13')
    ean = EAN(code)
    fullname = ean.save(f'barcode/{code}')

    width_list = []
    f = open(fullname, 'r')
    for i in f.readlines():
        if '15.000mm' in i:
            width_start = i.find('width=')
            width_end = i.find('mm" x="')
            width = i[width_start+7:width_end]
            width_list.append(Decimal(width))
    f.close()
    return width_list


def func_print_all_card():
    products = func_open_product()
    cards = {}
    for i in products.keys():
        if products[i].get('in_list'):
            width_list = func_init_barcode(i)
            cards[i] = products[i]
            cards[i].update({
                'width_list': width_list
            })
    return ProductCard(cards, '1_所有商品價格牌')


def func_print_card(cards, filename):
    for i in cards.keys():
        width_list = func_init_barcode(i)
        cards[i].update({
            'width_list': width_list
        })
    return ProductCard(cards, filename)


def func_get_product_in_list():
    products = func_open_product()
    cards = dict()
    if len(products) > 0:
        for i in products.keys():
            if products[i].get('in_list'):
                cards[i] = products[i]
    return cards


class ProductErrorWindow(QtWidgets.QDialog, Ui_Error):
    def __init__(self, message):
        super(ProductErrorWindow, self).__init__()
        self.messages = message
        self.setupUi(self)

        self.message.setText(self.messages)
        self.btn_confirm.clicked.connect(self.accept)


class EditProduct(QtWidgets.QDialog, Ui_EditProduct):
    def __init__(self, code):
        super(EditProduct, self).__init__()
        self.code = code
        self.setupUi(self)

        self.btn_add.clicked.connect(self.check_edit)
        self.btn_cancel.clicked.connect(self.reject)
        self.product_is_sale.stateChanged.connect(self.change_sale)

        self.res, self.data = func_search_product(self.code)
        self.name = self.data.get('name')
        self.price = self.data.get('price')
        self.product_code.setText(self.code)
        self.product_name.setText(self.name)
        self.product_price.setText(f'{self.price}')
        if self.data.get('is_sale'):
            self.sale_price = self.data.get('sale_price')
            self.product_is_sale.setChecked(True)
            self.product_is_sale.setText('是')
            self.product_sale_price.setEnabled(True)
            self.product_sale_price.setText(f'{self.sale_price}')
            self.product_code.setFocus(True)

    def change_sale(self):
        if self.product_is_sale.isChecked():
            self.product_is_sale.setText('是')
            self.product_sale_price.setEnabled(True)
            self.product_sale_price.setFocus(True)
        else:
            self.product_is_sale.setText('否')
            self.product_sale_price.setText('')
            self.product_sale_price.setEnabled(False)

    def check_edit(self):
        error_count = 0
        message = ''
        name = self.product_name.text()
        price = self.product_price.text()
        if self.product_is_sale.isChecked():
            sale_price = self.product_sale_price.text()

        if error_count == 0:
            if len(name) == 0 :
                message += '請輸入商品名稱。\n'
                error_count += 1
            if len(price) == 0 or price == 0:
                message += '請輸入商品價格。\n'
                error_count += 1
            if self.product_is_sale.isChecked():
                if len(sale_price) == 0 or sale_price == 0:
                    message += '請輸入商品特價價格。\n'
                    error_count += 1

        if error_count == 0:
            if len(name) > 20 :
                message += '商品名稱長度不可超過20字。\n'
                error_count += 1

        if error_count == 0:
            try:
                price = int(price)
                if price < 0:
                    message += '商品價格需為正整數。\n'
                    error_count += 1
            except:
                message += '商品價格需為正整數且不可有小數。\n'
                error_count += 1
        if error_count == 0 and self.product_is_sale.isChecked():
            try:
                sale_price = int(sale_price)
                if sale_price < 0:
                    message += '商品特價價格需為正整數。\n'
                    error_count += 1
                if sale_price > price:
                    message += '商品特價價格需小於商品原價。\n'
                    error_count += 1
            except:
                message += '商品特價價格需為正整數且不可有小數。\n'
                error_count += 1

        if error_count > 0:
            error_window = ProductErrorWindow(message)
            error_window.exec_()
        else:
            data = {
                'name': name,
                'price': price,
                'is_sale': False,
                'sale_price': 0,
            }
            if self.product_is_sale.isChecked():
                data['is_sale'] = True
                data['sale_price'] = sale_price

            res = func_add_edit_product(self.code, data)
            if res:
                self.accept()
            else:
                self.reject()


class AddNewWindow(QtWidgets.QDialog, Ui_AddNewProduct):
    def __init__(self, code):
        super(AddNewWindow, self).__init__()
        self.code = code
        self.setupUi(self)

        self.btn_cancel.clicked.connect(self.reject)
        self.btn_add.clicked.connect(self.check_product)
        self.product_is_sale.stateChanged.connect(self.change_sale)
        self.product_code.setText(code)

    def change_sale(self):
        if self.product_is_sale.isChecked():
            self.product_is_sale.setText('是')
            self.product_sale_price.setEnabled(True)
            self.product_sale_price.setFocus(True)
        else:
            self.product_is_sale.setText('否')
            self.product_sale_price.setText('')
            self.product_sale_price.setEnabled(False)

    def check_product(self):
        error_count = 0
        message = ''
        name = self.product_name.text()
        price = self.product_price.text()
        if self.product_is_sale.isChecked():
            sale_price = self.product_sale_price.text()

        if error_count == 0:
            if len(name) == 0 :
                message += '請輸入商品名稱。\n'
                error_count += 1
            if len(price) == 0 or price == 0:
                message += '請輸入商品價格。\n'
                error_count += 1
            if self.product_is_sale.isChecked():
                if len(sale_price) == 0 or sale_price == 0:
                    message += '請輸入商品特價價格。\n'
                    error_count += 1

        if error_count == 0:
            if len(name) > 20 :
                message += '商品名稱長度不可超過20字。\n'
                error_count += 1

        if error_count == 0:
            try:
                price = int(price)
                if price < 0:
                    message += '商品價格需為正整數。\n'
                    error_count += 1
            except:
                message += '商品價格需為正整數且不可有小數。\n'
                error_count += 1
        if error_count == 0 and self.product_is_sale.isChecked():
            try:
                sale_price = int(sale_price)
                if sale_price < 0:
                    message += '商品特價價格需為正整數。\n'
                    error_count += 1
                if sale_price > price:
                    message += '商品特價價格需小於商品原價。\n'
                    error_count += 1
            except:
                message += '商品特價價格需為正整數且不可有小數。\n'
                error_count += 1

        if error_count > 0:
            error_window = ProductErrorWindow(message)
            error_window.exec_()
        else:
            data = {
                'name': name,
                'price': price,
                'is_sale': False,
                'sale_price': 0,
                'in_list': True,
            }
            if self.product_is_sale.isChecked():
                data['is_sale'] = True
                data['sale_price'] = sale_price

            res = func_add_edit_product(self.code, data)
            if res:
                self.accept()
            else:
                self.reject()


class AskNewWindow(QtWidgets.QDialog, Ui_AskNewProduct):
    def __init__(self, code):
        super(AskNewWindow, self).__init__()
        self.code = code
        self.setupUi(self)
        self.bindFunc()

    def bindFunc(self):
        self.btn_cancel.clicked.connect(self.reject)
        self.btn_new.clicked.connect(self.accept)


class ProductManager(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(ProductManager, self).__init__()
        self.setupUi(self)

        self.initGUI()
        self.bindFunc()

    def initGUI(self):
        self.search_code.setText('')
        self.product_code.setText('')
        self.product_name.setText('')
        self.product_price.setText('')
        self.product_sale_price.setText('')

        self.product_is_sale.setText('')
        self.product_in_list.setText('')

        self.btn_remove_list.setEnabled(False)
        self.btn_add_list.setEnabled(False)
        self.btn_clean.setEnabled(False)
        self.btn_edit.setEnabled(False)

        self.search_code.setFocus(True)

    def initSearch(self):
        self.product_code.setText('')
        self.product_name.setText('')
        self.product_price.setText('')
        self.product_sale_price.setText('')

        self.product_is_sale.setText('')
        self.product_in_list.setText('')

        self.btn_remove_list.setEnabled(False)
        self.btn_add_list.setEnabled(False)
        self.btn_clean.setEnabled(False)
        self.btn_edit.setEnabled(False)

        self.search_code.setFocus(True)

    def open_edit_product(self):
        code = self.product_code.text()
        edit_window = EditProduct(code)
        self.message.append(f'開始編輯商品{code}。')
        if edit_window.exec_() == QtWidgets.QDialog.Accepted:
            # self.message.append(f'開始編輯商品{code}。')
            name = edit_window.product_name.text()
            price = edit_window.product_price.text()
            message = f'商品編輯成功，編碼：{code}、名稱：{name}、價格：{price}'
            if edit_window.product_is_sale.isChecked():
                is_sale = True
                sale_price = edit_window.product_sale_price.text()
                self.product_is_sale.setText('是')
                self.product_sale_price.setText(sale_price)
                message += f'、特價價格：{sale_price}'
            else:
                self.product_is_sale.setText('')
                self.product_sale_price.setText('')
            message += '。\n'
            self.product_code.setText(code)
            self.product_name.setText(name)
            self.product_price.setText(price)
            self.message.append(message)
        else:
            self.message.append(f'取消編輯商品{code}。\n')
        self.search_code.setFocus(True)

    def open_add_new(self, code):
        add_window = AddNewWindow(code)
        if add_window.exec_() == QtWidgets.QDialog.Accepted:
            code = add_window.product_code.text()
            name = add_window.product_name.text()
            price = add_window.product_price.text()
            message = f'商品新增成功，編碼：{code}、名稱：{name}、價格：{price}'
            if add_window.product_is_sale.isChecked():
                is_sale = True
                sale_price = add_window.product_sale_price.text()
                self.product_is_sale.setText('是')
                self.product_sale_price.setText(sale_price)
                message += f'、特價價格：{sale_price}'
            message += '。\n'
            self.product_code.setText(code)
            self.product_name.setText(name)
            self.product_price.setText(price)
            self.message.append(message)
            self.btn_remove_list.setEnabled(True)
            self.product_in_list.setText('是')
            self.btn_clean.setEnabled(True)
            self.btn_edit.setEnabled(True)
        else:
            self.message.append(f'取消新增商品。\n')

    def open_ask_new(self, code):
        ask_window = AskNewWindow(code)
        if ask_window.exec_() == QtWidgets.QDialog.Accepted:
            self.open_add_new(code)
        else:
            self.message.append(f'取消新增商品。\n')

    def bindFunc(self):
        self.search_btn.clicked.connect(self.searchProduct)
        self.search_code.returnPressed.connect(self.search_btn.click)
        self.btn_clean.clicked.connect(self.cleanProduct)
        self.btn_edit.clicked.connect(self.open_edit_product)
        self.btn_add_list.clicked.connect(self.addProductList)
        self.btn_remove_list.clicked.connect(self.removeProductList)
        self.product_card.triggered.connect(self.switchToProductCard)
        self.product_card_in_list.triggered.connect(self.switchToProductCardInList)
        self.product_all_card.triggered.connect(self.printAllCard)

    def printAllCard(self):
        self.message.append('開始從列印清單製作價格牌。')
        res = func_print_all_card()
        products_count = res.res.get('products_count')
        pages = res.res.get('pages')
        message = f'產生{pages}頁價格牌，總共{products_count}樣商品。\n'
        self.message.append(message)

    def addProductList(self):
        code = self.product_code.text()
        name = self.product_name.text()
        res = func_add_list(code)
        if res:
            self.product_in_list.setText('是')
            self.message.append(f'商品{name}加入列印清單成功。\n')
            self.btn_add_list.setEnabled(False)
            self.btn_remove_list.setEnabled(True)
        else:
            self.message.append(f'商品{name}加入列印清單失敗。\n')
        self.search_code.setFocus(True)

    def removeProductList(self):
        code = self.product_code.text()
        name = self.product_name.text()
        res = func_remove_list(code)
        if res:
            self.product_in_list.setText('')
            self.message.append(f'商品{name}已從列印清單中移除。\n')
            self.btn_add_list.setEnabled(True)
            self.btn_remove_list.setEnabled(False)
        else:
            self.message.append(f'從列印清單移除商品{name}失敗。\n')
        self.search_code.setFocus(True)

    def searchProduct(self):
        self.initSearch()
        code = self.search_code.text()
        self.message.append(f'查詢條碼：{code}')
        code = code.zfill(13)
        self.search_code.setText('')
        res, text = func_check_code(code)

        if res:
            res, data = func_search_product(code)
            if res:
                name = data.get('name')
                price = data.get('price')
                self.product_code.setText(code)
                self.product_name.setText(name)
                self.product_price.setText(f'{price}元')
                self.btn_clean.setEnabled(True)
                message = f'商品編碼：{code}、名稱：{name}、價格：{price}'
                if data.get('is_sale'):
                    sale_price = data.get('sale_price')
                    self.product_is_sale.setText('是')
                    self.product_sale_price.setText(f'{sale_price}')
                    message += f'、特價價格：{sale_price}'
                if data.get('in_list'):
                    self.btn_remove_list.setEnabled(True)
                    self.product_in_list.setText('是')
                else:
                    self.btn_add_list.setEnabled(True)
                message += '。\n'
                self.message.append(message)
                self.btn_edit.setEnabled(True)
            else:
                self.message.append(f'查無此商品{code}，是否新增商品？')
                self.open_ask_new(code)
        else:
            self.message.append(text)
            self.initGUI()

    def cleanProduct(self):
        code = self.product_code.text()
        self.message.append(f'清空{code}查詢結果。\n')
        self.initGUI()

    def switchToProductCard(self):
        InitialMainWindow.CardWindow.show()
        InitialMainWindow.MainWindow.hide()

    def switchToProductCardInList(self):
        InitialMainWindow.CardInListWindow.show()
        InitialMainWindow.MainWindow.hide()


class Message(QtWidgets.QDialog, Ui_Message):
    def __init__(self, message):
        super(Message, self).__init__()
        self.messages = message
        self.setupUi(self)

        self.message.setText(self.messages)
        self.btn_confirm.clicked.connect(self.accept)


class ProductCardWindow(QtWidgets.QMainWindow, Ui_CardWindow):
    def __init__(self):
        super(ProductCardWindow, self).__init__()
        self.setupUi(self)

        self.card_list = dict()

        self.initGUI()
        self.bindFunc()

    def initGUI(self):
        self.search_code.setText('')
        self.search_code.setFocus(True)
        self.card_table.insertRow(0)
        self.card_table.setItem(0, 0, QtWidgets.QTableWidgetItem('1234567890123'))
        self.card_table.setItem(0, 1, QtWidgets.QTableWidgetItem('一二三四五一二三四五一二三四五一二三四五'))
        self.card_table.setItem(0, 2, QtWidgets.QTableWidgetItem('9999'))
        self.card_table.setItem(0, 3, QtWidgets.QTableWidgetItem('是'))
        self.card_table.setItem(0, 4, QtWidgets.QTableWidgetItem('999'))
        self.card_table.resizeColumnsToContents()
        self.card_table.resizeRowsToContents()
        self.card_table.removeRow(0)
        self.card_list = dict()

    def bindFunc(self):
        self.search_btn.clicked.connect(self.searchProduct)
        self.search_code.returnPressed.connect(self.search_btn.click)
        self.clean_btn.clicked.connect(self.cleanTable)
        self.delete_btn.clicked.connect(self.deleteCard)
        self.print_btn.clicked.connect(self.printCard)
        self.product_manager.triggered.connect(self.switchToProductManager)
        self.product_card_in_list.triggered.connect(self.switchToProductCardInList)
        self.product_all_card.triggered.connect(self.switchToPrintAllCard)

    def printCard(self):
        res = func_print_card(self.card_list, '3_指定商品價格牌')
        products_count = res.res.get('products_count')
        pages = res.res.get('pages')
        message = f'產生{pages}頁價格牌，總共{products_count}樣商品。'
        message_window = Message(message)
        message_window.exec_()
        self.search_code.setFocus(True)

    def deleteCard(self):
        selectedIndexes = self.card_table.selectedIndexes()
        rows = [index.row() for index in selectedIndexes]
        rows = sorted(set(rows), reverse=True)

        for i in rows:
            code = self.card_table.item(i, 0).text()
            self.card_list.pop(code)
            self.card_table.removeRow(i)

        self.search_code.setFocus(True)

    def cleanTable(self):
        rowCount = self.card_table.rowCount()
        if rowCount > 0:
            for i in range(0, rowCount):
                self.card_table.removeRow(0)
        self.initGUI()
        message = '清空待印清單'
        message_window = Message(message)
        message_window.exec_()

    def searchProduct(self):
        code = self.search_code.text()
        code = code.zfill(13)
        res, data = func_search_product(code)
        if res:
            if self.card_list.get(code) is None:
                self.card_list[code] = data
                row = self.card_table.rowCount()
                code = QtWidgets.QTableWidgetItem(code)
                name = QtWidgets.QTableWidgetItem(data.get('name'))
                price = QtWidgets.QTableWidgetItem(f"{data.get('price')}元")
                if data.get('is_sale'):
                    is_sale = QtWidgets.QTableWidgetItem('是')
                    sale_price = QtWidgets.QTableWidgetItem(f"{data.get('sale_price')}元")
                else:
                    is_sale = QtWidgets.QTableWidgetItem('')
                    sale_price = QtWidgets.QTableWidgetItem('')
                self.card_table.insertRow(row)
                self.card_table.setItem(row, 0, code)
                self.card_table.setItem(row, 1, name)
                self.card_table.setItem(row, 2, price)
                self.card_table.setItem(row, 3, is_sale)
                self.card_table.setItem(row, 4, sale_price)
            else:
                message = '商品已在清單中'
                message_window = Message(message)
                message_window.exec_()
        else:
            message = '查無此商品'
            message_window = Message(message)
            message_window.exec_()
        self.search_code.setText('')
        self.search_code.setFocus(True)

    def switchToProductManager(self):
        InitialMainWindow.MainWindow.show()
        InitialMainWindow.CardWindow.hide()

    def switchToProductCardInList(self):
        InitialMainWindow.CardInListWindow.show()
        InitialMainWindow.CardWindow.hide()

    def switchToPrintAllCard(self):
        InitialMainWindow.MainWindow.show()
        InitialMainWindow.CardWindow.hide()
        InitialMainWindow.MainWindow.printAllCard()


class ProductCardInListWindow(QtWidgets.QMainWindow, Ui_CardInListWindow):
    def __init__(self):
        super(ProductCardInListWindow, self).__init__()
        self.setupUi(self)

        self.initGUI()
        self.bindFunc()

    def initGUI(self):
        rowCount = self.card_table.rowCount()
        if rowCount > 0:
            for i in range(0, rowCount):
                self.card_table.removeRow(0)
        self.card_table.insertRow(0)
        self.card_table.setItem(0, 0, QtWidgets.QTableWidgetItem('1234567890123'))
        self.card_table.setItem(0, 1, QtWidgets.QTableWidgetItem('一二三四五一二三四五一二三四五一二三四五'))
        self.card_table.setItem(0, 2, QtWidgets.QTableWidgetItem('9999'))
        self.card_table.setItem(0, 3, QtWidgets.QTableWidgetItem('是'))
        self.card_table.setItem(0, 4, QtWidgets.QTableWidgetItem('999'))
        self.card_table.resizeColumnsToContents()
        self.card_table.resizeRowsToContents()
        self.card_table.removeRow(0)
        self.card_list = func_get_product_in_list()
        self.setTable()
        self.search_code.setFocus(True)

    def bindFunc(self):
        self.product_manager.triggered.connect(self.switchToProductManager)
        self.product_card.triggered.connect(self.switchToProductCard)
        self.product_all_card.triggered.connect(self.switchToPrintAllCard)
        self.print_btn.clicked.connect(self.printCard)
        self.refresh_btn.clicked.connect(self.refreshTable)
        self.clean_btn.clicked.connect(self.initGUI)
        self.search_btn.clicked.connect(self.searchProduct)
        self.search_code.returnPressed.connect(self.search_btn.click)

    def refreshTable(self):
        selectedIndexes = self.card_table.selectedIndexes()
        rows = [index.row() for index in selectedIndexes]
        rows = sorted(set(rows))
        self.initGUI()
        self.card_table.setSelectionMode(QtWidgets.QTableWidget.MultiSelection)
        for i in rows:
            self.card_table.selectRow(i)
        self.card_table.setSelectionMode(QtWidgets.QTableWidget.ExtendedSelection)
        self.search_code.setFocus(True)

    def searchProduct(self):
        selectedIndexes = self.card_table.selectedIndexes()
        rows = [index.row() for index in selectedIndexes]
        rows = sorted(set(rows))
        self.card_table.setSelectionMode(QtWidgets.QTableWidget.MultiSelection)
        code = self.search_code.text()
        code = code.zfill(13)
        self.search_code.setText('')
        if self.card_list.get(code) is not None:
            a = self.card_table.findItems(code, QtCore.Qt.MatchExactly)
            if a[0].row() not in rows:
                self.card_table.selectRow(a[0].row())
        else:
            message = f'{code}不在清單中'
            message_window = Message(message)
            message_window.exec_()
        # for i in rows:
        #     self.card_table.selectRow(i)
        self.card_table.setSelectionMode(QtWidgets.QTableWidget.ExtendedSelection)
        self.search_code.setFocus(True)

    def printCard(self):
        selectedIndexes = self.card_table.selectedIndexes()
        rows = [index.row() for index in selectedIndexes]
        rows = sorted(set(rows))
        cards = dict()
        for i in rows:
            code = self.card_table.item(i, 0).text()
            cards[code] = self.card_list.get(code)
        res = func_print_card(cards, '2_清單中指定商品價格牌')
        products_count = res.res.get('products_count')
        pages = res.res.get('pages')
        message = f'產生{pages}頁價格牌，總共{products_count}樣商品。'
        message_window = Message(message)
        message_window.exec_()
        self.search_code.setFocus(True)

    def setTable(self):
        for i in self.card_list.keys():
            row = self.card_table.rowCount()
            code = QtWidgets.QTableWidgetItem(i)
            name = QtWidgets.QTableWidgetItem(str(self.card_list.get(i).get('name')))
            price = QtWidgets.QTableWidgetItem(f"{self.card_list.get(i).get('price')}元")
            if self.card_list.get(i).get('is_sale'):
                is_sale = QtWidgets.QTableWidgetItem('是')
                sale_price = QtWidgets.QTableWidgetItem(f"{self.card_list.get(i).get('sale_price')}元")
            else:
                is_sale = QtWidgets.QTableWidgetItem('')
                sale_price = QtWidgets.QTableWidgetItem('')
            self.card_table.insertRow(row)
            self.card_table.setItem(row, 0, code)
            self.card_table.setItem(row, 1, name)
            self.card_table.setItem(row, 2, price)
            self.card_table.setItem(row, 3, is_sale)
            self.card_table.setItem(row, 4, sale_price)

    def switchToProductManager(self):
        InitialMainWindow.MainWindow.show()
        InitialMainWindow.CardInListWindow.hide()

    def switchToProductCard(self):
        InitialMainWindow.CardWindow.show()
        InitialMainWindow.CardInListWindow.hide()

    def switchToPrintAllCard(self):
        InitialMainWindow.MainWindow.show()
        InitialMainWindow.CardInListWindow.hide()
        InitialMainWindow.MainWindow.printAllCard()


class InitialMainWindow:
    def __init__(self):
        app = QtWidgets.QApplication(sys.argv)
        InitialMainWindow.MainWindow = ProductManager()
        InitialMainWindow.MainWindow.show()
        InitialMainWindow.CardWindow = ProductCardWindow()
        InitialMainWindow.CardInListWindow = ProductCardInListWindow()
        # app.exec_()
        sys.exit(app.exec_())


def main():
    program = InitialMainWindow()


def initFile():
    if not os.path.isdir('barcode'):
        os.mkdir('barcode')
    if not os.path.isfile('products.pkl'):
        products = dict()
        with open('products.pkl', 'wb') as f:
            pickle.dump(products, f, pickle.HIGHEST_PROTOCOL)
        f.close()


if __name__ == "__main__":
    initFile()
    main()
    # app = QtWidgets.QApplication(sys.argv)
    # MainWindow = ProductManager()
    # CardWindow = ProductCard()
    # MainWindow.show()
    # sys.exit(app.exec_())
