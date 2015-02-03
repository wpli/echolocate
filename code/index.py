import os
import sys
import collections
import ConfigParser

def main():

    data_path = '/Users/wli/Dropbox/projects/text_tracing/txt' 
    ngram_size = 4

    # Load text files in dictionary 
    text_files = os.listdir( data_path )
    text_files.sort()
    docid_textfile_tuples = [ (idx, i) for (idx,i) in enumerate( text_files ) ]
    index_docid_textfile = dict( [ (idx, i) for (idx,i) in enumerate( text_files ) ] )
    index_textfile_docid = dict( [ ( j, i ) for (i,j) in docid_textfile_tuples ] )
    data_dict = {}
    for tf in text_files:
        docid = index_textfile_docid[tf]
        full_path = os.path.join( data_path, tf )
        with open( full_path ) as f:
            txt = f.read()

        data_dict[docid] = txt


    # create dictionaries with split text list and ngrams 
    rolling_ngram_dict = {}
    split_text_dict = {}
    for docid, txt in data_dict.items():
        ngrams = []
        lowercase_text = txt.lower()
        split_text = lowercase_text.split()
        for i in range( 0, len( split_text ) - ngram_size + 1):
            ngrams.append( tuple( split_text[i:i+ngram_size] ) )

        split_text_dict[docid] = split_text[:]
        rolling_ngram_dict[docid] = ngrams[:]    


    docid_positionid_ngram_tuples = []
    for docid, textfile in docid_textfile_tuples:
        ngrams = []
        split_text = data_dict[docid].split()
        for i in range( 0, len( split_text ) - ngram_size + 1):
            ngrams.append( tuple( split_text[i:i+ngram_size] ) )

        for positionid, ngram in enumerate( ngrams ):
            docid_positionid_ngram_tuples.append( ( docid, positionid, ngram ) )


    ngram_counter = collections.Counter( [ i[2] for i in docid_positionid_ngram_tuples ] )
    sorted_ngrams = sorted( ngram_counter.items(), key=lambda x:x[1], reverse=True )
    ngramid_ngram_tuples = [ (idx,i[0]) for idx,i in enumerate( sorted_ngrams ) ]

    index_ngramid_ngram = dict( ngramid_ngram_tuples )
    index_ngram_ngramid = dict( [ (i[1],i[0]) for i in ngramid_ngram_tuples ] )
    docid_positionid_ngramid_tuples = [ ( docid, positionid, index_ngram_ngramid[ngram] ) \
                                           for ( docid, positionid, ngram ) in docid_positionid_ngram_tuples ]


    index_ngramid_to_docid_position_id = {}

    for docid, positionid, ngramid in docid_positionid_ngramid_tuples:
        if ngramid in index_ngramid_to_docid_position_id:
            pass
        else:
            index_ngramid_to_docid_position_id[ngramid] = []

        index_ngramid_to_docid_position_id[ngramid].append( ( docid, positionid ) )

    ruling_docid = 4
    ruling_ngramid_list = [ i[2] for i in docid_positionid_ngramid_tuples if i[0] == ruling_docid ]

    match_list = []
    for ngramid in ruling_ngramid_list:
        match_list.append( index_ngramid_to_docid_position_id[ngramid] )

    # compute percentages
    total_ngrams = len( match_list )

    docidsets_list = []
    for ngram_position in match_list:
        docidsets_list.append( ( set([ i[0] for i in ngram_position ] ) ) )

    for docid in index_docid_textfile.keys():
        num_matches = len( [i for i in docidsets_list if docid in i ] )
        # print docid, index_docid_textfile[docid], num_matches, float( num_matches ) / len( ruling_ngramid_list ), float( num_matches ) / len( split_text_dict[docid] )
    ruling_docid = 4
    ruling_ngramid_list = [ i[2] for i in docid_positionid_ngramid_tuples if i[0] == ruling_docid ]

    ngramid_match_list = []
    for ngramid in ruling_ngramid_list:
        ngramid_match_list.append( ( ngramid, index_ngramid_to_docid_position_id[ngramid] ) )

    data0 = []
    for idx, entry in enumerate( match_list ):
        for i in entry:
            data0.append( ( i[0], idx ) )    

    return list( set( data0 ) )

import datetime
#from matplotlib import pyplot as plt
from matplotlib.dates import date2num
import dateutil




if __name__ == '__main__':
    main()
