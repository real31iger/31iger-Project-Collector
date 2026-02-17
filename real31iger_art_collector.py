# Project Version: a05v01
import os
user = os.getlogin() # thats your pc name to get some paths
config = {
    #################################################
    ################### CONFIGS #####################
    #################################################
# PATHS
    # note: paths can use // or \\ ! 
    # note: Path to Scan
    # "path__to_scan": rf"c:\!my_stuff\.secret_folder\api_data",
    "path__to_scan": rf"R:\!real31iger_DEV_Discord-Bot\test-bots\\bot-alpha-01/test_2",
    # note: Path to Create the Result.txt
    "path__safe_result": rf"C:\Users\{user}\desktop\.!0_COLLECTED_ART_by_r31.txt",
    # C:\Users\xrx\Desktop
# FILTERS
    # note: if keyword found in line, the complete line will skipped
    "filter__line_keywords": [
        # "token",
    ],
    # note: If Filter NOT Empty: if a target-path ends with a keyword it fill readed.
    # note: If Filter IS Empty: all files will tryed to read. (.exe, .db, .png, ...)
    "filter__only_file_endings": [
        # ".txt",
        # ".py",
        # ".php",
        # ".xyz",
    ],
    # note: If Filter is in target-Name, target will skipped means folders and files
    "filter__ignore_file_tags": [
        # '__py',
        # '.pyc'
    ],
# Error-Debug-Tag-Emojis
    # note: will change console logs ♥
    "print_test_errors_on_start": True, # True or False, test it out ♥
    "error_map": {
        "e": "❌ Error    : ",
        "d": "✅ Done     : ",
        "w": "⚠️  Warning  : ",
        "n": "🧻 Note     : ",
        "na": "❓ Tag=na   : ",
        "fi": "📝 File     : ",
        "fo": "📂 Folder   : ",
    },
# Result.txt Formatting Settings
    "settings": {
        # Toggles: True / False
        # To get spaces between files in Result.txt
        "spaces_between_files": True,
        # To Clean Console every start
        "clear_console_every_start": True,
    }
}
class collector:
    def __init__(self, config):
        self.setup()
# DEBUG
    def db(self, msg, tag):
        tag = self.error_map.get(tag, self.error_map['na'])
        print(f'{tag} {msg}')
# PATHS
    def pathFixMissingFolder(self, path):
        try:
            target = self.pathFixBrokenString(path)
            if '.' in os.path.basename(target): target = self.pathFixBrokenString(os.path.dirname(target))
            if os.path.exists(target): return
            os.makedirs(target, exist_ok=True); self.db(f'Fehlender Ordner erstellt: {target}', 'n')
        except Exception as e:
            self.db(f'pathFixMissingFolder failed! Error: {e}', 'e')
    def pathFixBrokenString(self, path):
        return path.strip().replace('\\', '/').replace('//', '/')
    def path(self, path, *adds):
        target = path
        if adds:
            for add in adds: target = rf'{target}/{add}'
        target = self.pathFixBrokenString(target)
        # self.pathFixMissingFolder(target)
        return target
# LOAD > CONFIG
    def config_setup(self):
        self.path_target = self.path(self.config.get('path__to_scan'))
        self.path_safe = self.path(self.config.get('path__safe_result'))
        self.filter__line_keywords = self.config.get('filter__line_keywords', [])
        self.filter__file_endings = self.config.get('filter__only_file_endings', [])
        self.filter__ignore_file_tags = self.config.get('filter__ignore_file_tags', [])
        self.error_map = self.config.get('error_map')
        self.settings = self.config.get('settings', {})
# LOAD > INIT
    def init_setup(self):
        self.data = """###############################
## 31iger Project Collector
## Made with ♥
###############################"""
# SETUP
    def setup(self):
# > INIT
        self.init_setup()
# > CONFIG
        self.config = config
        self.config_setup()
# > PRINT SETUP
        self.getSetup()
# > RUN COLLEC
        self.run_search()
# PRINT SETUP
    def getSetup(self):
        if self.settings.get('clear_console_every_start'): os.system('cls' if os.name == 'nt' else 'clear')
        print(f"""###############################
♥ | --- SETUP --- | ♥
♥ Paths:
>>     Target: {self.path_target}
>>     Safer: {self.path_safe}
♥ Filters:
>>    Line-Keywords: {self.filter__line_keywords}
###############################""")
        if self.config.get('print_test_errors_on_start', True):
            print('## Error-Debug Test:')
            for tag in self.error_map:
                self.db('Debug test! ♥ ', tag)
            print('###############################')
# SAFE
    def safe(self):
        data = self.data; path = self.path_safe
        try:
            if data:
                with open(path, 'w', encoding='utf-8') as file:
                    file.write(data)
                self.db(f'Result safed in {self.path_safe}', 'd')
        except Exception as e:
            self.db(f'Safe failed! Error: {e}', 'e')
# READ
    def read(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as file:
                return file.readlines()
        except Exception as e:
            self.db(f'Read failed! Error: {e}', 'e')
            return "pathData is n/a"
# FILTERS
    def filter(self, filters, tag, data):
        if not filters: return False
        match tag:
            case 'is_in_line':
                line = data.get('line')
                for f in filters:
                    if f in line: return True
                return False
            case 'file_endings':
                target = data.get('target')
                if target.lower().endswith(tuple(filters)):# or target.lower().startswith(tuple(filters)):
                    return False
                return True
            case 'ignore_tags':
                target = data.get('target')
                for f in filters:
                    if f in target.lower():
                        return True
                return False
            case _:
                self.db(f'filter failed! Error: unknow match tag', 'e')
        return False
# ACTIONS > FILES
    def file_action(self, obj, target):
        if self.filter(self.filter__file_endings, 'file_endings', {'target': target}): return
        if self.filter(self.filter__ignore_file_tags, 'ignore_tags', {'target': target}): return
        self.db(f'{obj}', 'fi')

        space_start = '\n'; space_end = '\n'
        if self.settings.get('spaces_between_files', False) == True: space_start = '\n\n'; space_end = '\n\n'

        line_head = f'{space_start}###########################| --- Object : {obj} -- | -- Path : {target} --- |{space_end}'
        self.data += line_head
        data = self.read(target)
        for line in data:
            if self.filter(self.filter__line_keywords, 'is_in_line', {'line': line}): continue
            self.data += line
# ACTIONS > FOLDERS
    def folder_action(self, obj, target):
        if self.filter(self.filter__ignore_file_tags, 'ignore_tags', {'target': target}): return
        # if self.fil
        self.db(f'{obj}', 'fo')
        self.deepSearch(target)
# DEEP-SEARCH
    def deepSearch(self, target):
        self.db(f'Target: {target}', 'n')
        for obj in os.listdir(target):
            targetPath = self.path(rf'{target}/{obj}')
            if os.path.isdir(targetPath): self.folder_action(obj, targetPath)
            else: self.file_action(obj, targetPath)
# COLLEC
    def run_search(self):
        if not self.path_target: self.db(f'Target-Path not found! Path: {self.path_target}', 'e'); return
        self.deepSearch(self.path_target)
        self.safe()
collector(config)
