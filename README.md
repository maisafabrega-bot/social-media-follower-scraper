# Automação de Monitoramento de Redes Sociais

Script em Python para extrair o número de seguidores do Instagram, YouTube, Facebook e LinkedIn usando Selenium e BeautifulSoup.

## Funcionalidades
- Abre o navegador Edge com perfil de usuário real (cookies salvos)
- Coleta seguidores de páginas públicas
- Salva histórico em planilha Excel
- Tratamento de erros para scraping no LinkedIn

## Como usar
1. Instale as dependências: "pip install -r requirements.txt"
2. Configure os caminhos das pastas no script
3. Execute o arquivo ".py"
   
##  Como Automatizar no Windows
Para que o script rode diariamente, recomendo o uso do Agendador de Tarefas do Windows
1. Abra o Agendador de Tarefas e clique em "Criar Tarefa"
2. Na aba Geral marque "Executar com privilégios mais altos"
3. Na aba Disparadores defina o horário 
4. Na aba Ações configure:
   - Programa: Caminho do arquivo em Python (ex: "C:\Python39\python.exe")
   - Adicionar argumentos: O caminho completo do script (ex: "C:\Projetos\bot_redes_sociais.py")
5. Na aba Condições, marque "Despertar o computador"
