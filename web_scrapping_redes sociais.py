from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import pandas as pd
from datetime import datetime
import os
import re

CAMINHO_USER_DATA = r"C:\Users\SEU_USUARIO\AppData\Local\Microsoft\Edge\User Data"
NOME_DO_PERFIL = "Default" 
NOME_ARQUIVO = r"C:\Caminho\Para\Seu\Arquivo\metricas_sociais.xlsx"
CAMINHO_DRIVER_MANUAL = r"C:\Caminho\Para\msedgedriver.exe"

def fechar_edge_forçado():
    """Fecha instâncias do Edge para liberar o uso do perfil/cookies"""
    print("Liberando perfil do navegador...")
    try:
        os.system("taskkill /f /im msedge.exe >nul 2>&1")
        time.sleep(2)
    except:
        pass

def limpar_numero(texto):
    if not texto: return 0
    
    texto_limpo = str(texto).upper().strip()
    
    multiplicador = 1
    

    if 'MIL' in texto_limpo or 'K' in texto_limpo:
        multiplicador = 1000
        texto_limpo = texto_limpo.replace('MIL', '').replace('K', '')
    elif 'MI' in texto_limpo or 'M' in texto_limpo:
        multiplicador = 1000000
        texto_limpo = texto_limpo.replace('MI', '').replace('M', '')
    
   
    texto_limpo = texto_limpo.replace('.', '').replace(',', '.')
    
    try:
   
        numero_final = re.sub(r"[^0-9\.]", "", texto_limpo)
        return int(float(numero_final) * multiplicador)
    except:
        return 0

def iniciar_driver():
    fechar_edge_forçado()
    
    edge_options = Options()
    edge_options.add_argument(f"user-data-dir={CAMINHO_USER_DATA}")
    edge_options.add_argument(f"profile-directory={NOME_DO_PERFIL}")
    

    edge_options.add_argument("--start-maximized")
    edge_options.add_argument("--disable-gpu")
    edge_options.add_argument("--disable-software-rasterizer")
    edge_options.add_argument("--log-level=3") 
    edge_options.add_argument("--silent")
    edge_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    edge_options.add_argument("--disable-blink-features=AutomationControlled")
    
    service = Service(executable_path=CAMINHO_DRIVER_MANUAL)
    driver = webdriver.Edge(service=service, options=edge_options)
    return driver

def pegar_dados_completos():
    driver = iniciar_driver()
    dados = {
        "Data_Atualizacao": datetime.now().strftime('%d/%m/%Y'),
        "Hora": datetime.now().strftime('%H:%M')
    }

    print("--- INICIANDO COLETA NAS REDES ---")


    redes_gerais = {
      "Instagram": "https://www.instagram.com/seu_perfil/",
        "YouTube": "https://www.youtube.com/@seu_perfil",
        "Facebook": "https://www.facebook.com/seu_perfil",
    }

    for rede, url in redes_gerais.items():
        try:
            print(f"Coletando: {rede}...")
            driver.get(url)
            time.sleep(5)
            
            try: webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
            except: pass

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            texto_pagina = soup.get_text(separator=' ')

            padrao = r"([0-9.,]+\s*(?:mil|mi|k|m)?)\s+(?:seguidores|followers|inscritos|subscribers)"
            match = re.search(padrao, texto_pagina, re.IGNORECASE)
            
            if match:
                dados[rede] = limpar_numero(match.group(1))
                print(f"   -> {rede}: {dados[rede]}")
            else:
                dados[rede] = "Não localizado"
        except Exception as e:
            print(f"Erro em {rede}: {e}")
            dados[rede] = 0


    try:
        print("Coletando: LinkedIn (Dado Detalhado)...")
        driver.get("https://www.linkedin.com/company/seu_perfil/posts/?feedView=all")
        time.sleep(7) 
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        

        texto_pagina = soup.get_text(separator=' ')
        match_exato = re.search(r"([\d\.]+)\s+seguidores", texto_pagina)
        
        if match_exato:
            valor_bruto = match_exato.group(1)
         
            dados['LinkedIn'] = limpar_numero(valor_bruto)
            print(f"   -> LinkedIn (Exato): {dados['LinkedIn']}")
        else:
         
            tag_seguidores = soup.find('a', href=re.compile(r"followers"))
            if tag_seguidores:
                dados['LinkedIn'] = limpar_numero(tag_seguidores.get_text())
                print(f"   -> LinkedIn (via Link): {dados['LinkedIn']}")
            else:
                dados['LinkedIn'] = "Não localizado"
                
    except Exception as e:
        print(f"Erro LinkedIn: {e}")
        dados['LinkedIn'] = 0

    driver.quit()
    return dados

if __name__ == "__main__":
    resultado = pegar_dados_completos()
    
  
    df = pd.DataFrame([resultado])
    colunas_ordenadas = ["Data_Atualizacao", "Hora", "Instagram", "Facebook", "LinkedIn", "YouTube"]
    df = df[[c for c in colunas_ordenadas if c in df.columns]]

    df.to_excel(NOME_ARQUIVO, index=False)


    print(f" Planilha '{NOME_ARQUIVO}' atualizada.")
