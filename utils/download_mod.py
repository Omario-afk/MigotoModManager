from .browser.start import ModDownloader


def download_mod(url, username=None, password=None):
    downloader = ModDownloader()
    try:
        result = downloader.download_mod(url, username, password)
        return result
    finally:
        # Note: We're not closing the browser here to keep it open as requested
        pass


if __name__ == "__main__":
    download_mod("https://gamebanana.com/mods/587147")