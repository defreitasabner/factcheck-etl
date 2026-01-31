from src.load import meta_ads


def test_save_to_bronze(tmp_path, monkeypatch):
    monkeypatch.setattr('src.load.datalake.BRONZE_PATH', tmp_path)
    query = 'test'
    ad_type = 'political_and_issue_ads'
    raw_ads = [
        {'raw_text': 'Test ad 1'},
        {'raw_text': 'Test ad 2'},
        {'raw_text': 'Test ad 3'}
    ]
    scrape_params = {
        'query': query,
        'ad_type': ad_type
    }
    
    meta_ads.save_to_bronze(raw_ads, scrape_params)
    
    expected_path = tmp_path / 'source=meta_ads' / f'ad_type={ad_type}' / f'query={query}'
    assert expected_path.exists(), f"Expected path {expected_path} does not exist"
    assert expected_path.is_dir(), f"Expected path {expected_path} is not a directory"
    
    files = list(expected_path.glob('*.json'))
    assert len(files) == 2, f"Expected 2 files, found {len(files)}"
    
    assert files[0].name.startswith(f'meta_ads_{ad_type}_{query}_') and files[1].name.startswith(f'meta_ads_{ad_type}_{query}_')
    assert files[0].name.endswith('.json') and files[1].name.endswith('.json')
    
    
    assert  len(files[0].name.replace(f'meta_ads_{ad_type}_{query}_', '').replace('.json', '').replace('_metadata', '')) == 15 \
        and  len(files[1].name.replace(f'meta_ads_{ad_type}_{query}_', '').replace('.json', '').replace('_metadata', '')) == 15 \
            , f"Expected timestamp format YYYYMMDD_HHMMSS got {files[0].name} and {files[1].name}"

    assert files[0].name.endswith('_metadata.json') \
        or files[1].name.endswith('_metadata.json'), "At least one file should be metadata"
