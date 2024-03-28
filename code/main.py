from deepl import Translator
import yaml
import os


class Main():
    def __init__(self):
        self.keysToIgnore = [
            "display.type",
            "tasks",
            "rewards",
            "options",
            "placeholders.progress",
            "placeholders.max"
        ]
        auth_key = "266f89c3-9fb8-4921-9132-78266795f0e5:fx"
        self.translator = Translator(auth_key)
        self.language_key = "en"
        self.deepl_target = "pl"

        self.filesDict = {}
        self.getFilesFromInput()
        self.translateFiles()
        self.saveFiles()

    def getFilesFromInput(self):
        # iterate through all files in the input folder
        for filename in os.listdir("../input"):
            if filename.endswith(".yml"):
                with open(f"../input/{filename}", "r", encoding='utf-8') as input_file:
                    data = yaml.load(input_file, Loader=yaml.SafeLoader)
                self.filesDict[filename] = data

    def translateFiles(self):
        for name, file in self.filesDict.items():
            self.goThroughDict(file, "")

    def goThroughDict(self, dictFile, keyI=""):
        for key, value in dictFile.items():
            print(keyI, "   ", key)
            if keyI == "":
                if key in self.keysToIgnore:
                    continue

            if key.startswith(keyI):
                if isinstance(value, str):
                    print(value)
                    if value == "":
                        continue
                    elif value.isdigit():
                        dictFile[key] = int(value)
                        continue
                    elif value == "true":
                        dictFile[key] = True
                        continue
                    elif value == "false":
                        dictFile[key] = False
                        continue
                    else:
                        dictFile[key] = self.translator.translate_text(value, source_lang=self.language_key,
                                                                       target_lang=self.deepl_target).text
                else:
                    if isinstance(value, list):
                        self.goThroughList(value)
                    if isinstance(value, dict):
                        self.goThroughDict(value)

    def goThroughList(self, list):
        for item in list:
            if isinstance(item, str):
                if item == "":
                    continue
                elif item.isdigit():
                    list[list.index(item)] = int(item)
                    continue
                elif item == "true":
                    list[list.index(item)] = True
                    continue
                elif item == "false":
                    list[list.index(item)] = False
                    continue
                else:
                    list[list.index(item)] = self.translator.translate_text(item, source_lang=self.language_key,
                                                                            target_lang=self.deepl_target).text
            elif isinstance(item, dict):
                self.goThroughDict(item)
            elif isinstance(item, list):
                self.goThroughList(item)

    def saveFiles(self):
        for name, file in self.filesDict.items():
            with open(f"../output/{name}", "w", encoding='utf-8') as output_file:
                yaml.dump(file, output_file, allow_unicode=True)


if __name__ == '__main__':
    Main()
