import itertools as it
import os
from logging import getLogger

import numpy as np
from scipy.special import comb

from pyms.basic.p_extract_clips import extract_clips_helper
from pyms.mlpy import DiskReadMda, readmda, writemda32, writemda64

parent_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

processor_name = 'pyms.anneal_segments'
processor_version = '0.17'

logger = getLogger(__name__)


def anneal_segments(*, timeseries_list, firings_list, firings_out,
                    dmatrix_out='', k1_dmatrix_out='', k2_dmatrix_out='',
                    dmatrix_templates_out='', time_offsets):
    """
    Combine a list of firings files to form a single firings file
    Link firings labels to first firings.mda, all other firings labels are
    incremented.

    Parameters
    ----------
    timeseries_list : INPUT
        A list of paths of timeseries mda files to be used for drift
        adjustment / time offsets
    firings_list : INPUT
        A list of paths of firings mda files to be concatenated/drift adjusted
    firings_out : OUTPUT
        The output firings
    dmatrix_out : OUTPUT
        The distance matrix used
    k1_dmatrix_out : OUTPUT
        The mean distances of k1 templates to k1 spikes
    k2_dmatrix_out : OUTPUT
        The mean distances of k2 templates to k2 spikes
    dmatrix_templates_out : OUTPUT
        The templates used to compute the distance matrix
        ...


    time_offsets : string
        An array of time offsets for each firings file. Expect one offset for
        each firings file.
        ...
    """
    logger.info('timeseries_list' + str(timeseries_list))
    logger.info('firings_list' + str(firings_list))
    logger.info('firings_out' + str(firings_out))
    logger.info('time_offsets ' + str(time_offsets))

    if time_offsets:
        time_offsets = np.fromstring(time_offsets, dtype=np.float_, sep=',')
    else:
        logger.warning('No time offsets provided - assuming zero time '
                       'gap/continuously recorded data')
        time_offsets = np.zeros(len(timeseries_list))
        # Get toffsets based on length of preceeding timeseries -
        # first one left as zero
        for timeseries in range(len(timeseries_list) - 1):
            X = DiskReadMda(timeseries_list[timeseries])
            time_offsets[timeseries + 1] = time_offsets[timeseries] + X.N2()

    concatenated_firings = concat_and_increment(firings_list, time_offsets)

    (dmatrix, k1_dmatrix, k2_dmatrix, templates, Kmaxes,
     segment_combos) = get_dmatrix_templates(timeseries_list, firings_list)
    dmatrix[np.isnan(dmatrix)] = -1  # set nans to -1 to avoid runtime error
    # replace all negative dist numbers (no comparison) with NaN
    k1_dmatrix[dmatrix < 0] = np.nan
    # replace all negative dist numbers (no comparison) with NaN
    k2_dmatrix[dmatrix < 0] = np.nan
    # then replace all negative dist numbers (no comparison) with NaN
    dmatrix[dmatrix < 0] = np.nan

    # TODO: Improve join function
    # Returns with base 1 adjustment
    pairs_to_merge = get_join_matrix(
        dmatrix, k1_dmatrix, templates, Kmaxes, segment_combos)

    pairs_to_merge = np.reshape(pairs_to_merge, (-1, 2))
    # Eliminate all rows with NaN
    pairs_to_merge = pairs_to_merge[~np.isnan(pairs_to_merge).any(axis=1)]
    # Assure that input is sorted
    pairs_to_merge = pairs_to_merge[np.argsort(pairs_to_merge[:, 0])]

    # Propagate merge pairs to lowest label number
    for idx, label in enumerate(pairs_to_merge[:, 1]):
        # Input should be sorted
        is_in_label = np.isin(pairs_to_merge[:, 0], label)
        pairs_to_merge[is_in_label, 0] = pairs_to_merge[idx, 0]

    # Merge firing labels
    for merge_pair in range(pairs_to_merge.shape[0]):
        is_in_pairs = np.isin(concatenated_firings[2, :],
                              pairs_to_merge[merge_pair, 1])
        # Already base 1 corrected
        concatenated_firings[2, is_in_pairs] = pairs_to_merge[merge_pair, 0]

    if dmatrix_out:
        writemda64(dmatrix, dmatrix_out)
    if dmatrix_templates_out:
        writemda32(templates, dmatrix_templates_out)
    if k1_dmatrix_out:
        writemda64(k1_dmatrix, k1_dmatrix_out)
    if k2_dmatrix_out:
        writemda64(k2_dmatrix, k2_dmatrix_out)

    # Write
    return writemda64(concatenated_firings, firings_out)


def get_join_matrix(dmatrix, k1_dmatrix, templates, Kmaxes, segment_combos):
    # Sweep forward in time, linking clust to min dist away
    pairs_to_merge = np.array([])
    adj_Kmaxes = np.cumsum(Kmaxes)
    for dframe in range(dmatrix.shape[2]):
        # if starting with the first segment and combination, 0 offset
        if segment_combos[dframe, 0] == 0:
            f1_adj = 0
        else:
            # otherwise increment cluster numbers based on max of previous
            # segment
            f1_adj = adj_Kmaxes[segment_combos[dframe, 0] - 1]
        f2_adj = adj_Kmaxes[segment_combos[dframe, 1] - 1]
        for f1_idx in range(dmatrix.shape[1]):
            # Ignore nan's and if all nans, return nan
            f2_pair = _nanargmin(dmatrix[f1_idx, :, dframe])
            if not np.isnan(f2_pair):
                f1_pair = _nanargmin(dmatrix[:, f2_pair, dframe])
                if f1_pair == f1_idx:  # mutual nearest
                    # Check if distance to new template is less than mean
                    # distance to spike
                    # changed from 0.1
                    dist_to_new_template_ratio = (
                        dmatrix[f1_idx, f2_pair, dframe] /
                        k1_dmatrix[f1_idx, f2_pair, dframe])
                    if dist_to_new_template_ratio < 1:
                        # Base 1 adjustment to match label
                        pairs_to_merge = np.append(
                            pairs_to_merge,
                            np.array([f1_idx + f1_adj + 1,
                                      f2_pair + f2_adj + 1]))
        # f1_adj+=Kmaxes[segment_combos[dframe,0]]
        # f2_adj+=Kmaxes[segment_combos[dframe,1]]
    return pairs_to_merge


def _nanargmin(X):
    # If all nans in slice, return nan; no axis
    try:
        return np.nanargmin(X)
    except ValueError:
        return np.nan


def concat_and_increment(firings_list, time_offsets, increment_labels='true'):
    if len(firings_list) == len(time_offsets):
        # default to case where the list is empty
        concatenated_firings = np.zeros((3, 0))
        first = True
        for idx, firings in enumerate(firings_list):
            to_append = readmda(firings)
            to_append[1, :] += time_offsets[idx]
            if not first:
                if increment_labels == 'true':
                    if concatenated_firings.any():  # if not empty
                        # add the Kmax from previous
                        to_append[2, :] += max(concatenated_firings[2, :])
                    else:  # if first firings is empty, move on to the next
                        concatenated_firings = to_append
            if first:
                concatenated_firings = to_append
            else:
                concatenated_firings = np.append(
                    concatenated_firings, to_append, axis=1)
            first = False
        return concatenated_firings
    else:
        logger.warning(
            'Mismatch between number of firings files and number of offsets')


def get_dmatrix_templates(timeseries_list, firings_list):
    X = DiskReadMda(timeseries_list[0])
    M = X.N1()
    CLIP_SIZE = 50
    num_segments = len(timeseries_list)
    # Get all possible segment combinations
    segment_combos = it.combinations(range(num_segments), 2)
    segment_combos = np.array(list(segment_combos))
    # Order segment combinations such that neighbors are first,
    # then non-neighbors
    segment_combos = np.append(
        segment_combos[np.where(np.diff(segment_combos) == 1)[0], :],
        segment_combos[np.where(np.diff(segment_combos) > 1)[0], :], axis=0)
    num_combos = int(comb(num_segments, 2))
    firings_arrays = [readmda(file) for file in firings_list]
    Kmaxes = []
    Kmax = 0
    for j, firings_array in enumerate(firings_arrays):
        logger.info(
            f'{len(firings_array[1, :])} clustered events in segment {j}')
        labels = firings_array[2, :]
        if len(labels) == 0:
            Kmax = 0
            Kmaxes.append(0)
        else:
            Kmax = int(max(Kmax, np.max(labels)))
            Kmaxes.append(np.max(labels))
    use_max = int(max(Kmaxes))
    dmatrix = np.full((use_max, use_max, num_combos), -1)
    k1_dmatrix = np.full_like(dmatrix, -1)
    k2_dmatrix = np.full_like(dmatrix, -1)
    templates = np.zeros((M, CLIP_SIZE, use_max, 2 * num_combos))

    for n in range(num_combos):
        # count up to number of combinations for dmatrix 3rd dimension indexing
        j1 = segment_combos[n, 0]
        j2 = segment_combos[n, 1]
        logger.info(f'Computing dmatrix between segments {j1} and {j2}')
        if (np.size(firings_arrays[j1]) == 0 or
                np.size(firings_arrays[j2]) == 0):
            continue
        else:
            (dmatrix0, k1_dmatrix0, k2_dmatrix0,
             templates1, templates2) = compute_dmatrix(
                timeseries_list[j1], timeseries_list[j2], firings_arrays[j1],
                firings_arrays[j2], clip_size=CLIP_SIZE)
            dmatrix[0:dmatrix0.shape[0], 0:dmatrix0.shape[1], n] = dmatrix0
            k1_dmatrix[0:dmatrix0.shape[0],
                       0:dmatrix0.shape[1], n] = k1_dmatrix0
            k2_dmatrix[0:dmatrix0.shape[0],
                       0:dmatrix0.shape[1], n] = k2_dmatrix0
            templates[:, :, 0:dmatrix0.shape[0], n * 2] = templates1
            templates[:, :, 0:dmatrix0.shape[1], n * 2 + 1] = templates2

    return dmatrix, k1_dmatrix, k2_dmatrix, templates, Kmaxes, segment_combos


def compute_dmatrix(timeseries1, timeseries2, F1, F2, *, clip_size):
    X = DiskReadMda(timeseries1)
    M = X.N1()
    F1b = get_last_events(F1, 500)
    F2b = get_first_events(F2, 500)
    times1 = F1b[1, :].ravel()
    labels1 = F1b[2, :].ravel()
    clips1 = extract_clips_helper(
        timeseries=timeseries1, times=times1, clip_size=clip_size)
    times2 = F2b[1, :].ravel()
    labels2 = F2b[2, :].ravel()
    clips2 = extract_clips_helper(
        timeseries=timeseries2, times=times2, clip_size=clip_size)

    K1 = int(max(labels1))
    K2 = int(max(labels2))
    dmatrix = np.zeros((K1, K2))

    k1_dmatrix = np.zeros((K1, K2))
    k2_dmatrix = np.zeros((K1, K2))

    templates1 = np.zeros((M, clip_size, K1))
    templates2 = np.zeros((M, clip_size, K2))
    for k1 in range(1, K1 + 1):
        inds_k1 = np.where(labels1 == k1)[0]
        clips1_k1 = clips1[:, :, inds_k1]
        templates1[:, :, k1 - 1] = np.mean(clips1_k1, axis=2)
        for k2 in range(1, K2 + 1):

            inds_k2 = np.where(labels2 == k2)[0]
            clips2_k2 = clips2[:, :, inds_k2]
            templates2[:, :, k2 - 1] = np.mean(clips2_k2, axis=2)
            dmatrix[k1 - 1, k2 - 1] = compute_distance_between_clusters(
                clips1_k1, clips2_k2)
            # get mean distance between each spike and the cluster remplate
            k1_dmatrix[k1 - 1, k2 -
                       1] = compute_distance_between_template_and_spikes(clips1_k1)
            k2_dmatrix[k1 - 1, k2 -
                       1] = compute_distance_between_template_and_spikes(clips2_k2)
    return dmatrix, k1_dmatrix, k2_dmatrix, templates1, templates2


def get_first_events(firings, num):
    L = firings.shape[1]
    times = firings[1, :]
    labels = firings[2, :]
    K = int(max(labels))
    to_use = np.zeros(L)
    for k in range(1, K + 1):
        inds_k = np.where(labels == k)[0]
        times_k = times[inds_k]
        if (len(times_k) <= num):
            # if whole cluster < num spikes, use all the spikes
            to_use[inds_k] = 1
        else:  # otherwise use the first and last num spikes
            times_k_sorted = np.sort(times_k)
            cutoff = times_k_sorted[num]
            to_use[inds_k[np.where(times_k <= cutoff)[0]]] = 1
    return firings[:, np.where(to_use == 1)[0]]


def get_last_events(firings, num):
    L = firings.shape[1]
    times = firings[1, :]
    labels = firings[2, :]
    K = int(max(labels))
    to_use = np.zeros(L)
    for k in range(1, K + 1):
        inds_k = np.where(labels == k)[0]
        times_k = times[inds_k]
        if (len(times_k) <= num):
            to_use[inds_k] = 1
        else:
            times_k_sorted = np.sort(times_k)
            cutoff = times_k_sorted[len(times_k_sorted) - num]
            to_use[inds_k[np.where(times_k >= cutoff)[0]]] = 1
    return firings[:, np.where(to_use == 1)[0]]


def compute_distance_between_clusters(clips1, clips2):
    centroid1 = np.mean(clips1, axis=2)
    centroid2 = np.mean(clips2, axis=2)
    dist = np.sum((centroid2 - centroid1) ** 2)
    return dist


def compute_distance_between_template_and_spikes(clips):
    centroid1 = np.mean(clips, axis=2)
    spk_mean_dist = 0
    for idx in range(clips.shape[2]):
        spk_mean_dist += np.sum(((centroid1 -
                                  clips[:, :, idx]) ** 2)) / clips.shape[2]
    return spk_mean_dist


anneal_segments.name = processor_name
anneal_segments.version = processor_version
anneal_segments.author = 'J Chung and J Magland'
