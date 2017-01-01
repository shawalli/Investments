
import string

def financial_string_to_float(fs):
    neg_trans = string.maketrans('(','-')
    return float(fs.translate(neg_trans, '$,)'))