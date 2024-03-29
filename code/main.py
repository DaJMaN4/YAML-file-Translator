from deepl import Translator
import yaml
import os


class Main:
    def __init__(self):
        self.keysToIgnore = [
            "display.type",
            "tasks",
            "rewards",
            "options",
            "placeholders.progress",
            "placeholders.max"
        ]
        self.predefinedTranslations = {
            "You need to do a certain activity": "Musisz wykonać określoną czynność",
            "before receiving the reward": "przed otrzymaniem nagrody",
            "Options": "Opcje",
            "Rewards": "Nagrody",
            "You will receive": "Otrzymasz",
            "options": "Opcje",
            "Quest has been started.": "Zadanie zostało rozpoczęte.",
            "Upon completion of this quest, you will be rewarded with": "Po ukończeniu tego zadania zostaniesz nagrodzony w postaci",
            "was added to your in-game balance": "zostało dodane do twojego salda",
        }

        auth_key = "ae5195ab-7d63-4c3c-9af1-169c7b6241d2:fx"
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

    def goThroughDict(self, dictFile, keyI):
        for key, value in dictFile.items():
            if keyI == "":
                if key in self.keysToIgnore:
                    continue
            for ignoreKey in self.keysToIgnore:
                if ignoreKey == keyI + key:
                    print("ignornig", ignoreKey, "   ", keyI, " ", key,)
                    break
            else:
                print(keyI, "   ", key)
                if isinstance(value, str):
                    dictFile[key] = self.translating(value)
                else:
                    if isinstance(value, list):
                        self.goThroughList(value)
                    if isinstance(value, dict):
                        self.goThroughDict(value, keyI + key + ".")

    def goThroughList(self, list):
        for item in list:
            if isinstance(item, str):
                list[list.index(item)] = self.translating(item)

    def translating(self, value):
        if value == "":
            return ""
        elif value.isdigit():
            return int(value)
        elif value == "true":
            return True
        elif value == "false":
            return False
        else:
            value = value.replace("Progress", "Postęp")
            for text in self.predefinedTranslations:
                if text in value:
                    return value.replace(text, self.predefinedTranslations[text])

            placeholder = ""
            isPlaceholder = False
            placeholderIndex = int
            for text in value:
                if text == "{":
                    placeholderIndex = value.index(text)
                    isPlaceholder = True
                if isPlaceholder:
                    placeholder += text
                if text == "}":
                    break
            if isPlaceholder:
                value = value.replace(placeholder, "")

            if value != "":
                outPutValue = self.translator.translate_text(value, source_lang=self.language_key,
                                                             target_lang=self.deepl_target).text
            if value == "":
                outPutValue = value
            if isPlaceholder:
                outPutValue = outPutValue[:placeholderIndex] + placeholder + outPutValue[placeholderIndex:]

            return outPutValue

    def saveFiles(self):
        for name, file in self.filesDict.items():
            with open(f"../output/{name}", "w", encoding='utf-8') as output_file:
                yaml.dump(file, output_file, allow_unicode=True)


if __name__ == '__main__':
    Main()
