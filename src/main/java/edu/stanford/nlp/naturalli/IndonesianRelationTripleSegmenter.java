package edu.stanford.nlp.naturalli;

import edu.stanford.nlp.ling.IndexedWord;
import edu.stanford.nlp.semgraph.SemanticGraph;

import java.util.*;

public class IndonesianRelationTripleSegmenter extends RelationTripleSegmenter {

    public final Set<String> VALID_SUBJECT_ARCS_ID = Collections.unmodifiableSet(new HashSet<String>(){{
        add("amod"); add("compound"); add("aux"); add("nummod"); add("nmod:poss"); add("nmod:tmod"); add("expl");
        add("nsubj"); add("case");
        add("name"); // add for indonesian UD treebank
    }});

    public final Set<String> VALID_OBJECT_ARCS_ID = Collections.unmodifiableSet(new HashSet<String>(){{
        add("amod"); add("compound"); add("aux"); add("nummod"); add("nmod"); add("nsubj"); add("nmod:*"); add("nmod:poss");
        add("nmod:tmod"); add("conj:and"); add("advmod"); add("acl"); add("case");
        // add("advcl"); // Born in Hawaii, Obama is a US citizen; citizen -advcl-> Born.
        add("name"); // add for indonesian UD treebank
    }});

    public IndonesianRelationTripleSegmenter() {
        super(false);
    }

    public IndonesianRelationTripleSegmenter(boolean allowNominalsWithoutNER) {
        super(allowNominalsWithoutNER);
    }

    @Override
    protected Optional<List<IndexedWord>> getValidSubjectChunk(SemanticGraph parse, IndexedWord root, Optional<String> noopArc) {
        return getValidChunk(parse, root, VALID_SUBJECT_ARCS_ID, noopArc);
    }

    @Override
    protected Optional<List<IndexedWord>> getValidObjectChunk(SemanticGraph parse, IndexedWord root, Optional<String> noopArc) {
        return getValidChunk(parse, root, VALID_OBJECT_ARCS_ID, noopArc);
    }

}
