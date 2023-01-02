import pandas as pd
import re
from playwright.sync_api import sync_playwright

#NECESSÁRIO INSTALAR A BIBLIOTECA PLAYWRIGHT

def create_tbl_price_0(user_pot):
    tbl_ref = pd.read_excel("..\\file\\TBL_REF.xlsx")# TABELA DE REFERENCIA QUE SERÁ CONSUMIDA DO BANCO 
    if user_pot<=tbl_ref.iloc[0,0]:
        price_kwh = tbl_ref.iloc[0,2]
    elif user_pot>tbl_ref.iloc[0,1] and user_pot<=tbl_ref.iloc[0,2]:
        price_kwh = tbl_ref.iloc[1,2]
    elif user_pot>tbl_ref.iloc[0,2] and user_pot<=tbl_ref.iloc[0,3]:
        price_kwh = tbl_ref.iloc[2,2]
    else:
        price_kwh = tbl_ref.iloc[3,2]
        
    price_usin = user_pot*price_kwh

    return tbl_ref,price_usin



def create_tbl_price_1(user_pot):
    values = create_tbl_price_0(user_pot)
    tbl_ref=values[0]
    if user_pot<=tbl_ref.iloc[0,0]:
        price_om = tbl_ref.iloc[0,1]
    elif user_pot>tbl_ref.iloc[0,1] and user_pot<=tbl_ref.iloc[0,2]:
        price_om = tbl_ref.iloc[1,1]
    elif user_pot>tbl_ref.iloc[0,2] and user_pot<=tbl_ref.iloc[0,3]:
        price_om = tbl_ref.iloc[2,1]
    else:
        price_om = tbl_ref.iloc[3,1]
    
    year_om = values[1]*price_om
    return year_om #VALOR DO O&M DO ANO DE ACORDO COM O CALCULO DO DATAFRAME MAYA



def create_tbl_price_2(user_pot, user_assina, user_height):
    values = create_tbl_price_1(user_pot)
    tbl_ref=create_tbl_price_0(user_pot)[0]
    if user_height==0:
        desc_altura = tbl_ref.iloc[0,4]
    elif user_height==1:
        desc_altura = tbl_ref.iloc[1,4]
    elif user_height==2:
        desc_altura = tbl_ref.iloc[2,4]
    else:
        desc_altura = tbl_ref.iloc[3,4]

    if user_assina=='KILOWATT':
        desc_ass = tbl_ref.iloc[0,6]
    elif user_assina=='MEGAWATT':
        desc_ass = tbl_ref.iloc[1,6]
    elif user_assina=='GIGAWATT':
        desc_ass = tbl_ref.iloc[2,6]
    else:
        desc_ass = tbl_ref.iloc[3,6]
    if user_assina=='KILOWATT':
        spread_desc_altura = 0 
    else:
        spread_desc_altura = values*desc_altura
    spread_desc_assin = values*(desc_ass)
    return spread_desc_altura,spread_desc_assin,values # valores da tablea B.2 fornecendo a potencia do usuario, altura da usina, e plano de assinatura (values=year_o&m)



def info_seg(user_pot,user_assina):
    tbl_ref=create_tbl_price_0(user_pot)[0]
    if user_assina=='GIGAWATT':
        desc = tbl_ref.iloc[0,8]
    else:
        desc = 0
    valor_seguro = create_tbl_price_0(user_pot)[1]*desc
    return valor_seguro



#WEB SCRAPING DISTANCIA GOOGLEMAPS
def user_dist(user_dist):
    with sync_playwright() as p:
        
        nav = p.chromium.launch()
        page = nav.new_page()
        page.goto("https://www.google.com/maps?q=google+maps&um=1&ie=UTF-8&sa=X&ved=2ahUKEwiH8d7v3sz7AhWnp5UCHct9AaMQ_AUoAXoECAEQAw")
        page.locator('id=searchboxinput').fill('Av. Professor Mário Werneck, 26 - Estoril, Belo Horizonte - MG, 30455-610, Brazil')
        page.locator('id=searchbox-searchbutton').click()
        page.locator('xpath=//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[4]/div[1]/button').click()
        
        page.locator('xpath=//*[@id="sb_ifc50"]/input').fill(f'{user_dist}')
        page.locator('xpath=//*[@id="directions-searchbox-0"]/button[1]').click()
        dist_raw = page.locator('xpath=/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[4]/div[1]/div[1]/div[1]/div[1]/div[2]/div').text_content()
        dist = float((re.findall('[0-9]+,[0-9]', dist_raw)[0]).replace(',','.'))
    return dist


def dist_price(user_address,user_pot,price_ratio):
    # dist = user_dist(user_address)  # Função já criada para calculo de distancia através do playwright
    #l= user_address # COMENTE CASO NAO USAR A FUNCAO DE RASPAGEM
    dist = 42.431
    if user_pot<100:
        dist_price = dist*4*price_ratio*2 # Multiplica pela qtd 
    else:
        dist_price = dist*5*2*price_ratio
    return dist_price

# print(dist_price('rua aquidaban,925',6.8,1))

#VALOR FINAL DA TABLEA B.2

def final_price(user_pot, user_assina, user_height,user_address,qtd,price_ratio):
    valor_0=create_tbl_price_2(user_pot, user_assina, user_height)[0]

    valor_1=create_tbl_price_2(user_pot, user_assina, user_height)[1]

    valor_2=create_tbl_price_2(user_pot, user_assina, user_height)[2]
    valor_seguro = info_seg(user_pot,user_assina)

    valor_distancia = dist_price(user_address,qtd,price_ratio)
    valor_final = valor_0+valor_1+valor_2+valor_seguro+valor_distancia# Valor final do custo
    return valor_final



# VALOR FINAL TABLEA B3 - GERANDO O CUSTO PARA OS PLANOS
def create_plano_mensal(user_pot, user_assina, user_height,user_address,price_ratio):
    tbl_ref=create_tbl_price_0(user_pot)[0]
    valor_2=create_tbl_price_2(user_pot, user_assina, user_height)[2]
    plano_m_kilo = valor_2-(tbl_ref.iloc[0,6]*valor_2)


    spread = create_tbl_price_2(user_pot, user_assina, user_height)[0]
    om_ano = create_tbl_price_1(user_pot)#Valor do O&M
    valor_dist = dist_price(user_address,user_pot,price_ratio)
    plano_m_mega=om_ano+spread+valor_dist

    om_ano = create_tbl_price_1(user_pot)#Valor do O&M
    valor_seg = info_seg(user_pot,user_assina)
    preco_usina = create_tbl_price_0(user_pot)[1]
    # plano_m_giga = om_ano+spread+valor_seg+valor_dist*2+((preco_usina*tbl_ref.iloc[0,8]))/12
    plano_m_giga= plano_m_mega+valor_seg+valor_dist
    #CRIAÇÃO DO PLANO 
    df = pd.DataFrame(index=['ASS. MES','ASS. ANO','O&M'],columns=['KILOWATT','MEGAWATT','GIGAWATT'])
    df.iloc[0,0]=round(plano_m_kilo/12,2)
    df.iloc[0,1]=round(plano_m_mega/12,2)
    df.iloc[0,2]=round(plano_m_giga/12,2)
    df.iloc[1,0]=round(plano_m_kilo,2)
    df.iloc[1,1]=round(plano_m_mega,2)
    df.iloc[1,2]=round(plano_m_giga,2)
    df.iloc[2,0]="{:.2%}".format(plano_m_kilo/preco_usina)
    df.iloc[2,1]="{:.2%}".format(plano_m_mega/preco_usina)
    df.iloc[2,2]="{:.2%}".format(plano_m_giga/preco_usina)
    
    return df.to_json() 


# OS PAREMETROS DE ENTRADA SÃO: POTENCIA DA USINA, TIPO DE PLANO, ALTURA, QUANTIDADE,ENDEREÇO PREÇO POR KW, 
#create_plano_mensal(user_pot (Kwp), user_assina (plano e assinatura), user_height (Usina solo ou telhado), user_address (Endereço de instalação),price_ratio)

#PARA INFORMÇÃO DE ALTURA: 
# VALOR 0 = ATÉ 4M
# VALOR 1 = 4 A 6M
# VALOR 2 = ACIMA DE 6M
# VALOR 3 = SOLO Av. Otacílio Negrão de Lima, 17 - Centro, Ibirité - MG, 32400-000, Brazil

# print(f"A distancia do usuario e {user_dist('Av. Otacílio Negrão de Lima, 17 - Centro, Ibirité - MG, 32400-000, Brazil')}")

# print(create_plano_mensal(6.8,'GIGAWATT',3,'Rua padre Eustáquio, 1024, padre Eustáquio',1))