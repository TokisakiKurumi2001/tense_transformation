import spacy
import re
from tense_transformation import tense_transformation, TenseTransformationOutput
from pattern.en import conjugate
class GeneralTenseTransformation:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def __call__(self, sent: str, tense: str, out_tense: str):
        if "would like" in sent:
            if tense != "Present Simple":
                return f"ERROR: Wrong tense. Not {tense}"
            elif out_tense != "Past Simple":
                return f"ERROR: Cannot transform to other tense except Past Simple"
            else:
                # Present Simple --> Past Simple
                new_sent = re.sub("would like", "would have liked", sent)
                output = TenseTransformationOutput(
                    sent, new_sent, tense, out_tense,
                    "would like", "would have liked"
                )
                return str(output)
        elif "would have liked" in sent:
            if tense != "Past Simple":
                return f"ERROR: Wrong tense. Not {tense}"
            elif out_tense != "Present Simple":
                return f"ERROR: Cannot transform to other tense except Present Simple"
            else:
                # Past Simple --> Present Simple
                new_sent = re.sub("would have liked", "would like", sent)
                output = TenseTransformationOutput(
                    sent, new_sent, tense, out_tense,
                    "would have liked", "would like"
                )
                return str(output)
        elif "would rather have" in sent:
            if tense == "Past Simple":
                doc = self.nlp(sent)
                no_tokens = len(doc)
                for i, curr_tok in enumerate(doc):
                    if i < no_tokens - 1:
                        look_ahead_tok = doc[i+1]
                    else:
                        look_ahead_tok = None
                    if curr_tok.text == "would" \
                        and look_ahead_tok is not None \
                        and look_ahead_tok.text == "rather":
                        if i < no_tokens - 2:
                            look_ahead_2_tok = doc[i+2]
                        if look_ahead_2_tok.text == "have":
                            if i < no_tokens - 3:
                                look_ahead_3_tok = doc[i+3]
                            else:
                                look_ahead_3_tok = None
                            if look_ahead_3_tok is None:
                                return f"ERROR: Wrong tense. Not {tense}"
                            else:
                                if look_ahead_3_tok.pos_ == "VERB":
                                    if out_tense == "Present Simple":
                                        new_verb = f"would rather {look_ahead_3_tok.lemma_}"
                                        original_verb = f'would rather have {look_ahead_3_tok.text}'
                                        new_sent = re.sub(original_verb, new_verb, sent)
                                        output = TenseTransformationOutput(
                                            sent, new_sent,
                                            tense, out_tense,
                                            original_verb, new_verb
                                        )
                                        return str(output)
                                    else:
                                        return f"ERROR: Cannot transform to other tense except Present Simple"
                                else:
                                    return f"ERROR: Wrong tense. Not {tense}"
            elif tense == "Present Simple":
                doc = self.nlp(sent)
                no_tokens = len(doc)
                for i, curr_tok in enumerate(doc):
                    if i < no_tokens - 1:
                        look_ahead_tok = doc[i+1]
                    else:
                        look_ahead_tok = None
                    if curr_tok.text == "would" \
                        and look_ahead_tok is not None \
                        and look_ahead_tok.text == "rather":
                            if i < no_tokens - 3:
                                look_ahead_3_tok = doc[i+3]
                            else:
                                look_ahead_3_tok = None
                            if look_ahead_3_tok is None:
                                if out_tense != "Past Simple":
                                    return f"ERROR: Cannot transform to other tense except Past Simple"
                                else:
                                    new_verb = "would rather have had"
                                    original_verb = "would rather have"
                                    new_sent = re.sub(original_verb, new_verb, sent)
                                    output = TenseTransformationOutput(
                                        sent, new_sent,
                                        tense, out_tense,
                                        original_verb, new_verb
                                    )
                                    return str(output)
                            else:
                                if look_ahead_3_tok.pos_ == "VERB":
                                    return f"ERROR: Wrong tense. Not {tense}"
                                else:
                                    if out_tense != "Past Simple":
                                        return f"ERROR: Cannot transform to other tense except Past Simple"
                                    else:
                                        new_verb = "would rather have had"
                                        original_verb = "would rather have"
                                        new_sent = re.sub(original_verb, new_verb, sent)
                                        output = TenseTransformationOutput(
                                            sent, new_sent,
                                            tense, out_tense,
                                            original_verb, new_verb
                                        )
                                        return str(output)
            else:
                return f"ERROR: Wrong tense. Not {tense}"
        elif "would rather" in sent:
            if tense == "Present Simple":
                if out_tense == "Past Simple":
                    doc = self.nlp(sent)
                    no_tokens = len(doc)
                    for i, curr_tok in enumerate(doc):
                        if i < no_tokens - 1:
                            look_ahead_tok = doc[i+1]
                        else:
                            look_ahead_tok = None
                        if curr_tok.text == "would" \
                            and look_ahead_tok is not None \
                            and look_ahead_tok.text == "rather":
                            if i < no_tokens - 2:
                                look_ahead_2_tok = doc[i+2]
                            else:
                                look_ahead_2_tok = None
                            if look_ahead_2_tok is None:
                                return f"ERROR: Wrong tense. Not {tense}"
                            else:
                                if look_ahead_2_tok.pos_ != "VERB":
                                    return f"ERROR: Wrong tense. Not {tense}"
                                else:
                                    try:
                                        verb = conjugate(look_ahead_2_tok.lemma_, tense="past", aspect="progressive")
                                    except:
                                        verb = conjugate(look_ahead_2_tok.lemma_, tense="past", aspect="progressive")
                                    original_verb = f'would rather {look_ahead_2_tok.lemma_}'
                                    new_verb = f'would rather have {verb}'
                                    new_sent = re.sub(original_verb, new_verb, sent)
                                    output = TenseTransformationOutput(
                                        sent, new_sent,
                                        tense, out_tense,
                                        original_verb, new_verb
                                    )
                                    return str(output)
                else:
                    return f"ERROR: Cannot transform to other tense except Past Simple"
            else:
                return f"ERROR: Wrong tense. Not {tense}"
        else:
            return self.standard_call(sent, tense, out_tense)

    
    def standard_call(self, sent: str, tense: str, out_tense: str):
        try:
            output = tense_transformation(self.nlp, sent, tense, out_tense)
            return str(output)
        except:
            return f"ERROR: Wrong tense. Not {tense}"

if __name__ == "__main__":
    general_tense_transformation = GeneralTenseTransformation()
    sent = "My greatest weakness was here"
    tense = "Past Simple"
    out_tense = "Present Simple"
    print(general_tense_transformation(sent, tense, out_tense))
    # out_tenses = {'Future Continuous': 0,
    #         'Past Continuous': 1,
    #         'Past Simple': 2,
    #         'Present Continuous': 3,
    #         'Present Perfect': 4,
    #         'Present Perfect Continuous': 5,
    #         'Present Simple': 6}
    # for out_tense in out_tenses.keys():
    #     print(general_tense_transformation(sent, tense, out_tense))
