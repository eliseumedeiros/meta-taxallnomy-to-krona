# meta-taxallnomy-to-krona

Para executar o  teste, basta realizaro download dos arquivos "metakaiju_taxallnomy_to_krona" e o exemplo de saída "kaiju.out" e o arquivo final será gerado com o nome "input_kaiju_krona". E a execução poderá ser feita com base nas duas abordagens:

## Análise Remota (acessa o taxallnomy através do link de resultados tabular)

  <h4>python kaiju_taxallnomy-to-krona.py --file kaiju.out</h4>

## Análise Local

  <h4>python kaiju_taxallnomy-to-krona.py --file kaiju.out -t l</h4>
    Forneça as ingotmações necessárias (login e senha do banco do taxallnomy)
  
  
  Parâmetos:
  -f ou --file: indica o caminho do arquivo de entrada
  -txm ou --taxallnomy: indica o caminho da pata do Taxallnomy local, que possui o script "get_lineage.pl"
  
  
  
  
  
 
