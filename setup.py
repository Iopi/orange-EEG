from setuptools import setup, find_packages

# Name of the package
NAME = "EEG"
DOCUMENTATION_NAME = 'Orange EEG'

VERSION = "1.0.0"

DESCRIPTION = "Add-on containing widgets that work with EEG data"
with open("README.md", "r") as f:
	LONG_DESCRIPTION = f.read()

KEYWORDS = (
	# TODO: are we gonna publish it on PyPi?
	# [PyPi](https://pypi.python.org) packages with keyword "orange3 add-on"
	# can be installed using the Orange Add-on Manager
	'orange3 add-on',
)

PACKAGES = find_packages()

PACKAGE_DATA = {
	# TODO: icons, maybe some tutorials
}

INSTALL_REQUIRES = [
	'Orange3',
	'mne==0.17.1', 'AnyQt', 'PyQt5', 'numpy', 'pylsl', 'pywt'
]

ENTRY_POINTS = {
	# TODO: do we want it to be shown in the add-ons manager?
	# Entry points that marks this package as an orange add-on. If set, addon will
	# be shown in the add-ons manager even if not published on PyPi.
	# 'orange3.addon': (
	# 	'EEG = EEG',
	# ),
	# Entry point used to specify packages containing tutorials accessible
	# from welcome screen. Tutorials are saved Orange Workflows (.ows files).
	# 'orange.widgets.tutorials': (
	# 	# Syntax: any_text = path.to.package.containing.tutorials
	# 	'exampletutorials = orangecontrib.example.tutorials',
	# ),

	# Entry point used to specify packages containing widgets.
	'orange.widgets': (
		# Widget category specification can be seen in
		#    orangecontrib/example/widgets/__init__.py
		'EEG = EEG.widgets',
	),
}

NAMESPACE_PACKAGES = ["EEG"]

# TODO: tests?
# TEST_SUITE = "EEG.tests.suite"

# TODO: Generating html documentation, im not sure how this works now
# def include_documentation(local_dir, install_dir):
# 	global DATA_FILES
# 	if 'bdist_wheel' in sys.argv and not path.exists(local_dir):
# 		print("Directory '{}' does not exist. "
# 		      "Please build documentation before running bdist_wheel."
# 		      .format(path.abspath(local_dir)))
# 		sys.exit(0)
#
# 	doc_files = []
# 	for dirpath, dirs, files in walk(local_dir):
# 		doc_files.append((dirpath.replace(local_dir, install_dir),
# 		                  [path.join(dirpath, f) for f in files]))
# 	DATA_FILES.extend(doc_files)


if __name__ == '__main__':
	setup(
		name=NAME,
		version=VERSION,
		description=DESCRIPTION,
		long_description=LONG_DESCRIPTION,
		packages=PACKAGES,
		package_data=PACKAGE_DATA,
		install_requires=INSTALL_REQUIRES,
		entry_points=ENTRY_POINTS,
		keywords=KEYWORDS,
		namespace_packages=NAMESPACE_PACKAGES,
		# test_suite=TEST_SUITE,
		include_package_data=True,
		zip_safe=False,
	)
