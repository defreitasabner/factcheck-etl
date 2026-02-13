import argparse
from src.common import log
from src.pipelines import meta_ads_bronze, meta_ads_silver
from src.pipelines import lupa


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='pipeline', required = True, help='Choose which pipeline to run')

    meta_ads_parser = subparsers.add_parser('meta-ads', help='Executa o pipeline de anúncios da Meta')
    meta_ads_parser.add_argument('--step', choices = ['bronze', 'silver', 'gold'], default = None, help='Executa um passo específico do pipeline')
    meta_ads_parser.add_argument('--query')
    meta_ads_parser.add_argument('--ad-type', choices = ['political_and_issue_ads', 'all'], default = 'political_and_issue_ads')
    meta_ads_parser.add_argument('--limit', type = int, default = None)
    meta_ads_parser.add_argument('--data-path', type = str, default = None)
    meta_ads_parser.add_argument('--metadata-path', type = str, default = None)
    
    lupa_parser = subparsers.add_parser('lupa', help='Executa o pipeline da Agência Lupa')
    lupa_parser.add_argument('--query', type = str, required = True, help='Consulta para buscar na Agência Lupa')
    lupa_parser.add_argument('--page', type = int, default = 1, help='Página inicial para começar a raspagem')
    lupa_parser.add_argument('--order', choices = ['ASC', 'DESC'], default = 'DESC', help='Ordem dos resultados (ASC para mais antigos primeiro, DESC para mais recentes primeiro)')
    lupa_parser.add_argument('--category', choices = ['todas', 'Verificação'], default = 'Verificação', help='Categoria dos resultados (ex: Verificação, todas)')
    lupa_parser.add_argument('--limit', type = int, default = None, help='Limite de notícias a serem raspadas')

    args = parser.parse_args()
    
    log.setup_logging()
    if args.pipeline == 'meta-ads':
        if args.step == 'bronze':
            meta_ads_bronze.run_meta_ads_to_bronze(args.query, args.ad_type, args.limit)
        elif args.step == 'silver':
            meta_ads_silver.run_meta_ads_to_silver(args.data_path, args.metadata_path)
        elif args.step == 'gold':
            pass
        else:
            data_path, metadata_path = meta_ads_bronze.run_meta_ads_to_bronze(args.query, args.ad_type, args.limit)
            meta_ads_silver.run_meta_ads_to_silver(data_path, metadata_path)
    elif args.pipeline == 'lupa':
        lupa.bronze(
            query = args.query,
            page = args.page,
            order = args.order,
            category = args.category,
            limit = args.limit
        )
