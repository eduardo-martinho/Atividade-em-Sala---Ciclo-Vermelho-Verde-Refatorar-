from __future__ import annotations

import calendar
from abc import ABC, abstractmethod
from datetime import date


class ErroGarantia(Exception):
    """Dados insuficientes ou inválidos para calcular o fim da garantia."""


def somar_meses(data: date, meses: int) -> date:
    """Soma meses; se o dia não existir no mês de destino, usa o último dia dele."""
    indice = data.month - 1 + meses
    ano = data.year + indice // 12
    mes = indice % 12 + 1
    dia = min(data.day, calendar.monthrange(ano, mes)[1])
    return date(ano, mes, dia)


# PADRÃO DE PROJETO: Template Method
#   AbstractClass     -> RegraDeGarantia
#   Template Method   -> RegraDeGarantia.fim_da_garantia()  (fixa a ordem: validar, depois calcular)
#   Operações/ganchos -> validar() (opcional) e calcular() (obrigatória)
#   ConcreteClass     -> GarantiaPorData, GarantiaPorMeses, GarantiaVitalicia
class RegraDeGarantia(ABC):
    def __init__(self, *, fim_informado=None, data_compra=None, meses=None):
        self.fim_informado = fim_informado
        self.data_compra = data_compra
        self.meses = meses

    def fim_da_garantia(self) -> date | None:
        """Template Method: o esqueleto é igual para todo tipo de garantia."""
        self.validar()
        return self.calcular()

    def validar(self) -> None:
        """Gancho: por padrão não exige nada. Os tipos que precisam, sobrescrevem."""

    @abstractmethod
    def calcular(self) -> date | None:
        """Passo que cada tipo de garantia obrigatoriamente implementa."""


class GarantiaPorData(RegraDeGarantia):
    def validar(self) -> None:
        if self.fim_informado is None:
            raise ErroGarantia("Informe a data final da garantia.")
        if self.data_compra is not None and self.fim_informado < self.data_compra:
            raise ErroGarantia("A garantia não pode terminar antes da compra.")

    def calcular(self) -> date:
        return self.fim_informado


class GarantiaPorMeses(RegraDeGarantia):
    def validar(self) -> None:
        if self.data_compra is None or self.meses is None or self.meses <= 0:
            raise ErroGarantia("Informe a data da compra e os meses (maior que zero).")

    def calcular(self) -> date:
        return somar_meses(self.data_compra, self.meses)


class GarantiaVitalicia(RegraDeGarantia):
    def calcular(self) -> None:
        return None


_REGRAS = {
    "data": GarantiaPorData,
    "meses": GarantiaPorMeses,
    "vitalicia": GarantiaVitalicia,
}


def calcular_fim_da_garantia(tipo, *, fim_informado=None, data_compra=None, meses=None):
    """Mesma interface da fase verde: escolhe a regra pelo tipo e delega."""
    regra = _REGRAS.get(tipo)
    if regra is None:
        raise ErroGarantia(f"Tipo de garantia desconhecido: {tipo!r}")
    return regra(
        fim_informado=fim_informado, data_compra=data_compra, meses=meses
    ).fim_da_garantia()


# =============================================================================
# AUTOAVALIAÇÃO (passo 3) 
# =============================================================================
# Critérios
#  1. Testes em arquivo separado, ao menos um por variação: ATINGIDO.
#     test_garantia.py cobre "data", "meses" e "vitalicia", mais fim de mês e erros.
#  2. Três commits com a fase na mensagem
#  3. Commit red só com os testes
#  4. Padrão nomeado em comentário, com participantes do domínio: ATINGIDO
#     (Template Method; RegraDeGarantia, GarantiaPorData/Meses/Vitalicia).
#  5. Suíte passa após o refactor, com a saída registrada
#
# O que mudou entre a fase verde e a refatorada
#  - Um if/elif único virou uma classe base (RegraDeGarantia) com o esqueleto
#    "validar, depois calcular" e uma subclasse por tipo de garantia.
#  - As validações saíram da função e foram para o passo validar() de cada tipo.
#  - calcular_fim_da_garantia virou só um despachante (tipo -> classe).
#  - Os testes não mudaram: o comportamento observável é o mesmo.
#  - Ganho real: tipo novo = subclasse nova + uma linha em _REGRAS.
#    Limite honesto: com só três tipos, o if/elif já era legível; o padrão
#    compensa se os tipos de garantia forem aumentando.
#
# Parte que deu mais trabalho
#  - Escolher o componente. Eu queria usar algo do app que estou construindo,
#    mas sem reaproveitar código antigo (o enunciado não permite). Foi difícil
#    achar uma função com variações de comportamento bem separadas: a maioria
#    era uma sequência de condições que vai afunilando os casos, e não três
#    comportamentos independentes. Por isso criei um componente novo (garantia),
#    com três tipos bem definidos.
#
# Uso de IA
#  - Ajudou em: escolher o tema e qual o padrão de projeto
#  - Atrapalhou em: sugeriu Strategy, que não lembro se foi visto em aula mas não estava nos slides.
# =============================================================================