import os
from collections import OrderedDict
from pathlib import Path
from PyPDF2 import PdfFileWriter, PdfFileReader
from tqdm import tqdm

root_dir = Path(os.path.abspath(os.path.dirname(__file__)))
print('\n\tRoot dir: {}\n'.format(root_dir))

pdfs = {
    'input.pdf': [1],
}

pdfs = OrderedDict(sorted(pdfs.items(), reverse=True))

one_file = True
# one_file = False
if one_file:
    output = PdfFileWriter()

for pdf_name, pdf_pages in tqdm(pdfs.items()):
    full_path = root_dir / Path(pdf_name)

    inputpdf = PdfFileReader(open(full_path, 'rb'))
    msg = 'specified pages range {} is out of range ({})'
    num_pages = inputpdf.numPages
    for page in pdf_pages:
        assert page <= num_pages, msg.format(pdf_name, num_pages)

    n, e = os.path.splitext(full_path)
    pages_range = '-'.join([str(x) for x in pdf_pages])
    out_name = '{}_{}{}'.format(n, pages_range, e)
    tqdm.write('  Input  file: {} (pages: {} out of total {})'.format(
               full_path, pages_range, num_pages))

    if not one_file:
        tqdm.write('  Output file: {}'.format(out_name))
        output = PdfFileWriter()

    for i in pdf_pages:
        tqdm.write('      Getting page {}...'.format(i))
        output.addPage(inputpdf.getPage(i-1))

    if not one_file:
        with open(out_name, 'wb') as oStream:
            output.write(oStream)

    tqdm.write('')

if one_file:
    out_name = 'output.pdf'
    tqdm.write('\n\tOutput file: {}'.format(out_name))
    with open(out_name, 'wb') as oStream:
        output.write(oStream)
