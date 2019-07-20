import sys
import os
root_path = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]
src_path = root_path + '\\src'
sys.path.append(src_path)

import transfer_network


