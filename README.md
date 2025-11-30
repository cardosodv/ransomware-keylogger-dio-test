# ransomware-keylogger-dio-test

Este repositório foi desenvolvido como desafio do curso de cibersegurança da DIO, implementando simulações seguras de Ransomware (usando criptografia Fernet) e Keylogger (com captura de teclas via pynput). O foco é educativo: entender como malwares operam para melhor prevenir ataques reais.
Projeto educacional que simula o funcionamento de um ransomware simples e de um keylogger com envio automático por e-mail, utilizando Python, em ambiente 100% controlado para fins de estudo em cibersegurança. 

## ⚠ Aviso Importante

Este projeto tem **apenas fins educacionais**.  
Os scripts devem ser executados **somente em ambientes de teste / máquinas virtuais**, nunca em sistemas de produção ou de terceiros. O uso malicioso é de total responsabilidade do usuário. 

---

## 🔐 Ransomware Simulado

### ransoware.py

Funções principais: 
- Gera uma chave de criptografia simétrica com `Fernet.generate_key()` e salva em `chave.key`.  
- Carrega a chave salva em `chave.key`.  
- Percorre o diretório `test_files/` recursivamente e monta uma lista de arquivos para criptografar, ignorando o próprio `ransoware.py` e arquivos com extensão `.key`.  
- Abre cada arquivo em modo binário, criptografa o conteúdo com Fernet e sobrescreve o arquivo com os dados criptografados.  
- Cria um arquivo de texto `LEIA ISSO.txt` com uma mensagem de “resgate” simulada.  
- Exibe no console a mensagem `Ransoware executado! Arquivos criptografados!`.  

### Uso sugerido

python ransoware.py


Antes de executar, crie uma pasta `test_files/` com alguns arquivos de teste (por exemplo, `.txt`) para observar o efeito da criptografia.

---

### descriptografar.py

Funções principais:
- Lê a chave de criptografia a partir do arquivo `chave.key`.  
- Percorre recursivamente o diretório `test_files/`, ignorando o script `ransoware.py` e arquivos `.key`.  
- Para cada arquivo encontrado, lê o conteúdo criptografado, descriptografa usando a chave e sobrescreve o arquivo com o conteúdo original.  
- Ao final, imprime a mensagem `Arquivos restaurados com sucesso`.  

### Uso sugerido

python descriptografar.py


> Importante: a descriptografia só funciona se `chave.key` for o mesmo arquivo gerado pelo `ransoware.py` no momento da criptografia.

---

## ⌨ Keyloggers

### keylogger_email.py (com envio por e-mail)

O script implementa um keylogger simples com envio automático de logs por e-mail:
- Usa `pynput.keyboard.Listener` para capturar as teclas pressionadas no sistema.  
- Mantém um buffer de texto na variável global `log`, onde são armazenadas as teclas capturadas.  
- Trata teclas especiais: espaço (` `), enter (`\n`) e backspace (registrado como `[<]`), enquanto ignora outras teclas de controle.  
- A função `enviar_email()` monta um e-mail com o conteúdo do `log` usando `MIMEText` e envia via `smtplib` para o endereço configurado.  
- Após o envio, o `log` é limpo e um novo envio é agendado a cada 60 segundos com `Timer(60, enviar_email).start()`.  

Configurações principais no topo do arquivo:
- `EMAIL_ORIGEM`  
- `EMAIL_DESTINO`  
- `SENHA_EMAIL` (recomendado usar **senha de app** do Gmail, não a senha principal da conta)

#### Uso sugerido

python keylogger_email.py

> Execute somente em ambiente controlado e com e-mail de teste. Nunca use esse tipo de script sem autorização expressa.

---

### keylogger.pyw (keylogger “furtivo” com log em arquivo)

Este script implementa um keylogger focado em captura silenciosa de teclas para um arquivo local `log.txt`, sem interface de console (por isso a extensão `.pyw` no Windows:
- Usa `pynput.keyboard.Listener` para monitorar eventos de teclado em segundo plano.  
- Mantém um conjunto `pressed_keys` para evitar registrar múltiplas vezes a mesma tecla enquanto ela permanece pressionada.  
- Ignora teclas de modificação como Shift, Ctrl, Alt, Caps Lock e tecla Windows, definidas no conjunto `ignorar`.  
- Para teclas alfanuméricas, grava diretamente o caractere em `log.txt` com codificação UTF-8.  
- Para teclas especiais, registra representações legíveis, como:
  - Espaço: `" "`  
  - Enter: `\n`  
  - Tab: `\t`  
  - Esc: ` [ESC] `  
  - Backspace: ` [BKSP] `  
  - Outras teclas especiais: forma `[TECLA]`, por exemplo `[Key.f1]`.  

Quando a tecla é liberada, ela é removida de `pressed_keys`, permitindo ser registrada novamente em um próximo pressionamento.

#### Uso sugerido

python keylogger.pyw


> A extensão `.pyw` faz com que o script rode sem abrir janela de console em sistemas Windows, tornando a execução mais discreta em cenários de teste. Use apenas em ambiente controlado.

---

## 🧪 Como Executar o Projeto

1. Certifique-se de ter o Python 3 instalado.  
2. Instale as dependências necessárias (exemplo):  
pip install cryptography pynput
3. Crie a pasta `test_files/` e coloque alguns arquivos de teste para o ransomware.  
4. Rode o ransomware simulado:  
python ransoware.py
5. Verifique os arquivos criptografados em `test_files/` e o arquivo `LEIA ISSO.txt`. 
6. Rode o script de descriptografia para restaurar os arquivos:  
python descriptografar.py
7. Para testar o keylogger com envio de e-mail, ajuste as credenciais de e-mail e senha no `keylogger_email.py` e execute:  
python keylogger_email.py
8. Para testar o keylogger “furtivo” que grava em `log.txt`, execute:  
python keylogger.pyw



---

## 🛡 Reflexão sobre Defesa e Prevenção

Este projeto ajuda a entender, na prática:  
- Como ransomwares dependem do acesso a arquivos e de uma chave de criptografia para sequestrar dados, e como a perda ou vazamento dessa chave impacta a recuperação.
- Como keyloggers podem capturar tudo o que é digitado e exfiltrar ou registrar esses dados, por exemplo, via e-mail automatizado ou logs locais, de forma silenciosa. 
