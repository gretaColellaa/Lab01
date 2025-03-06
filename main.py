import random


class Domanda:
    def __init__(self, testo, livello, risposta_corretta, risposte_errate):
        self.testo = testo
        self.livello = int(livello)
        self.risposta_corretta = risposta_corretta
        self.risposte = [risposta_corretta] + risposte_errate
        random.shuffle(self.risposte)

    def mostra_domanda(self):
        print(f"Livello {self.livello}) {self.testo}")
        for i, risposta in enumerate(self.risposte, 1):
            print(f"\t{i}. {risposta}")

    def verifica_risposta(self, scelta):
        return self.risposte[scelta - 1] == self.risposta_corretta


class Game:
    def __init__(self, file_domande, file_punteggi):
        self.file_domande = file_domande
        self.file_punteggi = file_punteggi
        self.domande = self.carica_domande()
        self.punteggi = self.carica_punteggi()
        self.livello_max = max(self.domande.keys())

    def carica_domande(self):
        domande = {}
        with open(self.file_domande, encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]

        for i in range(0, len(lines), 6):
            testo, livello, corretta, *errate = lines[i:i + 6]
            livello = int(livello)
            if livello not in domande:
                domande[livello] = []
            domande[livello].append(Domanda(testo, livello, corretta, errate))

        return domande

    def carica_punteggi(self):
        punteggi = []
        try:
            with open(self.file_punteggi, encoding='utf-8') as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) == 2 and parts[1].isdigit():
                        punteggi.append((parts[0], int(parts[1])))
        except FileNotFoundError:
            pass
        return punteggi

    def salva_punteggi(self, nickname, punti):
        self.punteggi.append((nickname, punti))
        self.punteggi.sort(key=lambda x: x[1], reverse=True)
        with open(self.file_punteggi, "w", encoding='utf-8') as f:
            for nome, score in self.punteggi:
                f.write(f"{nome} {score}\n")

    def inizia_gioco(self):
        livello = 0
        punteggio = 0

        while livello in self.domande:
            domanda = random.choice(self.domande[livello])
            domanda.mostra_domanda()

            try:
                risposta = int(input("Inserisci la risposta: "))
                if risposta < 1 or risposta > 4:
                    raise ValueError
            except ValueError:
                print("Input non valido! Inserisci un numero tra 1 e 4.")
                continue

            if domanda.verifica_risposta(risposta):
                print("Risposta corretta!\n")
                punteggio += 1
                livello += 1
            else:
                print(f"Risposta sbagliata! La risposta corretta era: {domanda.risposta_corretta}\n")
                break

        print(f"Hai totalizzato {punteggio} punti!")
        nickname = input("Inserisci il tuo nickname: ")
        self.salva_punteggi(nickname, punteggio)
        print("Classifica aggiornata!\n")


if __name__ == "__main__":
    gioco = Game("domande.txt", "punti.txt")
    gioco.inizia_gioco()
