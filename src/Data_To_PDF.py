import qrcode
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, PageBreak, Image, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def get_ID_from_url(url):
    id = url.split('/')[-1]
    if '?' in id : return id.split('?')[0] 
    else: return id

def generate_qr_code(url):
    qr_code_filename = f"./qrcodes/{get_ID_from_url(url)}.png"

    # Check if the QR code file already exists
    if os.path.exists(qr_code_filename): return

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(qr_code_filename)

def create_pdf(data_list, filename):
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.white),  # Set all backgrounds to white
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),   # Set text color to black for all cells
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),            # Center align horizontally
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),           # Center align vertically
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),      # Set font for all cells
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),          # Set bottom padding for all cells
        ('GRID', (0, 0), (-1, -1), 1, colors.black),      # Add grid lines
    ])

    pdf = SimpleDocTemplate(filename, pagesize=A4)
    elements = []

    styles = getSampleStyleSheet()

    # Prepare data for the table
    table_data1 = []
    table_row1 = []
    table_data2 = []
    table_row2 = []
    for i in range(0, len(data_list), 18):
        for j in range(18):
            if i + j < len(data_list):
                artist, track, year, spotify_id = data_list[i + j]
                artist = artist.replace(";", ",")
                track = track.replace(";", ",")
                cell_content = f"<para align='center'><font size='10'>{artist.replace('&&', ', ')}</font><br/><br/><br/><font size='24'>{year}</font><br/><br/><font size='10'>{track}</font></para>"
                paragraph = Paragraph(cell_content, styles['Normal'])
                table_row1.append(paragraph)
                if (len(table_row1) == 3): 
                    table_data1.append(table_row1.copy())
                    table_row1.clear()
                generate_qr_code(spotify_id)
                table_row2.append(Image(f"./qrcodes/{spotify_id.split('/')[-1]}.png", 2*cm, 2*cm))
                if (len(table_row2) == 3):
                    table_row2.reverse() 
                    table_data2.append(table_row2.copy())
                    table_row2.clear()

        if (len(table_row1) != 0 and len(table_row2) != 0):
            table_data1.append(table_row1.copy())
            table_row2.append("")
            if (len(table_row2) != 3): table_row2.append("")
            table_row2.reverse()
            table_data2.append(table_row2.copy())
        
        # Create a table for the current set of 18 songs
        col_width = [6*cm]*len(table_data1[0])
        row_width = [4*cm]*len(table_data1)
        table1 = Table(table_data1, colWidths=col_width, rowHeights=row_width)
        table1.setStyle(table_style)
        table2 = Table(table_data2, colWidths=col_width, rowHeights=row_width)
        table2.setStyle(table_style)

        elements.append(table1)
        elements.append(PageBreak())
        elements.append(table2)
        elements.append(PageBreak())
        table_data1.clear()
        table_data2.clear()

    pdf.build(elements)

def read_data(project_name):
    data_list = []
    with open(f"./csv/{project_name}-data.csv", "r") as file:
        for line in file:
            data_list.append(line.strip().split(","))
    return data_list

def data_to_pdf(project_name):
    data_list = read_data(project_name)
    create_pdf(data_list, f"./pdf/{project_name}-music-cards.pdf")

if __name__ == "__main__":
    name = "khira"
    data_to_pdf(name)