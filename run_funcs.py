# from modules.page_sourcer import ChromePageSourcer, RequestsPageSourcer
from modules.url_handler import generate_urls_from_config
from modules.page_sourcer import ChromePageSourcer
from pathlib import Path
import time
from modules.utils import read_config_yaml
from bs4 import BeautifulSoup



config_yaml_path = Path('./config.yaml')
config_data = read_config_yaml(config_yaml_path=config_yaml_path)

webdriver_path = Path(config_data['DRIVER_OPTIONS']['webdriver']['chrome']['driver_path'])
chrome_options = config_data['DRIVER_OPTIONS']['webdriver']['chrome']['options']

pagination_options = config_data['URL_CONFIG']['pagination']
sep = pagination_options['sep_str']
equality = pagination_options['equality_str']
page = pagination_options['page_str']
start_idx = pagination_options['start_idx_int']
product_tile_config = config_data['EXTRACTION']['product_level']



def add_pagination(
        url,
        idx,
        sep,
        page_str='page',
        equality_str='='
        ):
    return url + sep + page_str + equality_str + idx

if __name__ == "__main__":
    urls = generate_urls_from_config(
        config_data=config_data
    )
    print(urls)
    test_url = urls[1]
    print(test_url)

    

    test_url = add_pagination(
        url=test_url,
        idx=str(start_idx),
        sep=sep,
        page_str=page,

    )
    print(test_url)

    cpc = ChromePageSourcer(
        page_url=test_url,
        webdriver_path=webdriver_path,
        chrome_options=chrome_options
    )
    page_sauce = cpc.get_page_source()

    soup = BeautifulSoup(
        page_sauce,
        "html.parser"
        )
    
    product_details = config_data['EXTRACTION']['product_details']
    name, field_name, class_attr = product_tile_config
    
    products = soup.find_all(
        name=name,
        attrs={
            "class" : class_attr
        }
    )

    for product in products: 
        for detail in product_details:
            div_type, field_name_2, attr = detail
            found_detail = product.find(
                name=div_type,
                attrs={
                    "class" : attr
                    }
            )
            print(found_detail)


    time.sleep(60)
    # requests_page_sourcer = RequestsPageSourcer(
    #     page_url=url,
    #     **requests_args
    # )
    # print(requests_page_sourcer.get_page_source())


    # PageSourcer = ChromePageSourcer(
    #     page_url=url,
    #     webdriver_path=webdriver_path
    # )

    # page_source = PageSourcer.get_page_source()

    # page_soup = BeautifulSoup(page_source)

    # time.sleep(30)