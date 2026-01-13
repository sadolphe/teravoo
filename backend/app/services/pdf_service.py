from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
import datetime

class PdfService:
    def generate_contract(self, request_data: dict, offers_data: list) -> bytes:
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        
        # Header
        c.setFont("Helvetica-Bold", 18)
        c.drawString(100, 750, "TERAVOO - PURCHASE AGREEMENT")
        
        c.setFont("Helvetica", 12)
        c.drawString(100, 730, f"Contract Reference: REQ-{request_data.get('id')}")
        c.drawString(100, 715, f"Date: {datetime.datetime.now().strftime('%Y-%m-%d')}")
        
        # Buyer Section
        c.drawString(100, 680, "BUYER:")
        c.drawString(120, 665, f"Buyer ID: {request_data.get('buyer_id')}")
        c.drawString(120, 650, "Represented by: Sarah Import Corp") # Mock
        
        # Product Section
        c.drawString(100, 620, "PRODUCT SPECIFICATIONS:")
        c.drawString(120, 605, f"Product: {request_data.get('product_type')}")
        c.drawString(120, 590, f"Grade: {request_data.get('grade_target')}")
        c.drawString(120, 575, f"Total Volume: {request_data.get('volume_target_kg')} kg")
        
        # Sellers Section
        c.drawString(100, 540, "AGREED SELLERS (ANNEX A):")
        y = 520
        total_vol = 0
        total_price = 0
        
        c.setFont("Helvetica", 10)
        c.drawString(100, y, "Facilitator ID | Volume (kg) | Price (USD) | Status")
        y -= 15
        
        for offer in offers_data:
            c.drawString(100, y, f"{offer.get('facilitator_id')}             | {offer.get('volume_offered_kg')}          | ${offer.get('price_offered_usd')}      | {offer.get('status')}")
            total_vol += offer.get('volume_offered_kg')
            total_price += (offer.get('volume_offered_kg') * offer.get('price_offered_usd'))
            y -= 15
        
        c.setFont("Helvetica-Bold", 12)
        y -= 20
        c.drawString(100, y, f"TOTAL VALUE (FOB): ${total_price:,.2f}")
        
        # Signatures
        c.line(100, 200, 300, 200)
        c.drawString(100, 185, "Buyer Signature")
        
        c.line(350, 200, 550, 200)
        c.drawString(350, 185, "TeraVoo (Escrow Agent)")
        
        c.showPage()
        c.save()
        
        buffer.seek(0)
        return buffer.read()

pdf_service = PdfService()
