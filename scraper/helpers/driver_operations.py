from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
import zipfile
from decouple import config
from .proxy import manifest_json, background_js

# Chrome driver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

proxy_host = config('PROXY_HOST')
proxy_port = config('PROXY_PORT')
proxy_user = config('PROXY_USER')
proxy_pass = config('PROXY_PASS')

class driver_controller():
    _user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36"
    _browser_options = None
    _pluginfile = 'proxy_auth_plugin.zip'
    
    def __init__(self) -> None:
        self._browser_options = webdriver.ChromeOptions()
        
    def initialize_driver(self) -> None:
        """_summary_
        
        initialize_driver and store driver address
        """
        self._driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=self._browser_options)
        self._driver_address = self._driver.desired_capabilities['goog:chromeOptions']['debuggerAddress']
        
    def dispose_driver(self) -> None:
        """_summary_
        
        Terminate driver
        """
        self._driver.quit() 
        
    def connect_to_driver_address(self, driver_address: str):
        """_summary_

        Args:
            driver_address (str): address of the driver you want to connect to
        """
        if driver_address is not None:
            self._browser_options.add_experimental_option("debuggerAddress", driver_address)
        
    def remove_automation_experimental_options(self) -> None:
        """_summary_
        
        Disables connection to the driver address
        
        *Don't use when calling `connect_to_driver_address`
        """
        self._browser_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self._browser_options.add_experimental_option('useAutomationExtension', False)
        
    def create_proxy_extension(self) -> None:
        """_summary_
        
        Creates a zip file containing proxy configuration
        """
        with zipfile.ZipFile(self._pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
            
    def enable_proxy(self) -> None:
        """_summary_
        
        Add proxy configuration to the driver
        """
        if proxy_user != 'NA' and proxy_pass != 'NA':
            self._browser_options.add_extension(self._pluginfile)
        else:
            proxy_url = proxy_host + ":" + proxy_port
            self._browser_options.add_argument('--proxy-server=%s' % proxy_url)
            
    def disable_bot_detection(self) -> None:
        """_summary_
        
        Bot detection features disabled
        """
        # for testing during production
        # self._browser_options.add_argument("--auto-open-devtools-for-tabs")
        self._browser_options.add_argument("--start-maximized")
        self._browser_options.add_argument("--disable-blink-features")
        self._browser_options.add_argument("--disable-blink-features=AutomationControlled")
        self._browser_options.add_argument(f"user-agent = {self._user_agent}")
        
    def enable_headless_driver(self) -> None:
        """_summary_
        
        :Headless driver configuration
        :Includes gpu disabling
        :no-sandbow to disable malicious javascript
        """
        self._browser_options.add_argument('--headless')
        self._browser_options.add_argument('--disable-gpu')
        self._browser_options.add_argument('--no-sandbox')
        self._browser_options.add_argument('--disable-dev-shm-usage')
    
    @property
    def get_driver(self, security: str = None, proxy: bool = False, driver_address: str = None) -> WebDriver:
        """_summary_

        Args:
            security (str, optional):
                :`None` -> simple driver instance
                :`undetected` -> bot protection.
            proxy (str, optional):
                :`False` -> no proxy
                :`True` -> proxy applied to the driver
            driver_address (str, optional):
                :`None` -> new driver
                :`True` -> connect to a working driver
        Returns:
            WebDriver: driver instance
        """
        if proxy:
            self.enable_proxy()
        if security == 'undetected':
            self.disable_bot_detection()
            self.remove_automation_experimental_options()
        self.connect_to_driver_address(driver_address)
        self.initialize_driver()
        return self._driver
    
    @property
    def get_silent_driver(self, security: str = None, proxy: bool = False, driver_address: str = None) -> WebDriver:
        """_summary_

        Args:
            security (str, optional):
                :`None` -> simple driver instance
                :`undetected` -> bot protection.
            proxy (str, optional):
                :`False` -> no proxy
                :`True` -> proxy applied to the driver
            driver_address (str, optional):
                :`None` -> new driver
                :`True` -> connect to a working driver

        Returns:
            WebDriver: driver instance
        """
        if proxy:
            if proxy_user == 'NA' or proxy_pass == 'NA':
                self.enable_proxy()
            else:
                raise ValueError("""
                Authenticated proxy on a headless driver is not supported
                `Change PROXY_USER and PROXY_PASS to NA in .env`
                """)
        self.enable_headless_driver()
        if security == 'undetected':
            self.disable_bot_detection()
            self.remove_automation_experimental_options()
        self.connect_to_driver_address(driver_address)
        self.initialize_driver()
        return self._driver
    
    @property
    def get_driver_address(self) -> str:
        """_summary_

        Returns:
            str: debugger Address of the driver
        """
        return self._driver_address