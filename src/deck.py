
import random
from card import Card

import os


class Deck:
    def __init__(self):
        # All questions available. Key is id from question, value its description.
        self.__questions = {}
        # All answers available. Key is id from answers, value its description.
        self.__answers = {}
        # Key is the type of category, value is a list of answers from that category.
        self.__categories = {}
        # References question IDs with answer IDs.
        self.__questions_with_answers = {}
        # Object card that's created when a player interact with deck.
        self.__card = None
        # Function that create and sort all game data (questions, answers and their references).
        self.create_dicts()

    def create_card(self, controller):
        answers_card = {}

        # Get current questions
        questions_current_list = random.sample( list( self.__questions.keys() ), k=4 )
        questions_card = {key: self.__questions[key] for key in questions_current_list}

        # Create options for every question
        for question_key in questions_current_list:
            # Obter a resposta correta
            correct_answer_id = self.__questions_with_answers[question_key]
            correct_answer = self.__answers[correct_answer_id]
            # Determine the answer correct category
            category = None
            for cat_key, answer_ids in self.__categories.items():
                if correct_answer_id in answer_ids:
                    category = cat_key
                    break

            # Get answers from same category
            possible_answers_ids = self.__categories[category]

            # Select 3 false answers
            false_answers_ids = random.sample(
                [ans_id for ans_id in possible_answers_ids if ans_id != correct_answer_id], k=3 )
            false_answers = [self.__answers[ans_id] for ans_id in false_answers_ids]

            # Merge all answers
            all_answers = false_answers + [correct_answer]
            random.shuffle( all_answers )

            answers_card[question_key] = all_answers

        self.__card = Card(questions_card, answers_card)

        controller.draw_card(self.__card)

    def create_answers(self, key, controller):
        self.__card = Card( {key: self.__questions[key]}, self.__card.answers[key])
        controller.draw_card(self.__card, "answers")

    def check_answer(self, id_question, answer):
        correct_answer = self.__answers[self.__questions_with_answers[id_question]]

        if correct_answer == answer:
            return 1
        return -1

    def create_dicts(self):
        # Initial value
        questions = {
            0: 'Qual a cor do céu?',
            1: 'Qual a cor da luz que reflete todas as cores?',
            2: 'Qual a cor do sol?',
            3: 'Qual é a cor que representa elegância e luto?',
            4: 'Qual o país com o segundo maior número de habitantes? ',
            5: 'Qual a cor de uma flor de lavanda?',
            6: 'Qual é uma ave conhecida por seu bico grande e colorido?',
            7: 'Qual animal é famoso por andar de lado na praia?',
            8: 'Qual é o maior peixe brasileiro?',
            9: 'Qual animal é conhecido por suas listras?',
            10: 'Qual animal é considerado o melhor amigo do homem?',
            11: 'Qual é o maior animal marinho?',
            12: 'Qual é a cidade maravilhosa do Brasil?',
            13: 'Qual é um país que sofreu um grande terremoto em 2010?',
            14: 'Qual é o país do sol nascente?',
            15: 'Qual é a famosa montanha do Japão?',
            16: 'Qual é o ponto mais alto do Brasil?',
            17: 'Qual é o estado brasileiro que muitas pessoas dizem não existir?',
            18: 'Em que ano o Brasil foi descoberto?',
            19: 'Em que ano o Brasil se tornou uma república?',
            20: 'Em que ano ocorreu a independência do Brasil?',
            21: 'Em que ano aconteceu a revolta da vacina no Brasil?',
            22: 'Em que ano foi assinado o Tratado de Petrópolis?',
            23: 'Em que ano ocorreu a guerra da Cisplatina?'
        }

        self.__answers = {
            0: "Azul", 1: "Branco", 2: "Amarelo", 3: "Preto", 4: "Russia",  5: "Roxo",
            6: "Tucano", 7: "Caranguejo", 8: "Pirarucu", 9: "Zebra", 10: "Cachorro", 11: "Baleia",
            12: "Rio de Janeiro", 13: "Haiti", 14: "Japão", 15: "Monte Fuji", 16: "Pico da Neblina", 17: "Acre",
            18: "1500", 19: "1889", 20: "1822", 21: "1904", 22: "1903", 23: "1832",
            24: "Verde", 25: "Vermelho", 26: "Tubarão Baleia", 27: "Cinza", 28: "Chile", 29: "Rosa",
            30: "1700", 31: "Peru", 32: "1667", 33: "Santa Catarina", 34: "Itália", 35: "Jamaica",
            36: "1501", 37: "Beija-flor", 38: "Paraná", 39: "Laranja", 40: "Pato", 41: "Galinha",
            42: "Águia", 43: "Pombo", 44: "Tartaruga", 45: "Golfinho", 46: "Foca", 47: "Peixe",
            48: "Pinguim", 49: "Coruja", 50: "Gavião", 51: "Cavalo", 52: "Elefante", 53: "Gato",
            54: "Girafa", 55: "Papagaio", 56: "Hamster", 57: "Coelho", 58: "Golfinho", 59: "Tubarão",
            60: "Pinguim", 61: "Jacaré", 62: "São Paulo", 63: "Brasília", 64: "Salvador", 65: "Curitiba",
            66: "Cuba", 67: "República Dominicana", 68: "Jamaica", 69: "Porto Rico", 70: "China", 71: "Coreia do Sul",
            72: "Índia", 73: "Tailândia", 74: "Everest", 75: "Kilimanjaro", 76: "Mont Blanc", 77: "Monte Roraima",
            78: "Aconcágua", 79: "2000", 80: "K2", 81: "Pará", 82: "Amazonas", 83: "Rondônia",
            84: "Roraima", 85: "1800", 86: "1700", 87: "1600", 88: "1400", 89: "1989",
            90: "1789", 91: "1869", 92: "1900", 93: "1922", 94: "1722", 95: "1622",
            96: "2022", 97: "1804", 98: "2004", 99: "1704", 100: "1604", 101: "1803",
            102: "2003", 103: "1703", 104: "1603", 105: "1932", 106: "1732", 107: "1632", 108: "1532"
        }
        # Types: 0 = Colors, 1 = Animals, 2 = Locations, 3 = Dates
        self.__categories = {
            0: [0, 1, 2, 3, 5, 24, 25, 27, 29, 39],
            1: [6, 7, 8, 9, 10, 11, 26, 37, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58,
                59, 60, 61],
            2: [4, 12, 13, 14, 15, 16, 17, 28, 31, 33, 34, 35, 38, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74,
                75, 76, 77, 78, 80, 81, 82, 83, 84],
            3: [18, 19, 20, 21, 22, 23, 30, 32, 36, 79, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100,
                101, 102, 103, 104, 105, 106, 107, 108]
        }

        self.__questions_with_answers = {
            0: 0,  # Qual a cor do céu? -> Azul
            1: 1,  # Qual a cor da luz que reflete todas as cores? -> Branco
            2: 2,  # Qual a cor do sol? -> Amarelo
            3: 3,  # Qual é a cor que representa elegância e luto? -> Preto
            4: 72,  # Qual o país com o segundo maior número de habitantes?  -> Branco
            5: 5,  # Qual a cor de uma flor de lavanda? -> Roxo
            6: 6,  # Qual é uma ave conhecida por seu bico grande e colorido? -> Tucano
            7: 7,  # Qual animal é famoso por andar de lado na praia? -> Caranguejo
            8: 8,  # Qual ave é símbolo das florestas tropicais? -> Tucano
            9: 9,  # Qual animal é conhecido por suas listras? -> Zebra
            10: 10,  # Qual animal é considerado o melhor amigo do homem? -> Cachorro
            11: 11,  # Qual é o maior animal marinho? -> Baleia
            12: 12,  # Qual é a cidade maravilhosa do Brasil? -> Rio de Janeiro
            13: 13,  # Qual é um país que sofreu um grande terremoto em 2010? -> Haiti
            14: 14,  # Qual é o país do sol nascente? -> Japão
            15: 15,  # Qual é a famosa montanha do Japão? -> Monte Fuji
            16: 16,  # Qual é o ponto mais alto do Brasil? -> Pico da Neblina
            17: 17,  # Qual é um estado brasileiro que muitas pessoas dizem ser uma lenda? -> Acre
            18: 18,  # Em que ano o Brasil foi descoberto? -> 1500
            19: 19,  # Em que ano o Brasil se tornou uma república? -> 1889
            20: 20,  # Em que ano ocorreu a independência do Brasil? -> 1822
            21: 21,  # Em que ano aconteceu a revolta da vacina no Brasil? -> 1904
            22: 22,  # Em que ano foi assinado o Tratado de Petrópolis? -> 1903
            23: 23  # Em que ano ocorreu a guerra da Cisplatina? -> 1832
        }
        # Shuffle keys
        keys = list( questions.keys() )
        random.shuffle( keys )

        # Update dicts with shuffle values
        self.__questions = {new_key: questions[old_key] for new_key, old_key in enumerate( keys )}
        self.__questions_with_answers = {new_key: old_key for new_key, old_key in enumerate( keys )}
