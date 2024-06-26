import argparse
import os
from collections import OrderedDict
from pathlib import Path
from pypdf import PdfWriter, PdfReader
from tqdm import tqdm


def extract_pages(input_files, pages, output_file):
    root_dir = Path(os.path.abspath(os.path.dirname(__file__)))
    print('\n\tRoot dir: {}\n'.format(root_dir))

    pdfs = {}
    for f, p in zip(input_files, pages):
        pdfs[f] = parse_ranges(p)

    pdfs = OrderedDict(sorted(pdfs.items(), reverse=True))
    print(pdfs)

    one_file = True
    # one_file = False
    if one_file:
        output = PdfWriter()

    for pdf_name, pdf_pages in tqdm(pdfs.items()):
        full_path = root_dir / Path(pdf_name)

        inputpdf = PdfReader(full_path)
        msg = 'specified pages range {} is out of range ({})'
        num_pages = len(inputpdf.pages)
        for page in pdf_pages:
            assert page <= num_pages, msg.format(pdf_name, num_pages)

        n, e = os.path.splitext(full_path)
        pages_range = '-'.join([str(x) for x in pdf_pages])
        out_name = '{}_{}{}'.format(n, pages_range, e)
        tqdm.write('  Input  file: {} (pages: {} out of total {})'.format(
                   full_path, pages_range, num_pages))

        if not one_file:
            tqdm.write('  Output file: {}'.format(out_name))
            output = PdfWriter()

        for i in pdf_pages:
            tqdm.write('      Getting page {}...'.format(i))
            output.add_page(inputpdf.pages[i-1])

        if not one_file:
            with open(out_name, 'wb') as oStream:
                output.write(oStream)

        tqdm.write('')

    if one_file:
        out_name = output_file
        tqdm.write('\n\tOutput file: {}'.format(out_name))
        with open(out_name, 'wb') as oStream:
            output.write(oStream)


def parse_ranges(string):
    """Parse ranges of numbers, e.g. '1,3-6'
    """
    s_split = [x.replace('-', ',').replace(':', ',')
               for x in string.split(',')]
    ret = []
    for el in s_split:
        nums = [int(x) for x in el.split(',')]
        if len(nums) < 2:
            nums.append(nums[-1])
        nums[-1] += 1
        ret.extend(list(range(*nums)))
    return ret


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Extract and combine pages from multiple pdf files')
    parser.add_argument('-i', '--input-files', dest='input_files',
                        default=None, nargs='+',
                        help='blank-separated input pdf-file list')
    parser.add_argument('-p', '--pages', dest='pages',
                        default=None, nargs='+',
                        help='blank-separated list of pages list')
    parser.add_argument('-o', '--output-file', dest='output_file',
                        default='output.pdf',
                        help='output file name')

    args = parser.parse_args()

    if None in [args.input_files, args.pages]:
        parser.print_help()
        parser.exit()

    kwargs = {'input_files': args.input_files,
              'pages': args.pages,
              'output_file': args.output_file}

    extract_pages(**kwargs)
