from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
import zipfile
from decouple import config
from driver_config.proxy import manifest_json, background_js
from driver_config.spoofer import Spoofer, overwrite_window
import helpers.constants as constants
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth
import undetected_chromedriver as uc

proxy_host = config('PROXY_HOST')
proxy_port = config('PROXY_PORT')
proxy_user = config('PROXY_USER')
proxy_pass = config('PROXY_PASS')

class MultiDriverController():
    def __init__(self):
        """_summary_
        
        Initializes an empty dictionary for storing drivers
        """
        self._driver_dict = {}
    
    def initialize_multi_driver(self, browser_options: ChromeOptions, security: str = None) -> WebDriver:
        """_summary_

        Args:
            browser_options (ChromeOptions): selected browser features

        Returns:
            WebDriver: driver instance
        """
        if security == "undetected":
            driver = uc.Chrome(options=browser_options)
        else:
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=browser_options)
        return driver
        
    def store(self, driver: WebDriver, address: ChromeOptions):
        """_summary_

        Args:
            driver (WebDriver): driver instance
            address (ChromeOptions): driver's debugger address
        
        stores the driver and it's address in a dictionary
        """
        self._driver_dict[address] = driver
    def delete_store(self, address: ChromeOptions) -> bool:
        """_summary_

        Args:
            address (ChromeOptions): driver's debugger address

        Returns:
            bool: return True or False depending on if the address was in the store or not
        """
        if address in self._driver_dict.keys():
            self._driver_dict[address].quit()
            self._driver_dict[address] = None
            return False
        else:
            return True
        

driver_storage = MultiDriverController()
        
class DriverController():
    _driver = None
    _driver_address = None
    _pluginfile = 'proxy_auth_plugin.zip'
    
    def __init__(self) -> None:
        """_summary_

        sets _browser_options to google chrome options
        """
        self._driver = None
        self._driver_address = None
    
    def __dict__(self) -> tuple[WebDriver, str]:
        """_summary_

        Returns:
            tuple[WebDriver, str]: contains driver and it's driver address
        """
        return self._driver, self._driver_address
    
    def __call__(self, security: str = None) -> None:
        """_summary_

        Args:
            security (str, optional): sets browser options depending on the security. Defaults to None.
        """
        if security == 'undetected':
            self._browser_options = uc.ChromeOptions()
        else:
            self._browser_options = webdriver.ChromeOptions()
        self._browser_options.add_argument('--start-maximized')
    
    def initialize_driver(self, multi_driver: bool = False, security: str = None) -> WebDriver:
        """_summary_

        Args:
            multi_driver (bool, optional): If the driver needs to be stored for delayed connection. Defaults to False.
            security (str, optional): Defaults to None.

        Raises:
            ProcessLookupError: If the driver is not found/crashes

        Returns:
            WebDriver: returns a webdriver instance
        """
        if multi_driver:
            try:
                driver = driver_storage.initialize_multi_driver(self._browser_options, security)
                address = self.get_driver_address(driver)
                driver_storage.store(driver, address)
                self.__init__()
                return driver
            except Exception as driver_exception:
                raise ValueError(driver_exception)
        else:
            if security == "undetected":
                self._driver = uc.Chrome(options=self._browser_options)
            else:
                self._driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=self._browser_options)
            self._driver_address = self.get_driver_address()
            return self._driver
        
    def get_driver_address(self, driver: WebDriver = None) -> str:
        """_summary_

        Args:
            driver (WebDriver, optional): driver instance. Defaults to None.

        Raises:
            LookupError: In case the driver is not found/crashes

        Returns:
            str: debugger Address of the driver instance
        """
        try:
            if driver is None:
                return self._driver.desired_capabilities['goog:chromeOptions']['debuggerAddress']
            else:
                return driver.desired_capabilities['goog:chromeOptions']['debuggerAddress']
        except Exception:
            print("No driver instance found in self._driver. Please provide the driver in the parameter")
        
    def dispose_driver(self, driver_info: WebDriver|str = None) -> None:
        """_summary_

        Args:
            driver_info (WebDriver | str, optional)
                : (`driver` or `driver_address`)For closing multi driver instance. Defaults to None. Defaults to None.
        """
        try:
            if driver_info is None:
                self._driver.quit()
            else:
                if type(driver_info) == WebDriver:
                    driver_info = self.get_driver_address(driver_info)
                    if driver_storage.delete_store(driver_info):
                        self.delete_driver_from_root(driver_info)
                elif type(driver_info) == str:
                    if driver_storage.delete_store(driver_info):
                        self.delete_driver_from_root(driver_info)
        except Exception:
            print("No driver instance found in self._driver. Please provide the driver in the parameter")
    
    def delete_driver_from_root(self, driver_address: str) -> None:
        """_summary_

        Args:
            driver_address (str): driver address of the driver to be terminated from root
        """
        # Write and API Call here to the root to terminate the driver
        pass
    
    def connect_to_driver_address(self, driver_address: str) -> None:
        """_summary_

        Args:
            driver_address (str): address of the driver you want to connect to
        """
        if driver_address is not None:
            self._browser_options.add_experimental_option('debuggerAddress', driver_address)
        
    def remove_automation_experimental_options(self) -> None:
        """_summary_
        
        Disables connection to the driver address
        
        *Don't use when calling `connect_to_driver_address`
        """
        print("Opening Secure Driver")
        self._browser_options.add_experimental_option('useAutomationExtension', False)
        self._browser_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self._browser_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    
    def overwrite_chrome_dev_tools(self, driver: WebDriver) -> None:
        """_summary_

        Args:
            driver (WebDriver): takes a driver instance and executes Cdp commands
        """
        page_domain_events = "Page.addScriptToEvaluateOnNewDocument"
        overwrite_navigator_permissions_query = """
        let originalQuery = window.navigator.permissions.query;
        window.navigator.permissions.query = (parameters) => {
            return parameters.name === 'notifications'
                ? Promise.resolve({ state: Notification.permission })
                : originalQuery(parameters)
        };
        """
        # covered in `overwrite_window`
        # overwrite_chrome = "window.chrome = {runtime: {},};"
        # overwrite_plugins = "Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});"
        # overwrite_languages = "Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});"
        # driver.execute_cdp_cmd(page_domain_events,{"source": overwrite_chrome})
        # driver.execute_cdp_cmd(page_domain_events,{"source": overwrite_plugins})
        # driver.execute_cdp_cmd(page_domain_events,{"source": overwrite_languages})
        driver.execute_cdp_cmd(page_domain_events,{"source": overwrite_window})
        driver.execute_cdp_cmd(page_domain_events,{"source": overwrite_navigator_permissions_query})
        
    def selenium_stealth_execution(self, driver: WebDriver) -> None:
        """_summary_

        Args:
            driver (WebDriver): takes a driver instance and executes selenium stealth
        """
        stealth(
            driver,
            user_agent=self.helperSpoofer.userAgent,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            run_on_insecure_origins=True,
        )
    
    def create_proxy_extension(self) -> None:
        """_summary_
        
        Creates a zip file containing proxy configuration
        """
        with zipfile.ZipFile(self._pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
    
    def call_spoofer(self, proxy: str, security: str) -> None:
        """_summary_

        Args:
            proxy (str): `tesing`
            security (str): `undetected` or `manual`
        """
        if proxy == 'testing' or security == 'undetected' or security == 'manual':
            self.helperSpoofer = Spoofer()
    
    def proxy_spoof(self, proxy: str = None, silent: bool = False) -> None:
        """_summary_

        Args:
            proxy (str, optional): type of proxy applied. Defaults to None.
            silent (bool, optional): if headless driver. Defaults to False.
        """
        if proxy is not None:
            if silent and proxy == 'secure' and (proxy_user != 'NA' or proxy_pass != 'NA'):
                raise ValueError("""
                Authenticated proxy on a headless driver is not supported
                `Change PROXY_USER and PROXY_PASS to NA in .env`
                """)
            else:
                self.enable_proxy(proxy)
            
    def enable_proxy(self, proxy: str) -> None:
        """_summary_

        Args:
            proxy (str):
                :`secure` -> proxy applied to the driver via .env
                :`testing` -> fake proxy applied to the driver
        """
        if proxy == 'secure':
            if proxy_user != 'NA' and proxy_pass != 'NA':
                self.create_proxy_extension()
                self._browser_options.add_extension(self._pluginfile)
            else:
                proxy_url = proxy_host + ":" + proxy_port
                self._browser_options.add_argument('--proxy-server={}'.format(proxy_url))
        elif proxy == 'testing':
            self._browser_options.add_argument('--proxy-server={}'.format(self.helperSpoofer.ip))
    
    def apply_manual_security(self, driver_address: str = None, multi_driver: bool = False) -> WebDriver:
        """_summary_

        Args:
            driver_address (str, optional): Defaults to None.
            multi_driver (bool, optional): Defaults to False.

        Returns:
            WebDriver: driver instance
        """
        self.disable_bot_detection(True if driver_address is None else False)
        self.connect_to_driver_address(driver_address)
        driver = self.initialize_driver(multi_driver)
        # Manually overwriten window
        # self.overwrite_chrome_dev_tools(driver)
        self.selenium_stealth_execution(driver)
        return driver
    
    def disable_bot_detection(self, add_experimental_features: bool) -> None:
        """_summary_

        Args:
            add_experimental_features (bool): add bot detection experimental features if `True`
        """
        # For testing during production
        # self._browser_options.add_argument('--auto-open-devtools-for-tabs')
        self._browser_options.add_argument('--no-sandbox')
        self._browser_options.add_argument('--disable-infobars')
        self._browser_options.add_argument('--disable-extensions')
        self._browser_options.add_argument('--disable-dev-shm-usage')
        # blocks from overwriting navigator permissions query
        # self._browser_options.add_argument('--disable-notifications')
        self._browser_options.add_argument('--disable-popup-blocking')
        self._browser_options.add_argument('--disable-blink-features')
        self._browser_options.add_argument('--profile-directory=Default')
        self._browser_options.add_argument('--disable-plugins-discovery')
        self._browser_options.add_argument('--disable-software-rasterizer')
        self._browser_options.add_argument('--disable-blink-features=AutomationControlled')
        # included in selenium stealth
        # self._browser_options.add_argument('user-agent={}'.format(self.helperSpoofer.userAgent))
        if add_experimental_features:
            self.remove_automation_experimental_options()
        
    def enable_headless_driver(self) -> None:
        """_summary_
        
        :Headless driver configuration
        :Includes gpu disabling
        :no-sandbow to disable malicious javascript
        """
        # Experimental Feature
        # self._browser_options.add_argument("--incognito")
        self._browser_options.add_argument('--headless')
        self._browser_options.add_argument('--disable-gpu')
    
    def get_driver(self, security: str = None, proxy: str = None, driver_address: str = None, 
                   silent: bool = False, multi_driver: bool = False) -> WebDriver:
        """_summary_

        Args:
            security (str, optional):
                :`None` -> simple driver instance
                :`manual` -> manually handled bot detection services
                :`undetected` -> bot protection.
            proxy (str, optional):
                :`None` -> no proxy
                :`secure` -> proxy applied to the driver via .env
                :`testing` -> fake proxy applied to the driver
            driver_address (str, optional):
                :`None` -> new driver
                :`True` -> connect to a working driver
            silent (bool, optional):
                :`False` -> normal driver instance
                :`True` -> headless driver instance
            multi_driver (bool, optional):
                :`False` -> normal driver instance
                :`True` -> driver instance is stored
        Returns:
            WebDriver: driver instance
        """
        self.__call__(security)
        self.call_spoofer(proxy, security)
        self.proxy_spoof(proxy, silent)
        if silent: self.enable_headless_driver()
        if security == 'manual':
            driver = self.apply_manual_security(driver_address, multi_driver)
        else:
            self.connect_to_driver_address(driver_address)
            driver = self.initialize_driver(multi_driver, security)
        return driver