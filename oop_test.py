from pathlib import Path
from modules.page_sourcer import YAMLConfigReader, SubConfigParser, BaseURLsCreater
from modules.page_sourcer import ChromePageSourcer
from bs4 import BeautifulSoup


config_yaml_path = Path('./config.yaml')
base_url_config_keys = ('URL_CONFIG', 'root', 'base')
extensions_url_config_keys = ('URL_CONFIG', 'root', 'extensions')
concat_str_config_keys = ('URL_CONFIG', 'root', 'concat_str')
driver_path_config_keys = ('DRIVER_OPTIONS','webdriver','chrome','driver_path')
chrome_options_config_keys = ('DRIVER_OPTIONS','webdriver','chrome','options')
extraction_config_keys = ('EXTRACTION', 'product_level')
extraction_product_details = ('EXTRACTION', 'product_details')

start_idx = 1
sep = '?'
page_str = 'page'
equality_str = '='


def add_pagination(
        url,
        idx,
        sep,
        page_str='page',
        equality_str='='
        ):
    return url + sep + page_str + equality_str + idx


yaml_reader = YAMLConfigReader(
    yaml_config_path=config_yaml_path
)

yaml_data = yaml_reader.read_config()
scp = SubConfigParser(config_data=yaml_data)

base_urls  = scp.parse_sub_section_by_keys(sub_config_keys=base_url_config_keys)
extensions = scp.parse_sub_section_by_keys(sub_config_keys=extensions_url_config_keys)
concat_str = scp.parse_sub_section_by_keys(sub_config_keys=concat_str_config_keys)
webdriver_path = scp.parse_sub_section_by_keys(sub_config_keys=driver_path_config_keys)
chrome_options = scp.parse_sub_section_by_keys(sub_config_keys=chrome_options_config_keys)
product_panels = scp.parse_sub_section_by_keys(sub_config_keys=extraction_config_keys)
product_details = scp.parse_sub_section_by_keys(sub_config_keys=extraction_product_details)

buc = BaseURLsCreater(
    base_urls=base_urls,
    extensions=extensions,
    concat_str=concat_str
)

base_urls = buc.create_base_urls()



test_url = base_urls[1]
print(test_url)


test_url = add_pagination(
    url=test_url,
    idx=str(start_idx),
    sep=sep,
    page_str=page_str,

)
print(test_url)
print(product_panels)
for _, page_attr in product_panels.items():

    div_type, class_attr = page_attr

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


    products = soup.find_all(
        name=div_type,
        attrs={
            "class" : class_attr
        }
    )

    for product in products: 

        for detail_name, detail_tag in product_details.items():
            div_type, prod_class_attr = detail_tag
            found_detail = product.find(
                name=div_type,
                attrs={
                    "class" : prod_class_attr
                    }
                )
            if found_detail:
                print(found_detail)