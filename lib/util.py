import string
import hashlib

def financial_string_to_float(fs):
    neg_trans = string.maketrans('(','-')
    return float(fs.translate(neg_trans, '$,)'))

def percent_to_degrees(pct):
    return (360.00 * pct) / 100

def generate_hash_id(s):
    return int(hashlib.md5(s).hexdigest()[:8], 16)