# -*- coding: utf-8 -*-

# ROC4ML
# config.py : the configuration file
#
# Author: Jiachen Liu / LCY.Hugepanda

# ------------------------------------------------------------
# The plot style
#   'xkcd': using funny xkcd style
#   'seaborn': using seaborn style (github.com/mwaskom/seaborn)
#   'pretty': using prettyplotlib style (github.com/olgabot/prettyplotlib)
#   'normal': using default matplotlib style
style = 'seaborn'

# Path of score files
# you can place one or more score files in this path.
# Each score file represents a machine learning model.
# We plot the ROC curves of them in a same figure.
# The appearing name of the models are the same with
# their score files (without postfix).
#
# Note that the score files should be plain text files
# and each line contain one float value, e.g.:
# 1.223
# 4.333
# 9.321
# ...
path_score = 'data_score'

# Path of the label file
# You can place only one label file in this path. And
# each line of this file contains one label (must be
# an integer), e.g.:
# 1
# 0
# 1
# ...
path_label = 'data_label'

# The label of the positive class
positive_label = 3
