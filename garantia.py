import calendar
from datetime import date


class ErroGarantia(Exception):
    """Dados insuficientes ou inválidos para calcular o fim da garantia."""


def _somar_meses(data, meses):
    indice = data.month - 1 + meses
    ano = data.year + indice // 12
    mes = indice % 12 + 1
    dia = min(data.day, calendar.monthrange(ano, mes)[1])
    return date(ano, mes, dia)


def calcular_fim_da_garantia(tipo, *, fim_informado=None, data_compra=None, meses=None):
    if tipo == "vitalicia":
        return None
    if tipo == "data":
        if fim_informado is None:
            raise ErroGarantia("Informe a data final da garantia.")
        if data_compra is not None and fim_informado < data_compra:
            raise ErroGarantia("A garantia não pode terminar antes da compra.")
        return fim_informado
    if tipo == "meses":
        if data_compra is None or meses is None or meses <= 0:
            raise ErroGarantia("Informe a data da compra e os meses (maior que zero).")
        return _somar_meses(data_compra, meses)
    raise ErroGarantia(f"Tipo de garantia desconhecido: {tipo!r}")