# Copyright 2017 The Chiron Authors. All Rights Reserved.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Created on Mon Apr 10 04:16:40 2017

from __future__ import absolute_import
import argparse
import os
import sys
import h5py

from chiron.utils import labelop
import tensorflow as tf
import numpy as np
tf.logging.set_verbosity(tf.logging.ERROR)

def _int64_feature(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))

def _bytes_feature(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

def extract(root_folder,output_folder,tfrecord_writer,raw_folder=None):
    count = 1
    if not os.path.isdir(root_folder):
        raise IOError('Input directory does not found.')
    for dir_n,_,file_list in tf.gfile.Walk(root_folder):
     for file_n in file_list:
        if file_n.endswith('fast5'):
#            output_file = output_folder + os.path.splitext(file_n)[0]
            file_n = os.path.join(dir_n,file_n)
            success, (raw_data, raw_data_array),(offset,digitisation,range_s) = extract_file(file_n)
            if success:
                if FLAGS.unit:
                    raw_data=reunit(raw_data,offset,digitisation,range_s)
                count += 1
                example = tf.train.Example(features=tf.train.Features(feature={
                    'raw_data': _bytes_feature(raw_data.tostring()),
                    'features': _bytes_feature(raw_data_array.tostring()),
                    'fname':_bytes_feature(str.encode(file_n))}))
                tfrecord_writer.write(example.SerializeToString())
                sys.stdout.write("%s file transfered.   \n" % (file_n))
            else:
                sys.stdout.write("FAIL on %s file.   \n" % (file_n))
def reunit(signal,offset,digitisation,range_s):
    """
    Rescale the signal to the pA unit. Signal is calculated by
    tr_sig = (signal+offset)*range_s/digitisation
    The offset, digitisation, range_s can be got from /UniqueGlobalKey/channel_id/ entry of the fast5 file.
    Input Args:
        signal: the array contain the digitalised signal.
        offset: offset information read from fast5 file.
        digitisation: channel used for digitalised the signal.
        range_s: range_s entry from fast5 file.
    """
    signal=(signal+offset)*float(range_s)/float(digitisation)
    return np.asarray(signal,dtype=np.float32)
def run_list(dirs,output_folder):
    """
    Run extract() function on all directories if FLAGS.input is a list.
    Input Args:
        dirs: Directories that contain resquiggled fast5 files.
        output_folder: Directory to output the TFRecrod file.
    """
    if output_folder is None:
        output_folder = os.path.abspath(os.path.join(root_folder, os.pardir)) + '/raw/'
    if not os.path.isdir(output_folder):
        os.mkdir(output_folder)
    tfrecords_filename = output_folder + FLAGS.tffile
    writer = tf.python_io.TFRecordWriter(tfrecords_filename)
    for directory in dirs:
        root_folder = directory + os.path.sep
        extract(root_folder,output_folder,writer)
    writer.close()
def extract_file(input_file):
    try:
        raw_info,channel_info = labelop.get_label_raw(
            input_file, FLAGS.basecall_group,
            FLAGS.basecall_subgroup)
        raw_data, raw_label, raw_start, raw_length = raw_info
        offset,range_s,digitisation = channel_info
    except Exception as e:
        print(str(e))
        return False, (None, None) ,(None, None,None)
    raw_data_array = []
    for index, start in enumerate(raw_start):
#        if raw_length[index]==0:
#            print("input_file:" + input_file)
#            raise ValueError("catch a label with length 0")
        raw_data_array.append(
            [start, start + raw_length[index], str(raw_label['base'][index])])
    if FLAGS.mode=='rna':
        raw_data = raw_data[::-1]
    return True, (raw_data, np.array(raw_data_array, dtype='S8')) , (offset,digitisation,range_s)


def run(args):
    global FLAGS
    FLAGS = args
    dirs = FLAGS.input.split(',')
    for root_folder in dirs:
        if not os.path.isdir(root_folder):
            raise IOError('Input directory %s does not found.'%(root_folder))
    output_folder = FLAGS.output + os.path.sep
    run_list(dirs,output_folder)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Transfer fast5 to raw_pair file.')
    parser.add_argument('-i', '--input', required = True,
                        help="Directory that store the fast5 files, multiple directories separted by commas.")
    parser.add_argument('-o', '--output', required = True, help="Output folder")
    parser.add_argument('--basecall_group',default = "RawGenomeCorrected_000",
                        help='The attribute group to extract the training data from. e.g. RawGenomeCorrected_000')
    parser.add_argument('-f', '--tffile', default="train.tfrecords",
                        help="tfrecord file")
    parser.add_argument('--basecall_subgroup', default='BaseCalled_template',
                        help='Basecall subgroup Nanoraw resquiggle into. Default is BaseCalled_template')
    parser.add_argument('--unit',dest='unit',action='store_true',help='Use the pA unit instead of the original digital signal.')
    parser.add_argument('--mode',default = 'dna',
                        help='Type of data to basecall, default is dna, can be chosen from dna, rna and methylation(under construction)')
    args = parser.parse_args(sys.argv[1:])
    run(args)

