import click
import glob
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger


@click.group()
def pdf_splitter():
    pass


@pdf_splitter.command()
@click.argument('filename', type=click.Path(exists=True))
def split(filename):
    pdf = PdfFileReader(filename)
    for page in range(pdf.getNumPages()):
        pdf_writer = PdfFileWriter()
        pdf_writer.addPage(pdf.getPage(page))

        output_filename = '{}_page_{}.pdf'.format(
            filename, page+1)

        with open(output_filename, 'wb') as out:
            pdf_writer.write(out)

        print('Created: {}'.format(output_filename))


@click.group()
def pdf_merger():
    pass


@pdf_merger.command()
@click.argument('input_paths')
@click.argument('output', type=click.File('wb'))
def merge(input_paths, output):
    paths = glob.glob(input_paths)
    paths.sort()

    pdf_merger = PdfFileMerger()

    for path in paths:
        pdf_merger.append(path)

    pdf_merger.write(output)


pdf = click.CommandCollection(sources=[pdf_splitter, pdf_merger])

if __name__ == '__main__':
    pdf()
