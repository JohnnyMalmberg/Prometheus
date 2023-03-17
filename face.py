

class Face():
    def __init__(self, name, epithet, description, style, goals, temperature=1.4):
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

def parse_face(rep):
    s = [x.strip() for x in rep.split('|')]
    if len(s) > 5:
        s5 = float(s[5])
    else:
        s5 = 1.4
    return Face(s[0], s[1], s[2], s[3], s[4], s5)

def load_faces():
    with open('faces', 'r') as faces_file:
        face_strings = faces_file.readlines()

    faces = []

    for face_string in face_strings:
        try:
            faces += [parse_face(face_string)]
        except Exception as e:
            print(e)
    
    return faces