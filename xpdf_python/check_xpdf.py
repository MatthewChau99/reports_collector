import os
import sys

<<<<<<< HEAD

if os.path.isfile('/usr/local/pdftotext'):
=======
if os.path.isfile('/usr/bin/pdftotext'):
>>>>>>> parent of ee3dc92... save
	pass
else:
	sys.exit("Did not detect correctly installed xpdf. Please follow install instructions at: https://github.com/ecatkins/xpdf_python.")
