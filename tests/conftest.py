import pytest


@pytest.fixture
def sample_ad_text():
    """Fixture containing sample ad text for testing."""
    return """Ativo
Identificação da biblioteca: 743756688282936
Veiculação iniciada em 10 de ago de 2025
Plataformas
Categorias
Tamanho estimado do público:
>1 mi
Valor gasto (BRL):
R$25 mil a R$30 mil
Impressões:
>1 mi
Abrir menu suspenso
Ver detalhes do anúncio
Roberto Cláudio Bezerra
Patrocinado • Pago por Roberto Cláudio Bezerra
🔴 A violência tem nome e sobrenome: incompetência do PT.

Das 20 cidades mais violentas do Brasil, 14 estão na Bahia e no Ceará, dois estados sob o comando do PT.

Enquanto o crime cresce, o governo cruza os braços. Falta coragem, sobra omissão.

O Ceará não precisa de desculpas. Precisa de ação!
0:00 / 0:00
WWW.INSTAGRAM.COM
Roberto Cláudio Bezerra
Acessar o perfil do Instagram"""

@pytest.fixture
def another_sample_ad_text():
    """Another fixture containing different sample ad text for testing."""
    return """Inativo\nIdentificação da biblioteca: 680016768176090\n2 de jun de 2025 a 26 de jan de 2026\nPlataformas\nCategorias\nTamanho estimado do público:\n>1 mi\nValor gasto (BRL):\nR$2 mil a R$2,5 mil\nImpressões:\n>1 mi\nAbrir menu suspenso\nVer detalhes do anúncio\nPlínio Valério\nPatrocinado • Pago por Plínio Valério\nÉ o dinheiro do povo voltando para o povo!\n\nEssa é a minha missão como senador. Não é favor, é dever!\n\nForam R$ 258 milhões em emendas para a saúde do Amazonas, chegando a todos os hospitais de Manaus e também ao interior do nosso estado. E para os povos indígenas, destinamos mais de R$ 15 milhões, com o respeito e a dignidade que merecem.\n\nQuando a gente entende que o dinheiro público é do povo, o compromisso muda: ele vai para as mãos de quem realmente precisa.\n\n#PlínioValério #Amazonas #SaúdeÉPrioridade #DinheiroPúblico #TrabalhoDeVerdade\n0:00 / 0:00\nLINKTR.EE\nPlínio Valério\nSaiba mais"""
