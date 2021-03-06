import unittest
from simdna import fileProcessing as fp
import simdna
from simdna import synthetic as sn
import numpy as np
import random

class TestRun(unittest.TestCase):

    def test_simple_motif_grammar(self):
        random.seed(1234)
        np.random.seed(1234)
        loaded_motifs = sn.LoadedEncodeMotifs(
                         simdna.ENCODE_MOTIFS_PATH,
                         pseudocountProb=0.001)
        motif1_generator = sn.PwmSamplerFromLoadedMotifs(
                            loaded_motifs, "SIX5_known5")
        motif2_generator = sn.PwmSamplerFromLoadedMotifs(
                            loaded_motifs, "ZNF143_known2")
        separation_generator = sn.UniformIntegerGenerator(2,10)
        embedder = sn.EmbeddableEmbedder(
                    sn.PairEmbeddableGenerator(
                     motif1_generator, motif2_generator, separation_generator))
        embed_in_background = sn.EmbedInABackground(
                               sn.ZeroOrderBackgroundGenerator(500),
                               [embedder])
        generated_sequences = sn.GenerateSequenceNTimes(
                               embed_in_background, 500).generateSequences()
        generated_seqs = [seq for seq in generated_sequences]
        for seq in generated_seqs:
            embedding1 = seq.embeddings[0]
            embedding2 = seq.embeddings[1]
            embedding3 = seq.embeddings[2]
            assert len(embedding1.what) == len(embedding1.what.string)
            assert len(embedding2.what) == len(embedding2.what.string)
            assert len(embedding3.what) == (len(embedding1.what)+
                                            len(embedding2.what)+
                                            embedding3.what.separation)
            #testing that the string of the first motif is placed correctly
            assert (seq.seq[
             embedding1.startPos:embedding1.startPos+len(embedding1.what)]
             == embedding1.what.string)
            #testing that the string of the second motif is placed correctly
            assert (seq.seq[
             embedding2.startPos:embedding2.startPos+len(embedding2.what)]
             == embedding2.what.string) 
            #testing that the motifs are placed correctly
            assert ((embedding2.startPos - (embedding1.startPos
                                          + len(embedding1.what.string)))
                     == embedding3.what.separation)
            #testing the separation is in the right limits
            assert embedding3.what.separation >= 2 
            assert embedding3.what.separation <= 10 
