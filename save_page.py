import uuid
from os import path
from subprocess import call


def _make_outfile_name(url: str) -> str:
    found_unique_name = False
    while not found_unique_name:
        file_name = (
            url
            .replace('https://', '')
            .replace('http://', '')
            .replace('.', '-dot-')
            .replace('/', '-')
            .replace('?', '-q-')
            .replace('&', '-and-')
        )
        file_path = path.join(
            'out',
            'py',
            f'{file_name}-{str(uuid.uuid4())}.pdf'
        )
        found_unique_name = not path.isfile(file_path)
    return str(file_path)


def generate_pdf(url: str) -> None:
    out_file_name = _make_outfile_name(url)
    # call([
    #     'phantomjs',
    #     '--web-security=no',
    #     '--ssl-protocol=any',
    #     'rasterize.js',
    #     url,
    #     out_file_name,
    #     'A4',          # paper format
    #     'portrait',    # orientation
    #     '1cm',         # margin
    #     '1'            # zoom
    # ])
    call([
        'phantomjs',
        '--web-security=no',
        '--ssl-protocol=any',
        'rasterize.js',
        url,
        out_file_name,
        '11in*11in',     # paper size
        'landscape',   # orientation
        '1cm',         # margin
        '0.5'          # zoom
    ])


if __name__ == '__main__':
    # generate_pdf('http://google.com')  # static
    # generate_pdf('http://peterfonseca.gq')  # react
    generate_pdf('https://you.23andme.com/public/lucky-you/')
