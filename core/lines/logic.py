from api_wrap.openai import *

def logic_exam(question):
    m = []
    m += gpt_message('system', 'You are a supremely intelligent logician. You will ruthlessly dissect any argument you are given. You can spot the subtlest flaws. You enjoy tearing down invalid arguments. You enjoy catching fallacies. You will only allow absolutely perfect arguments to pass your judgement. You are going to take a very tricky logic exam.')

    m += gpt_message('user', f'Q1. {question}')

    return simple_chat(m, top_p=0.1)

async def find_argument(text):
    system = logic_exam(f'Here is an informal argument:\n\n{text}\n\nIf you were to formalize this argument, what system of logic would be best to use? Your options are: "Modal logic", "Probabalistic logic", "First-order logic", "Inductive logic", "Paraconsistent logic", "Free logic". Please do not provide any further commentary or explanation, just write your answer.')

    response = logic_exam(f'You are going to identify the argument in the following text:\n{text}\nPlease write up the provided text as a formal logical argument. You should express the argument in {system}. You do not need to consider the validity or soundness of the argument for now: your job is simply to formalize it.')

    response2 = logic_exam(f'Here is an argument:\n{text}\n\nHere is a formalization of the argument:\n{response}\n\nIf the formalization is correct, write "Correct". Otherwise, rewrite the formalization to be correct. Please keep in mind that you are NOT ')

    return [system, response, response2]

    response2 = logic_exam(f'I will present an argument, and you will determine if it is valid or invalid. You must walk through your reasoning step-by-step before stating your conclusion. Here is the argument:\n\n{response}')

    m = []
    m += gpt_message('system', 'You are a supremely intelligent logician. You will ruthlessly dissect any argument you are given. You can spot the subtlest flaws. You enjoy tearing down invalid arguments. You enjoy catching fallacies. You will only allow absolutely perfect arguments to pass your judgement. You are going to take a very tricky logic exam.')
    m += gpt_message('user', f'Q1. I will present an argument, and an analysis of that argument. You will correct any and all mistakes in the analysis of the argument.\n\nArgument: {response}\n\nAnalysis: {response2}')

    response3s = simple_chat(m, 0.8, 5)

    wrongs = [x for x in response3s if (('wrong' in x.lower()) or ('incorrect' in x.lower()))]

    wrong_ct = len(wrongs)

    def right(responses, wrongs):
        for res in responses:
            if res not in wrongs:
                return res

    if wrong_ct == 5:
        response3 = wrongs[0]
    elif wrong_ct == 0:
        response3 = response3s[0]
    else:
        response3 = f'Sorry, me and the other graders got together and couldn\'t come to a consensus on how to grade this one. Here are our opinions: \n\nOpinion A: {wrongs[0]}\n\nOpinion B: {right(response3s, wrongs)}'
        pass # Non-consensus, most difficult case

    m = []

    m += gpt_message('system', 'You are a supremely intelligent logician. You will ruthlessly dissect any argument you are given. You can spot the subtlest flaws. You enjoy tearing down invalid arguments. You enjoy catching fallacies. You will only allow absolutely perfect arguments to pass your judgement.')
    m += gpt_message('user', f'Hello. I had a grad student review a student\'s logic homework. Can you please summarize all this to just directly state the correct conclusion? Here\'s the argument:\n\n{response}\n\nAnd the student\'s analysis:{response2}\n\nAnd the grad student\'s review:{response3}')

    response4 = simple_chat(m, 0.6)

    return [response, response2, response3, response4]