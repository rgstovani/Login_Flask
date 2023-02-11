import requests
import time
from datetime import datetime


def cotar():
    requisicao = requests.get('http://economia.awesomeapi.com.br/json/last/USD-BRL,GBP-BRL,CAD-BRL,EUR-BRL,ARS-BRL,JPY-BRL,AUD-BRL,PYG-BRL,COP-BRL,BOB-BRL')
    cotacao = requisicao.json()
    moeda = float(cotacao[sigla_moeda[escolha]]['bid'])
    return moeda
#
# #Cotação da moeda
# print(f'O valor atual do {moeda_escolhida[escolha]} é ',cotar())
# while True:
#     try:
#         preco_alvo = float(input('Digite o valor desejado: R$'))
#         cria_linha()
#         break
#     except ValueError:
#         print('Valor Invalido. Use o ponto para casas decimais.')
#         cria_linha()
#
# #tempo de atualização
# while True:
#     tempo_de_atualizacao = input('Digite o tempo de atualização (em segundos):')
#     cria_linha()
#     if tempo_de_atualizacao.isnumeric():
#         tempo = int(tempo_de_atualizacao)
#         break
#     else:
#         print('Digite apenas numeros.!')
#
# #Execução
# cria_linha2()
# print(f"{'Agora você pode minimizar, te avisaremos quando atigir o valor desejado.':^80}")
# cria_linha2()
#
# while True:
#     cotar()
#     print('Atualizado em: ', datetime.now().strftime("%d-%m-%y %H:%M:%S"))
#     print('Cotação Atual:', cotar())
#     if (cotar() <= preco_alvo):
#         print('Bora comprar!')
#         hora_de_comprar()
#     elif (cotar() > preco_alvo):
#         print('Ainda está caro!')
#         cria_linha2()
#     time.sleep(tempo)