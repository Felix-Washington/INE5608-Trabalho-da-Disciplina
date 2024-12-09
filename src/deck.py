import random
from card import Card


class Deck:
    def __init__(self):
        # All questions available. Key is id from question, value its description.
        self.__questions = {}
        # All answers available. Key is id from answers, value its description.
        self.__answers = {}
        # Key is the type of category, value is a list of answers from that category.
        self.__categories_answers = {}
        # Object card that's created when a player interact with deck.
        self.__card = Card([0])
        # Function that create and sort all game data (questions, answers and their references).
        self.create_dicts()

        self.__card_current_answers = {}

    def create_card(self):
        # Get current questions
        questions_current_list = random.sample( list( self.__questions.keys() ), k=4 )

        # Create options for every question
        for question_key in questions_current_list:
            # Determine the category by correct answers from selected question.
            category = None
            for cat_key, answer_ids in self.__categories_answers.items():
                if question_key in answer_ids:
                    category = cat_key
                    break

            # Get answers from same category
            possible_answers_ids = self.__categories_answers[category]

            # Select 3 false answers
            false_answers_ids = random.sample(
                [ans_id for ans_id in possible_answers_ids if ans_id != question_key], k=3 )

            # Merge all answers ids.
            all_answers_ids = false_answers_ids + [question_key]
            random.shuffle( all_answers_ids )

            # Create a dict with its key, question id, and its value a list of answers.
            self.__card_current_answers[question_key] = all_answers_ids

        self.__card = Card( questions_current_list )

    def create_card_options(self, state, options):
        if state == "create_questions":
            self.create_card()
        elif state == "create_answers":
            # If type = answers, options will be a key from a selected question.
            self.__card = Card( self.__card_current_answers[options], options )
        else:
            # If type = players, options will be a list of players ids.
            self.__card = Card( options )

    def check_answer(self, answer):
        if answer == self.__card.question:
            return 1
        return -1
    
    def discard_question(self):
        question = self.__card.question
        self.__questions.pop(question)

    def get_card_option_text(self, text_type, position_board=1, data_id=-1):
        if text_type == "question_title":
            return self.__questions[self.__card.question]
        elif text_type == "create_questions":
            # Set to 5 just for testing.
            if position_board < 3:
                return "?"
            else:
                return self.__questions[data_id]
        elif text_type == "create_answers":
            return self.__answers[data_id]

    def create_dicts(self):
        # Initial value
        self.__questions = {
            # Animals
            0: "Qual é o maior mamífero do mundo?",
            1: "Qual é o animal mais rápido do planeta?",
            2: "Qual animal possui a maior envergadura de asas?",
            3: "Qual animal é conhecido por sua habilidade de mudar de cor?",
            4: "Qual é o único mamífero que põe ovos?",
            5: "Qual é o maior réptil do mundo?",
            6: "Que animal tem a mordida mais forte?",
            7: "Que inseto é conhecido por produzir mel?",
            8: "Qual é o maior peixe do mundo?",
            9: "Qual animal vive a maior parte do tempo de cabeça para baixo?",

            # Colors
            10: "Qual é a cor do céu em um dia limpo?",
            11: "Qual a cor do texto da bandeira do Brasil?",
            12: "Qual a cor que representa elegência e luto?",
            13: "Qual é a cor do sangue humano?",
            14: "Que cor simboliza a paz em várias culturas?",
            15: "Qual é a cor da banana madura?",
            16: "Qual(is) cor(es) são utilizadas para representar o Brasil?",
            17: "Qual cor a pele de uma pessoa com carotenemia fica?",
            18: "Que cor da flor de lavanda?",
            19: "Qual cor é formado com a mistura de vermelho e branco?",

            # Dates
            21: "Em que ano o Brasil foi descoberto?",
            22: "Em que ano o Brasil se tornou uma república?",
            23: "Em que ano ocorreu a Independência do Brasil?",
            24: "Em que ano aconteceu a Revolta da Vacina no Brasil?",
            25: "Em que ano foi assinado o Tratado de Petrópolis?",
            26: "Em que ano ocorreu a Guerra da Cisplatina?",
            27: "Em que ano ocorreu a Revolução da Chibata?",
            28: "Quando começou a Guerra do Paraguai?",
            29: "Em que ano foi firmado o Tratado de Tordesilhas?",

            # Locations
            30: "Qual é o maior país do mundo em território?",
            31: "Qual é a capital da Itália?",
            32: "Qual é o nome do maior deserto do mundo?",
            33: "Que continente abriga o Monte Everest?",
            34: "Qual é o nome da floresta tropical mais extensa do mundo?",
            35: "Qual é o país conhecido como 'terra do sol nascente'?",
            36: "Qual é o menor país do mundo?",
            37: "Que cidade é famosa por sua Torre Eiffel?",
            38: "Qual é a capital da Argentina?",
            39: "Que país tem uma ilha chamada Groenlândia?",

            # Objects
            40: "Que objeto usamos para medir o tempo?",
            41: "Que instrumento usamos para observar estrelas?",
            42: "Que objeto usamos para cortar papel?",
            43: "Que objeto usamos para armazenar dados digitalmente?",
            44: "Que objeto usamos para iluminar ambientes?",
            45: "Qual é o nome do objeto usado para proteger da chuva?",
            46: "Que objeto usamos para nos pentear?",
            47: "Que instrumento usamos para medir a temperatura?",
            48: "Que objeto usamos para servir chá?",
            49: "Que objeto usamos para abrir garrafas?",

            # Movies
            50: "Qual filme apresenta um robô chamado Wall-E?",
            51: "Qual é o nome do leão em 'O Rei Leão'?",
            52: "Que filme tem um bruxo chamado Harry Potter?",
            53: "Qual é o nome da princesa de gelo em 'Frozen'?",
            54: "Que filme apresenta um anel mágico e hobbits?",
            55: "Qual é o nome do dinossauro principal em 'Jurassic Park'?",
            56: "Que filme tem brinquedos que ganham vida?",
            57: "Qual é o nome do peixe que é procurado em 'Procurando Nemo'?",
            58: "Que filme conta a história de um guerreiro chamado Maximus?",
            59: "Qual é o nome do vilão principal em 'Vingadores: Guerra Infinita'?",

            # Sports
            60: "Qual esporte é jogado com uma bola oval?",
            61: "Qual esporte Michael Phelps se destacou?",
            62: "Que esporte usa um taco e uma bola pequena branca?",
            63: "Qual esporte é jogado em uma quadra com uma rede no meio?",
            64: "Qual foi o último esporte praticado por Usain Bolt na sua carreira?",
            65: "Qual esporte é jogado em uma piscina com uma bola?",
            66: "Que esporte inclui patins no gelo?",
            67: "Qual esporte utiliza um arco e flechas?",
            68: "Qual esporte é praticado com tacos e buracos no gramado?",
            69: "Que esporte inclui um ringue e luvas?",

            # Foods
            70: "Que fruta é famosa por ser rica em potássio?",
            71: "Qual é o ingrediente principal do sushi?",
            72: "Que queijo é usado em pizzas?",
            73: "Que alimento é produzido por abelhas?",
            74: "Que grão é a base de pão?",
            75: "Qual fruta é famosa por sua casca espinhosa?",
            76: "Qual é o prato típico da Itália feito com massa e molho?",
            77: "Que ingrediente é a base do guacamole?",
            78: "Que alimento é a principal fonte de cacau?",
            79: "Que carne é usada em um hambúrguer tradicional?"
        }

        self.__answers = {
            # Correct answers (0 a 79)
            # Animals
            0: "Baleia-azul", 1: "Falcão-peregrino", 2: "Albatroz", 3: "Camaleão", 4: "Ornitorrinco",
            5: "Crocodilo-de-água-salgada", 6: "Jacaré", 7: "Abelha", 8: "Tubarão-baleia", 9: "Preguiça",

            # Colors
            10: "Azul",11: "Verde", 12: "Preto", 13: "Vermelho", 14: "Branco",
            15: "Amarelo", 16: "Verde e Amarelo", 17: "Laranja ou Amarelo", 18: "Roxo", 19: "Rosa",

            # Dates
            20: "1669", 21: "1500", 22: "1889", 23: "1822", 24: "1904",
            25: "1903", 26: "1832", 27: "1910", 28: "1864", 29: "1494",

            # Locations
            30: "Rússia", 31: "Roma", 32: "Saara", 33: "Ásia", 34: "Amazônia",
            35: "Japão", 36: "Vaticano", 37: "Paris", 38: "Buenos Aires", 39: "Dinamarca",

            # Objects
            40: "Relógio", 41: "Telescópio", 42: "Tesoura", 43: "Pendrive", 44: "Lâmpada",
            45: "Guarda-chuva", 46: "Pente", 47: "Termômetro", 48: "Bule", 49: "Abridor",

            # Movies
            50: "Wall-E", 51: "Simba", 52: "Harry Potter", 53: "Elsa", 54: "Senhor dos Anéis",
            55: "T-Rex", 56: "Toy Story", 57: "Nemo", 58: "Gladiador", 59: "Thanos",

            # Sports
            60: "Futebol americano", 61: "Natação", 62: "Golfe", 63: "Tênis", 64: "Futebol",
            65: "Polo aquático", 66: "Patinação no gelo", 67: "Tiro com arco", 68: "Golfe", 69: "Boxe",

            # Food
            70: "Banana", 71: "Arroz", 72: "Mussarela", 73: "Mel", 74: "Trigo",
            75: "Durian", 76: "Pizza", 77: "Abacate", 78: "Cacau", 79: "Carne bovina",

            # False anwers (80 a 159)
            # Animals
            80: "Girafa", 81: "Leão-marinho", 82: "Pombo", 83: "Golfinho", 84: "Raposa",
            85: "Cobra", 86: "Gato", 87: "Vespa", 88: "Estrela-do-mar", 89: "Anta",

            # Colors
            90: "Preto e Branco", 91: "Marrom", 92: "Amarelo e azul", 93: "Cinza", 94: "Lilás",
            95: "Verde e vermelho", 96: "Azul claro", 97: "Dourado", 98: "Ciano", 99: "Prateado",

            # Dates
            100: "1501", 101: "1831", 102: "1922", 103: "1492", 104: "1905",
            105: "1879", 106: "1911", 107: "1770", 108: "1670", 109: "1764",

            # Locations
            110: "China", 111: "Londres", 112: "Gobi", 113: "África", 114: "Pantanal",
            115: "Coreia do Sul", 116: "Mônaco", 117: "Berlim", 118: "Lima", 119: "Noruega",

            # Objects
            120: "Relógio de sol", 121: "Microscópio", 122: "Faca", 123: "CD", 124: "Velas",
            125: "Capa de chuva", 126: "Escova", 127: "Barômetro", 128: "Chaleira", 129: "Saca-rolhas",

            # Movies
            130: "R2-D2", 131: "Nala", 132: "Hermione", 133: "Anna", 134: "Hobbit",
            135: "Velociraptor", 136: "Buzz Lightyear", 137: "Dory", 138: "César", 139: "Ultron",

            # Sports
            140: "Rugby", 141: "Certo ou Errado", 142: "Baseball", 143: "Vôlei", 144: "Canoagem",
            145: "Nado sincronizado", 146: "Hóquei no gelo", 147: "Dardos", 148: "Sinuca", 149: "Luta livre",

            # Food
            150: "Laranja", 151: "Salmão", 152: "Parmesão", 153: "Geléia", 154: "Cevada",
            155: "Jaca", 156: "Lasanha", 157: "Tomate", 158: "Chocolate", 159: "Carne suína"
        }

        # Types: 0 = Animals, 1 = Colors, 2 = Dates, 3 = Locations, 4 = Objects, 5 = Movies, 6 = Sports, 7 = Foods
        self.__categories_answers = {
            0: list( range( 0, 10 ) ) + list( range( 80, 90 ) ),  # Animals
            1: list( range( 10, 20 ) ) + list( range( 90, 100 ) ),  # Colors
            2: list( range( 20, 30 ) ) + list( range( 100, 110 ) ),  # Dates
            3: list( range( 30, 40 ) ) + list( range( 110, 120 ) ),  # Locations
            4: list( range( 40, 50 ) ) + list( range( 120, 130 ) ),  # Objects
            5: list( range( 50, 60 ) ) + list( range( 130, 140 ) ),  # Movies
            6: list( range( 60, 70 ) ) + list( range( 140, 150 ) ),  # Sports
            7: list( range( 70, 80 ) ) + list( range( 150, 160 ) ),  # Foods
        }

    @property
    def card(self):
        return self.__card

    @property
    def card_current_answers(self):
        return self.__card_current_answers

    @card_current_answers.setter
    def card_current_answers(self, card_current_answers):
        self.__card_current_answers = card_current_answers

    @property
    def questions(self):
        return self.__questions
