import argparse
from src.pipelines import meta_ads_bronze
from src.common import log


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--pipeline', choices=['meta-ads-bronze'], required = True)
    parser.add_argument('--query', required = True)
    parser.add_argument('--ad-type', choices = ['political_and_issue_ads', 'all'], default = 'political_and_issue_ads')
    parser.add_argument('--limit', type = int, default = None)
    args = parser.parse_args()
    
    log.setup_logging()
    if args.pipeline == 'meta-ads-bronze':
        meta_ads_bronze.run_meta_ads_to_bronze(args.query, args.ad_type, args.limit)
