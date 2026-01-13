from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import os
from datetime import datetime

class ContractService:
    def generate_contract(self, order_id: int, buyer_name: str, product_name: str, amount: float) -> str:
        """
        Generates a PDF Sales Agreement.
        Returns the local path or URL (simulated).
        """
        filename = f"contract_order_{order_id}.pdf"
        filepath = os.path.join("/tmp", filename) # S3 in prod, tmp for MVP local

        c = canvas.Canvas(filepath, pagesize=A4)
        c.setTitle(f"Sales Agreement #{order_id}")

        # Title
        c.setFont("Helvetica-Bold", 24)
        c.drawString(100, 750, "TERAVOO SALES AGREEMENT")
        
        # Details
        c.setFont("Helvetica", 12)
        c.drawString(100, 700, f"Date: {datetime.now().strftime('%Y-%m-%d')}")
        c.drawString(100, 680, f"Order Reference: #{order_id}")
        
        c.drawString(100, 640, "SELLER: TeraVoo Facilitator Network (On behalf of Producer)")
        c.drawString(100, 620, f"BUYER: {buyer_name}")

        # Product Table
        c.line(100, 580, 500, 580)
        c.drawString(100, 560, f"Product: {product_name}")
        c.drawString(100, 540, f"Total Amount (FOB): ${amount:,.2f}")
        c.line(100, 520, 500, 520)

        # Legal Boilerplate
        c.setFont("Helvetica-Oblique", 10)
        c.drawString(100, 480, "This agreement confirms the sale of the goods listed above.")
        c.drawString(100, 465, "Funds must be deposited to the Escrow account within 48 hours.")
        c.drawString(100, 450, "Quality is guaranteed as per the AI Audit Report attached.")
        
        # Signatures
        c.line(100, 300, 250, 300)
        c.drawString(100, 285, "Seller Signature")
        
        c.line(350, 300, 500, 300)
        c.drawString(350, 285, "Buyer Signature")

        c.save()
        
        # In real world, upload to S3 and return public URL.
        # For localhost MVP, we can serve likely via static or just return path for now.
        # We will assume we serve it via a static endpoint or just mock the URL for the frontend.
        return f"/api/v1/orders/{order_id}/download_contract" 

contract_service = ContractService()
