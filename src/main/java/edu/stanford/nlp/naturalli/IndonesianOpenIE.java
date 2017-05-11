package edu.stanford.nlp.naturalli;

import java.util.Properties;

public class IndonesianOpenIE extends OpenIE {
    public IndonesianOpenIE() {
        super(new Properties());
    }

    public IndonesianOpenIE(Properties props) {
        super(props);

        // Override the relation segmenter
        boolean allNominals = Boolean.parseBoolean(props.getProperty("triple.all_nominals", "false"));
        segmenter = new IndonesianRelationTripleSegmenter(allNominals);
    }

}
