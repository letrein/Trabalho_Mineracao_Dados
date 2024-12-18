# Trabalho_Mineracao_Dados
Este trabalho foi realizado utilizando as bases de dados públicas da Prefeitura de Curitiba. Os dados são oriundos do SiGesGuarda, que contém as ocorrências atendidas pela Guarda Municipal de Curitiba.

1) O trabalho iniciou com a pergunta "Será que a renda influencia o perfil das ocorrências policiais no bairro em Curitiba-PR?", para isso foi necessário a utilização de 2 bases de dados, tanto a da SiGesGuarda quando das informações de renda média da população de cada bairro.  

2) Após a união dos datasets, foi criado um novo dataset contendo as frequências de cada tipo de ocorrência para utilização na modelagem de clusterização.  

3) Foram utilizados modelos de clusterização (por modelo KMeans) para unir os bairros em grupos mais semelhantes, primeiramente unindo-os pelos tipos de ocorrência mais frequentes e depois pela semelhança da renda populacional

4) Após entendido como os grupos se comportariam de forma independente, foi realizada a análise comparativa dos clusters formados, unindo apenas aqueles que se assemelharam nas modelagens anteriores, resultando em apenas 10 grupos semelhantes em ambas clusterizações

5) Para validação do resultado obtido, foi realizado a análise de contigência (pelo qui-quadrado) para validar ou negar a hipotese nula ("A renda do bairro influencia no perfil dos principais tipos de ocorrência policiais" ). 
- Com um p-valor: 0.7413111492453468, temos que a hipotese nula é rejeitada e concluimos que a renda não é influenciadora no perfil dos principais tipos de ocorrências policiais. 
