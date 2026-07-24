from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def create_test_pdf():
    c = canvas.Canvas("test_contract.pdf", pagesize=letter)
    
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 750, "CONTRATO DE PRESTAÇÃO DE SERVIÇOS")
    
    c.setFont("Helvetica", 12)
    c.drawString(100, 700, "Contrato nº 001/2024")
    c.drawString(100, 680, "Data: 15 de Janeiro de 2024")
    
    c.drawString(100, 640, "PARTES:")
    c.drawString(100, 620, "Contratante: Empresa ABC Ltda")
    c.drawString(100, 600, "CNPJ: 12.345.678/0001-90")
    c.drawString(100, 580, "Contratada: Soluções TI S/A")
    c.drawString(100, 560, "CNPJ: 98.765.432/0001-10")
    
    c.drawString(100, 520, "CLÁUSULA 1 - OBJETO")
    c.drawString(100, 500, "O presente contrato tem como objeto a prestação de serviços de")
    c.drawString(100, 480, "desenvolvimento de software para a Contratante.")
    
    c.drawString(100, 440, "CLÁUSULA 2 - VALOR")
    c.drawString(100, 420, "O valor total do contrato é de R$ 50.000,00")
    c.drawString(100, 400, "Pagamento em 12 parcelas mensais de R$ 4.166,67")
    
    c.drawString(100, 360, "CLÁUSULA 3 - PRAZO")
    c.drawString(100, 340, "O prazo de vigência é de 12 meses a partir da assinatura.")
    c.drawString(100, 320, "Data de término: 15 de Janeiro de 2025")
    
    c.drawString(100, 280, "CLÁUSULA 4 - MULTA")
    c.drawString(100, 260, "Em caso de descumprimento, aplica-se multa de 10% sobre")
    c.drawString(100, 240, "o valor total do contrato.")
    
    c.drawString(100, 200, "CLÁUSULA 5 - CONFIDENCIALIDADE")
    c.drawString(100, 180, "As partes comprometem-se a manter sigilo sobre todas as")
    c.drawString(100, 160, "informações trocadas durante a vigência deste contrato.")
    
    c.drawString(100, 120, "CLÁUSULA 6 - RESCISÃO")
    c.drawString(100, 100, "O contrato pode ser rescindido por qualquer das partes mediante")
    c.drawString(100, 80, "aviso prévio de 30 dias.")
    
    c.save()
    print("PDF criado: test_contract.pdf")

if __name__ == "__main__":
    create_test_pdf()
