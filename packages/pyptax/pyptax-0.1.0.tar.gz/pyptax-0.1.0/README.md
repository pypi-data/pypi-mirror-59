# PyPtax

PyPtax is a Python library to retrieve information on
[Ptax rates](https://www.bcb.gov.br/conteudo/relatorioinflacao/EstudosEspeciais/EE042_A_taxa_de_cambio_de_referencia_Ptax.pdf).

## What is Ptax?

Ptax exchange rate is the reference exchange rate for U.S. Dollar, expressed as the amount of Brazilian Reais per one U.S. Dollar,
published by the [Central Bank of Brazil](https://www.bcb.gov.br/en).

## Installation
```bash
$ pip install pyptax
```

## Usage

### Get closing rates on a certain date

```python
>>> from pyptax import ptax

>>> close = ptax.close('01-17-2020')
>>> print(close)
{
    'datetime': '2020-01-17 13:09:30.096',
    'bid': '4.1831',
    'ask': '4.1837',
}
```
