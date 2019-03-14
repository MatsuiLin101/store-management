import math
from decimal import *

PAGE_HEIGHT = Decimal(277.000)
PAGE_WIDTH = Decimal(190.000)

# CARD_HEIGHT = Decimal(33.750)
# CARD_WIDTH = Decimal(45.000)
CARD_HEIGHT = Decimal(44.000)
CARD_WIDTH = Decimal(56.000)

GAP_HEIGHT = Decimal(2.000)
GAP_WIDTH = Decimal(3.000)

CODE_HEIGHT = Decimal(5.000)

FONT_NAME = 14
FONT_PRICE = 24
FONT_IS_SALE = 14
FONT_SALE_PRICE = 10
FONT_CODE = 10

CARDS_PER_PAGE = 18
CARDS_PER_ROW = 3

FILL = ['black', 'white', 'red']


class ProductCard(object):
    def __init__(self, cards, filename):
        self.cards = cards
        self.filename = filename
        self.main()

    def calc_barcode_len(self, width_list):
        for i in range(len(width_list)):
            width_list[i] = Decimal(width_list[i])
        return sum(width_list)

    def main(self):
        products_count = len(self.cards)
        pages = math.ceil(products_count / CARDS_PER_PAGE)
        total_page_height = (PAGE_HEIGHT * pages) - 1

        SVG = []
        SVG.append(f'<?xml version="1.0" encoding="UTF-8"?>\n')
        SVG.append(f'<svg height="{total_page_height}mm" version="1.1" width="{PAGE_WIDTH}mm" xmlns="http://www.w3.org/2000/svg">\n')

        index = 0
        page = 1

        SVG.append(f'<g id="barcode_group">\n')
        SVG.append(f'<rect height="100%" style="fill:{FILL[1]}" width="100%"/>\n')
        for i in self.cards.keys():

            if index % CARDS_PER_PAGE == 0 and index != 0:
                page += 1

            start_x = Decimal((index % CARDS_PER_ROW) * (CARD_WIDTH + GAP_WIDTH))
            start_y = Decimal((int((index % CARDS_PER_PAGE) / CARDS_PER_ROW) * (CARD_HEIGHT + GAP_HEIGHT)) + (PAGE_HEIGHT * (page - 1)) + 1)

            code = i
            name = self.cards[i].get('name')
            price = self.cards[i].get('price')
            is_sale = self.cards[i].get('is_sale')
            sale_price = self.cards[i].get('sale_price')
            width_list = self.cards[i].get('width_list')
            barcode_len = self.calc_barcode_len(width_list)

            name_x = start_x + Decimal(3.000)
            name_y = start_y + Decimal(6.500)
            name2_y = name_y + Decimal(4.500)

            price_x = start_x + Decimal(CARD_WIDTH / 2)
            price_y = start_y + Decimal(Decimal(44.000) / Decimal(2.0)) + Decimal(4.0)

            codebar_x = start_x + Decimal((CARD_WIDTH - Decimal(barcode_len)) / 2)
            codebar_y = start_y + Decimal(CARD_HEIGHT / Decimal(1.5)) + Decimal(3.75)

            codenum_x = start_x + Decimal(CARD_WIDTH / 2)
            codenum_y = start_y + Decimal(CARD_HEIGHT / Decimal(1.1)) + Decimal(1.5)

            SVG.append(f'<text style="fill:{FILL[0]};font-size:{FONT_NAME}pt;font-weight:bold;" x="{name_x}mm" y="{name_y}mm">{name[:10]}</text>\n')
            if len(name) > 10:
                SVG.append(f'<text style="fill:{FILL[0]};font-size:{FONT_NAME}pt;font-weight:bold;" x="{name_x}mm" y="{name2_y}mm">{name[10:]}</text>\n')
            if is_sale:
                is_sale_x = start_x + Decimal(2.500)
                is_sale_y = start_y + Decimal(Decimal(28.000) / Decimal(1.5))
                sale_x = start_x + Decimal(32.000) + Decimal(10.0)
                sale_y = start_y + Decimal(Decimal(44.000) / Decimal(1.5)) + Decimal(2.75)
                SVG.append(f'<text style="fill:{FILL[2]};font-size:{FONT_IS_SALE}pt;text-anchor:left;" x="{is_sale_x}mm" y="{is_sale_y}mm">特價</text>\n')
                SVG.append(f'<text style="fill:{FILL[2]};font-size:{FONT_PRICE}pt;text-anchor:middle;" x="{price_x}mm" y="{price_y}mm">{sale_price}元</text>\n')
                SVG.append(f'<text style="fill:{FILL[0]};font-size:{FONT_SALE_PRICE}pt;text-anchor:right;" x="{sale_x}mm" y="{sale_y}mm"><tspan text-decoration="line-through">{price}元</tspan></text>\n')
            else:
                SVG.append(f'<text style="fill:{FILL[0]};font-size:{FONT_PRICE}pt;text-anchor:middle;" x="{price_x}mm" y="{price_y}mm">{price}元</text>\n')
            SVG.append(f'<text style="fill:{FILL[0]};font-size:{FONT_CODE}pt;text-anchor:middle;" x="{codenum_x}mm" y="{codenum_y}mm">{code}</text>\n')

            for j in range(len(width_list)):
                code_width = width_list[j]
                if j % 2 == 0:
                    SVG.append(f'<rect height="{CODE_HEIGHT}mm" style="fill:{FILL[0]};" width="{code_width}mm" x="{codebar_x}mm" y="{codebar_y}mm"/>\n')
                else:
                    SVG.append(f'<rect height="{CODE_HEIGHT}mm" style="fill:{FILL[1]};" width="{code_width}mm" x="{codebar_x}mm" y="{codebar_y}mm"/>\n')
                codebar_x += code_width

            # left top right bottom
            SVG.append(f'<rect height="{CARD_HEIGHT}mm" style="fill:{FILL[0]};" width="1.000mm" x="{start_x}mm" y="{start_y}mm"/>\n')
            SVG.append(f'<rect height="1.000mm" style="fill:{FILL[0]};" width="{CARD_WIDTH}mm" x="{start_x}mm" y="{start_y}mm"/>\n')
            SVG.append(f'<rect height="{CARD_HEIGHT}mm" style="fill:{FILL[0]};" width="1.000mm" x="{start_x + CARD_WIDTH - 1}mm" y="{start_y}mm"/>\n')
            SVG.append(f'<rect height="1.000mm" style="fill:{FILL[0]};" width="{CARD_WIDTH}mm" x="{start_x}mm" y="{start_y + CARD_HEIGHT - 1}mm"/>\n')

            index += 1

        SVG.append('</g></svg>')
        f = open(f'{self.filename}.svg', 'w', encoding="utf8")
        f.writelines(SVG)
        f.close()

        self.products_count = products_count
        self.pages = pages

    @property
    def res(self):
        return {
            'products_count': self.products_count,
            'pages': self.pages,
        }
