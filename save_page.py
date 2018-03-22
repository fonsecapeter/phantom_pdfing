import uuid
from os import path
from subprocess import call


def _make_outfile_name(url: str) -> str:
    file_name = (
        url
        .replace('https://', '')
        .replace('http://', '')
        .replace('.', '-dot-')
        .replace('/', '-')
    )
    return str(path.join(
        'out',
        'py',
        f'{file_name}-{str(uuid.uuid4())}.pdf'
    ))


def generate_pdf(url: str) -> None:
    out_file_name = _make_outfile_name(url)
    call([
        'phantomjs',
        '--web-security=no',
        '--ssl-protocol=any',
        'rasterize.js',
        url,
        out_file_name,
        'A4',          # paper format
        'portrait',    # orientation
        '1cm',         # margin
        '1'            # zoom
    ])


if __name__ == '__main__':
    # generate_pdf('http://google.com')  # static
    generate_pdf('http://peterfonseca.gq')  # react
