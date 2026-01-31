import argparse
from src.pipelines import meta_ads_bronze, meta_ads_silver
from src.common import log


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--pipeline', choices=['meta-ads-bronze', 'meta-ads-silver', 'meta-ads'], required = True)
    parser.add_argument('--query')
    parser.add_argument('--ad-type', choices = ['political_and_issue_ads', 'all'], default = 'political_and_issue_ads')
    parser.add_argument('--limit', type = int, default = None)
    parser.add_argument('--data-path', type = str, default = None)
    parser.add_argument('--metadata-path', type = str, default = None)
    args = parser.parse_args()
    
    log.setup_logging()
    if args.pipeline == 'meta-ads-bronze':
        meta_ads_bronze.run_meta_ads_to_bronze(args.query, args.ad_type, args.limit)
    if args.pipeline == 'meta-ads-silver':
        meta_ads_silver.run_meta_ads_to_silver(args.data_path, args.metadata_path)
    if args.pipeline == 'meta-ads':
        data_path, metadata_path = meta_ads_bronze.run_meta_ads_to_bronze(args.query, args.ad_type, args.limit)
        meta_ads_silver.run_meta_ads_to_silver(data_path, metadata_path)