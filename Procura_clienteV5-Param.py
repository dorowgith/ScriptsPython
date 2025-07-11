import requests
import argparse

# Parser de argumentos de linha de comando
parser = argparse.ArgumentParser(description="Consulta de clientes na API.")
parser.add_argument("--clientes", required=True, help="Lista de códigos de cliente separados por vírgula")
args = parser.parse_args()

# Converte a string para lista de códigos
codigos_cliente = [codigo.strip() for codigo in args.clientes.split(',')]

# URL e parâmetros fixos
url_base = "https://api-tic.senior.com.br/erp/contratos/cloud/qtd-usuarios-cloud"
codigos_servico = "090243,0904162,0902103,090244,090805,090808,090951,0904331,090499"

# Consulta para cada cliente
for cod in codigos_cliente:
    params = {
        "CodSer": codigos_servico,
        "CodCliente": cod
    }

    try:
        response = requests.get(url_base, params=params)
        response.raise_for_status()
        dados = response.json()

        print(f"\n🟢 Código do Cliente: {cod}")
        print("-" * 60)

        if isinstance(dados, list) and any(item.get('SIT_SRV') == 'A' for item in dados):
            for item in dados:
                if item.get('SIT_SRV') == 'A':
                    print(f"📌 Serviço: {item.get('DES_SRV', 'N/A')}")
                    print(f"   Situação: {item.get('SIT_SRV', 'N/A')}")
                    print(f"   Usuários: {item.get('QTD_USU', 'N/A')}")
                    print(f"   Usuários Vetados: {item.get('USU_VET', 'N/A')}")
                    print(f"   Pontos: {item.get('QTD_PTO', 'N/A')}")
                    print()
        else:
            print("❌ Cliente inativo!")

        print("=" * 60)

    except requests.exceptions.HTTPError as errh:
        print(f"Código: {cod} ➜ Erro HTTP: {errh}\n")
    except requests.exceptions.ConnectionError as errc:
        print(f"Código: {cod} ➜ Erro de conexão: {errc}\n")
    except requests.exceptions.Timeout as errt:
        print(f"Código: {cod} ➜ Timeout: {errt}\n")
    except requests.exceptions.RequestException as err:
        print(f"Código: {cod} ➜ Erro: {err}\n")
    except ValueError:
        print(f"Código: {cod} ➜ Erro ao decodificar JSON\n")
