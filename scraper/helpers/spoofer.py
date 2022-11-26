from fp.fp import FreeProxy
from scraper.helpers.user_agent_controller import UserAgent

class Spoofer(object):

    def __init__(self, country_id: list = ['IN'], rand: bool = True, anonym: bool = False):
        self.country_id = country_id
        self.rand = rand
        self.anonym = anonym
        self.userAgent, self.ip = self.get()

    def get(self) -> tuple[str,str]:
        """_summary_

        Returns:
            tuple[str,str]: fake user agent and a random proxy server address
        """
        user_agent = UserAgent()
        proxy = FreeProxy(country_id=self.country_id, rand=self.rand, anonym=self.anonym).get()
        ip = proxy.split("://")[1]
        return user_agent.random, ip

overwrite_window = """
    Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined
    });
    Object.defineProperty(navigator, 'plugins', {
        get: () => [{"0":{}},{"0":{}},{"0":{}},{"0":{}},{"0":{}}]
    });
    Object.defineProperty(navigator, 'languages', {
        get: () => ["en-US", "en"]
    });
    Object.defineProperty(navigator, 'mimeTypes', {
        get: () => [{"0":{}},{"0":{}}]
    });

    window.screenY=23;
    window.screenTop=23;
    window.outerWidth=1337;
    window.outerHeight=825;
    window.chrome =
    {
    	app: {
        	isInstalled: false,
      	},
		webstore: {
			onInstallStageChanged: {},
			onDownloadProgress: {},
		},
		runtime: {
			PlatformOs: {
				MAC: 'mac',
				WIN: 'win',
				ANDROID: 'android',
				CROS: 'cros',
				LINUX: 'linux',
				OPENBSD: 'openbsd',
			},
			PlatformArch: {
				ARM: 'arm',
				X86_32: 'x86-32',
				X86_64: 'x86-64',
			},
			PlatformNaclArch: {
				ARM: 'arm',
				X86_32: 'x86-32',
				X86_64: 'x86-64',
			},
			RequestUpdateCheckStatus: {
				THROTTLED: 'throttled',
				NO_UPDATE: 'no_update',
				UPDATE_AVAILABLE: 'update_available',
			},
			OnInstalledReason: {
				INSTALL: 'install',
				UPDATE: 'update',
				CHROME_UPDATE: 'chrome_update',
				SHARED_MODULE_UPDATE: 'shared_module_update',
			},
			OnRestartRequiredReason: {
				APP_UPDATE: 'app_update',
				OS_UPDATE: 'os_update',
				PERIODIC: 'periodic',
			},
		},
	};
	window.navigator.chrome =
	{
		app: {
			isInstalled: false,
		},
		webstore: {
			onInstallStageChanged: {},
			onDownloadProgress: {},
		},
		runtime: {
			PlatformOs: {
				MAC: 'mac',
				WIN: 'win',
				ANDROID: 'android',
				CROS: 'cros',
				LINUX: 'linux',
				OPENBSD: 'openbsd',
			},
			PlatformArch: {
				ARM: 'arm',
				X86_32: 'x86-32',
				X86_64: 'x86-64',
			},
			PlatformNaclArch: {
				ARM: 'arm',
				X86_32: 'x86-32',
				X86_64: 'x86-64',
			},
			RequestUpdateCheckStatus: {
				THROTTLED: 'throttled',
				NO_UPDATE: 'no_update',
				UPDATE_AVAILABLE: 'update_available',
			},
			OnInstalledReason: {
				INSTALL: 'install',
				UPDATE: 'update',
				CHROME_UPDATE: 'chrome_update',
				SHARED_MODULE_UPDATE: 'shared_module_update',
			},
			OnRestartRequiredReason: {
				APP_UPDATE: 'app_update',
				OS_UPDATE: 'os_update',
				PERIODIC: 'periodic',
			},
		},
	};
	['height', 'width'].forEach(property => {
		const imageDescriptor = Object.getOwnPropertyDescriptor(HTMLImageElement.prototype, property);

		// redefine the property with a patched descriptor
		Object.defineProperty(HTMLImageElement.prototype, property, {
			...imageDescriptor,
			get: function() {
				// return an arbitrary non-zero dimension if the image failed to load
			if (this.complete && this.naturalHeight == 0) {
				return 20;
			}
				return imageDescriptor.get.apply(this);
			},
		});
	});

	const getParameter = WebGLRenderingContext.getParameter;
	WebGLRenderingContext.prototype.getParameter = function(parameter) {
		if (parameter === 37445) {
			return 'Intel Open Source Technology Center';
		}
		if (parameter === 37446) {
			return 'Mesa DRI Intel(R) Ivybridge Mobile ';
		}
		return getParameter(parameter);
	};

	const elementDescriptor = Object.getOwnPropertyDescriptor(HTMLElement.prototype, 'offsetHeight');

	Object.defineProperty(HTMLDivElement.prototype, 'offsetHeight', {
		...elementDescriptor,
		get: function() {
			if (this.id === 'modernizr') {
				return 1;
			}
			return elementDescriptor.get.apply(this);
		},
	});
"""