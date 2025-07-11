import requests

codigos_input = "28872, 28230, 16889, 28856, 5523, 27258, 28763, 27782, 28930, 27850, 24517, 28785, 28667, 29023, 29716, 28460, 29011, 30181, 24270, 30052, 21868, 30180, 29907, 15696, 29022, 21335, 28670, 24861, 18094, 26744, 29041, 25394, 29540, 30066, 502, 28689, 28778, 16123, 28736, 28966, 30016, 15899, 28932, 28775, 28815, 15030, 29938, 29072, 8098, 30057, 30143, 30059, 29928, 24270, 728275, 16236, 24239, 26122, 28813, 24270, 28939, 28604, 728275, 18389, 24270, 19519, 29419, 17371, 20909, 12154, 30045, 5547, 26093, 16244, 24270"

codigos_cliente = [codigo.strip() for codigo in codigos_input.split(',')]

url_base = "https://api-tic.senior.com.br/erp/contratos/cloud/qtd-usuarios-cloud"
codigos_servico = "090243,0904162,0902103,090244,090805,090808,090951,0904331,090499"

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
