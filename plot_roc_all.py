# -*- coding: utf-8 -*-

# ROC4ML
# plot_roc_all.py : the main plotting file
#
# Author: Jiachen Liu / LCY.Hugepanda

import os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import ROC4ML_config as config

path_score = config.path_score
path_label = config.path_label
positive_label = config.positive_label

def load_data():
  # load scores and store them in a list, its element is a tuple (score, name)
  #   - score: a numpy array
  #   - name:  name of the input file without postfix
  scores = list()
  for parent, dirnames, filenames in os.walk(path_score):
    if 0 == len(filenames):
      print '[!ERROR!] Please place one label file in the path_label folder'
      return
    for filename in filenames:
      data = np.loadtxt(path_score + '\\' + filename, dtype=np.float64, delimiter="\n")
      scores.append((data, filename.split('.')[0:-1]))
      print '[INFO] score loaded from ' + filename

  # load labels and store them in a list, it is a numpy array
  for parent, dirnames, filenames in os.walk(path_label):
    if not 1 == len(filenames):
      print '[!ERROR!] Please place one label file in the path_label folder'
      return
    for filename in filenames:
      label = np.loadtxt(path_label + '\\' + filename, dtype=np.int16, delimiter='\n')
      print '[INFO] label loaded from ' + filename
      label_set = set(label.tolist())

      if not 2 == len(label_set):
        print '[!ERROR!] Not two classes found, please check the label file'
        return
      else:
        label_list = list(label_set)

        if positive_label == label_list[0]:
          pass
        elif positive_label == label_list[1]:
          label_list = label_list[::-1]

        print '[INFO] Labels: %d (Positive) and %d (Negative)' % (label_list[0], label_list[1])


  return scores, label, label_list


def plot_roc(tpr_list, fpr_list, name_list):
  if 'xkcd' == config.style:
    plt.xkcd()
    sns.set(style='ticks', palette='Set2')
  elif 'seaborn' == config.style:
    pass
  elif 'pretty' == config.style:
    sns.set(style='ticks', palette='Set2')

  mpl.rc('xtick', labelsize=12)
  mpl.rc('ytick', labelsize=12)

  fig = plt.figure()
  fig.suptitle('ROC curves', fontsize=14, fontweight='bold')
  ax = fig.add_subplot(111)
  fig.subplots_adjust(top=0.92)
  #ax.set_title('axes title')
  ax.set_xlabel('False positive rate', fontsize=14, fontweight='bold')
  ax.set_ylabel('True positive rate', fontsize=14, fontweight='bold')

  handles = list()
  for i in range(0, len(tpr_list)):
    h, = plt.plot(tpr_list[i], fpr_list[i])
    handles.append(h)
    name_list[i] += ': AUC = %.3f' % auc_list[i]

  ax.legend(handles, name_list, loc=4, fontsize=15)

  plt.plot([0, 1], [0, 1], '--')

  # ax.text(0.95, 0.01, 'colored text in axes coords',\
  #   verticalalignment='bottom', horizontalalignment='right',\
  #   transform=ax.transAxes,\
  #   color='green', fontsize=15)

if __name__ == "__main__":
  scores, label, label_list = load_data()

  auc_list = list()
  tpr_list = list()
  fpr_list = list()
  name_list = list()
  for model_idx in range(0, len(scores)):
    score = scores[model_idx][0]
    name_list.append(scores[model_idx][1][0])

    score_positive = score[label_list[0] == label]
    score_negative = score[label_list[1] == label]

    score_all = np.r_[score_positive, score_negative]
    score_all = score_all[score_all.argsort()]
    len_score_all = score_all.shape[0]

    tpr = np.zeros((len_score_all, 1))
    fpr = np.zeros((len_score_all, 1))

    for i in range(0, len_score_all):
      thr = score_all[i]
      tpr[i] = 1.0 * len(score_positive[score_positive.T > thr]) / score_positive.shape[0]
      fpr[i] = 1.0 * len(score_negative[score_negative.T > thr]) / score_negative.shape[0]

    tpr_list.append(tpr)
    fpr_list.append(fpr)

    auc = 0
    # for i in range(0, score_positive.shape[0]):
    #   for j in range(0, score_negative.shape[0]):
    #     if score_positive[i] < score_negative[j]:
    #         auc += 1
    #     elif score_positive[i] == score_negative[j]:
    #         auc += 0.5
    #
    # auc_list.append(1.0 * auc / score_positive.shape[0] * score_negative.shape[0])

    width_left = 0;
    for i in range(0, len(tpr)):
      width_right = fpr[i]
      auc = auc + (width_right - width_left)*tpr[i]
      width_left = fpr[i]
    auc_list.append(auc)

  plot_roc(tpr_list, fpr_list, name_list)
  plt.show()


