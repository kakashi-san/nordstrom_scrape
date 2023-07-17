"""
this module provides implementation for getting page source from url
"""
from abc import ABC, abstractmethod
from pathlib import Path
import requests
from typing import Dict, Any, List
from ruamel.yaml import YAML
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options


class PageSourcer(ABC):
    """
    abstract class to get page source from url
    """
    @property
    def page_url(self):
        """
        getter method for page url
        """
        pass

    @abstractmethod
    def get_page_source(self):
        """
        abstract method to get page source from the url.
        """

class WebDriverPageSourcer(PageSourcer):
    """
    class to handle page source using webdriver
    """
    @property
    def page_url(self):
        return self._page_url

    def __init__(
            self,
            page_url: str,
            webdriver_path: Path,
    ) -> None:
        self._page_url = page_url
        self.webdriver_path = webdriver_path


class RequestsPageSourcer(PageSourcer):
    """
    a class to get page source using requests library
    """

    def __init__(
            self,
            page_url: str,
            **kwargs
    ) -> None:
        super().__init__(
            page_url
        )
        self._kwargs = kwargs

    def get_page_source(self):
        return requests.get(
            self.page_url,
            **self._kwargs,
            timeout=5
            ).content


class ChromePageSourcer(WebDriverPageSourcer):
    """
    class to get page source for url using Chrome Driver
    """

    def get_page_source(self):
        return self.driver.page_source
    
    def __init__(
            self,
            page_url,
            webdriver_path,
            chrome_options=None,
    ) -> None:
        super().__init__(page_url, webdriver_path)

        options = Options()
        if chrome_options:
            for option in chrome_options:
                options.add_experimental_option(*option)

        self.driver = Chrome(
            chrome_options=options,
            executable_path=webdriver_path,
        )

        self.driver.get(
            url=self.page_url
        )


class ConfigReader(ABC):
    '''
    abstract class to read config file
    '''
    @property
    @abstractmethod
    def config_path(self):
        '''
        abstract method to store config path
        '''

    @abstractmethod
    def read_config(self):
        '''
        abstract method to read config file.
        '''

class YAMLConfigReader(ConfigReader):

    @property
    def config_path(self):
        return self._config_path
            
    def read_config(self):
        '''
        helper function to read config from yaml files.
        '''
        with open(self.config_path, 'r') as f:
            data = YAML().load(f)
            return data
        
    def __init__(
        self,
        yaml_config_path,
        ) -> None:
        self._config_path = yaml_config_path



class ISubConfigParser(ABC):
    '''
    abstract class to parse
    config sub-section
    '''

    @abstractmethod
    def parse_sub_section_by_keys(self):
        """
        abstract method to parse 
        """    


class SubConfigParser(ISubConfigParser):
    '''
    class to read Scraping 
    '''
    def parse_sub_section_by_keys(
            self,
            sub_config_keys

            ):
        for key in sub_config_keys:
            data = data[key]
        return data
    
    def __init__(
            self,
            config_data,
            ) -> None:
        self._config_data = config_data


class IBaseURLsCreater(ABC):
    '''
    abstract class to create base urls.
    '''
    @property
    @abstractmethod
    def base_urls(self):
        '''
        base url to be created from the data stored here.
        '''

    @property
    @abstractmethod
    def extensions(self):
        '''
        extensions to be created from the data stored here.
        '''
    @property
    @abstractmethod
    def concat_str(self):
        '''
        concat str to be used for url creation
        '''

    @abstractmethod
    def create_base_urls(self):
        '''
        abstract function to create base urls.
        '''

class BaseURLsCreater(IBaseURLsCreater):

    @property
    def base_urls(self):
        return self._base_urls
    
    @property
    def extensions(self):
        return self._extensions
    
    @property
    def concat_str(self):
        return self._concat_str
    
    def create_base_urls(self):

        urls = self._base_urls

        for _, value in self._extensions.items():
            if value:
                urls = self.generate_urls(
                    urls=urls,
                    extensions=value,
                    concat_str=self.concat_str
                    )
        
        return urls


    def __init__(
            self,
            base_urls,
            extensions,
            concat_str
            ) -> None:
        self._base_urls = base_urls
        self._extensions = extensions
        self._concat_str = concat_str

    @staticmethod
    def generate_urls(
        urls: List[str],
        extensions: List[str],
        concat_str: str,
        ):
        urls.extend([
                url + concat_str + extension
                for extension in extensions
                for url in urls
            ])
        
        return urls
