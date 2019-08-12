"""Back Translation to augment a dataset."""

from __future__ import print_function
from __future__ import division

from tensor2tensor.data_generators import problem
from tensor2tensor.data_generators import text_problems
from tensor2tensor.utils import registry

import unidecode


@registry.register_problem
class TranslateVivi(text_problems.Text2TextProblem):
  """Problem spec for IWSLT'15 En-Vi translation."""

  @property
  def approx_vocab_size(self):
    return 2**15  # 32768

  @property
  def dataset_splits(self):
    """Splits of data to produce and number of output shards for each."""
    # 10% evaluation data
    return [{
        "split": problem.DatasetSplit.TRAIN,
        "shards": 9,
    }, {
        "split": problem.DatasetSplit.EVAL,
        "shards": 1,
    }]

  @property
  def is_generate_per_split(self):
    return False  

  def generate_samples(self, data_dir, tmp_dir, dataset_split):
    #del data_dir
    del tmp_dir
    del dataset_split

    #vn = 'aáàảãạăắằẳẵặâấầẩẫậeéèẻẽẹêếềểễệiíìỉĩịoóòỏõọôốồổỗộơớờởỡợuúùủũụưứừửữựyýỳỷỹỵdđ'
    #aeiouyd = ['a', 'e', 'i', 'o', 'u', 'y', 'd']
    legal = ' !"#$%&\'()*+,-./0123456789:;<=>?@[\\]^_`abcdefghijklmnopqrstuvwxyzáàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵđ{|}~'
    punct = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
    train_data = "%s/train.txt" % data_dir
    #train_data = "%s/corpus-full.txt" % data_dir
    with open(train_data, 'r') as f:
      lines = f.readlines()
      for line in lines:
          line = line.strip().lower()
          line = ''.join(c if c not in punct else '-' for c in line)  # replace all punctuations with '-'
          line = ''.join(c if c in legal else '?' for c in line)  # replace unknown characters with '?'
          line_no_tone = unidecode.unidecode(line)
          if len(line) <= 300:
            yield {
                "inputs": line_no_tone,
                "targets": line,
            }

