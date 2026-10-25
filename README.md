# RD SENSI + RD OTIMIZAÇÃO

Painéis para Free Fire / Free Fire MAX com sensibilidades e otimização para Apple, Motorola, Samsung, Poco e Redmi (366 modelos).

## iPhone (Web App)
- **RD SENSI:** https://rickznn.github.io/RD-SENSI/
- **RD OTIMIZAÇÃO:** https://rickznn.github.io/RD-SENSI/otimizacao/

Abra no **Safari** → **Compartilhar** → **Adicionar à Tela de Início**.

## Android (APK)
- [RD-SENSI.apk](downloads/RD-SENSI.apk)
- [RD-OTIMIZACAO.apk](downloads/RD-OTIMIZACAO.apk)

Baixe no celular, abra o arquivo e permita "Instalar apps desconhecidos".

## Estrutura
| Pasta | Conteúdo |
|---|---|
| `/` | Web App do RD SENSI (GitHub Pages) |
| `/otimizacao/` | Web App do RD OTIMIZAÇÃO |
| `/downloads/` | APKs prontos |
| `/projeto/` | Código-fonte: `index.html` (RD SENSI), `make_iphone.py`, `make_otim.py` e projetos Android (`apk/`, `apk-otim/`) |

## Gerar os APKs
Requer Android SDK (platform 34, build-tools 34.0.0) em `~/android-sdk` e a keystore (não incluída no repositório).

```bash
cd projeto
python3 make_otim.py
KS_PASS=<senha> bash apk/build.sh
KS_PASS=<senha> bash apk-otim/build.sh
```
