import yaml
from autoclass import autoclass
import pathlib
from typing import Optional


@autoclass
class Config:
    DATA_DIR = 'data'

    def __init__(self,
                 project_dir: pathlib.Path,
                 customer: str,
                 src_lang: str,
                 tgt_lang: str,
                 flavor: Optional[str]=None,
                 version=1,
                 processors=None, #TODO typing
                 tokenizer=None, #TODO typing
                 truecaser=None, #TODO typing,
                 bpe=None, #TODO typing
                 trainer=None #TODO typing
                 ):
        self.data_dir = project_dir.joinpath(Config.DATA_DIR)

    @staticmethod
    def load(project_dir)->'Config':
        with open(project_dir.joinpath('config.yml'), "r") as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
        return Config(project_dir,
                      data['customer'],
                      data['srcLang'],
                      data['tgtLang'],
                      data['flavor'],
                      data['version'],
                      data['processors'],
                      data['tokenizer'],
                      data['truecaser'],
                      data['bpe'],
                      data['trainer'])

    def save(self)->None:
        with open(self.project_dir.joinpath('config.yml'), "w") as file:
            data = {'customer': self.customer,
                    'srcLang': self.src_lang,
                    'tgtLang': self.tgt_lang,
                    'flavor': self.flavor,
                    'version': self.version,
                    'processors': self.processors,
                    'tokenizer': self.tokenizer,
                    'truecaser': self.truecaser,
                    'bpe': self.bpe,
                    'trainer': self.trainer
                    }

            yaml.dump(data, file, sort_keys=False)

    # @staticmethod
    # def add_tokenizer(src_tokenizer, tgt_tokenizer, project_dir):
    #     with open(os.path.join(project_dir, 'config.yml'), "r") as file:
    #         data = yaml.load(file, Loader=yaml.FullLoader)
    #         data['tokenizer'] = {
    #             'src': src_tokenizer,
    #             'tgt': tgt_tokenizer
    #         }
    #
    #         total_data = {
    #             'customer': data['customer'],
    #             'srcLang': data['srcLang'],
    #             'tgtLang': data['tgtLang'],
    #             'flavor': data['flavor'],
    #             'version': data['version'],
    #             'processors': data['processors'],
    #             'tokenizer': data['tokenizer'],
    #             'truecaser': data['truecaser'],
    #             'bpe': data['bpe'],
    #             'trainer': data['trainer']
    #         }
    #
    #         with open(os.path.join(project_dir, 'config.yml'), "w") as file_write:
    #             yaml.dump(total_data, file_write, sort_keys=False)
    #
    # @staticmethod
    # def add_truecaser(src_truecaser, tgt_truecaser, project_dir):
    #     with open(os.path.join(project_dir, 'config.yml'), "r") as file:
    #         data = yaml.load(file, Loader=yaml.FullLoader)
    #         data['truecaser'] = {
    #             'src': src_truecaser,
    #             'tgt': tgt_truecaser
    #         }
    #
    #         total_data = {
    #             'customer': data['customer'],
    #             'srcLang': data['srcLang'],
    #             'tgtLang': data['tgtLang'],
    #             'flavor': data['flavor'],
    #             'version': data['version'],
    #             'processors': data['processors'],
    #             'tokenizer': data['tokenizer'],
    #             'truecaser': data['truecaser'],
    #             'bpe': data['bpe'],
    #             'trainer': data['trainer']
    #         }
    #
    #         with open(os.path.join(project_dir, 'config.yml'), "w") as file_write:
    #             yaml.dump(total_data, file_write, sort_keys=False)

