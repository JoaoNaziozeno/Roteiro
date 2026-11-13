# Deploy do login multiusuário

Este guia publica a Lambda nova (`aws_lambda_dynamodb.py`) e o site novo (`feat/login-multiusuario`).
Os dois precisam entrar no ar **juntos**: a Lambda nova não entende o site antigo e vice-versa.
Enquanto só um deles estiver publicado, a sincronização e o login ficam fora do ar.

- **Site:** https://joaonaziozeno.github.io/Roteiro/ (GitHub Pages, branch `main`, raiz)
- **Lambda:** Function URL `https://x37p5anc5yesrwweqfbwxcexsu0dpzdu.lambda-url.us-east-2.on.aws/` (us-east-2)
- **Tabela:** `roteiro_estudos_joao` (DynamoDB). Não é preciso criar tabela nova.

Tempo estimado: cerca de 40 minutos, sem contar a liberação do SES pela AWS (pode levar até 24 h).

---

## Antes do dia do deploy

### 1. Prepare o Amazon SES
Abra o SES já na região certa: `https://us-east-2.console.aws.amazon.com/ses/home?region=us-east-2`.

1. **Configuração → Identidades → Criar identidade → Endereço de e-mail**: verifique o remetente (por exemplo, o seu Gmail) clicando no link que a AWS mandar. Esse endereço vai em `SES_SENDER_EMAIL`.
2. Envie um **e-mail de teste** para você mesmo (Identidades → marque o e-mail → Enviar e-mail de teste → Personalizado). Com remetente `@gmail.com`, ele costuma cair no **spam**: marque "Não é spam".

**Sandbox ou produção?** Nesta conta, o botão **Solicitar acesso à produção** só é liberado depois de verificar um **domínio** (aviso "Verificação de domínio necessária"). Dá para funcionar de graça no sandbox:

- O SES só entrega para endereços verificados, até 200 e-mails por dia.
- **Antes de convidar um aluno**, cadastre o e-mail dele em **Identidades** e peça para ele clicar no link da AWS. Depois convide pelo `admin.html`. Se o convite sair antes, o painel avisa que o e-mail não foi enviado: verifique o endereço e use **Reenviar convite**.
- Para liberar convites para qualquer pessoa (e ajudar a sair do spam), registre um domínio (Registro.br ou Route 53), verifique-o em **Criar identidade → Domínio** colando os registros DKIM no DNS, e então use **Solicitar acesso à produção** (tipo **Transacional**, site `https://joaonaziozeno.github.io/Roteiro/`).

### 2. Gere os dois segredos
Rode no seu terminal, duas vezes, e guarde cada resultado num gerenciador de senhas:

```bash
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

- O primeiro resultado será o `TOKEN_SECRET`. Ele assina os logins. Se vazar, troque-o: todo mundo precisa entrar de novo.
- O segundo será o `BOOTSTRAP_SECRET`. Ele só serve para criar a conta admin e é apagado no fim deste guia.

### 3. Faça um backup da tabela
DynamoDB → Tables → `roteiro_estudos_joao` → **Backups → Create backup** (sob demanda). Assim dá para voltar tudo se algo sair errado.

---

## No dia do deploy

### 4. Ajuste a Lambda (antes de trocar o código)
Na função Lambda:

1. **Configuration → Environment variables → Edit**, adicione:

   | Chave | Valor |
   |---|---|
   | `TOKEN_SECRET` | o primeiro segredo do passo 2 |
   | `BOOTSTRAP_SECRET` | o segundo segredo do passo 2 |
   | `SES_SENDER_EMAIL` | o remetente verificado no SES |
   | `APP_URL` | `https://joaonaziozeno.github.io/Roteiro/index.html` |

   Pode apagar as variáveis antigas do WhatsApp/Twilio, se existirem.
2. **Configuration → General configuration → Edit**: memória **256 MB** e tempo limite **10 s**. A senha é conferida com PBKDF2 (600 mil iterações), o que pesa um pouco na CPU.
3. **Configuration → Permissions →** clique na Role: confirme que ela tem acesso ao DynamoDB (`AmazonDynamoDBFullAccess` ou equivalente) e adicione `ses:SendEmail` (por exemplo, a política `AmazonSESFullAccess`, ou uma política só com `ses:SendEmail`).

### 5. Restrinja o CORS da Function URL
**Configuration → Function URL → Edit → Configure CORS**:

- **Allow origin:** `https://joaonaziozeno.github.io` (sem `/Roteiro` e sem barra no fim)
- **Allow methods:** `GET`, `POST`
- **Allow headers:** `content-type`, `authorization`
- **Allow credentials:** desmarcado
- **Auth type:** continua `NONE`, porque quem confere o acesso agora é o próprio código.

### 6. Publique o código novo (a partir daqui o site antigo para de sincronizar)
1. **Code**: abra `lambda_function.py`, apague tudo, cole todo o conteúdo de `aws_lambda_dynamodb.py` deste branch e clique em **Deploy**.
2. Confirme que o **Handler** (em Runtime settings) é `lambda_function.lambda_handler`.
3. No seu terminal, na pasta do projeto:

   ```bash
   python verificar_deploy.py
   ```

   Ele confere a versão da Lambda, o CORS e se ela recusa pedidos sem login. Siga em frente só quando todos os itens estiverem OK.

### 7. Crie a conta admin
Use um e-mail **diferente** do seu e-mail de aluno.

```bash
python criar_admin.py
```

O script pede a URL (Enter usa a padrão), o `BOOTSTRAP_SECRET`, o e-mail, o nome e a senha do admin. A senha não aparece na tela.

### 8. Publique o site novo
Faça o merge do PR do branch `feat/login-multiusuario` na `main`. O GitHub Pages republica em 1 a 2 minutos. Depois disso, rode de novo:

```bash
python verificar_deploy.py --site
```

### 9. Convide você mesmo como aluno
1. Abra `https://joaonaziozeno.github.io/Roteiro/admin.html` e entre com a conta admin.
2. Convide o seu e-mail de aluno, o mesmo que você usava antes. A mensagem deve dizer que **o progresso que já existia foi importado**.
3. Abra o site, clique em **Tenho um convite**, use o código do e-mail e crie a senha.
4. Confira se o seu progresso apareceu. Nos aparelhos em que você marcava "Lembrar meu acesso" com esse e-mail, o que estava salvo localmente também é mantido.

### 10. Apague o BOOTSTRAP_SECRET
Lambda → Environment variables → remova `BOOTSTRAP_SECRET` → Save. Sem ele, ninguém consegue criar outro admin.
Se um dia você esquecer a senha do admin, coloque um `BOOTSTRAP_SECRET` novo, rode `criar_admin.py` com o mesmo e-mail do admin (isso redefine a senha) e apague a variável de novo.

---

## Conferência final

- [ ] No site, sem login, abrir `ia.html` leva para a tela de login.
- [ ] Entrar com a sua conta de aluno mostra o seu progresso; marcar um tópico mostra "Salvo na nuvem".
- [ ] Em outra janela anônima, a conta admin **não** entra no site do aluno, e a conta de aluno **não** entra no `admin.html`.
- [ ] Convidar um segundo e-mail seu (ou de alguém de confiança) e conferir se o convite chega.
- [ ] No painel, o histórico mostra o convite e a importação.

## Se algo der errado

- **Voltar a Lambda:** cole de novo o código antigo (`git show fd52415:aws_lambda_dynamodb.py`) e clique em Deploy. O site antigo volta a funcionar com os dados de antes.
- **Voltar o site:** reverta o merge na `main` (`git revert -m 1 <commit do merge>`) e envie.
- **Dados:** restaure o backup do passo 3 (DynamoDB → Backups → Restore).

## Limpeza (depois de alguns dias funcionando)

Os itens antigos da tabela, com a chave igual ao e-mail puro (sem `acct#` ou `data#`), ainda guardam o hash de senha do formato antigo.
Depois de confirmar que o seu progresso foi importado, apague esses itens em DynamoDB → Explore items.
