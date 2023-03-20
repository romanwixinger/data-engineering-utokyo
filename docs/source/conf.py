# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('../../src'))


# -- Project information -----------------------------------------------------

project = 'Data Engineering UTokyo'
copyright = '2023, Roman Wixinger, Shintaro Nagase, Naoya Ozawa'
author = 'Roman Wixinger, Shintaro Nagase, Naoya Ozawa'


# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.napoleon",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.todo",
    "sphinx.ext.linkcode",
    "sphinx.ext.intersphinx",
    "sphinx.ext.duration",
    "sphinx.ext.doctest",
]

autosummary_generate = True

napoleon_google_docstring = True
napoleon_include_private_with_doc = True

autodoc_member_order = 'bysource'
autodoc_typehints = "both"
autodoc_typehints_format = "short"  # This is handy too

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.

html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

{
    'python': ('https://docs.python.org/', None),
    'numpy': ('https://numpy.org/doc/stable/', None),
    'typing': ('https://docs.python.org/3/library/typing.html', None),
    'pandas': ('https://pandas.pydata.org/', None)
}

def autodoc_process_signature(app, what, name, obj, options, signature, return_annotation):
    # Do something
    return signature, return_annotation


def setup(app):
    app.connect("autodoc-process-signature", autodoc_process_signature)


def linkcode_resolve(domain, info):
    if domain != 'py':
        return None
    if not info['module']:
        return None
    filename = info['module'].replace('.', '/')
    return "https://github.com/romanwixinger/data-engineering-utokyo/tree/main/%s.py" % filename


def linkcode_resolve(domain, info):
    """Adds a [source] button to the docs.
    """
    if domain != 'py':
        return None
    if not info['module']:
        return None
    filename = info['module'].replace('.', '/')
    class_or_instance = info['fullname'].split(".")[0]

    # Recorders
    source_lookup = {
        "Recorder": "data_eng_utokyo/_recorders/recorder",
        "SSDRecorder": "data_eng_utokyo/_recorders/ssd_recorder",
        "PMTRecorder": "data_eng_utokyo/_recorders/pmt_recorder",
        "CoilRecorder": "data_eng_utokyo/_recorders/coil_recorder",
        "FileRecorder": "data_eng_utokyo/_recorders/file_recorder",
        "FileParser": "data_eng_utokyo/_recorders/file_recorder",
        "ImageFileRecorder": "data_eng_utokyo/_recorders/image_file_recorder",
        "IonRecorder": "data_eng_utokyo/_recorders/ion_recorder",
        "LaserRecorder": "data_eng_utokyo/_recorders/laser_recorder",
        "GaugeRecorder": "data_eng_utokyo/_recorders/gauge_recorder",
        "HeaterRecorder": "data_eng_utokyo/_recorders/heater_recorder",
        "ParameterRecorder": "data_eng_utokyo/_recorders/parameter_recorder",
        "CycleRecorder": "data_eng_utokyo/_recorders/cycle_recorder",
        "StaticRecorder": "data_eng_utokyo/_recorders/static_recorder",
    }

    # Algorithms
    source_lookup.update({
        "MOTMLE": "data_eng_utokyo/_algorithms/fit_mot_number",
        "Peak": "data_eng_utokyo/_algorithms/peak",
        "PeakFinder": "data_eng_utokyo/_algorithms/peak_finder",
    })

    # Analyses
    source_lookup.update({
        "Analysis": "data_eng_utokyo/_analyses/analysis",
        "ResultParameter": "data_eng_utokyo/_analyses/analysis",
        "ImageAnalysis": "data_eng_utokyo/_analyses/image_analysis",
        "SSDAnalysis": "data_eng_utokyo/_analyses/ssd_analysis",
        "SSDAnalysisWrapper": "data_eng_utokyo/_analyses/ssd_analysis",
        "PMTAnalysis": "data_eng_utokyo/_analyses/pmt_analysis",
        "SSDHistogramAnalysis": "data_eng_utokyo/_analyses/ssd_histogram_analysis",
    })

    # Utilites
    source_lookup.update({
        "Runner": "data_eng_utokyo/_utilities/runner",
        "create_folders": "data_eng_utokyo/_utilities/mkdir",
        "mkdir_if_not_exist": "data_eng_utokyo/_utilities/mkdir",
    })

    # Constants
    constants = ["CameraConstants", "c_ccd", "c_cmos_Fr_20220918", "c_cmos_laser_room", "c_cmos_Rb_20220918"]
    source_lookup.update({
        c: "data_eng_utokyo/_algorithms/camera_constants" for c in constants
    })

    # Replace filename if the source is hidden
    if class_or_instance in source_lookup:
        filename = source_lookup[class_or_instance]

    return f"https://github.com/romanwixinger/data-engineering-utokyo/tree/main/src/{filename}.py"
