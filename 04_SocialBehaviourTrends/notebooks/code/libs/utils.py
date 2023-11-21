import pandas as pd
import zipfile

def read_csv(fn, **kwargs):
  return pd.read_csv(fn, **kwargs)

def read_xlsx(fn, **kwargs):
  return pd.read_excel(open(fn, 'rb'),**kwargs) 
  
def read_csv_in_zip(fn_zip, fn_pattern, **kwargs):
  
  zf = zipfile.ZipFile(fn_zip, 'r')
  fn = [fn for fn in zf.namelist() if fn.startswith(fn_pattern)][0]
  
  f = zf.open(fn)
  return pd.read_csv(f, **kwargs)