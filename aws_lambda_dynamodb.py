# -*- coding: utf-8 -*-
"""
Função AWS Lambda para Sincronização Automática em Tempo Real com Amazon DynamoDB
=================================================================================
Custo: US$ 0,00 (100% dentro do AWS Always Free Tier: 25 GB no DynamoDB + 1M reqs/mês no Lambda).

Suporta:
- Multi-região automática (busca a tabela em us-east-2 e us-east-1 sem travar por divergência de região).
- Decodificação Base64 automática de payloads do navegador.
- Diagnóstico detalhado de conexão para teste direto no frontend.
- CORS completo para origens locais (file://) e remotas.
"""

import json
import os
import time
import base64
import boto3
from decimal import Decimal

TABLE_NAME = os.environ.get("DYNAMODB_TABLE", "roteiro_estudos_joao")
REGIONS_TO_TRY = ["us-east-2", "us-east-1", "sa-east-1"]


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
            "Access-Control-Allow-Headers": "Content-Type, Authorization, X-Requested-With, *"
        },
        "body": json.dumps(body_dict, cls=DecimalEncoder, ensure_ascii=False)
    }


def _execute_dynamo_op(op_func):
    """Executa operação no DynamoDB tentando as regiões us-east-2 e us-east-1 para evitar erros de região."""
    env_region = os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")
    ordered_regions = [env_region] if env_region else []
    for r in REGIONS_TO_TRY:
        if r not in ordered_regions:
            ordered_regions.append(r)

    last_exc = None
    for reg in ordered_regions:
        try:
            dynamodb = boto3.resource("dynamodb", region_name=reg)
            table = dynamodb.Table(TABLE_NAME)
            result = op_func(table)
            return result, reg
        except Exception as exc:
            err_code = getattr(exc, "response", {}).get("Error", {}).get("Code", "")
            if err_code == "ResourceNotFoundException" or "ResourceNotFoundException" in str(exc):
                last_exc = exc
                continue
            # Se for erro de permissão (AccessDenied) ou outro, lança imediatamente
            raise exc

    if last_exc:
        raise last_exc
    raise RuntimeError(f"Tabela {TABLE_NAME} não encontrada nas regiões testadas: {ordered_regions}")


def lambda_handler(event, context):
    method = (
        event.get("requestContext", {}).get("http", {}).get("method")
        or event.get("httpMethod")
        or "GET"
    ).upper()

    if method == "OPTIONS":
        return _cors_response(200, {"ok": True, "cors": "enabled"})

    try:
        if method == "GET":
            params = event.get("queryStringParameters") or {}
            user_id = (params.get("user_id") or "joao@roteiro.ia").strip().lower()

            def _get_item(tbl):
                return tbl.get_item(Key={"user_id": user_id})

            resp, reg = _execute_dynamo_op(_get_item)
            item = resp.get("Item")
            if not item:
                return _cors_response(200, {
                    "ok": True,
                    "connected": True,
                    "found": False,
                    "user_id": user_id,
                    "region": reg,
                    "table": TABLE_NAME
                })
            return _cors_response(200, {
                "ok": True,
                "connected": True,
                "found": True,
                "data": item,
                "region": reg,
                "table": TABLE_NAME
            })

        elif method == "POST":
            raw_body = event.get("body") or "{}"
            if event.get("isBase64Encoded", False):
                try:
                    raw_body = base64.b64decode(raw_body).decode("utf-8")
                except Exception:
                    pass

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

            def _put_item(tbl):
                return tbl.put_item(Item=item)

            _, reg = _execute_dynamo_op(_put_item)

            return _cors_response(200, {
                "ok": True,
                "synced": True,
                "connected": True,
                "user_id": user_id,
                "region": reg,
                "table": TABLE_NAME,
                "updated_at": item["updated_at"]
            })

        return _cors_response(405, {"ok": False, "error": f"Método {method} não suportado"})

    except Exception as exc:
        err_msg = str(exc)
        hint = ""
        if "AccessDeniedException" in err_msg:
            hint = "A Role da Lambda precisa da permissão 'AmazonDynamoDBFullAccess' no console do IAM."
        elif "ResourceNotFoundException" in err_msg:
            hint = f"A tabela '{TABLE_NAME}' não foi encontrada nas regiões us-east-2 nem us-east-1."

        return _cors_response(500, {
            "ok": False,
            "connected": False,
            "error": err_msg,
            "hint": hint
        })
