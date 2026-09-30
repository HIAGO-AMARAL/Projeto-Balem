"""Lê o tamanho de um vídeo MP4 sem precisar de nenhum programa extra.

Serve para a página educativa saber se o vídeo da equipe é vertical (gravado de celular)
ou horizontal, e montar a caixa do vídeo com a proporção certa desde o primeiro carregamento.
"""

import struct


def _blocos(arquivo, inicio, fim):
    """Percorre os blocos ("atoms") de um MP4 entre duas posições do arquivo."""
    arquivo.seek(inicio)
    while arquivo.tell() < fim:
        posicao = arquivo.tell()
        cabecalho = arquivo.read(8)
        if len(cabecalho) < 8:
            return
        tamanho, tipo = struct.unpack(">I4s", cabecalho)
        cabecalho_tam = 8
        if tamanho == 1:
            tamanho = struct.unpack(">Q", arquivo.read(8))[0]
            cabecalho_tam = 16
        elif tamanho == 0:
            tamanho = fim - posicao
        if tamanho < cabecalho_tam:
            return
        yield tipo, posicao, tamanho, cabecalho_tam
        arquivo.seek(posicao + tamanho)


def _achar(arquivo, inicio, fim, caminho):
    """Acha um bloco seguindo um caminho, ex.: ('moov', 'trak')."""
    for tipo, pos, tam, cab in _blocos(arquivo, inicio, fim):
        if tipo == caminho[0].encode():
            if len(caminho) == 1:
                yield pos + cab, pos + tam
            else:
                yield from _achar(arquivo, pos + cab, pos + tam, caminho[1:])


def dimensoes_mp4(caminho):
    """Devolve (largura, altura) como o vídeo aparece na tela, ou None se não conseguir ler."""
    try:
        with open(caminho, "rb") as arquivo:
            arquivo.seek(0, 2)
            fim = arquivo.tell()
            for inicio_trak, fim_trak in _achar(arquivo, 0, fim, ("moov", "trak")):
                # "tkhd" guarda o tamanho e a matriz de rotação da faixa de vídeo
                for ini, fi in _achar(arquivo, inicio_trak, fim_trak, ("tkhd",)):
                    arquivo.seek(ini)
                    versao = arquivo.read(1)[0]
                    # versão+flags (4) + datas/id/duração (20 ou 32) + reservado (8)
                    # + camada/grupo/volume/reservado (8) = início da matriz de rotação
                    arquivo.seek(ini + 4 + (32 if versao == 1 else 20) + 8 + 8)
                    matriz = struct.unpack(">9i", arquivo.read(36))
                    largura, altura = struct.unpack(">II", arquivo.read(8))
                    largura, altura = largura >> 16, altura >> 16
                    if not largura or not altura:
                        continue  # faixa de áudio
                    girado = matriz[0] == 0 and abs(matriz[1]) == 0x10000
                    return (altura, largura) if girado else (largura, altura)
    except (OSError, struct.error, IndexError):
        pass
    return None


def eh_vertical(caminho):
    """True se o vídeo é mais alto do que largo."""
    tamanho = dimensoes_mp4(caminho)
    return bool(tamanho) and tamanho[1] > tamanho[0]
