import yaml
import os
import deepl

class main:
    def __init__(self):
        self.files = {}
        self.readFiles()
        self.posProcess()
        #self.translator = deepl.Translator(auth_key)

        #result = self.translator.translate_text("Hello, world!", target_lang="PL")
        #print(result)

    def readFiles(self):
        for filename in os.listdir('input'):
            if filename.endswith(".yaml") or filename.endswith(".yml"):
                with open('input/' + filename, encoding='utf-8') as file:
                    documents = yaml.full_load(file)
                    data = {}
                    for item, doc in documents.items():
                        if item == 'tasks':
                            continue
                        if item == 'rewards':
                            continue
                        data[item] = doc
                    self.files[filename] = data


    def posProcess(self):
        for key, value in self.files.items():
            print(value['display']['name'])
            for string in value['display']['lore-normal']:
                if string == "&9Rewards:":
                    string = "&9Nagrody:"

                if string == "&9Options:":
                    string = "&9Opcje:"


                print(string)


if __name__ == '__main__':
    main = main()


