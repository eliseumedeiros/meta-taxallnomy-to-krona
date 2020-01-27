# meta-taxallnomy-to-krona

Para executar o  teste, basta realizar o download dos arquivos "metakaiju_taxallnomy-to-krona.py" e o exemplo de saída "kaiju.out". Ao final será gerado o arquivo com o nome "input_kaiju_krona". E a execução poderá ser feita com base nas duas abordagens:

## Análise Remota (acessa o taxallnomy através do link de resultados tabular)

  <h4>python metakaiju_taxallnomy-to-krona.py --file kaiju.out</h4>

## Análise Local

  <h4>python metakaiju_taxallnomy-to-krona.py --file kaiju.out --type l --taxallnomy %caminho_do_arquivo_get_lineage.pl%</h4>
    Forneça as ingotmações necessárias (login e senha do banco do taxallnomy)
  
  
  Parâmetos:
  -f ou --file: indica o caminho do arquivo de entrada
  -txm ou --taxallnomy: indica o caminho da pata do Taxallnomy local, que possui o script "get_lineage.pl"
  -t ou --type: indica o tipo de análise que será realizada (remota 'r' ou local 'l'). Para escolher diretamente uma análise locar, também pode-se digitar apenas --remote ou -r para análise remota; e --local ou -l para análise local.
  
  
  
  
  
 
