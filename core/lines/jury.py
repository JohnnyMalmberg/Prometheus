from api_wrap.openai import *

class BooleanJuryInstructions():
    def __init__(self, question, short_question, yes_means, no_means, juror_count=3):
        self.question = question
        self.yes_means = yes_means
        self.no_means = no_means
        self.juror_count = juror_count
        self.short_question = short_question

    def run_trial(self, raw_text):
        messages = [] 
        messages += gpt_message('user', f'I have a single simple yes-or-no question about the following message:\n\n```\n{raw_text}\n```\n\nThe message is over now. Regarding the message: {self.question}\n\nYour answer must ONLY be the word "YES" or the word "NO", with no further commentary nor explanation.\n\n"YES" means that {self.yes_means}\n\n"NO" would mean that {self.no_means}.\n\n{self.short_question}')

        responses = simple_chat(messages, 1.6, self.juror_count, max_tokens=3)

        yeas = ["YES" in x for x in responses].count(True)
        nays = ["NO" in x for x in responses].count(True)
        abstain = self.juror_count - (yeas + nays)

        return (yeas, nays, abstain)
