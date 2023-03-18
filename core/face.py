import openai
from api_wrap.openai import gpt_message

model = 'gpt-3.5-turbo'

class Face():
    def __init__(self, name, epithet, description, style, goals, temperature=1.25):
        self.aliases = [n.strip() for n in name.split(' aka ') if n != '']
        self.name = self.aliases[0]
        self.epithet = epithet
        self.description = description
        self.style = style
        self.goals = goals
        self.temperature = temperature

    def info_string(self):
        ns = ' aka '.join(self.aliases)
        n = self.name
        return f'**{ns}, {self.epithet}**.\n\n{n} is {self.description}.\n\n{n}\'s writings are {self.style}.\n\n{n} seeks to {self.goals}.\n\n{n}\'s temperature is {self.temperature}.'

    def serialize(self):
        ns = ' aka '.join(self.aliases)
        return '|'.join([ns, self.epithet, self.description, self.style, self.goals, str(self.temperature)])

    def short_description(self):
        ns = ' aka '.join(self.aliases)
        return f'{ns}, {self.epithet}'

def auto_face(prompt):
    sp = prompt.split(',', maxsplit=2)
    names = sp[0].strip()

    epithet = 'Spirit'
    if len(sp) > 1:
        epithet = sp[1].strip()

    
    aliases = [n.strip() for n in names.split(' aka ') if n != '']
    name0 = aliases[0]

    akas = ''
    if len(aliases) > 1:
        akas = ', '.join(aliases[1:])
        akas = f'\n{name0} is also known as by these names: {akas}'
    
    if len(sp) > 2:
        if len(sp) > 1:
            prompt = f'{name0}, {epithet}: {sp[2]}{akas}'
        else:
            prompt = f'{name0}: {sp[2]}{akas}'
    else:
        if len(sp) > 1:
            prompt = f'{name0}: {epithet}{akas}'
        else:
            prompt = f'{name0}{akas}'

    # todo: improve epithet handling on later prompts
    description_messages = face_aspect_messages(prompt, 'the character\'s description', 'The character is', 'Albert Einstein', 'a theoretical physicist who worked on generalizing of Newton\'s laws of physics, with contributions such as special and general relativity, the matter-energy equivalence formula (E=mc2), and work on quantum mechanics; and who won a Nobel Prize for his contributions to theoretical physics')
    description = simple_chat(description_messages, 1.2)

    prompt = f'{name0}, {epithet}{akas}\n\n{name0} is {description}'
    style_messages = face_aspect_messages(prompt, 'the character\'s distinctive writing style', 'The character\'s writings are', 'The Mad ', 'crude, jocular, unique, ignorant, meandering, and often incoherent')
    style = simple_chat(style_messages, 1.2)

    prompt = f'{name0}, {epithet}{akas}\n\n{name0} is {description}\n\n{name0}\'s writings are {style}'
    goals_messages = face_aspect_messages(prompt, 'the character\'s goals and desires', 'The character seeks to', 'Sauron', 'acquire his ring and rule Middle Earth, and emulate his master, Morgoth, also known as Melkor')
    goals = simple_chat(goals_messages, 1.2)

    return Face(names, epithet, description, style, goals)

def face_aspect_messages(prompt, aspect, context, example_char, example_result):
    m = gpt_message('system', f'You will assist the user in inventing a new character. In particular, you will be helping invent {aspect}. Your response should be the completion of this sentence: "{context}...". Please do not include "{context}" in your reply, just your completion of that single sentence, and no further commentary.')
    m += gpt_message('user', f'Hello! I have a character idea and I need your help writing up {aspect}. I also need you to reply only by completing the sentence "{context}..." and producing no other output. To show that you understand, please tell me what you would write for the character {example_char}.')
    m += gpt_message('assistant', example_result)
    m += gpt_message('user', f'Excellent, you got the reply format right. Now, here\'s my character idea: {prompt}')
    m += gpt_message('system', f'Remember, you are ONLY supposed to reply with the completion of the sentence - do not include the first part of the sentence, "{context}".')
    return m

def parse_face(rep):
    s = [x.strip() for x in rep.split('|')]
    if len(s) > 5:
        s5 = float(s[5])
    else:
        s5 = 1.4
    return Face(s[0], s[1], s[2], s[3], s[4], s5)

def load_faces():
    with open('data/text/faces', 'r') as faces_file:
        face_strings = faces_file.readlines()

    faces = []

    for face_string in face_strings:
        try:
            faces += [parse_face(face_string)]
        except Exception as e:
            print(f'{"="*80}\n\n{e}\n\n{"="*80}')
    
    return faces