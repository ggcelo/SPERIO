"""Verifica nomes de arquivos privados no Git antes da publicacao."""

from pathlib import Path, PurePosixPath
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
PRIVATE_SUFFIXES = {
    '.pt', '.pth', '.onnx', '.h5', '.hdf5', '.keras', '.pkl', '.pickle',
    '.joblib', '.safetensors', '.ckpt', '.xls', '.xlsx', '.xlsm', '.xlsb',
    '.ods', '.csv', '.tsv', '.pyc', '.pyo',
}
PRIVATE_DIRS = {'.local', '.github-publicacao', '.venv', 'venv', '__pycache__', '.vscode'}


def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args])


def private(name):
    path = PurePosixPath(name.lower())
    return (
        path.suffix in PRIVATE_SUFFIXES
        or bool(set(path.parts) & PRIVATE_DIRS)
        or ('models' in path.parts and path.as_posix() not in {'models', 'models/readme.md'})
        or (path.name.startswith('.env') and path.name != '.env.example')
        or path.as_posix() == '.streamlit/secrets.toml'
    )


def main():
    candidates = git('ls-files', '--cached', '--others', '--exclude-standard', '-z')
    current = {name.decode('utf-8') for name in candidates.split(b'\0') if name}
    history = set()
    for line in git('-c', 'core.quotePath=false', 'rev-list', '--objects', '--all').decode('utf-8').splitlines():
        _, separator, name = line.partition(' ')
        if separator:
            history.add(name)
    # Caches e configuracoes de editor antigos nao sao modelos nem dados privados.
    historical_problems = {
        name for name in history if private(name)
        and not (set(PurePosixPath(name).parts) & {'.vscode', '__pycache__'})
        and PurePosixPath(name).suffix not in {'.pyc', '.pyo'}
    }
    problems = sorted({name for name in current if private(name)} | historical_problems)
    if problems:
        print('BLOQUEADO: arquivos privados no indice, arquivos novos ou historico:')
        print('\n'.join(f'  {name}' for name in problems))
        return 1
    print(f'OK: {len(current)} arquivos atuais e {len(history)} caminhos historicos verificados.')
    print('Nenhum modelo, planilha ou backup privado identificado. Revise tambem o conteudo do diff.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
