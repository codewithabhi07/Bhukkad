"""
Lucky Traders - UML & Architectural Diagrams PDF Generator (Refined)
Generates an academic project PDF containing all 8 diagrams:
0. ER Diagram (Entity-Relationship Diagram)
1. Class Diagram
2. Object Diagram
3. Component Diagram
4. Deployment Diagram
5. Use Case Diagram
6. Activity Diagram
7. Sequence Diagram
"""

import os
import math
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
)
from reportlab.graphics.shapes import (
    Drawing, Rect, String, Line, Group, Polygon, Circle, Ellipse
)
from reportlab.pdfgen import canvas

# ==========================================================
# COLOR PALETTE
# ==========================================================
COLOR_PRIMARY_DARK = colors.HexColor('#0D1B2A')   # Navy / Midnight
COLOR_PRIMARY = colors.HexColor('#1B263B')        # Deep Slate Blue
COLOR_ACCENT_RED = colors.HexColor('#C0392B')     # Spice Red
COLOR_ACCENT_GOLD = colors.HexColor('#B7950B')    # Golden Amber
COLOR_ACCENT_GREEN = colors.HexColor('#27AE60')   # Fresh Green
COLOR_BG_LIGHT = colors.HexColor('#F8F9FA')       # Soft background
COLOR_BORDER = colors.HexColor('#BDC3C7')         # Clean border
COLOR_TEXT_DARK = colors.HexColor('#2C3E50')      # Slate text
COLOR_BOX_HEADER = colors.HexColor('#EAEDED')     # Table header light
COLOR_MUTED = colors.HexColor('#7F8C8D')          # Subdued gray


class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas to dynamically compute and display total page count."""
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            return  # Skip cover page

        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(COLOR_PRIMARY)

        # Header
        self.drawString(36, 810, "LUCKY TRADERS - UML & ARCHITECTURAL SPECIFICATION")
        self.setFont("Helvetica", 8)
        self.setFillColor(COLOR_MUTED)
        self.drawRightString(559, 810, "SPPU CS331FP Computer Engineering Project")
        self.setStrokeColor(COLOR_BORDER)
        self.setLineWidth(0.5)
        self.line(36, 804, 559, 804)

        # Footer
        self.line(36, 45, 559, 45)
        self.setFont("Helvetica", 8)
        self.setFillColor(COLOR_MUTED)
        self.drawString(36, 33, "Academic Laboratory & Viva Voce Defense Documentation")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(559, 33, page_str)
        self.restoreState()


# ==========================================================
# VECTOR DRAWING HELPERS
# ==========================================================
def draw_rounded_box(d, x, y, w, h, bg_color=colors.white, stroke_color=COLOR_PRIMARY, stroke_width=1, radius=4):
    d.add(Rect(x, y, w, h, fillColor=bg_color, strokeColor=stroke_color, strokeWidth=stroke_width, rx=radius, ry=radius))

def draw_header_box(d, x, y, w, h, header_h, title, header_bg=COLOR_PRIMARY, body_bg=colors.white, border_color=COLOR_PRIMARY):
    # Main outer box
    d.add(Rect(x, y, w, h, fillColor=body_bg, strokeColor=border_color, strokeWidth=1, rx=4, ry=4))
    # Header box (top portion)
    d.add(Rect(x, y + h - header_h, w, header_h, fillColor=header_bg, strokeColor=border_color, strokeWidth=1, rx=4, ry=4))
    # Square out bottom corners of header
    d.add(Rect(x, y + h - header_h, w, 4, fillColor=header_bg, strokeColor=colors.transparent, strokeWidth=0))
    # Header Title
    d.add(String(x + w / 2, y + h - (header_h / 2) - 3, title, textAnchor='middle', fontName='Helvetica-Bold', fontSize=8, fillColor=colors.white))

def draw_line(d, x1, y1, x2, y2, color=COLOR_PRIMARY, width=1, dashed=False):
    line = Line(x1, y1, x2, y2, strokeColor=color, strokeWidth=width)
    if dashed:
        line.strokeDashArray = [3, 3]
    d.add(line)

def draw_arrow(d, x1, y1, x2, y2, label="", color=COLOR_PRIMARY, width=1, dashed=False, arrow_style="normal", label_y_offset=4):
    draw_line(d, x1, y1, x2, y2, color=color, width=width, dashed=dashed)

    angle = math.atan2(y2 - y1, x2 - x1)
    arrow_len = 7
    arrow_angle = math.pi / 6

    if arrow_style == "normal":
        p1 = (x2, y2)
        p2 = (x2 - arrow_len * math.cos(angle - arrow_angle), y2 - arrow_len * math.sin(angle - arrow_angle))
        p3 = (x2 - arrow_len * math.cos(angle + arrow_angle), y2 - arrow_len * math.sin(angle + arrow_angle))
        d.add(Polygon([p1[0], p1[1], p2[0], p2[1], p3[0], p3[1]], fillColor=color, strokeColor=color, strokeWidth=0.5))

    elif arrow_style == "open":
        p2 = (x2 - arrow_len * math.cos(angle - arrow_angle), y2 - arrow_len * math.sin(angle - arrow_angle))
        p3 = (x2 - arrow_len * math.cos(angle + arrow_angle), y2 - arrow_len * math.sin(angle + arrow_angle))
        d.add(Line(x2, y2, p2[0], p2[1], strokeColor=color, strokeWidth=width))
        d.add(Line(x2, y2, p3[0], p3[1], strokeColor=color, strokeWidth=width))

    elif arrow_style == "triangle_white":
        p1 = (x2, y2)
        p2 = (x2 - 10 * math.cos(angle - arrow_angle), y2 - 10 * math.sin(angle - arrow_angle))
        p3 = (x2 - 10 * math.cos(angle + arrow_angle), y2 - 10 * math.sin(angle + arrow_angle))
        d.add(Polygon([p1[0], p1[1], p2[0], p2[1], p3[0], p3[1]], fillColor=colors.white, strokeColor=color, strokeWidth=1))

    elif arrow_style == "diamond_filled":
        d_len = 9
        d_angle = math.pi / 8
        dp1 = (x1, y1)
        dp2 = (x1 + d_len * math.cos(angle - d_angle), y1 + d_len * math.sin(angle - d_angle))
        dp3 = (x1 + d_len * 1.6 * math.cos(angle), y1 + d_len * 1.6 * math.sin(angle))
        dp4 = (x1 + d_len * math.cos(angle + d_angle), y1 + d_len * math.sin(angle + d_angle))
        d.add(Polygon([dp1[0], dp1[1], dp2[0], dp2[1], dp3[0], dp3[1], dp4[0], dp4[1]], fillColor=color, strokeColor=color, strokeWidth=1))

    if label:
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2 + label_y_offset
        d.add(String(mid_x, mid_y, label, textAnchor='middle', fontName='Helvetica', fontSize=6.5, fillColor=COLOR_TEXT_DARK))


# ==========================================================
# 0. ER DIAGRAM BUILDER
# ==========================================================
def create_er_diagram_drawing():
    d = Drawing(520, 260)
    d.add(Rect(0, 0, 520, 260, fillColor=COLOR_BG_LIGHT, strokeColor=COLOR_BORDER, strokeWidth=0.8, rx=6, ry=6))

    # 1. CATEGORIES (Left Top)
    draw_header_box(d, 20, 150, 130, 95, 20, "CATEGORIES", header_bg=COLOR_PRIMARY_DARK)
    d.add(String(26, 212, "PK  id : INTEGER", fontName='Helvetica-Bold', fontSize=7, fillColor=COLOR_ACCENT_RED))
    d.add(String(26, 200, "     slug : VARCHAR(50)", fontName='Helvetica', fontSize=7, fillColor=COLOR_TEXT_DARK))
    d.add(String(26, 188, "     name : VARCHAR(100)", fontName='Helvetica', fontSize=7, fillColor=COLOR_TEXT_DARK))
    d.add(String(26, 176, "     icon : VARCHAR(10)", fontName='Helvetica', fontSize=7, fillColor=COLOR_TEXT_DARK))
    d.add(String(26, 164, "     banner_image : TEXT", fontName='Helvetica', fontSize=7, fillColor=COLOR_TEXT_DARK))

    # 2. PRODUCTS (Center Top)
    draw_header_box(d, 195, 140, 140, 110, 20, "PRODUCTS", header_bg=COLOR_PRIMARY)
    d.add(String(201, 218, "PK  id : INTEGER", fontName='Helvetica-Bold', fontSize=7, fillColor=COLOR_ACCENT_RED))
    d.add(String(201, 206, "FK  category_id : INT", fontName='Helvetica-Bold', fontSize=7, fillColor=COLOR_ACCENT_GOLD))
    d.add(String(201, 194, "     name : VARCHAR(120)", fontName='Helvetica', fontSize=7, fillColor=COLOR_TEXT_DARK))
    d.add(String(201, 182, "     price_1kg : DECIMAL", fontName='Helvetica', fontSize=7, fillColor=COLOR_TEXT_DARK))
    d.add(String(201, 170, "     price_250g : DECIMAL", fontName='Helvetica', fontSize=7, fillColor=COLOR_TEXT_DARK))
    d.add(String(201, 158, "     stock_qty : INTEGER", fontName='Helvetica', fontSize=7, fillColor=COLOR_TEXT_DARK))
    d.add(String(201, 146, "     image_url : TEXT", fontName='Helvetica', fontSize=7, fillColor=COLOR_TEXT_DARK))

    # 3. USERS (Right Top)
    draw_header_box(d, 375, 150, 130, 95, 20, "USERS", header_bg=COLOR_PRIMARY_DARK)
    d.add(String(381, 212, "PK  id : INTEGER", fontName='Helvetica-Bold', fontSize=7, fillColor=COLOR_ACCENT_RED))
    d.add(String(381, 200, "     username : VARCHAR", fontName='Helvetica', fontSize=7, fillColor=COLOR_TEXT_DARK))
    d.add(String(381, 188, "     password_hash : TEXT", fontName='Helvetica', fontSize=7, fillColor=COLOR_TEXT_DARK))
    d.add(String(381, 176, "     role : VARCHAR(20)", fontName='Helvetica', fontSize=7, fillColor=COLOR_TEXT_DARK))
    d.add(String(381, 164, "     phone : VARCHAR(15)", fontName='Helvetica', fontSize=7, fillColor=COLOR_TEXT_DARK))

    # 4. ORDER_ITEMS (Center Bottom)
    draw_header_box(d, 195, 15, 140, 95, 20, "ORDER_ITEMS", header_bg=COLOR_ACCENT_RED)
    d.add(String(201, 77, "PK  id : INTEGER", fontName='Helvetica-Bold', fontSize=7, fillColor=COLOR_ACCENT_RED))
    d.add(String(201, 65, "FK  order_id : INT", fontName='Helvetica-Bold', fontSize=7, fillColor=COLOR_ACCENT_GOLD))
    d.add(String(201, 53, "FK  product_id : INT", fontName='Helvetica-Bold', fontSize=7, fillColor=COLOR_ACCENT_GOLD))
    d.add(String(201, 41, "     weight : VARCHAR(10)", fontName='Helvetica', fontSize=7, fillColor=COLOR_TEXT_DARK))
    d.add(String(201, 29, "     quantity : INTEGER", fontName='Helvetica', fontSize=7, fillColor=COLOR_TEXT_DARK))

    # 5. ORDERS (Right Bottom)
    draw_header_box(d, 375, 10, 130, 105, 20, "ORDERS", header_bg=COLOR_PRIMARY)
    d.add(String(381, 82, "PK  id : INTEGER", fontName='Helvetica-Bold', fontSize=7, fillColor=COLOR_ACCENT_RED))
    d.add(String(381, 70, "     order_number : VARCHAR", fontName='Helvetica', fontSize=7, fillColor=COLOR_TEXT_DARK))
    d.add(String(381, 58, "FK  user_id : INT (opt)", fontName='Helvetica-Bold', fontSize=7, fillColor=COLOR_ACCENT_GOLD))
    d.add(String(381, 46, "     payment_method : STR", fontName='Helvetica', fontSize=7, fillColor=COLOR_TEXT_DARK))
    d.add(String(381, 34, "     total_amount : DECIMAL", fontName='Helvetica', fontSize=7, fillColor=COLOR_TEXT_DARK))
    d.add(String(381, 22, "     status : VARCHAR(20)", fontName='Helvetica', fontSize=7, fillColor=COLOR_TEXT_DARK))

    # Connectors
    draw_line(d, 150, 195, 195, 195, color=COLOR_PRIMARY, width=1.2)
    d.add(String(154, 200, "1", fontName='Helvetica-Bold', fontSize=8, fillColor=COLOR_PRIMARY))
    d.add(String(185, 200, "N", fontName='Helvetica-Bold', fontSize=8, fillColor=COLOR_PRIMARY))
    d.add(String(172, 185, "has", fontName='Helvetica-Oblique', fontSize=6.5, fillColor=COLOR_MUTED))

    draw_line(d, 440, 150, 440, 115, color=COLOR_PRIMARY, width=1.2)
    d.add(String(444, 138, "1", fontName='Helvetica-Bold', fontSize=8, fillColor=COLOR_PRIMARY))
    d.add(String(444, 120, "N", fontName='Helvetica-Bold', fontSize=8, fillColor=COLOR_PRIMARY))
    d.add(String(447, 128, "places", fontName='Helvetica-Oblique', fontSize=6.5, fillColor=COLOR_MUTED))

    draw_line(d, 375, 62, 335, 62, color=COLOR_ACCENT_RED, width=1.2)
    d.add(String(363, 67, "1", fontName='Helvetica-Bold', fontSize=8, fillColor=COLOR_ACCENT_RED))
    d.add(String(340, 67, "N", fontName='Helvetica-Bold', fontSize=8, fillColor=COLOR_ACCENT_RED))
    d.add(String(355, 52, "contains", fontName='Helvetica-Oblique', fontSize=6.5, fillColor=COLOR_MUTED))

    draw_line(d, 265, 140, 265, 110, color=COLOR_PRIMARY, width=1.2)
    d.add(String(270, 130, "1", fontName='Helvetica-Bold', fontSize=8, fillColor=COLOR_PRIMARY))
    d.add(String(270, 114, "N", fontName='Helvetica-Bold', fontSize=8, fillColor=COLOR_PRIMARY))
    d.add(String(272, 122, "in", fontName='Helvetica-Oblique', fontSize=6.5, fillColor=COLOR_MUTED))

    # Legend
    d.add(Rect(20, 20, 150, 60, fillColor=colors.white, strokeColor=COLOR_BORDER, strokeWidth=0.5, rx=3, ry=3))
    d.add(String(26, 68, "RELATIONSHIP CARDINALITY", fontName='Helvetica-Bold', fontSize=7, fillColor=COLOR_PRIMARY))
    d.add(String(26, 56, "* 1:N - One Category to Many Products", fontName='Helvetica', fontSize=6.5, fillColor=COLOR_TEXT_DARK))
    d.add(String(26, 44, "* 1:N - One User to Many Orders", fontName='Helvetica', fontSize=6.5, fillColor=COLOR_TEXT_DARK))
    d.add(String(26, 32, "* 1:N - One Order to Many Line Items", fontName='Helvetica', fontSize=6.5, fillColor=COLOR_TEXT_DARK))

    return d


# ==========================================================
# 1. CLASS DIAGRAM BUILDER
# ==========================================================
def create_class_diagram_drawing():
    d = Drawing(520, 280)
    d.add(Rect(0, 0, 520, 280, fillColor=COLOR_BG_LIGHT, strokeColor=COLOR_BORDER, strokeWidth=0.8, rx=6, ry=6))

    # Base User Class (Center Top)
    draw_header_box(d, 195, 200, 130, 70, 16, "User", header_bg=COLOR_PRIMARY_DARK)
    d.add(String(201, 238, "- id: int", fontName='Helvetica', fontSize=6.5, fillColor=COLOR_TEXT_DARK))
    d.add(String(201, 228, "- username: str", fontName='Helvetica', fontSize=6.5, fillColor=COLOR_TEXT_DARK))
    d.add(String(201, 218, "- role: str", fontName='Helvetica', fontSize=6.5, fillColor=COLOR_TEXT_DARK))
    d.add(Line(195, 214, 325, 214, strokeColor=COLOR_BORDER, strokeWidth=0.5))
    d.add(String(201, 204, "+ login(): bool", fontName='Helvetica', fontSize=6.5, fillColor=COLOR_PRIMARY))

    # Subclass Customer (Left Mid)
    draw_header_box(d, 40, 105, 120, 72, 16, "Customer", header_bg=COLOR_PRIMARY)
    d.add(String(46, 146, "- address: str", fontName='Helvetica', fontSize=6.5, fillColor=COLOR_TEXT_DARK))
    d.add(String(46, 136, "- phone: str", fontName='Helvetica', fontSize=6.5, fillColor=COLOR_TEXT_DARK))
    d.add(Line(40, 132, 160, 132, strokeColor=COLOR_BORDER, strokeWidth=0.5))
    d.add(String(46, 122, "+ placeOrder(): Order", fontName='Helvetica', fontSize=6.5, fillColor=COLOR_PRIMARY))
    d.add(String(46, 112, "+ viewHistory(): list", fontName='Helvetica', fontSize=6.5, fillColor=COLOR_PRIMARY))

    # Subclass Administrator (Center Mid)
    draw_header_box(d, 195, 105, 130, 72, 16, "Administrator", header_bg=COLOR_PRIMARY)
    d.add(String(201, 146, "- permissions: list", fontName='Helvetica', fontSize=6.5, fillColor=COLOR_TEXT_DARK))
    d.add(Line(195, 140, 325, 140, strokeColor=COLOR_BORDER, strokeWidth=0.5))
    d.add(String(201, 130, "+ addProduct()", fontName='Helvetica', fontSize=6.5, fillColor=COLOR_PRIMARY))
    d.add(String(201, 120, "+ updateStock()", fontName='Helvetica', fontSize=6.5, fillColor=COLOR_PRIMARY))
    d.add(String(201, 110, "+ updateOrderStatus()", fontName='Helvetica', fontSize=6.5, fillColor=COLOR_PRIMARY))

    # Product Class (Right Mid)
    draw_header_box(d, 360, 100, 135, 82, 16, "Product", header_bg=COLOR_PRIMARY)
    d.add(String(366, 152, "- id: int", fontName='Helvetica', fontSize=6.5, fillColor=COLOR_TEXT_DARK))
    d.add(String(366, 142, "- name: str", fontName='Helvetica', fontSize=6.5, fillColor=COLOR_TEXT_DARK))
    d.add(String(366, 132, "- price_1kg: float", fontName='Helvetica', fontSize=6.5, fillColor=COLOR_TEXT_DARK))
    d.add(String(366, 122, "- stock_qty: int", fontName='Helvetica', fontSize=6.5, fillColor=COLOR_TEXT_DARK))
    d.add(Line(360, 117, 495, 117, strokeColor=COLOR_BORDER, strokeWidth=0.5))
    d.add(String(366, 106, "+ decrementStock(q)", fontName='Helvetica', fontSize=6.5, fillColor=COLOR_PRIMARY))

    # Order Class (Left Bottom)
    draw_header_box(d, 40, 15, 120, 75, 16, "Order", header_bg=COLOR_ACCENT_RED)
    d.add(String(46, 60, "- orderNumber: str", fontName='Helvetica', fontSize=6.5, fillColor=COLOR_TEXT_DARK))
    d.add(String(46, 50, "- subtotal: float", fontName='Helvetica', fontSize=6.5, fillColor=COLOR_TEXT_DARK))
    d.add(String(46, 40, "- totalAmount: float", fontName='Helvetica', fontSize=6.5, fillColor=COLOR_TEXT_DARK))
    d.add(Line(40, 36, 160, 36, strokeColor=COLOR_BORDER, strokeWidth=0.5))
    d.add(String(46, 26, "+ calculateTax(): float", fontName='Helvetica', fontSize=6.5, fillColor=COLOR_PRIMARY))
    d.add(String(46, 16, "+ generateBill(): dict", fontName='Helvetica', fontSize=6.5, fillColor=COLOR_PRIMARY))

    # OrderItem Class (Center Bottom)
    draw_header_box(d, 195, 15, 130, 70, 16, "OrderItem", header_bg=COLOR_ACCENT_RED)
    d.add(String(201, 60, "- weight: str", fontName='Helvetica', fontSize=6.5, fillColor=COLOR_TEXT_DARK))
    d.add(String(201, 50, "- unitPrice: float", fontName='Helvetica', fontSize=6.5, fillColor=COLOR_TEXT_DARK))
    d.add(String(201, 40, "- quantity: int", fontName='Helvetica', fontSize=6.5, fillColor=COLOR_TEXT_DARK))
    d.add(Line(195, 36, 325, 36, strokeColor=COLOR_BORDER, strokeWidth=0.5))
    d.add(String(201, 24, "+ getSubtotal(): float", fontName='Helvetica', fontSize=6.5, fillColor=COLOR_PRIMARY))

    # Category Class (Right Bottom)
    draw_header_box(d, 360, 15, 135, 60, 16, "Category", header_bg=COLOR_PRIMARY_DARK)
    d.add(String(366, 50, "- id: int", fontName='Helvetica', fontSize=6.5, fillColor=COLOR_TEXT_DARK))
    d.add(String(366, 40, "- name: str", fontName='Helvetica', fontSize=6.5, fillColor=COLOR_TEXT_DARK))
    d.add(Line(360, 36, 495, 36, strokeColor=COLOR_BORDER, strokeWidth=0.5))
    d.add(String(366, 24, "+ getProducts(): list", fontName='Helvetica', fontSize=6.5, fillColor=COLOR_PRIMARY))

    # Inheritance arrows
    draw_arrow(d, 100, 177, 230, 200, arrow_style="triangle_white")
    draw_arrow(d, 260, 177, 260, 200, arrow_style="triangle_white")

    # Composition
    draw_arrow(d, 160, 50, 195, 50, arrow_style="diamond_filled")
    d.add(String(164, 55, "1", fontName='Helvetica-Bold', fontSize=7, fillColor=COLOR_PRIMARY))
    d.add(String(188, 55, "1..*", fontName='Helvetica-Bold', fontSize=7, fillColor=COLOR_PRIMARY))

    # Association
    draw_arrow(d, 325, 60, 395, 100, label="refers to", arrow_style="open")

    # Aggregation
    draw_arrow(d, 427, 75, 427, 100, arrow_style="normal")
    d.add(String(432, 80, "1", fontName='Helvetica-Bold', fontSize=7, fillColor=COLOR_PRIMARY))
    d.add(String(432, 95, "*", fontName='Helvetica-Bold', fontSize=7, fillColor=COLOR_PRIMARY))

    # Association Customer -> Order
    draw_arrow(d, 100, 105, 100, 90, label="places", arrow_style="open")

    return d


# ==========================================================
# 2. OBJECT DIAGRAM BUILDER
# ==========================================================
def create_object_diagram_drawing():
    d = Drawing(520, 260)
    d.add(Rect(0, 0, 520, 260, fillColor=COLOR_BG_LIGHT, strokeColor=COLOR_BORDER, strokeWidth=0.8, rx=6, ry=6))

    # 1. customer:Customer (Top Left)
    draw_header_box(d, 20, 145, 140, 95, 20, "customer : Customer", header_bg=COLOR_PRIMARY)
    d.add(String(26, 204, "id = 2", fontName='Helvetica', fontSize=7, fillColor=COLOR_TEXT_DARK))
    d.add(String(26, 192, "username = 'User'", fontName='Helvetica', fontSize=7, fillColor=COLOR_TEXT_DARK))
    d.add(String(26, 180, "fullName = 'Customer User'", fontName='Helvetica', fontSize=7, fillColor=COLOR_TEXT_DARK))
    d.add(String(26, 168, "phone = '9876543210'", fontName='Helvetica', fontSize=7, fillColor=COLOR_TEXT_DARK))
    d.add(String(26, 156, "role = 'customer'", fontName='Helvetica', fontSize=7, fillColor=COLOR_TEXT_DARK))

    # 2. admin:Administrator (Top Center)
    draw_header_box(d, 185, 155, 140, 85, 20, "admin : Administrator", header_bg=COLOR_PRIMARY_DARK)
    d.add(String(191, 204, "id = 1", fontName='Helvetica', fontSize=7, fillColor=COLOR_TEXT_DARK))
    d.add(String(191, 192, "username = 'admin'", fontName='Helvetica', fontSize=7, fillColor=COLOR_TEXT_DARK))
    d.add(String(191, 180, "role = 'admin'", fontName='Helvetica', fontSize=7, fillColor=COLOR_TEXT_DARK))
    d.add(String(191, 168, "status = 'Active'", fontName='Helvetica', fontSize=7, fillColor=COLOR_TEXT_DARK))

    # 3. category1:Category (Top Right)
    draw_header_box(d, 350, 155, 150, 85, 20, "catMasalas : Category", header_bg=COLOR_PRIMARY_DARK)
    d.add(String(356, 204, "id = 1", fontName='Helvetica', fontSize=7, fillColor=COLOR_TEXT_DARK))
    d.add(String(356, 192, "slug = 'masalas'", fontName='Helvetica', fontSize=7, fillColor=COLOR_TEXT_DARK))
    d.add(String(356, 180, "name = 'Masalas (Spices)'", fontName='Helvetica', fontSize=7, fillColor=COLOR_TEXT_DARK))
    d.add(String(356, 168, "icon = 'Chilli Icon'", fontName='Helvetica', fontSize=7, fillColor=COLOR_TEXT_DARK))

    # 4. activeOrder:Order (Bottom Left)
    draw_header_box(d, 20, 15, 140, 110, 20, "activeOrder : Order", header_bg=COLOR_ACCENT_RED)
    d.add(String(26, 90, "orderNumber = 'ORD-7821'", fontName='Helvetica', fontSize=7, fillColor=COLOR_TEXT_DARK))
    d.add(String(26, 78, "subtotal = Rs. 1260.00", fontName='Helvetica', fontSize=7, fillColor=COLOR_TEXT_DARK))
    d.add(String(26, 66, "cgst = Rs. 31.50 (2.5%)", fontName='Helvetica', fontSize=7, fillColor=COLOR_TEXT_DARK))
    d.add(String(26, 54, "sgst = Rs. 31.50 (2.5%)", fontName='Helvetica', fontSize=7, fillColor=COLOR_TEXT_DARK))
    d.add(String(26, 42, "total = Rs. 1323.00", fontName='Helvetica-Bold', fontSize=7, fillColor=COLOR_ACCENT_RED))
    d.add(String(26, 30, "status = 'Confirmed'", fontName='Helvetica', fontSize=7, fillColor=COLOR_ACCENT_GREEN))

    # 5. lineItem1:OrderItem (Bottom Center)
    draw_header_box(d, 185, 25, 140, 95, 20, "item1 : OrderItem", header_bg=COLOR_ACCENT_RED)
    d.add(String(191, 86, "orderId = 101", fontName='Helvetica', fontSize=7, fillColor=COLOR_TEXT_DARK))
    d.add(String(191, 74, "productId = 2 (Bedgi)", fontName='Helvetica', fontSize=7, fillColor=COLOR_TEXT_DARK))
    d.add(String(191, 62, "weight = '1 Kg'", fontName='Helvetica', fontSize=7, fillColor=COLOR_TEXT_DARK))
    d.add(String(191, 50, "quantity = 1", fontName='Helvetica', fontSize=7, fillColor=COLOR_TEXT_DARK))
    d.add(String(191, 38, "itemSubtotal = Rs. 1000.0", fontName='Helvetica', fontSize=7, fillColor=COLOR_TEXT_DARK))

    # 6. prodBedgi:Product (Bottom Right)
    draw_header_box(d, 350, 25, 150, 95, 20, "prod2 : Product", header_bg=COLOR_PRIMARY)
    d.add(String(356, 86, "name = 'Bedgi Mirchi'", fontName='Helvetica-Bold', fontSize=7, fillColor=COLOR_PRIMARY))
    d.add(String(356, 74, "price_1kg = Rs. 1000.00", fontName='Helvetica', fontSize=7, fillColor=COLOR_TEXT_DARK))
    d.add(String(356, 62, "price_250g = Rs. 260.00", fontName='Helvetica', fontSize=7, fillColor=COLOR_TEXT_DARK))
    d.add(String(356, 50, "stock_qty = 49 (deducted)", fontName='Helvetica', fontSize=7, fillColor=COLOR_ACCENT_GREEN))
    d.add(String(356, 38, "image = '2_bedgi_mirchi.jpg'", fontName='Helvetica', fontSize=7, fillColor=COLOR_TEXT_DARK))

    # Links
    draw_line(d, 90, 145, 90, 125, color=COLOR_PRIMARY, width=1.2)
    d.add(String(95, 133, "places", fontName='Helvetica-Oblique', fontSize=6.5, fillColor=COLOR_PRIMARY))

    draw_line(d, 160, 70, 185, 70, color=COLOR_ACCENT_RED, width=1.2)
    d.add(String(172, 75, "has", fontName='Helvetica-Oblique', fontSize=6.5, fillColor=COLOR_ACCENT_RED))

    draw_line(d, 325, 70, 350, 70, color=COLOR_PRIMARY, width=1.2)
    d.add(String(337, 75, "refers", fontName='Helvetica-Oblique', fontSize=6.5, fillColor=COLOR_PRIMARY))

    draw_line(d, 425, 155, 425, 120, color=COLOR_PRIMARY_DARK, width=1.2)
    d.add(String(430, 136, "categorizes", fontName='Helvetica-Oblique', fontSize=6.5, fillColor=COLOR_PRIMARY_DARK))

    return d


# ==========================================================
# 3. COMPONENT DIAGRAM BUILDER
# ==========================================================
def create_component_diagram_drawing():
    d = Drawing(520, 260)
    d.add(Rect(0, 0, 520, 260, fillColor=COLOR_BG_LIGHT, strokeColor=COLOR_BORDER, strokeWidth=0.8, rx=6, ry=6))

    def draw_uml_component(x, y, w, h, name, stereotype="<<component>>", bg_color=colors.white):
        d.add(Rect(x, y, w, h, fillColor=bg_color, strokeColor=COLOR_PRIMARY, strokeWidth=1, rx=3, ry=3))
        d.add(Rect(x - 5, y + h - 14, 10, 6, fillColor=bg_color, strokeColor=COLOR_PRIMARY, strokeWidth=0.8))
        d.add(Rect(x - 5, y + h - 26, 10, 6, fillColor=bg_color, strokeColor=COLOR_PRIMARY, strokeWidth=0.8))
        d.add(String(x + w / 2, y + h - 12, stereotype, textAnchor='middle', fontName='Helvetica-Oblique', fontSize=6.5, fillColor=COLOR_MUTED))
        d.add(String(x + w / 2, y + h - 24, name, textAnchor='middle', fontName='Helvetica-Bold', fontSize=7.5, fillColor=COLOR_PRIMARY))

    # 1. UI Component
    draw_uml_component(25, 150, 130, 80, "Client Presentation", bg_color=colors.white)
    d.add(String(32, 185, "* HTML5 & CSS3 Views", fontName='Helvetica', fontSize=6.5, fillColor=COLOR_TEXT_DARK))
    d.add(String(32, 175, "* Cart Drawer (app.js)", fontName='Helvetica', fontSize=6.5, fillColor=COLOR_TEXT_DARK))
    d.add(String(32, 165, "* Dynamic GST Bill Modal", fontName='Helvetica', fontSize=6.5, fillColor=COLOR_TEXT_DARK))

    # 2. Flask Controller
    draw_uml_component(195, 150, 130, 80, "Flask REST API (app.py)", bg_color=colors.HexColor('#EBF5FB'))
    d.add(String(202, 185, "* /api/products Endpoint", fontName='Helvetica', fontSize=6.5, fillColor=COLOR_TEXT_DARK))
    d.add(String(202, 175, "* /api/orders Endpoint", fontName='Helvetica', fontSize=6.5, fillColor=COLOR_TEXT_DARK))
    d.add(String(202, 165, "* /api/auth/login Endpoint", fontName='Helvetica', fontSize=6.5, fillColor=COLOR_TEXT_DARK))

    # 3. Business Services
    draw_uml_component(365, 150, 130, 80, "Business Logic Layer", bg_color=colors.white)
    d.add(String(372, 185, "* Stock Auto-Decrement", fontName='Helvetica', fontSize=6.5, fillColor=COLOR_TEXT_DARK))
    d.add(String(372, 175, "* 5% GST Tax Engine", fontName='Helvetica', fontSize=6.5, fillColor=COLOR_TEXT_DARK))
    d.add(String(372, 165, "* Role Authorization Guard", fontName='Helvetica', fontSize=6.5, fillColor=COLOR_TEXT_DARK))

    # 4. Data Access Component
    draw_uml_component(195, 30, 130, 75, "Data Access Layer (db.py)", bg_color=colors.HexColor('#FCF3CF'))
    d.add(String(202, 65, "* SQLite3 Row Connection", fontName='Helvetica', fontSize=6.5, fillColor=COLOR_TEXT_DARK))
    d.add(String(202, 55, "* ACID Transactions", fontName='Helvetica', fontSize=6.5, fillColor=COLOR_TEXT_DARK))
    d.add(String(202, 45, "* Prepared SQL Statements", fontName='Helvetica', fontSize=6.5, fillColor=COLOR_TEXT_DARK))

    # 5. Database Component
    draw_uml_component(365, 30, 130, 75, "SQLite Engine (db file)", bg_color=colors.white)
    d.add(String(372, 65, "* lucky_traders.db", fontName='Helvetica-Bold', fontSize=6.5, fillColor=COLOR_PRIMARY))
    d.add(String(372, 55, "* Tables, Indexes, Views", fontName='Helvetica', fontSize=6.5, fillColor=COLOR_TEXT_DARK))
    d.add(String(372, 45, "* FK Cascades & Triggers", fontName='Helvetica', fontSize=6.5, fillColor=COLOR_TEXT_DARK))

    # 6. Payment Component
    draw_uml_component(25, 30, 130, 75, "UPI Gateway Rail", bg_color=colors.HexColor('#FDEDEC'))
    d.add(String(32, 65, "* Ashwini Bramhankar QR", fontName='Helvetica', fontSize=6.5, fillColor=COLOR_ACCENT_RED))
    d.add(String(32, 55, "* ashutb1210@okhdfcbank", fontName='Helvetica', fontSize=6, fillColor=COLOR_TEXT_DARK))
    d.add(String(32, 45, "* UTR Transaction Proof", fontName='Helvetica', fontSize=6.5, fillColor=COLOR_TEXT_DARK))

    # Interfaces
    draw_line(d, 155, 190, 195, 190, color=COLOR_PRIMARY, width=1.2)
    d.add(Circle(175, 190, 3, fillColor=colors.white, strokeColor=COLOR_PRIMARY, strokeWidth=1))
    d.add(String(175, 198, "HTTP/REST", textAnchor='middle', fontName='Helvetica', fontSize=6.5, fillColor=COLOR_PRIMARY))

    draw_line(d, 325, 190, 365, 190, color=COLOR_PRIMARY, width=1.2)
    d.add(Circle(345, 190, 3, fillColor=colors.white, strokeColor=COLOR_PRIMARY, strokeWidth=1))
    d.add(String(345, 198, "IPC / Call", textAnchor='middle', fontName='Helvetica', fontSize=6.5, fillColor=COLOR_PRIMARY))

    draw_line(d, 260, 150, 260, 105, color=COLOR_PRIMARY, width=1.2)
    d.add(Circle(260, 127, 3, fillColor=colors.white, strokeColor=COLOR_PRIMARY, strokeWidth=1))
    d.add(String(280, 125, "db.* API", fontName='Helvetica', fontSize=6.5, fillColor=COLOR_PRIMARY))

    draw_line(d, 325, 67, 365, 67, color=COLOR_PRIMARY, width=1.2)
    d.add(Circle(345, 67, 3, fillColor=colors.white, strokeColor=COLOR_PRIMARY, strokeWidth=1))
    d.add(String(345, 75, "SQL / IO", textAnchor='middle', fontName='Helvetica', fontSize=6.5, fillColor=COLOR_PRIMARY))

    draw_line(d, 90, 150, 90, 105, color=COLOR_ACCENT_RED, width=1.2, dashed=True)
    d.add(String(112, 125, "QR Deep-Link", fontName='Helvetica', fontSize=6.5, fillColor=COLOR_ACCENT_RED))

    return d


# ==========================================================
# 4. DEPLOYMENT DIAGRAM BUILDER
# ==========================================================
def create_deployment_diagram_drawing():
    d = Drawing(520, 260)
    d.add(Rect(0, 0, 520, 260, fillColor=COLOR_BG_LIGHT, strokeColor=COLOR_BORDER, strokeWidth=0.8, rx=6, ry=6))

    def draw_3d_node(x, y, w, h, name, stereotype="<<device>>", depth=12, bg_color=colors.white):
        d.add(Rect(x, y, w, h, fillColor=bg_color, strokeColor=COLOR_PRIMARY, strokeWidth=1))
        d.add(Polygon([x, y + h, x + depth, y + h + depth, x + w + depth, y + h + depth, x + w, y + h],
                      fillColor=colors.HexColor('#EAEDED'), strokeColor=COLOR_PRIMARY, strokeWidth=1))
        d.add(Polygon([x + w, y, x + w + depth, y + depth, x + w + depth, y + h + depth, x + w, y + h],
                      fillColor=colors.HexColor('#D5D8DC'), strokeColor=COLOR_PRIMARY, strokeWidth=1))
        d.add(String(x + w / 2, y + h - 14, stereotype, textAnchor='middle', fontName='Helvetica-Oblique', fontSize=6.5, fillColor=COLOR_MUTED))
        d.add(String(x + w / 2, y + h - 25, name, textAnchor='middle', fontName='Helvetica-Bold', fontSize=8, fillColor=COLOR_PRIMARY))

    # Node 1: Client Machine (Left)
    draw_3d_node(15, 80, 125, 130, "Client Device", stereotype="<<device>> Client PC/Mobile")
    draw_rounded_box(d, 22, 92, 111, 70, bg_color=colors.HexColor('#F4F6F7'), stroke_color=COLOR_BORDER)
    d.add(String(28, 148, "<<execution environment>>", fontName='Helvetica-Oblique', fontSize=6, fillColor=COLOR_MUTED))
    d.add(String(28, 138, "Web Browser (Edge/Chrome)", fontName='Helvetica-Bold', fontSize=6.5, fillColor=COLOR_PRIMARY))
    d.add(Rect(26, 100, 103, 26, fillColor=colors.white, strokeColor=COLOR_BORDER, strokeWidth=0.5))
    d.add(String(30, 114, "[artifact] Web Client Bundle", fontName='Helvetica', fontSize=6, fillColor=COLOR_TEXT_DARK))
    d.add(String(30, 105, "(HTML5, CSS3, JS App)", fontName='Helvetica', fontSize=5.5, fillColor=COLOR_MUTED))

    # Node 2: Web / Application Server (Center)
    draw_3d_node(185, 60, 150, 160, "App Server Node", stereotype="<<device>> Host / Server")
    draw_rounded_box(d, 193, 72, 134, 102, bg_color=colors.HexColor('#EBF5FB'), stroke_color=COLOR_BORDER)
    d.add(String(198, 160, "<<execution environment>>", fontName='Helvetica-Oblique', fontSize=6, fillColor=COLOR_MUTED))
    d.add(String(198, 150, "Python 3.13 Runtime & Flask", fontName='Helvetica-Bold', fontSize=6.5, fillColor=COLOR_PRIMARY))
    d.add(Rect(198, 118, 124, 24, fillColor=colors.white, strokeColor=COLOR_BORDER, strokeWidth=0.5))
    d.add(String(202, 131, "[artifact] app.py", fontName='Helvetica-Bold', fontSize=6.5, fillColor=COLOR_PRIMARY))
    d.add(String(202, 122, "Flask WSGI REST Controller", fontName='Helvetica', fontSize=5.5, fillColor=COLOR_MUTED))
    d.add(Rect(198, 82, 124, 24, fillColor=colors.white, strokeColor=COLOR_BORDER, strokeWidth=0.5))
    d.add(String(202, 95, "[artifact] db.py", fontName='Helvetica-Bold', fontSize=6.5, fillColor=COLOR_PRIMARY))
    d.add(String(202, 86, "Relational SQL Data Layer", fontName='Helvetica', fontSize=5.5, fillColor=COLOR_MUTED))

    # Node 3: Database Storage (Right)
    draw_3d_node(380, 80, 125, 130, "Database System", stereotype="<<device>> File System")
    draw_rounded_box(d, 387, 92, 111, 70, bg_color=colors.HexColor('#FCF3CF'), stroke_color=COLOR_BORDER)
    d.add(String(392, 148, "<<execution environment>>", fontName='Helvetica-Oblique', fontSize=6, fillColor=COLOR_MUTED))
    d.add(String(392, 138, "SQLite Relational Engine", fontName='Helvetica-Bold', fontSize=6.5, fillColor=COLOR_PRIMARY))
    d.add(Rect(391, 100, 103, 26, fillColor=colors.white, strokeColor=COLOR_BORDER, strokeWidth=0.5))
    d.add(String(395, 114, "[artifact] lucky_traders.db", fontName='Helvetica-Bold', fontSize=6, fillColor=COLOR_PRIMARY))
    d.add(String(395, 105, "ACID Relational Storage", fontName='Helvetica', fontSize=5.5, fillColor=COLOR_MUTED))

    # Communication Links with wide clear spacing
    draw_line(d, 140, 145, 185, 145, color=COLOR_PRIMARY, width=1.5)
    d.add(String(162, 153, "HTTP/REST", textAnchor='middle', fontName='Helvetica-Bold', fontSize=6.5, fillColor=COLOR_PRIMARY))
    d.add(String(162, 135, "Port 5000", textAnchor='middle', fontName='Helvetica', fontSize=6, fillColor=COLOR_MUTED))

    draw_line(d, 335, 145, 380, 145, color=COLOR_PRIMARY, width=1.5)
    d.add(String(358, 153, "OS File I/O", textAnchor='middle', fontName='Helvetica-Bold', fontSize=6.5, fillColor=COLOR_PRIMARY))
    d.add(String(358, 135, "POSIX Locks", textAnchor='middle', fontName='Helvetica', fontSize=6, fillColor=COLOR_MUTED))

    # Protocol summary card bottom
    draw_rounded_box(d, 15, 15, 490, 32, bg_color=colors.white, stroke_color=COLOR_BORDER)
    d.add(String(24, 34, "DEPLOYMENT PROTOCOLS & SYSTEM CONFIGURATION:", fontName='Helvetica-Bold', fontSize=7, fillColor=COLOR_PRIMARY))
    d.add(String(24, 22, "* Client-Server: TCP/IP Socket, HTTP/1.1 JSON REST API, Port 5000 (Local / Intranet / Cloud)", fontName='Helvetica', fontSize=6.5, fillColor=COLOR_TEXT_DARK))
    d.add(String(315, 22, "* Storage: Zero-config in-process C-Engine (SQLite3), lucky_traders.db", fontName='Helvetica', fontSize=6.5, fillColor=COLOR_TEXT_DARK))

    return d


# ==========================================================
# 5. USE CASE DIAGRAM BUILDER
# ==========================================================
def create_use_case_diagram_drawing():
    d = Drawing(520, 270)
    d.add(Rect(0, 0, 520, 270, fillColor=COLOR_BG_LIGHT, strokeColor=COLOR_BORDER, strokeWidth=0.8, rx=6, ry=6))

    # Boundary box
    d.add(Rect(110, 10, 300, 250, fillColor=colors.white, strokeColor=COLOR_PRIMARY, strokeWidth=1, rx=4, ry=4))
    d.add(String(260, 248, "Lucky Traders Web System", textAnchor='middle', fontName='Helvetica-Bold', fontSize=9, fillColor=COLOR_PRIMARY))

    def draw_actor(x, y, name):
        d.add(Circle(x, y + 25, 7, fillColor=colors.HexColor('#FDEDEC'), strokeColor=COLOR_PRIMARY, strokeWidth=1))
        d.add(Line(x, y + 18, x, y, strokeColor=COLOR_PRIMARY, strokeWidth=1))
        d.add(Line(x - 12, y + 10, x + 12, y + 10, strokeColor=COLOR_PRIMARY, strokeWidth=1))
        d.add(Line(x, y, x - 9, y - 14, strokeColor=COLOR_PRIMARY, strokeWidth=1))
        d.add(Line(x, y, x + 9, y - 14, strokeColor=COLOR_PRIMARY, strokeWidth=1))
        d.add(String(x, y - 24, name, textAnchor='middle', fontName='Helvetica-Bold', fontSize=7.5, fillColor=COLOR_PRIMARY))

    def draw_uc_oval(x, y, w, h, text):
        d.add(Ellipse(x, y, w / 2, h / 2, fillColor=colors.HexColor('#EBF5FB'), strokeColor=COLOR_PRIMARY, strokeWidth=0.8))
        d.add(String(x, y - 2.5, text, textAnchor='middle', fontName='Helvetica', fontSize=6.5, fillColor=COLOR_TEXT_DARK))

    # Actors
    draw_actor(55, 170, "Customer / User")
    draw_actor(55, 60, "Registered User")
    draw_actor(465, 170, "Store Admin")
    draw_actor(465, 60, "Payment Gateway")

    # Use cases
    draw_uc_oval(260, 225, 150, 20, "Browse Categories & Catalog")
    draw_uc_oval(260, 195, 150, 20, "Select Weight (1kg / 250g)")
    draw_uc_oval(260, 165, 140, 20, "Manage Shopping Basket")
    draw_uc_oval(260, 135, 150, 20, "Checkout & Compute GST (5%)")
    draw_uc_oval(260, 105, 140, 20, "Pay via UPI QR / Cash on Del")
    draw_uc_oval(260, 75, 140, 20, "View Itemized Tax Invoice")
    draw_uc_oval(260, 45, 150, 20, "Manage Products & Inventory")
    draw_uc_oval(260, 20, 150, 20, "View Orders & Sales Reports")

    # Connectors
    draw_line(d, 70, 180, 185, 225, color=COLOR_PRIMARY, width=0.8)
    draw_line(d, 70, 180, 185, 195, color=COLOR_PRIMARY, width=0.8)
    draw_line(d, 70, 175, 190, 165, color=COLOR_PRIMARY, width=0.8)
    draw_line(d, 70, 170, 185, 135, color=COLOR_PRIMARY, width=0.8)
    draw_line(d, 70, 165, 190, 105, color=COLOR_PRIMARY, width=0.8)
    draw_line(d, 70, 160, 190, 75, color=COLOR_PRIMARY, width=0.8)

    draw_line(d, 450, 170, 335, 45, color=COLOR_PRIMARY, width=0.8)
    draw_line(d, 450, 165, 335, 20, color=COLOR_PRIMARY, width=0.8)
    draw_line(d, 450, 180, 335, 75, color=COLOR_PRIMARY, width=0.8)

    draw_line(d, 450, 65, 330, 105, color=COLOR_ACCENT_RED, width=0.8, dashed=True)
    d.add(String(390, 92, "<<verifies>>", textAnchor='middle', fontName='Helvetica-Oblique', fontSize=6, fillColor=COLOR_ACCENT_RED))

    return d


# ==========================================================
# 6. ACTIVITY DIAGRAM BUILDER
# ==========================================================
def create_activity_diagram_drawing():
    d = Drawing(520, 280)
    d.add(Rect(0, 0, 520, 280, fillColor=COLOR_BG_LIGHT, strokeColor=COLOR_BORDER, strokeWidth=0.8, rx=6, ry=6))

    lane_w = 520 / 3
    # Lane 1
    d.add(Rect(0, 0, lane_w, 280, fillColor=colors.HexColor('#FFFFFF'), strokeColor=COLOR_BORDER, strokeWidth=0.5))
    d.add(Rect(0, 260, lane_w, 20, fillColor=COLOR_PRIMARY, strokeColor=COLOR_BORDER, strokeWidth=0.5))
    d.add(String(lane_w / 2, 266, "CUSTOMER / BROWSER", textAnchor='middle', fontName='Helvetica-Bold', fontSize=7.5, fillColor=colors.white))

    # Lane 2
    d.add(Rect(lane_w, 0, lane_w, 280, fillColor=colors.HexColor('#F4F6F7'), strokeColor=COLOR_BORDER, strokeWidth=0.5))
    d.add(Rect(lane_w, 260, lane_w, 20, fillColor=COLOR_PRIMARY_DARK, strokeColor=COLOR_BORDER, strokeWidth=0.5))
    d.add(String(lane_w + lane_w / 2, 266, "FLASK CONTROLLER (app.py)", textAnchor='middle', fontName='Helvetica-Bold', fontSize=7.5, fillColor=colors.white))

    # Lane 3
    d.add(Rect(lane_w * 2, 0, lane_w, 280, fillColor=colors.HexColor('#FFFFFF'), strokeColor=COLOR_BORDER, strokeWidth=0.5))
    d.add(Rect(lane_w * 2, 260, lane_w, 20, fillColor=COLOR_PRIMARY, strokeColor=COLOR_BORDER, strokeWidth=0.5))
    d.add(String(lane_w * 2 + lane_w / 2, 266, "DATABASE (db.py / SQLite)", textAnchor='middle', fontName='Helvetica-Bold', fontSize=7.5, fillColor=colors.white))

    def draw_action(x, y, w, h, text, bg_color=colors.HexColor('#EBF5FB')):
        d.add(Rect(x, y, w, h, fillColor=bg_color, strokeColor=COLOR_PRIMARY, strokeWidth=0.8, rx=5, ry=5))
        d.add(String(x + w / 2, y + h / 2 - 2.5, text, textAnchor='middle', fontName='Helvetica', fontSize=6.5, fillColor=COLOR_TEXT_DARK))

    def draw_diamond(cx, cy, w, h, text):
        hw = w / 2
        hh = h / 2
        d.add(Polygon([cx, cy + hh, cx + hw, cy, cx, cy - hh, cx - hw, cy],
                      fillColor=colors.HexColor('#FCF3CF'), strokeColor=COLOR_PRIMARY, strokeWidth=0.8))
        d.add(String(cx, cy - 2.5, text, textAnchor='middle', fontName='Helvetica-Bold', fontSize=6, fillColor=COLOR_PRIMARY))

    # Initial Node
    d.add(Circle(86, 240, 6, fillColor=COLOR_PRIMARY, strokeColor=COLOR_PRIMARY, strokeWidth=1))
    draw_arrow(d, 86, 234, 86, 218, arrow_style="open")

    # Step 1
    draw_action(20, 192, 133, 24, "Browse Catalog & Select Weight")
    draw_arrow(d, 86, 192, 86, 175, arrow_style="open")

    # Step 2
    draw_action(20, 150, 133, 24, "Add to Basket & Click Checkout")
    draw_arrow(d, 153, 162, 200, 162, arrow_style="open")

    # Step 3
    draw_action(195, 150, 130, 24, "Calculate Subtotal + 5% GST")
    draw_arrow(d, 325, 162, 370, 162, arrow_style="open")

    # Step 4
    draw_action(370, 150, 130, 24, "SQL: SELECT stock_qty")
    draw_arrow(d, 435, 150, 435, 132, arrow_style="open")

    # Decision: In Stock?
    draw_diamond(435, 115, 46, 28, "In Stock?")
    draw_arrow(d, 435, 101, 435, 80, label="Yes", arrow_style="open")

    # Branch No -> Back to Customer
    draw_line(d, 412, 115, 86, 115, color=COLOR_ACCENT_RED, width=0.8, dashed=True)
    draw_arrow(d, 86, 115, 86, 150, label="No (Alert)", arrow_style="open", color=COLOR_ACCENT_RED)

    # Step 5
    draw_action(195, 70, 130, 24, "Verify Payment (UPI / COD)")
    draw_arrow(d, 370, 70, 325, 70, arrow_style="open")

    # Step 6
    draw_action(370, 56, 130, 24, "COMMIT Order & Auto-Decr Stock")
    draw_arrow(d, 260, 70, 370, 68, arrow_style="open")

    # Step 7
    draw_arrow(d, 370, 56, 153, 56, arrow_style="open")
    draw_action(20, 44, 133, 24, "Render GST Invoice Modal")
    draw_arrow(d, 86, 44, 86, 26, arrow_style="open")

    # Final Node
    d.add(Circle(86, 16, 7, fillColor=colors.white, strokeColor=COLOR_PRIMARY, strokeWidth=1))
    d.add(Circle(86, 16, 4, fillColor=COLOR_PRIMARY, strokeColor=COLOR_PRIMARY, strokeWidth=1))

    return d


# ==========================================================
# 7. SEQUENCE DIAGRAM BUILDER
# ==========================================================
def create_sequence_diagram_drawing():
    d = Drawing(520, 280)
    d.add(Rect(0, 0, 520, 280, fillColor=COLOR_BG_LIGHT, strokeColor=COLOR_BORDER, strokeWidth=0.8, rx=6, ry=6))

    lifelines = [
        ("Customer", 50),
        ("Browser UI", 150),
        ("app.py (REST API)", 260),
        ("db.py (Data Layer)", 375),
        ("SQLite DB", 475)
    ]

    for name, x in lifelines:
        draw_rounded_box(d, x - 38, 245, 76, 24, bg_color=COLOR_PRIMARY, stroke_color=COLOR_PRIMARY)
        d.add(String(x, 256, name, textAnchor='middle', fontName='Helvetica-Bold', fontSize=6.5, fillColor=colors.white))
        draw_line(d, x, 245, x, 25, color=COLOR_BORDER, width=0.8, dashed=True)

    def draw_activation(x, y, h):
        d.add(Rect(x - 4, y, 8, h, fillColor=colors.HexColor('#EAEDED'), strokeColor=COLOR_PRIMARY, strokeWidth=0.6))

    draw_activation(150, 45, 190)
    draw_activation(260, 60, 165)
    draw_activation(375, 75, 135)
    draw_activation(475, 90, 105)

    y = 230
    draw_arrow(d, 50, y, 150, y, label="1: selectWeight('1 Kg'), addCart()", arrow_style="normal", label_y_offset=4)

    y -= 25
    draw_arrow(d, 50, y, 150, y, label="2: submitOrderForm(shippingDetails)", arrow_style="normal", label_y_offset=4)

    y -= 25
    draw_arrow(d, 150, y, 260, y, label="3: POST /api/orders (JSON payload)", arrow_style="normal", label_y_offset=4)

    y -= 25
    draw_arrow(d, 260, y, 375, y, label="4: db.create_order(items, details)", arrow_style="normal", label_y_offset=4)

    y -= 25
    draw_arrow(d, 375, y, 475, y, label="5: SQL: INSERT orders, items; UPDATE stock", arrow_style="normal", label_y_offset=4)

    y -= 25
    draw_arrow(d, 475, y, 375, y, label="6: Transaction Committed (ACID OK)", arrow_style="open", dashed=True, label_y_offset=4)

    y -= 25
    draw_arrow(d, 375, y, 260, y, label="7: Return order_number & totals", arrow_style="open", dashed=True, label_y_offset=4)

    y -= 25
    draw_arrow(d, 260, y, 150, y, label="8: HTTP 201 {success: true, order: {...}}", arrow_style="open", dashed=True, label_y_offset=4)

    y -= 25
    draw_arrow(d, 150, y, 50, y, label="9: Display Printable GST Bill Modal", arrow_style="open", dashed=True, label_y_offset=4)

    return d


# ==========================================================
# PDF DOCUMENT BUILDER
# ==========================================================
def build_uml_diagrams_pdf(output_pdf_path):
    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=45,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()

    style_title = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=COLOR_PRIMARY_DARK,
        alignment=1,
        spaceAfter=8
    )

    style_subtitle = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=COLOR_ACCENT_RED,
        alignment=1,
        spaceAfter=20
    )

    style_heading = ParagraphStyle(
        'SecHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=COLOR_PRIMARY,
        spaceBefore=14,
        spaceAfter=6
    )

    style_body = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=COLOR_TEXT_DARK,
        spaceAfter=6
    )

    story = []

    # ==========================================================
    # COVER / TITLE PAGE
    # ==========================================================
    story.append(Spacer(1, 40))
    story.append(Paragraph("LUCKY TRADERS", style_title))
    story.append(Paragraph("Unified Modeling Language (UML) & System Architectural Specification", style_subtitle))
    story.append(HRFlowable(width="100%", thickness=2, color=COLOR_ACCENT_RED, spaceBefore=5, spaceAfter=20))

    cover_meta = [
        [Paragraph("<b>Course / Syllabus:</b>", style_body), Paragraph("SPPU Final Year Computer Engineering - Project CS331FP", style_body)],
        [Paragraph("<b>Project Title:</b>", style_body), Paragraph("Lucky Traders - Authentic Spices, Chutneys & Pickles Web Portal", style_body)],
        [Paragraph("<b>Architecture:</b>", style_body), Paragraph("3-Tier Web Architecture (Client UI + Flask WSGI + SQLite RDBMS)", style_body)],
        [Paragraph("<b>Backend Runtime:</b>", style_body), Paragraph("Python 3.13 / Flask 3.1 RESTful Web Framework", style_body)],
        [Paragraph("<b>Database:</b>", style_body), Paragraph("SQLite3 Relational Engine (lucky_traders.db) with ACID Transactions", style_body)],
        [Paragraph("<b>Payment Gateway:</b>", style_body), Paragraph("Ashwini Bramhankar UPI (ashutb1210@okhdfcbank) & Cash on Delivery", style_body)],
        [Paragraph("<b>Documentation Scope:</b>", style_body), Paragraph("Complete UML 2.5 Specification (8 Structural & Behavioral Diagrams)", style_body)],
        [Paragraph("<b>Verification:</b>", style_body), Paragraph("Automated Python unittest Suite (8/8 Verified Tests Passing)", style_body)]
    ]

    t_meta = Table(cover_meta, colWidths=[140, 380])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), COLOR_BG_LIGHT),
        ('BOX', (0, 0), (-1, -1), 1, COLOR_BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 25))

    summary_text = (
        "<b>Executive Architectural Summary:</b><br/>"
        "This document contains the official architectural design and UML diagrams for the Lucky Traders e-commerce "
        "system as required by the University Project Curriculum. The system implements a full-stack, responsive web application "
        "with dual packaging selection (1 Kg vs 250 Gm), atomic inventory auto-decrement, dynamic itemized GST bill computation, "
        "role-based authentication (Customer vs Administrator), and direct UPI merchant payment integration. All 8 diagrams adhere "
        "to formal UML 2.5 standards and accurately model the physical implementation in Python and SQLite."
    )
    t_summary = Table([[Paragraph(summary_text, style_body)]], colWidths=[520])
    t_summary.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#EBF5FB')),
        ('BOX', (0, 0), (-1, -1), 1, COLOR_PRIMARY),
        ('PADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(t_summary)
    story.append(PageBreak())

    # ==========================================================
    # 0. ER DIAGRAM
    # ==========================================================
    story.append(Paragraph("0. Entity-Relationship (ER) Diagram", style_heading))
    story.append(Paragraph(
        "The Entity-Relationship Diagram models the persistent relational data structure of the SQLite database "
        "(<code>lucky_traders.db</code>). It captures entities, primary/foreign keys, and relational cardinalities (1:N and M:N).",
        style_body
    ))
    story.append(create_er_diagram_drawing())
    story.append(Spacer(1, 10))

    er_table_data = [
        ["Entity", "Primary Key", "Foreign Keys", "Cardinality & Description"],
        ["USERS", "id (INTEGER)", "None", "1:N with ORDERS. Stores customer and administrator credentials."],
        ["CATEGORIES", "id (INTEGER)", "None", "1:N with PRODUCTS. Hierarchical grouping (Masalas, Chutneys, Pickles)."],
        ["PRODUCTS", "id (INTEGER)", "category_id -> CATEGORIES.id", "1:N with ORDER_ITEMS. Stores pricing for 1kg and 250g, and stock_qty."],
        ["ORDERS", "id (INTEGER)", "user_id -> USERS.id (optional)", "1:N with ORDER_ITEMS. Contains subtotal, 2.5% CGST, 2.5% SGST, total."],
        ["ORDER_ITEMS", "id (INTEGER)", "order_id -> ORDERS.id, product_id -> PRODUCTS.id", "Associative table resolving M:N between ORDERS and PRODUCTS."]
    ]
    t_er = Table([[Paragraph(f"<b>{c}</b>", style_body) if i == 0 else Paragraph(c, style_body) for c in row] for i, row in enumerate(er_table_data)], colWidths=[85, 80, 155, 200])
    t_er.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_BOX_HEADER),
        ('BOX', (0, 0), (-1, -1), 0.8, COLOR_BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_er)
    story.append(PageBreak())

    # ==========================================================
    # 1. CLASS DIAGRAM
    # ==========================================================
    story.append(Paragraph("1. Class Diagram", style_heading))
    story.append(Paragraph(
        "The Class Diagram specifies the object-oriented structure of the backend application services, domain entities, "
        "and data access controllers. It illustrates inheritance, composition, and associations.",
        style_body
    ))
    story.append(create_class_diagram_drawing())
    story.append(Spacer(1, 10))

    class_notes = (
        "<b>Design Pattern & OOP Principles:</b><br/>"
        "* <b>Generalization:</b> <code>Customer</code> and <code>Administrator</code> inherit from the base <code>User</code> class.<br/>"
        "* <b>Composition:</b> <code>Order</code> strongly composes <code>OrderItem</code> (1 to 1..*); line items cannot exist without an order.<br/>"
        "* <b>Aggregation:</b> <code>Category</code> aggregates <code>Product</code> instances (1 to *).<br/>"
        "* <b>Encapsulation:</b> Stock decrement is encapsulated in <code>Product.decrementStock()</code> and executed atomically in SQL."
    )
    t_class = Table([[Paragraph(class_notes, style_body)]], colWidths=[520])
    t_class.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), COLOR_BG_LIGHT),
        ('BOX', (0, 0), (-1, -1), 0.8, COLOR_BORDER),
        ('PADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_class)
    story.append(PageBreak())

    # ==========================================================
    # 2. OBJECT DIAGRAM
    # ==========================================================
    story.append(Paragraph("2. Object Diagram", style_heading))
    story.append(Paragraph(
        "The Object Diagram represents a concrete runtime snapshot of the system during an active customer transaction. "
        "It depicts instantiated objects, their bound attribute values, and execution links.",
        style_body
    ))
    story.append(create_object_diagram_drawing())
    story.append(Spacer(1, 10))

    obj_notes = (
        "<b>Runtime State Analysis (Order ORD-7821 Execution Snapshot):</b><br/>"
        "* <code>customer:Customer</code> (id=2, 'User') has authenticated and placed <code>activeOrder:Order</code>.<br/>"
        "* The order references <code>item1:OrderItem</code> containing 1 unit of <code>prod2:Product</code> (Bedgi Mirchi Powder, 1 Kg, Rs. 1000).<br/>"
        "* Total tax is computed at 5% (CGST: Rs. 31.50, SGST: Rs. 31.50), resulting in Rs. 1323.00.<br/>"
        "* Product stock is atomically decremented from 50 to 49 upon confirmation."
    )
    t_obj = Table([[Paragraph(obj_notes, style_body)]], colWidths=[520])
    t_obj.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), COLOR_BG_LIGHT),
        ('BOX', (0, 0), (-1, -1), 0.8, COLOR_BORDER),
        ('PADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_obj)
    story.append(PageBreak())

    # ==========================================================
    # 3. COMPONENT DIAGRAM
    # ==========================================================
    story.append(Paragraph("3. Component Diagram", style_heading))
    story.append(Paragraph(
        "The Component Diagram models the high-level modular software architecture, provided/required interfaces, "
        "and physical software components comprising the client and server.",
        style_body
    ))
    story.append(create_component_diagram_drawing())
    story.append(Spacer(1, 10))

    comp_table_data = [
        ["Component", "Type", "Interface Provided / Consumed", "Responsibility"],
        ["Client Presentation", "Frontend Client", "Consumes /api/* REST Endpoints", "UI rendering, cart state, dynamic invoice printing, modal handling."],
        ["Flask REST API (app.py)", "Web Controller", "Provides HTTP RESTful Endpoints", "Route dispatching, CORS, payload validation, status response codes."],
        ["Business Logic Layer", "Service Domain", "Stock & Tax Computation APIs", "Auto-decrementing stock, 5% GST computation, role authorization."],
        ["Data Access Layer (db.py)", "Database Client", "Provides db.* Python Functions", "Connection pooling, row factory, prepared statements, ACID transactions."],
        ["SQLite Storage", "Relational Engine", "Consumes OS File I/O & Locks", "ACID compliant disk storage (lucky_traders.db)."]
    ]
    t_comp = Table([[Paragraph(f"<b>{c}</b>", style_body) if i == 0 else Paragraph(c, style_body) for c in row] for i, row in enumerate(comp_table_data)], colWidths=[100, 75, 145, 200])
    t_comp.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_BOX_HEADER),
        ('BOX', (0, 0), (-1, -1), 0.8, COLOR_BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_comp)
    story.append(PageBreak())

    # ==========================================================
    # 4. DEPLOYMENT DIAGRAM
    # ==========================================================
    story.append(Paragraph("4. Deployment Diagram", style_heading))
    story.append(Paragraph(
        "The Deployment Diagram models the physical hardware and execution environment nodes, runtime artifacts, "
        "and network protocols required to execute Lucky Traders in development and production.",
        style_body
    ))
    story.append(create_deployment_diagram_drawing())
    story.append(Spacer(1, 10))

    dep_notes = (
        "<b>Deployment Topology & Node Specifications:</b><br/>"
        "* <b>Client Device Node:</b> Any modern web browser running on Windows/Linux/macOS or mobile devices. Communicates via HTTP/1.1 or HTTP/2 over TCP/IP.<br/>"
        "* <b>Application Server Node:</b> Python 3.13 runtime hosting Flask WSGI server on port 5000. Deploys <code>app.py</code> and <code>db.py</code>.<br/>"
        "* <b>Database System:</b> SQLite embedded in-process database engine writing to local disk file <code>lucky_traders.db</code> with POSIX/Win32 file locks."
    )
    t_dep = Table([[Paragraph(dep_notes, style_body)]], colWidths=[520])
    t_dep.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), COLOR_BG_LIGHT),
        ('BOX', (0, 0), (-1, -1), 0.8, COLOR_BORDER),
        ('PADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_dep)
    story.append(PageBreak())

    # ==========================================================
    # 5. USE CASE DIAGRAM
    # ==========================================================
    story.append(Paragraph("5. Use Case Diagram", style_heading))
    story.append(Paragraph(
        "The Use Case Diagram defines functional requirements from the perspective of primary actors (Customer, "
        "Administrator, and Payment Gateway), showing system boundary and use case relationships.",
        style_body
    ))
    story.append(create_use_case_diagram_drawing())
    story.append(Spacer(1, 10))

    uc_table_data = [
        ["Actor", "Role Classification", "Associated Key Use Cases"],
        ["Customer (Guest / User)", "Primary External Actor", "Browse catalog, select packaging (1kg/250g), manage cart, checkout, scan UPI QR, print bill."],
        ["Store Administrator", "Primary Internal Actor", "Manage catalog products, adjust stock quantities, view orders, update dispatch status, view reports."],
        ["Payment Gateway (UPI)", "Secondary External Actor", "Receive deep-link intent, authenticate banking PIN, return transaction UTR confirmation."]
    ]
    t_uc = Table([[Paragraph(f"<b>{c}</b>", style_body) if i == 0 else Paragraph(c, style_body) for c in row] for i, row in enumerate(uc_table_data)], colWidths=[100, 110, 310])
    t_uc.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_BOX_HEADER),
        ('BOX', (0, 0), (-1, -1), 0.8, COLOR_BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_uc)
    story.append(PageBreak())

    # ==========================================================
    # 6. ACTIVITY DIAGRAM
    # ==========================================================
    story.append(Paragraph("6. Activity Diagram", style_heading))
    story.append(Paragraph(
        "The Activity Diagram models the step-by-step business process flow for product selection, stock verification, "
        "tax calculation, and order processing across three swimlanes (Customer, Controller, Database).",
        style_body
    ))
    story.append(create_activity_diagram_drawing())
    story.append(Spacer(1, 10))

    act_notes = (
        "<b>Swimlane Execution & Transactional Flow:</b><br/>"
        "* <b>Customer Swimlane:</b> Initiates selection, provides shipping credentials, and reviews final bill.<br/>"
        "* <b>Controller Swimlane:</b> Performs validation, computes 2.5% CGST + 2.5% SGST, and routes payment confirmations.<br/>"
        "* <b>Database Swimlane:</b> Executes atomic transactions. If stock is available, <code>stock_qty</code> is decremented and order is committed."
    )
    t_act = Table([[Paragraph(act_notes, style_body)]], colWidths=[520])
    t_act.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), COLOR_BG_LIGHT),
        ('BOX', (0, 0), (-1, -1), 0.8, COLOR_BORDER),
        ('PADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_act)
    story.append(PageBreak())

    # ==========================================================
    # 7. SEQUENCE DIAGRAM
    # ==========================================================
    story.append(Paragraph("7. Sequence Diagram", style_heading))
    story.append(Paragraph(
        "The Sequence Diagram captures chronological interactions and synchronous/asynchronous message exchanges "
        "between actors, UI components, REST controllers, and database lifelines during order placement.",
        style_body
    ))
    story.append(create_sequence_diagram_drawing())
    story.append(Spacer(1, 10))

    seq_table_data = [
        ["Step #", "Sender -> Receiver", "Message Signature / Operation", "Description"],
        ["1", "Customer -> UI", "selectWeight('1 Kg'), addCart()", "User chooses packaging weight and updates browser cart."],
        ["2", "Customer -> UI", "submitOrderForm(shippingDetails)", "Submits name, phone, address, and payment method."],
        ["3", "UI -> app.py", "POST /api/orders (JSON payload)", "Asynchronous fetch API request with line items."],
        ["4", "app.py -> db.py", "create_order(items, details)", "Invokes Python database transaction manager."],
        ["5", "db.py -> SQLite", "INSERT orders; UPDATE products", "Executes atomic SQL transaction with stock deduction."],
        ["6-8", "SQLite -> UI", "HTTP 201 Created {order: {...}}", "Returns confirmed order number, tax totals, and items."],
        ["9", "UI -> Customer", "renderBillModal(order)", "Displays printable GST tax invoice with order confirmation."]
    ]
    t_seq = Table([[Paragraph(f"<b>{c}</b>", style_body) if i == 0 else Paragraph(c, style_body) for c in row] for i, row in enumerate(seq_table_data)], colWidths=[40, 110, 170, 200])
    t_seq.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_BOX_HEADER),
        ('BOX', (0, 0), (-1, -1), 0.8, COLOR_BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_seq)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated academic PDF: {output_pdf_path}")


if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.abspath(__file__))
    target_pdf = os.path.join(base_dir, "PROJECT_UML_DIAGRAMS.pdf")
    build_uml_diagrams_pdf(target_pdf)
