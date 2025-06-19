import json
import random
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os
import argparse

# Configuración
JSON_PATH = "5b1d4147-f2a6-497b-9b58-9d8979cdc995.json"
PDF_PATH = "reporte_shodan.pdf"
MAX_SAMPLE = 10  # Número de líneas a muestrear


def sample_lines(file_path, max_sample=10):
    """Obtiene una muestra de líneas: las más largas y las más cortas."""
    with open(file_path, 'r') as f:
        lines = f.readlines()
    if len(lines) <= max_sample:
        return lines
    # Ordenar por longitud
    sorted_lines = sorted(lines, key=len)
    sample = sorted_lines[:max_sample//2] + sorted_lines[-max_sample//2:]
    # Aleatorizar el orden
    random.shuffle(sample)
    return sample


def parse_entry(entry):
    """Extrae los campos relevantes de una entrada JSON."""
    ip = entry.get('ip_str', 'N/A')  # Cambiado a ip_str
    hostnames = entry.get('hostnames', [])
    ports = entry.get('port', [])
    if not isinstance(ports, list):
        ports = [ports]
    data = entry.get('data', '')
    vulns = entry.get('vulns', {})
    # Extraer solo los IDs CVE (las claves del diccionario vulns)
    cve_ids = list(vulns.keys()) if isinstance(vulns, dict) else []
    return {
        'ip': ip,
        'hostnames': hostnames,
        'ports': ports,
        'data': data,
        'vulns': cve_ids
    }


def get_all_lines(file_path):
    """Lee todas las líneas del archivo."""
    with open(file_path, 'r') as f:
        return f.readlines()


def build_pdf_report(entries, pdf_path, banner_path=None):
    from reportlab.platypus import Image, PageBreak, Frame, FrameBreak
    from reportlab.lib.units import inch
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(pdf_path, pagesize=letter,
        leftMargin=36, rightMargin=36, topMargin=letter[0]*0.25+18, bottomMargin=36)
    story = []
    def add_banner(canvas, doc):
        canvas.saveState()
        if banner_path:
            try:
                canvas.drawImage(
                    banner_path,
                    0,
                    letter[1] - (letter[0] * 0.25),
                    width=letter[0],
                    height=letter[0] * 0.25,
                    preserveAspectRatio=False,
                    mask='auto'
                )
            except Exception:
                pass
        else:
            # Si no hay banner, solo deja el espacio en blanco
            canvas.setFillColorRGB(1, 1, 1)
            canvas.rect(0, letter[1] - (letter[0] * 0.25), letter[0], letter[0] * 0.25, fill=1, stroke=0)
        canvas.restoreState()
    doc.build(story_generator(entries, styles), onFirstPage=add_banner, onLaterPages=add_banner)
    print(f"Reporte generado en: {os.path.abspath(pdf_path)}")


def story_generator(entries, styles):
    from reportlab.platypus import Paragraph, Spacer, Table, TableStyle
    from reportlab.lib import colors
    from reportlab.lib.colors import HexColor
    story = []
    title = Paragraph("<b>Reporte Shodan - Activos Analizados</b>", styles['Title'])
    story.append(Spacer(1, 24))  # Espacio para separar del banner
    story.append(title)
    story.append(Spacer(1, 12))
    for idx, entry in enumerate(entries):
        story.append(Paragraph(f"<b>Activo {idx+1}</b>", styles['Heading2']))
        story.append(Paragraph(f"<b>IP:</b> {entry['ip']}", styles['Normal']))
        if entry['hostnames']:
            story.append(Paragraph(f"<b>Hostnames:</b> {', '.join(entry['hostnames'])}", styles['Normal']))
        else:
            story.append(Paragraph(f"<b>Hostnames:</b> N/A", styles['Normal']))
        story.append(Spacer(1, 8))  # Espacio extra antes de la tabla
        # Tabla de puertos
        # Calcular ancho de la tabla para que quede centrada y con márgenes iguales
        page_width = letter[0] - 36*2  # Ancho de página menos márgenes izquierdo y derecho
        puerto_width = 60
        salida_width = page_width - puerto_width
        port_data = [["Puerto", "Salida"]]
        for port in entry['ports']:
            salida = entry['data']
            if len(salida) > 500:
                salida = salida[:500] + '...'
            # Reemplazar saltos de línea por espacios y envolver texto para que no se desborde
            from textwrap import fill
            salida = fill(salida.replace('\n', ' '), width=90)
            port_data.append([str(port), salida])
        t = Table(port_data, hAlign='LEFT', colWidths=[puerto_width, salida_width], repeatRows=1)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), HexColor("#546fa2")),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0,0), (-1,0), 8),
            ('BACKGROUND', (0,1), (-1,-1), colors.white),
            ('GRID', (0,0), (-1,-1), 1, colors.black),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ]))
        story.append(t)
        story.append(Spacer(1, 8))
        # Vulnerabilidades
        if entry['vulns']:
            story.append(Paragraph("<b>Vulnerabilidades:</b>", styles['Normal']))
            for cve in entry['vulns']:
                story.append(Paragraph(f"- {cve}", styles['Normal']))
        else:
            story.append(Paragraph("<b>Vulnerabilidades:</b> Ninguna detectada", styles['Normal']))
        story.append(Spacer(1, 18))
    return story


def main():
    parser = argparse.ArgumentParser(description="Genera un reporte PDF a partir de un JSON de Shodan.")
    parser.add_argument('-i', '--input', required=True, help="Archivo JSON de entrada")
    parser.add_argument('-o', '--output', required=True, help="Archivo PDF de salida")
    parser.add_argument('-b', '--banner', default=None, help="Archivo de imagen para el banner (opcional)")
    if len(os.sys.argv) == 1:
        parser.print_help()
        exit(1)
    args = parser.parse_args()

    lines = get_all_lines(args.input)
    entries = []
    for line in lines:
        try:
            entry = json.loads(line)
            parsed = parse_entry(entry)
            entries.append(parsed)
        except Exception as e:
            continue  # Saltar líneas mal formateadas
    if not entries:
        print("No se encontraron entradas válidas para el reporte.")
        return
    build_pdf_report(entries, args.output, args.banner)

if __name__ == "__main__":
    main()
