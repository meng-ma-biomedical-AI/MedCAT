""" I would just ignore this whole class, it's just a lot of rules that work nicely for CDB
once the software is trained the main thing are the context vectors.
"""
import numpy as np
import operator

class BaseAnnotationChecker(object):
    def __init__(self, cdb, spacy_cat):
        self.cdb = cdb
        self._cat = spacy_cat
        self.pref_names = set(cdb.cui2pref_name.values())


    def CheckAnnotation(self, name, tkns, doc, to_disamb, doc_words):
        # Do not add annotations here, but just return what needs to be done

        # Must be one token, multiple is very dangerous
        if len(name) < config.general['min_name_len']:
            # Skip names below the limit
            return 'skip'

        # Is the detected name uppercase and only one token
        one_tkn_upper = False
        if len(tkns) == 1 and tkns[0].is_upper:
            one_tkn_upper = True

        # First check length limit and uppercase limit
        if len(name) < config.upper_case_limit_len and not one_tkn_upper:
            # Skip this detection
            return 'skip'
        elif len(name) < config.length_limit:
            # Disambiguate
            return 'disambiguate'
        elif self.cdb.name2status[name] == 'A': # Check the cdb 
            if len(self.cdb.name2cui[name]) == 1:
                # Links to only one CUI
                return 'annotate'
            else:
                # Links to multiple CUIs
                return 'disambiguate'
        elif self.cdb.name2status == 'N':
            return 'disambiguate'
        elif self.cdb.
            return 'annotate'


### This is for annotation, should be moved

        if is_train:
            if len(name) < config.disamb_length_limit:
                cuis = self.cdb.name2cuis[name]
                if len(cuis) == 1:
                    if self.cdb.name2cui2status[name][cuis[0]] != 'N':
                        return cuis[0]
                else:
                    for cui in cuis:
                        if self.cdb.name2cui2status[name][cui] == 'P':
                            # Means this name should be used for training as it nearly always links to
                            #the concept with this CUI
                            return cui # Break the loop, one name marked with 'P' linkes to max 1 concept
            return None

        else:
            cuis = self.cdb.name2cuis[name]
            if len(name) < config.disamb_length_limit:
                return disambiguate()
            elif len(cuis) == 1:
                if self.cdb.name2cui2status[name][cuis[0]] == 'N':
                    return disambiguate()
                else:
                    return cuis[0]
            else:
                # Returns None if below thrashold
                return disambiguate(doc, ent, cuis, cdb, config)

# Disambiguate function should check the cut-offs based on min context similarity
#- Reward P, but punish N, leave 0 for A
#- Take 1000 most frequent words, set length limit and make them all 'N'
### End of annotation


        if len(name) > 1 or one_tkn_upper:
            if name in self.cdb.name_isunique:
                # Is the number of tokens matching for short words
                if len(name) >= 7 or len(tkns) in self.cdb.name2ntkns[name]:
                    if self.cdb.name_isunique[name]:
                        # Annotate
                        cui = list(self.cdb.name2cui[name])[0]
                        self._cat._add_ann(cui, doc, tkns, acc=1, name=name)
                    else:
                        to_disamb.append((list(tkns), name))
                else:
                    # For now ignore if < 7 and tokens don't match
                    #to_disamb.append((list(tkns), name))
                    pass
            else:
                # Is the number of tokens matching for short words
                if len(name) > 7 or len(tkns) in self.cdb.name2ntkns[name]:
                    if len(self.cdb.name2cui[name]) == 1 and len(name) > 2:
                        # There is only one concept linked to this name and has
                        #more than 2 characters
                        cui = list(self.cdb.name2cui[name])[0]
                        self._cat._add_ann(cui, doc, tkns, acc=1, name=name)
                    elif self._cat.train and name in self.pref_names and len(name) > 3:
                        # If training use prefered names as ground truth
                        cuis = self.cdb.name2cui[name]
                        for cui in cuis:
                            if name == self.cdb.cui2pref_name.get(cui, 'nan-nan'):
                                self._cat._add_ann(cui, doc, tkns, acc=1, name=name)
                    else:
                        to_disamb.append((list(tkns), name))
                else:
                    # For now ignore
                    #to_disamb.append((list(tkns), name))
                    pass