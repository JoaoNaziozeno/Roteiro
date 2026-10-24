# -*- coding: utf-8 -*-
"""
Função AWS Lambda para Sincronização Automática em Tempo Real com Amazon DynamoDB
=================================================================================
Custo: US$ 0,00 (100% dentro do AWS Always Free Tier: 25 GB no DynamoDB + 1M reqs/mês no Lambda).

COMO ATIVAR NA SUA CONTA AWS EM 2 MINUTOS:
1. No Console da AWS, abra o serviço **DynamoDB** -> **Criar tabela**:
   - Nome da tabela: `roteiro_estudos_joao`
   - Chave de partição (Partition key): `user_id` (Tipo: String)
   - Configurações: Selecione "Personalizar configurações" -> "Provisionado" (1 RCU / 1 WCU, Always Free) ou "Sob demanda" -> Criar tabela.
2. No Console da AWS, abra o serviço **Lambda** -> **Criar função**:
   - Nome da função: `roteiro-ia-dynamodb-sync`
   - Runtime: `Python 3.12`
   - Em "Configurações avançadas", marque **Habilitar URL da função (Enable function URL)**:
     - Tipo de autenticação: `NONE` (público para o seu frontend acessar via HTTPS)
     - Marque **Configurar CORS (Configure CORS)**:
       - Allow origin: `*`
       - Allow methods: `GET, POST, OPTIONS`
       - Allow headers: `content-type`
3. Na aba **Configuração -> Permissões** da Lambda, clique na Role (função IAM) e anexe a permissão `AmazonDynamoDBFullAccess` (ou permissão de leitura/escrita na tabela `roteiro_estudos_joao`).
4. Cole todo o código abaixo no arquivo `lambda_function.py` do editor da Lambda e clique em **Deploy**.
5. Copie a **Function URL** gerada (ex: `https://xxxxxx.lambda-url.us-east-1.on.aws/`) e cole no modal **Sincronização AWS -> Parâmetros Técnicos** do seu Roteiro IA!
"""

import json
import os
import time
import boto3
from decimal import Decimal

TABLE_NAME = os.environ.get("DYNAMODB_TABLE", "roteiro_estudos_joao")
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj) if obj % 1 == 0 else float(obj)
        return super().default(obj)


def _cors_response(status_code, body_dict):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json; charset=utf-8",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization"
        },
        "body": json.dumps(body_dict, cls=DecimalEncoder, ensure_ascii=False)
    }


def lambda_handler(event, context):
    method = (
        event.get("requestContext", {}).get("http", {}).get("method")
        or event.get("httpMethod")
        or "GET"
    ).upper()

    if method == "OPTIONS":
        return _cors_response(200, {"ok": True})

    try:
        if method == "GET":
            params = event.get("queryStringParameters") or {}
            user_id = (params.get("user_id") or "joao@roteiro.ia").strip().lower()
            resp = table.get_item(Key={"user_id": user_id})
            item = resp.get("Item")
            if not item:
                return _cors_response(200, {"ok": True, "found": False, "user_id": user_id})
            return _cors_response(200, {"ok": True, "found": True, "data": item})

        elif method == "POST":
            raw_body = event.get("body") or "{}"
            payload = json.loads(raw_body, parse_float=Decimal)
            user_id = str(payload.get("user_id") or "joao@roteiro.ia").strip().lower()

            item = {
                "user_id": user_id,
                "user_name": payload.get("user_name") or "João Naziozeno",
                "pwd_hash": payload.get("pwd_hash") or "",
                "progress": payload.get("progress") or {},
                "projects": payload.get("projects") or [],
                "start_date": payload.get("start_date") or "",
                "pace": payload.get("pace") or "std",
                "updated_at": int(payload.get("updated_at") or int(time.time() * 1000))
            }
            table.put_item(Item=item)
            return _cors_response(200, {
                "ok": True,
                "synced": True,
                "user_id": user_id,
                "updated_at": item["updated_at"]
            })

        return _cors_response(405, {"ok": False, "error": f"Método {method} não suportado"})
    except Exception as exc:
        return _cors_response(500, {"ok": False, "error": str(exc)})
