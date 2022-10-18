import re
import spacy
from pattern.en import conjugate, tenses

class TenseTransformationOutput:
  def __init__(
    self, original_sent: str, new_sent: str,
    original_tense: str, new_tense: str,
    original_verb: str, new_verb: str
  ):
    self.original_sent = original_sent
    self.new_sent = new_sent
    self.original_tense = original_tense
    self.new_tense = new_tense
    self.original_verb = original_verb
    self.new_verb = new_verb

def tense_transformation(nlp, sent: str, tense: str, out_tense: str):
  # remove punctuation
  sent = re.sub(r',|\.', "", sent)
  doc = nlp(sent)
  no_tokens = len(doc)

  for i, token in enumerate(doc):
    curr_tok = token
    if i < no_tokens - 1:
      look_ahead_tok = doc[i+1]
    else:
      look_ahead_tok = None
    if "Perfect" in tense and "Continuous" in tense:
      if curr_tok.lemma_ == "have" \
        and look_ahead_tok is not None \
        and look_ahead_tok.lemma_ == "be":
        if i + 2 <= no_tokens - 1:
          main_verb_tok = doc[i+2]
        else:
          main_verb_tok = None
        if main_verb_tok is not None and main_verb_tok.pos_ == "VERB":
          verbs_indexes = [i, i+3]
          verbs_lemma = [curr_tok.lemma_, look_ahead_tok.lemma_, main_verb_tok.lemma_]
        else:
          raise Exception("No verb. Wrong tense identification")
    elif "Future" in tense:
      if "Continuous" in tense:
        if curr_tok.lemma_ == "will" \
          and look_ahead_tok is not None \
          and look_ahead_tok.lemma_ == "be":
          if i + 2 <= no_tokens - 1:
            main_verb_tok = doc[i+2]
          else:
            main_verb_tok = None
          if main_verb_tok is not None and main_verb_tok.pos_ == "VERB":
            verbs_indexes = [i, i+3]
            verbs_lemma = [curr_tok.lemma_, look_ahead_tok.lemma_, main_verb_tok.lemma_]
          else:
            raise Exception("No verb. Wrong tense identification")
      elif "Simple" in tense:
        if curr_tok.lemma_ == "will" \
          and look_ahead_tok is not None:
          main_verb_tok = look_ahead_tok
          if main_verb_tok.pos_ == "VERB":
            verbs_indexes = [i, i+2]
            verbs_lemma = [curr_tok.lemma_, main_verb_tok.lemma_]
          else:
            raise Exception("No verb. Wrong tense identification")
    elif "Perfect" in tense:
      if curr_tok.lemma_ == "have" and look_ahead_tok is not None:
        main_verb_tok = look_ahead_tok
        if main_verb_tok.pos_ == "VERB":
          verbs_indexes = [i, i+2]
          verbs_lemma = [curr_tok.lemma_, main_verb_tok.lemma_]
        else:
          raise Exception("No verb. Wrong tense identification")
    elif "Continuous" in tense:
      if curr_tok.lemma_ == "be" and look_ahead_tok is not None:
        main_verb_tok = look_ahead_tok
        if main_verb_tok.pos_ == "VERB":
          verbs_indexes = [i, i+2]
          verbs_lemma = [curr_tok.lemma_, main_verb_tok.lemma_]
        else:
          raise Exception("No verb. Wrong tense identification")
    elif "Simple" in tense:
      if curr_tok.pos_ == "VERB":
        main_verb_tok = curr_tok
        verbs_indexes = [i, i+1]
        verbs_lemma = [main_verb_tok.lemma_]

  # print(verbs_indexes)
  # print(verbs_lemma)
  # print(doc[verbs_indexes[0]:verbs_indexes[1]])
  verb = verbs_lemma[-1]
  arr = [token.text for token in doc]
  if out_tense == "Present Simple":
    arr[verbs_indexes[0]:verbs_indexes[1]] = [verb]
    new_sent = " ".join(arr)
    return TenseTransformationOutput(
        sent, new_sent, tense, out_tense,
        doc[verbs_indexes[0]:verbs_indexes[1]], verb
    )
  elif out_tense == "Past Simple":
    verb = conjugate(verb, tense="past")
    arr[verbs_indexes[0]:verbs_indexes[1]] = [verb]
    new_sent = " ".join(arr)
    # print(new_sent)
    return TenseTransformationOutput(
        sent, new_sent, tense, out_tense,
        doc[verbs_indexes[0]:verbs_indexes[1]], verb
    )
  elif out_tense == "Future Simple":
    verb = f'will {verb}'
    arr[verbs_indexes[0]:verbs_indexes[1]] = [verb]
    new_sent = " ".join(arr)
    # print(new_sent)
    return TenseTransformationOutput(
        sent, new_sent, tense, out_tense,
        doc[verbs_indexes[0]:verbs_indexes[1]], verb
    )
  elif "Continuous" in out_tense:
    verb = conjugate(verb, tense="present", aspect="progressive")
    if "Future" in out_tense:
      verb = f'will be {verb}'
      arr[verbs_indexes[0]:verbs_indexes[1]] = [verb]
      new_sent = " ".join(arr)
      # print(new_sent)
      return TenseTransformationOutput(
          sent, new_sent, tense, out_tense,
          doc[verbs_indexes[0]:verbs_indexes[1]], verb
      )
    elif "Present Perfect" in out_tense:
      verb = f'have been {verb}'
      arr[verbs_indexes[0]:verbs_indexes[1]] = [verb]
      new_sent = " ".join(arr)
      # print(new_sent)
      return TenseTransformationOutput(
          sent, new_sent, tense, out_tense,
          doc[verbs_indexes[0]:verbs_indexes[1]], verb
      )
    elif "Present" in out_tense:
      verb = f'be {verb}'
      arr[verbs_indexes[0]:verbs_indexes[1]] = [verb]
      new_sent = " ".join(arr)
      # print(new_sent)
      return TenseTransformationOutput(
          sent, new_sent, tense, out_tense,
          doc[verbs_indexes[0]:verbs_indexes[1]], verb
      )
    elif "Past" in out_tense:
      verb = f'was {verb}'
      arr[verbs_indexes[0]:verbs_indexes[1]] = [verb]
      new_sent = " ".join(arr)
      # print(new_sent)
      return TenseTransformationOutput(
          sent, new_sent, tense, out_tense,
          doc[verbs_indexes[0]:verbs_indexes[1]], verb
      )
  elif out_tense == "Present Perfect":
    verb = conjugate(verb, tense="past", aspect="progressive")
    verb = f'have {verb}'
    arr[verbs_indexes[0]:verbs_indexes[1]] = [verb]
    new_sent = " ".join(arr)
    # print(new_sent)
    return TenseTransformationOutput(
        sent, new_sent, tense, out_tense,
        doc[verbs_indexes[0]:verbs_indexes[1]], verb
    )

nlp = spacy.load('en_core_web_sm')
sent = "I work at a education company."
tense = "Present Simple"
out_tense = "Past Simple"
tense_transformation(nlp, sent, tense, out_tense)