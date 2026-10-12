"""
PLANO (passo 1)

Componente: cálculo da data em que termina a garantia de um produto.
Função pública: calcular_fim_da_garantia(tipo, *, fim_informado, data_compra, meses)

Casos que vou testar:
  CT1  tipo "data":      devolve o fim informado pelo fabricante
  CT2  tipo "meses":     data da compra + N meses
  CT3  tipo "vitalicia": a garantia não termina (None)
  CT4  meses em fim de mês: 31/01 + 1 mês cai no último dia de fevereiro (28 ou 29)
  CT5  erros: "data" sem fim; fim antes da compra; "meses" sem compra ou com
       meses <= 0; tipo desconhecido

Padrão de projeto escolhido: Template Method.
Por quê: cada tipo de garantia repete o mesmo esqueleto (validar os dados e
  depois calcular). No Template Method esse esqueleto fica fixo na classe base
  e cada tipo só preenche os passos que mudam. Um tipo novo vira uma subclasse
  nova, sem mexer nas existentes.

Tempo por fase (120 min no total):
  plano 0-10 | red 10-17 | green 17-25 | refactor 25-100
  folga e conferência 100-110 | autoavaliação 110-120


"""
from datetime import date

import pytest

from garantia import ErroGarantia, calcular_fim_da_garantia


def test_tipo_data_devolve_o_fim_informado():
    fim = calcular_fim_da_garantia("data", fim_informado=date(2027, 12, 31))
    assert fim == date(2027, 12, 31)


def test_tipo_meses_soma_os_meses_a_data_da_compra():
    fim = calcular_fim_da_garantia("meses", data_compra=date(2026, 3, 10), meses=12)
    assert fim == date(2027, 3, 10)


def test_tipo_vitalicia_nao_tem_fim():
    assert calcular_fim_da_garantia("vitalicia") is None


@pytest.mark.parametrize(
    ("data_compra", "meses", "esperado"),
    [
        (date(2026, 1, 31), 1, date(2026, 2, 28)),
        (date(2028, 1, 31), 1, date(2028, 2, 29)),  # 2028 é bissexto
        (date(2026, 10, 31), 4, date(2027, 2, 28)),  # passa da virada do ano
    ],
)
def test_meses_em_fim_de_mes_usa_o_ultimo_dia_do_mes_de_destino(data_compra, meses, esperado):
    assert calcular_fim_da_garantia("meses", data_compra=data_compra, meses=meses) == esperado


def test_tipo_data_sem_fim_levanta_erro():
    with pytest.raises(ErroGarantia):
        calcular_fim_da_garantia("data")


def test_tipo_data_com_fim_antes_da_compra_levanta_erro():
    with pytest.raises(ErroGarantia):
        calcular_fim_da_garantia(
            "data", fim_informado=date(2026, 1, 1), data_compra=date(2026, 3, 10)
        )


def test_tipo_meses_sem_data_da_compra_levanta_erro():
    with pytest.raises(ErroGarantia):
        calcular_fim_da_garantia("meses", meses=12)


def test_tipo_meses_com_zero_meses_levanta_erro():
    with pytest.raises(ErroGarantia):
        calcular_fim_da_garantia("meses", data_compra=date(2026, 3, 10), meses=0)


def test_tipo_desconhecido_levanta_erro():
    with pytest.raises(ErroGarantia):
        calcular_fim_da_garantia("quinzenal")