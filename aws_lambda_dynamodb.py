# -*- coding: utf-8 -*-
"""
Função AWS Lambda para Sincronização Automática em Tempo Real com Amazon DynamoDB
=================================================================================
Custo: US$ 0,00 (100% dentro do AWS Always Free Tier: 25 GB no DynamoDB + 1M reqs/mês no Lambda).

Suporta:
- Multi-região automática (busca a tabela em us-east-2 e us-east-1 sem travar por divergência de região).
- Decodificação Base64 automática de payloads do navegador.
- Headers limpos sem duplicação de CORS (o AWS Function URL já gerencia o CORS nativamente).
"""

import json
import os
import time
import base64
import random
import re
import urllib.request
import urllib.parse
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
    # NOTA CRUCIAL: O AWS Function URL já injeta Access-Control-Allow-Origin automaticamente.
    # Não devemos duplicar esses headers aqui para evitar o erro do Chrome 'multiple values *, *'.
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json; charset=utf-8"
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
        return _cors_response(200, {"ok": True})

    try:
        if method == "GET":
            params = event.get("queryStringParameters") or {}
            user_id = (params.get("user_id") or "estudante").strip().lower()

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
            action = payload.get("action")
            user_id = str(payload.get("user_id") or "estudante").strip().lower()

            # -----------------------------------------------------------------
            # AÇÃO 1: SOLICITAR CÓDIGO DE RECUPERAÇÃO (OTP 6 DÍGITOS)
            # -----------------------------------------------------------------
            if action == "request_reset":
                channel = str(payload.get("channel") or "email").strip().lower()
                phone = str(payload.get("phone") or "").strip()
                otp_code = f"{random.randint(100000, 999999)}"
                expires_at = int(time.time()) + 600  # 10 minutos de validade

                # 1. Salvar código OTP e expiração no DynamoDB
                def _save_otp(tbl):
                    return tbl.update_item(
                        Key={"user_id": user_id},
                        UpdateExpression="SET reset_code = :c, reset_expires_at = :e, reset_channel = :ch, updated_at = :u",
                        ExpressionAttributeValues={
                            ":c": otp_code,
                            ":e": expires_at,
                            ":ch": channel,
                            ":u": int(time.time() * 1000)
                        }
                    )
                try:
                    _, reg = _execute_dynamo_op(_save_otp)
                except Exception:
                    def _create_user_otp(tbl):
                        return tbl.put_item(Item={
                            "user_id": user_id,
                            "user_name": "Estudante",
                            "pwd_hash": "",
                            "reset_code": otp_code,
                            "reset_expires_at": expires_at,
                            "reset_channel": channel,
                            "updated_at": int(time.time() * 1000)
                        })
                    _, reg = _execute_dynamo_op(_create_user_otp)

                masked_dest = user_id

                # 2A. CANAL E-MAIL (AMAZON SES)
                if channel == "email":
                    ses_sender = os.environ.get("SES_SENDER_EMAIL") or user_id
                    env_region = os.environ.get("AWS_REGION") or reg or "us-east-2"
                    ses_client = boto3.client("ses", region_name=env_region)

                    email_subject = f"🔐 Código de Verificação: {otp_code} · Roteiro de IA"
                    email_html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#0f172a;color:#f8fafc;padding:30px 15px;margin:0">
  <div style="max-width:520px;margin:0 auto;background:#1e293b;border:1px solid #334155;border-radius:14px;padding:28px 24px;box-shadow:0 10px 25px rgba(0,0,0,0.5)">
    <div style="text-align:center;margin-bottom:20px">
      <span style="font-size:42px">🚀</span>
      <h2 style="color:#ff9900;margin:10px 0 4px;font-size:22px;letter-spacing:-0.5px">Roteiro de Estudo · Do Zero à IA</h2>
      <p style="color:#94a3b8;font-size:13px;margin:0">Verificação Segura de Acesso em Duas Etapas (OTP)</p>
    </div>
    
    <div style="background:#0f172a;border:1px solid #ff9900;border-radius:10px;padding:20px;text-align:center;margin:24px 0">
      <div style="color:#94a3b8;font-size:12px;font-weight:700;letter-spacing:1px;text-transform:uppercase;margin-bottom:8px">Seu Código de Segurança</div>
      <div style="font-family:monospace;font-size:36px;font-weight:800;letter-spacing:8px;color:#ff9900">{otp_code}</div>
      <div style="color:#64748b;font-size:12px;margin-top:8px">⏱️ Válido por 10 minutos</div>
    </div>
    
    <p style="font-size:14px;line-height:1.6;color:#cbd5e1;margin-bottom:12px">
      Olá! Recebemos uma solicitação para redefinir a senha da sua conta <b>{user_id}</b>. Insira o código acima no formulário de recuperação para criar sua nova senha.
    </p>
    <p style="font-size:12px;color:#64748b;line-height:1.5;margin-top:24px;border-top:1px solid #334155;padding-top:14px">
      🛡️ Se você não solicitou esta redefinição, fique tranquilo: sua senha e anotações permanecem protegidas.
    </p>
  </div>
</body>
</html>"""
                    email_text = f"Roteiro de IA - Código de Verificação: {otp_code}\n\nUtilize este código para redefinir sua senha. Ele expira em 10 minutos."

                    try:
                        ses_client.send_email(
                            Source=ses_sender,
                            Destination={"ToAddresses": [user_id]},
                            Message={
                                "Subject": {"Data": email_subject, "Charset": "UTF-8"},
                                "Body": {
                                    "Html": {"Data": email_html, "Charset": "UTF-8"},
                                    "Text": {"Data": email_text, "Charset": "UTF-8"}
                                }
                            }
                        )
                    except Exception as ses_err:
                        err_str = str(ses_err)
                        hint = "Verifique se o e-mail está verificado no console do Amazon SES (Identities) e se a Role da Lambda possui a permissão 'ses:SendEmail'."
                        return _cors_response(400, {
                            "ok": False,
                            "error": f"Falha ao enviar e-mail via Amazon SES: {err_str}",
                            "hint": hint
                        })

                    parts = user_id.split("@")
                    masked_dest = f"{parts[0][:2]}***@{parts[1]}" if len(parts[0]) > 2 else f"*@{parts[1]}"

                # 2B. CANAL WHATSAPP (WEBHOOK OU TWILIO)
                elif channel == "whatsapp":
                    clean_phone = "".join(filter(str.isdigit, phone))
                    if len(clean_phone) < 10:
                        return _cors_response(400, {
                            "ok": False,
                            "error": "Número de WhatsApp inválido. Informe o DDD e o número completo (mínimo 10 dígitos)."
                        })

                    msg_text = f"🔐 *Roteiro de IA* - Seu código de verificação é: *{otp_code}*\n\n(Válido por 10 minutos para redefinir sua senha)"
                    webhook_url = os.environ.get("WHATSAPP_WEBHOOK_URL")
                    twilio_sid = os.environ.get("TWILIO_ACCOUNT_SID")
                    twilio_token = os.environ.get("TWILIO_AUTH_TOKEN")
                    twilio_from = os.environ.get("TWILIO_WHATSAPP_NUMBER", "whatsapp:+14155238886")

                    if webhook_url:
                        try:
                            req_payload = json.dumps({
                                "phone": clean_phone,
                                "message": msg_text,
                                "code": otp_code,
                                "user_id": user_id
                            }).encode("utf-8")
                            req = urllib.request.Request(
                                webhook_url,
                                data=req_payload,
                                headers={"Content-Type": "application/json", "User-Agent": "RoteiroIA-Lambda/1.0"}
                            )
                            with urllib.request.urlopen(req, timeout=10) as resp:
                                pass
                        except Exception as wh_err:
                            return _cors_response(400, {
                                "ok": False,
                                "error": f"Falha ao acionar Webhook do WhatsApp: {str(wh_err)}",
                                "hint": "Verifique se a URL em WHATSAPP_WEBHOOK_URL está acessível."
                            })
                    elif twilio_sid and twilio_token:
                        try:
                            to_num = f"whatsapp:+55{clean_phone}" if not clean_phone.startswith("55") else f"whatsapp:+{clean_phone}"
                            twilio_url = f"https://api.twilio.com/2010-04-01/Accounts/{twilio_sid}/Messages.json"
                            form_data = urllib.parse.urlencode({
                                "From": twilio_from,
                                "To": to_num,
                                "Body": msg_text
                            }).encode("utf-8")
                            auth_header = base64.b64encode(f"{twilio_sid}:{twilio_token}".encode("utf-8")).decode("utf-8")
                            req = urllib.request.Request(
                                twilio_url,
                                data=form_data,
                                headers={
                                    "Authorization": f"Basic {auth_header}",
                                    "Content-Type": "application/x-www-form-urlencoded"
                                }
                            )
                            with urllib.request.urlopen(req, timeout=10) as resp:
                                pass
                        except Exception as tw_err:
                            return _cors_response(400, {
                                "ok": False,
                                "error": f"Falha ao enviar WhatsApp via Twilio: {str(tw_err)}",
                                "hint": "Verifique o TWILIO_ACCOUNT_SID e TWILIO_AUTH_TOKEN na Lambda, e se o seu número ingressou no Twilio Sandbox."
                            })
                    else:
                        return _cors_response(400, {
                            "ok": False,
                            "error": "Envio por WhatsApp ainda não configurado na Lambda.",
                            "hint": "Para ativar o WhatsApp, configure as variáveis de ambiente 'WHATSAPP_WEBHOOK_URL' ou 'TWILIO_ACCOUNT_SID' + 'TWILIO_AUTH_TOKEN' na Lambda AWS. Você também pode utilizar a opção de E-mail (SES)!"
                        })

                    masked_dest = f"({clean_phone[:2]}) 9****-{clean_phone[-4:]}" if len(clean_phone) >= 11 else f"***{clean_phone[-4:]}"

                return _cors_response(200, {
                    "ok": True,
                    "sent": True,
                    "channel": channel,
                    "masked_destination": masked_dest,
                    "expires_in_seconds": 600
                })

            # -----------------------------------------------------------------
            # AÇÃO 2: VALIDAR CÓDIGO OTP & ATUALIZAR SENHA
            # -----------------------------------------------------------------
            elif action == "confirm_reset":
                code = str(payload.get("code") or "").strip()
                new_pwd_hash = str(payload.get("new_pwd_hash") or "").strip()

                if not code or len(code) != 6:
                    return _cors_response(400, {"ok": False, "error": "Informe o código de 6 dígitos."})
                if not new_pwd_hash:
                    return _cors_response(400, {"ok": False, "error": "Hash da nova senha não fornecido."})

                def _get_user(tbl):
                    return tbl.get_item(Key={"user_id": user_id})

                resp, reg = _execute_dynamo_op(_get_user)
                item = resp.get("Item")
                if not item:
                    return _cors_response(404, {"ok": False, "error": "Usuário não encontrado."})

                saved_code = str(item.get("reset_code") or "").strip()
                expires_at = int(item.get("reset_expires_at") or 0)

                if not saved_code or saved_code != code:
                    return _cors_response(400, {
                        "ok": False,
                        "error": "Código de verificação incorreto. Verifique os dígitos e tente novamente."
                    })

                if int(time.time()) > expires_at:
                    return _cors_response(400, {
                        "ok": False,
                        "error": "Código de verificação expirado (validade de 10 minutos). Solicite um novo código."
                    })

                def _update_pass(tbl):
                    return tbl.update_item(
                        Key={"user_id": user_id},
                        UpdateExpression="SET pwd_hash = :p, updated_at = :u REMOVE reset_code, reset_expires_at, reset_channel",
                        ExpressionAttributeValues={
                            ":p": new_pwd_hash,
                            ":u": int(time.time() * 1000)
                        }
                    )

                _execute_dynamo_op(_update_pass)

                return _cors_response(200, {
                    "ok": True,
                    "success": True,
                    "user_id": user_id,
                    "user_name": item.get("user_name", "João Naziozeno"),
                    "message": "Senha redefinida com sucesso no DynamoDB!"
                })

            # -----------------------------------------------------------------
            # AÇÃO PADRÃO: SINCRONIZAÇÃO EM TEMPO REAL COM DYNAMODB (PUT ITEM)
            # -----------------------------------------------------------------
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
