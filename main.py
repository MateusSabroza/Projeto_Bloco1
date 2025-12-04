import oracledb
import os
from dotenv import load_dotenv
from datetime import datetime


#Definindo as variaveis globais
load_dotenv()
HOST = os.getenv("hostname")
PORT = os.getenv("port")
USER = os.getenv("username")
PASSWORD = os.getenv("password")
SERVICE = os.getenv("servicename")
caminho='init_modelagem.sql'
carrinho=dict()
estoque=dict()
colunas=list()
## Criando funcaos essenciais
def main():
    '''Função principal de interação com o usuario'''
    criar_modelo()

    
    print(f'  {'#'*29}\n ## Bem vindo a Amazonense! ##\n{'#'*29}\n')
    while True:
        entrada=input('O que deseja?\n1-Adicionar produtos\n2-Escolher Produtos\n3-Carrinho\n4-Sair\n')
        
        print('#'*30,'\n'*20)
        if entrada=='1':
            print('Cadastro de produto')
            cadatro_produtos()
                   
        elif entrada=='2':
            print('Selecionar itens do catalogo')
            selecionar_catalogo()
            
        elif entrada=='3':
            controlar_carrinho()
            
        elif entrada=='4':
            print('Até a próxima!')
            conn.close()
            print('Conexão com Oracle fechada')
            break

  
def ler_ddl(caminho: str)->list:
    '''Pega os comandos do arquivo ddl e retorna um lista dele'''
    try:
        with open(caminho,'r',encoding='utf-8') as arquivo:
            conteudo=arquivo.read()
            lista_comandos=list()
            comando=str()
            for linha in conteudo.splitlines():
                #print(linha)
                linha=linha.strip()
                if linha.startswith('--') or not linha:
                    #print(' '*3,'Passando')
                    continue
                
                if linha =='/':
                    #print(' '*3,'PLSQL')
                    if comando.strip():
                        #print(' '*3,'adicionado')
                        lista_comandos.append(comando)
                    comando=str()
                    continue
                if linha.endswith(';') and 'BEGIN' not in comando:
                    #print(' '*3,'final de comando')
                    comando+= ' '+ linha[:-1]
                    lista_comandos.append(comando)
                    comando=str()
                    continue
                    
                comando+=' '+linha
            if comando.strip():
                #print(' '*3,'adicionado')
                lista_comandos.append(comando.strip())
                    
    except Exception as e:
        print(f"Erro ao criar ao importar a modelagem: {e}")

    return lista_comandos

def criar_modelo()->None:
    try:
        cursor.execute('Select * from PRODUTO')
    except:
        lista_comandos = ler_ddl(caminho)
        for command in lista_comandos:
            try:
                cursor.execute(command)
                print('Comando rodado com sucesso:\n',command,'\n')
            except Exception as e:
                print(f"Erro ao criar: {e}")
        
def cadatro_produtos()->None:
    while True:
        nome,preco,qtd='','',''
        nome=input('Qual o nome do produto?\n')
        try:
            preco=float(f"{float(input('Qual o valor do produto?\n')):.2f}")
        except:
            print(f'Formato Invalido\n  Escreva no formato 12.34')
            
        try:
            qtd=int(input('Qual a quantidade?\n'))
        except:
            print(f'Formato Invalido\n  Escreva no formato 100')
            
        if nome and preco  and qtd :
            while True:
                print(f'O seu produto vai ser registrado como:\nNome:{nome} , Preço:R${preco} , Quantidade:{qtd}')
                try:
                  entrada=int(input('Confirma?\n1-Sim\n2-Não\n\n'))
                  if entrada ==1:
                      try:
                          produto={'nome':nome,'preco':preco,'qtd':qtd}
                          comando=f'INSERT INTO PRODUTO (NOME,PRECO,QTD_ESTOQUE) VALUES (:nome,:preco,:qtd)'
                          cursor.execute(comando,produto)
                          conn.commit()
                          print('Produto Registrado!') 
                          return
                      except Exception as e:
                          conn.rollback()
                          print('Erro ao casdastrar produto no banco:',e)
                  if entrada==2:
                      print('Produto cancelado. Recomeçando o cadastro.')
                      break
                  else:
                      print('Opção inválida. Digite apenas o número.')
                except ValueError:
                    print('Opção inválida. Digite apenas o número.')
                    continue # Volta a perguntar a confirmação
        
    #cursor.execute(comando)

def saida_do_diconario(coluna_list:list,estoque:dict,tamanho_bloco=50):
        saida='|'
        
        for col in coluna_list:
            tamanho=len(str(col))
            espaco=' '*(tamanho_bloco//2-tamanho//2)
            texto=espaco+str(col)+espaco
            if len(texto)%2!=0:
                texto=texto[:-1]
            saida+=texto+'|'

        print(saida)
        for id in estoque.keys():
            saida='|'  

            for num,val in enumerate(estoque[id].values()):        
                tamanho=len(str(val))
                espaco=' '*(tamanho_bloco//2-tamanho//2)
                if espaco:
                    texto=espaco+str(val)+espaco
                    if len(texto)%2!=0:
                        texto=texto[:-1]
                    saida+=texto+'|'       
                # sem espaço faz uma quebra de linha
                # adicionando outra
                else:
                    lista=str(val).split()
                    texto=str()
                    for palavra in lista:
                        if len(texto)+len(palavra)+1<=tamanho_bloco:
                            texto+=' ' +palavra
    
                        else:
                            #coloca a saida primeiro e depois a palavra
                            tamanho=len(texto)
                            espaco=' '*(tamanho_bloco//2-tamanho//2)
                            texto=espaco+str(texto)+espaco
                            if len(texto)%2!=0 and len(texto)!=tamanho_bloco:
                                texto=texto[:-1]
                            saida+=texto+'|' 
                            print(saida)
                            texto=palavra
                            bloco=' '*tamanho_bloco+'|'       
                            saida='|'+bloco*num
                            #num_cols=len(estoque[id].values())
                    tamanho=len(texto)
                    espaco=' '*(tamanho_bloco//2-tamanho//2)
                    texto=espaco+str(texto)+espaco
                    if len(texto)%2!=0:
                        texto=texto[:-1]
                    saida+=texto+'|'

            print(saida)

def selecionar_catalogo()->None:
    global carrinho
    global estoque
    global colunas
    if not list(estoque.values()):
        print('Checando o banco')
        try:
            cursor.execute('Select * from PRODUTO')
        except Exception as e:
            print(f"Erro ao consulta o banco: {e}")
            return

        produtos=cursor.fetchall()
        colunas=[col[0] for col in cursor.description]

        for produto in produtos:
            estoque[produto[0]]=dict(zip(colunas,produto))
            # Se a lista estiver vazia, avisa o usuário:
        if not produtos:
            print("Nenhum produto encontrado no catálogo.")

    print("\n###  Catálogo de Produtos  ###")

    saida_do_diconario(colunas,estoque)        
        
    while True:
        try:
            entrada=input('Escreva o ID do item que deseja:\nEscreva "q" pra voltar\n')
            if entrada=='q':
                break
            else:
                id=int(entrada)
                nome=estoque[id]['NOME']
                while True:
                    entrada=input(f'Escreva a quantidade do item {nome} que deseja:\nEscreva "q" pra voltar\n')
                    if entrada=='q':
                        break
                    quantidade_pedido=int(entrada)
                    quantidade_estoque=estoque[id]['QTD_ESTOQUE']
                    novo_qtd_estoque=quantidade_estoque-quantidade_pedido
                    if novo_qtd_estoque<0:
                        print(f'Quantidade indisponivel, quantidade disponivel {quantidade_estoque}')
                    else:
                        carrinho[id]=estoque[id]
                        if not 'QTD_PEDIDA' in carrinho[id]:
                            carrinho[id]['QTD_PEDIDA']=0
                        carrinho[id]['QTD_PEDIDA']+=quantidade_pedido
                        estoque[id]['QTD_ESTOQUE']=novo_qtd_estoque
                        total=carrinho[id]['QTD_PEDIDA']*carrinho[id]['PRECO']
                        carrinho[id]['VALOR_TOTAL']=total
                        #print(carrinho)
                        break
                print('\n'*30)
                print(f'Pedido {nome} adiconado ao carrinho, por R${total}')
                
        except:
            print('Formato invalido, escreva apenas números')
         
    print('\n'*30)

    ## Criando a modelagem no oracle

def controlar_carrinho():
    global carrinho
    global estoque
    def deletar_carrinho():
        pass
        
    #exibindo o carrinho pro usuario
    if not list(carrinho.values()):
        print('Carrinho vazio.')
        return
        
    print('Carrinho:')    
    saida_do_diconario(list(carrinho.values())[0].keys(),carrinho,30)  
    total=sum([i['VALOR_TOTAL'] for i in list(carrinho.values())])
    
    entrada=input(f'O que deseja fazer com o carrinho?\nO total da compra deu: R${total:.2f}\n1-Fechar pedido\n2-Tirar/Alterar um item\n3-Esvaziar Carrinho\n4-Voltar\n')
    if entrada=='1':
        try:
            ######## Inserção na tabela venda ########
            venda_id_gerado = cursor.var(oracledb.NUMBER)
            venda={'data_venda':datetime.now(),'VALOR_TOTAL': total, 'venda_id': venda_id_gerado}
            comando=f'INSERT INTO VENDA (DATA_VENDA,VALOR_TOTAL) VALUES (:data_venda,:VALOR_TOTAL) RETURNING ID INTO :venda_id'
            cursor.execute(comando,venda)
            
            
            ######## Inserção na tabela item_venda ########
            venda_id=venda_id_gerado.getvalue()[0]
            item_venda=[{'venda_id':venda_id,'produto_id':val['ID'],'QTD_PEDIDA': val['QTD_PEDIDA'], 'PRECO_UNITARIO': val['PRECO'] } for val in carrinho.values()]
            comando=f'INSERT INTO ITEM_VENDA (venda_id,produto_id,QTD_PEDIDA,PRECO_UNITARIO) VALUES (:venda_id,:produto_id,:QTD_PEDIDA,:PRECO_UNITARIO)'
            cursor.executemany(comando,item_venda)
            
            
            ######## Update na tabela produto ########
            prod=[{'ID':val['ID'], 'QTD_ESTOQUE': val['QTD_ESTOQUE'] } for val in carrinho.values()]
            comando=f'UPDATE produto SET  QTD_ESTOQUE = :QTD_ESTOQUE WHERE ID = :ID'
            cursor.executemany(comando,prod)
            
            
            conn.commit()
            print('Venda Registrado!') 
            carrinho={}
            return 
        except Exception as e:
          conn.rollback()
          print('Erro ao casdastrar venda no banco:',e)
               
    elif entrada=='2':
        while True:
            entrada=input('Escolha o id do pedido pra alterar\n')
            try:
                id=int(entrada)
                entrada=input('O que deseja?\n1-Deletar item\n2-Atualizar quantidade da compra\n')
                if entrada=='1':
                    qtd_cancelada=carrinho[id]['QTD_PEDIDA']
                    del carrinho[id]
                    estoque[id]['QTD_ESTOQUE']+=qtd_cancelada
                    
                    return 
                elif entrada=='2':
                    while True:
                        try:
                            qtd_atual=int(input('Escreva a nova quantidade:\n'))
                            qtd_cancelada= carrinho[id]['QTD_PEDIDA']-qtd_atual
                            # adicona ou retira do estoque se qtd cancelada for positiva
                            estoque[id]['QTD_ESTOQUE']+=qtd_cancelada
                            carrinho[id]['QTD_PEDIDA']=qtd_atual
                            return 
                        except:
                            print('Formato inválido.')
                            break
            except:
                print('ID inválido.')
        
    elif entrada=='3':
        carrinho={}
        print('Carrinho esvaziado.')
        return 
    elif entrada=='4':
        return 



try:

    # Example for OracleDB connection (adjust for your specific driver)
    conn = oracledb.connect(
        user=USER, 
        password=PASSWORD, 
        host=HOST,
        port=PORT, 
        service_name=SERVICE
    )
    cursor=conn.cursor()
    print("Conectado ao Oracle\n\n")
    
except Exception as e :
    print(f"Erro ao conectar ao banco: {e}")

if __name__ == "__main__":
    main()
