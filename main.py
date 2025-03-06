import random


class Domanda:
    def __init__(self, testo, livello, risposta_corretta, risposte_errate):
        self.testo = testo
        self.livello = int(livello)
        self.risposta_corretta = risposta_corretta
        self.risposte = [risposta_corretta] + risposte_errate
        random.shuffle(self.risposte) #le mette in disordine già il costruttore

    def mostra_domanda(self):                                   #enumerate(self.risposte, 1) genera coppie (indice, risposta), partendo da 1.
            print(f"Livello {self.livello}) {self.testo}")      #Il \t (tabulazione) rende la formattazione più leggibile.
            for i, risposta in enumerate(self.risposte, 1):     #Le risposte sono già mescolate casualmente nel costruttore (__init__).
                print(f"\t{i}. {risposta}")

    def verifica_risposta(self, scelta):
        return self.risposte[scelta - 1] == self.risposta_corretta #return true se corretta


class Game:
    def __init__(self, file_domande, file_punteggi):
        self.file_domande = file_domande
        self.file_punteggi = file_punteggi
        self.domande = self.carica_domande()
        self.punteggi = self.carica_punteggi()
        self.livello_max = max(self.domande.keys())

    def carica_domande(self):
        domande = {}
        with open(self.file_domande, encoding='utf-8') as f:                            # open(self.file_domande, encoding='utf-8') apre il file di testo in modalità lettura (r di default).
                                                                                        #encoding='utf-8' garantisce che il file venga letto correttamente, evitando problemi con caratteri speciali (come accenti é, à, ò).
                                                                                        #with open(...) as f: assicura che il file venga chiuso automaticamente alla fine, anche in caso di errori.

            lines = [line.strip() for line in f.readlines() if line.strip()]            #f.readlines() legge tutte le righe del file e le restituisce come una lista.
                                                                                        #line.strip() rimuove eventuali spazi o caratteri di nuova linea (\n) all’inizio e alla fine di ogni riga.
                                                                                        #if line.strip() esclude le righe vuote. Se line.strip() restituisce una stringa vuota (""), quella riga non viene inclusa nella lista.

        for i in range(0, len(lines), 6):
            testo, livello, corretta, *errate = lines[i:i + 6]
            livello = int(livello)
            if livello not in domande:                                                  #domande è un dizionario con chiavi = livelli di difficoltà e valori = liste di domande per quel livello.
                                                                                        #Se il livello non è ancora nel dizionario, viene aggiunto con una lista vuota.

                domande[livello] = []
            domande[livello].append(Domanda(testo, livello, corretta, errate))

        return domande

    def carica_punteggi(self):
        punteggi = []
        try:
            with open(self.file_punteggi, encoding='utf-8') as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) == 2 and parts[1].isdigit():              #parts[1].isdigit() verifica che il secondo valore sia composto solo da cifre (0-9), evitando errori nel cast a int.
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
            domanda = random.choice(self.domande[livello]) #prende una domanda a caso dal dizionario domande nella lisat di domande del livello chiesto
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
