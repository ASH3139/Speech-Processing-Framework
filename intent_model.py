import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense

# ═══════════════════════════════════════════════════════════
#  Multilingual Training Data
#  Languages: English, Hindi (romanised), Telugu (romanised), Spanish
#  The LSTM learns intent from keyword patterns across all 4 languages.
# ═══════════════════════════════════════════════════════════

data = []

# ─── AC ────────────────────────────────────────────────────
# English
for action in ["cool","warm","reduce","increase","set","lower","raise","change"]:
    for target in ["temperature","ac","air conditioning","temp","climate"]:
        data += [(f"{action} {target}", "AC"),
                 (f"{action} the {target}", "AC"),
                 (f"{action} car {target}", "AC")]
for t in range(16, 31):
    data += [(f"set temperature to {t}", "AC"),
             (f"set ac to {t}", "AC"),
             (f"temperature {t}", "AC"),
             (f"make it {t} degrees", "AC")]

# Hindi (romanised)
data += [
    ("temperature badao", "AC"), ("temperature kam karo", "AC"),
    ("ac chalao", "AC"), ("ac band karo", "AC"),
    ("thanda karo", "AC"), ("garam karo", "AC"),
    ("ac on karo", "AC"), ("ac off karo", "AC"),
    ("temperature set karo", "AC"), ("temperature badhao", "AC"),
    ("temperature ghataao", "AC"), ("temperature 22 karo", "AC"),
    ("ठंडा karo", "AC"), ("garam kar do", "AC"),
    ("ac theek karo", "AC"), ("climate control karo", "AC"),
]
for t in range(16, 31):
    data += [(f"temperature {t} karo", "AC"),
             (f"ac {t} pe set karo", "AC")]

# Telugu (romanised)
data += [
    ("temperature penchinchu", "AC"), ("temperature tagginchu", "AC"),
    ("ac pettinchu", "AC"), ("ac aapu", "AC"),
    ("chali cheyyi", "AC"), ("vennela cheyyi", "AC"),
    ("ac on cheyyi", "AC"), ("ac off cheyyi", "AC"),
    ("temperature set cheyyi", "AC"), ("ac adjust cheyyi", "AC"),
    ("guditam cheyyi", "AC"), ("temperature marchinchu", "AC"),
]
for t in range(16, 31):
    data += [(f"temperature {t} cheyyi", "AC"),
             (f"ac {t} ki set cheyyi", "AC")]

# Spanish
data += [
    ("pon la temperatura a", "AC"), ("sube la temperatura", "AC"),
    ("baja la temperatura", "AC"), ("enciende el aire", "AC"),
    ("apaga el aire", "AC"), ("ajusta el clima", "AC"),
    ("temperatura mas fria", "AC"), ("temperatura mas caliente", "AC"),
    ("aire acondicionado", "AC"), ("control de clima", "AC"),
    ("cambia la temperatura", "AC"), ("pon el ac", "AC"),
]
for t in range(16, 31):
    data += [(f"pon la temperatura a {t}", "AC"),
             (f"temperatura {t} grados", "AC")]


# ─── WINDOW ────────────────────────────────────────────────
# English
for action in ["open","close","lower","raise","roll down","roll up"]:
    for target in ["window","glass","driver window","passenger window","windows"]:
        data += [(f"{action} {target}", "WINDOW"),
                 (f"{action} the {target}", "WINDOW")]

# Hindi
data += [
    ("khidki kholo", "WINDOW"), ("khidki band karo", "WINDOW"),
    ("window kholo", "WINDOW"), ("window band karo", "WINDOW"),
    ("sheesha neeche karo", "WINDOW"), ("sheesha upar karo", "WINDOW"),
    ("window neeche kar", "WINDOW"), ("window upar kar", "WINDOW"),
    ("khidki uthao", "WINDOW"), ("khidki girayo", "WINDOW"),
    ("glass kholo", "WINDOW"), ("glass band karo", "WINDOW"),
]

# Telugu
data += [
    ("kiddiki teruvu", "WINDOW"), ("kiddiki muyyi", "WINDOW"),
    ("window teruvu", "WINDOW"), ("window close cheyyi", "WINDOW"),
    ("kiddiki kindiki cheyyi", "WINDOW"), ("kiddiki paikki cheyyi", "WINDOW"),
    ("window open cheyyi", "WINDOW"), ("window band cheyyi", "WINDOW"),
    ("abba teruvu", "WINDOW"), ("abba muyyi", "WINDOW"),
]

# Spanish
data += [
    ("abre la ventana", "WINDOW"), ("cierra la ventana", "WINDOW"),
    ("baja la ventana", "WINDOW"), ("sube la ventana", "WINDOW"),
    ("abre el vidrio", "WINDOW"), ("cierra el vidrio", "WINDOW"),
    ("ventana abajo", "WINDOW"), ("ventana arriba", "WINDOW"),
    ("baja el cristal", "WINDOW"), ("sube el cristal", "WINDOW"),
]


# ─── MEDIA ─────────────────────────────────────────────────
# English
for action in ["play","stop","start","pause","resume","next","previous"]:
    for target in ["music","radio","songs","audio","song"]:
        data.append((f"{action} {target}", "MEDIA"))
data += [("play", "MEDIA"), ("stop the music", "MEDIA"),
         ("next song", "MEDIA"), ("previous song", "MEDIA")]

# Hindi
data += [
    ("gaana bajao", "MEDIA"), ("music bajao", "MEDIA"),
    ("gaana band karo", "MEDIA"), ("music band karo", "MEDIA"),
    ("gaana chalao", "MEDIA"), ("radio chalao", "MEDIA"),
    ("agle gaane pe jao", "MEDIA"), ("pause karo", "MEDIA"),
    ("music rok do", "MEDIA"), ("gaana shuru karo", "MEDIA"),
    ("volume badhao", "MEDIA"), ("volume kam karo", "MEDIA"),
]

# Telugu
data += [
    ("paata veyyi", "MEDIA"), ("music veyyi", "MEDIA"),
    ("paata aapu", "MEDIA"), ("music aapu", "MEDIA"),
    ("radio veyyi", "MEDIA"), ("gaana pettinchu", "MEDIA"),
    ("music start cheyyi", "MEDIA"), ("paata start cheyyi", "MEDIA"),
    ("tarvata paata", "MEDIA"), ("pause cheyyi", "MEDIA"),
]

# Spanish
data += [
    ("pon musica", "MEDIA"), ("reproduce musica", "MEDIA"),
    ("para la musica", "MEDIA"), ("detener musica", "MEDIA"),
    ("siguiente cancion", "MEDIA"), ("cancion anterior", "MEDIA"),
    ("pon el radio", "MEDIA"), ("pausa la musica", "MEDIA"),
    ("sube el volumen", "MEDIA"), ("baja el volumen", "MEDIA"),
]


# ─── NAVIGATION ────────────────────────────────────────────
places = ["home","office","hospital","school","mall","airport",
          "ghar","aspatal","daftar","school","bazar",
          "illu","hospital","office","school","shopping mall",
          "casa","hospital","oficina","escuela","aeropuerto","centro comercial"]

# English
for place in ["home","office","hospital","school","mall","airport"]:
    data += [(f"navigate to {place}", "NAVIGATION"),
             (f"go to {place}", "NAVIGATION"),
             (f"take me to {place}", "NAVIGATION"),
             (f"drive to {place}", "NAVIGATION"),
             (f"directions to {place}", "NAVIGATION"),
             (f"find {place}", "NAVIGATION")]

# Hindi
data += [
    ("ghar chalo", "NAVIGATION"), ("ghar le chalo", "NAVIGATION"),
    ("aspatal chalo", "NAVIGATION"), ("daftar chalo", "NAVIGATION"),
    ("navigate karo", "NAVIGATION"), ("rasta dikhao", "NAVIGATION"),
    ("school le jao", "NAVIGATION"), ("airport le jao", "NAVIGATION"),
    ("mall chalo", "NAVIGATION"), ("wahan le chalo", "NAVIGATION"),
    ("idhar chalo", "NAVIGATION"), ("mujhe le chalo", "NAVIGATION"),
]

# Telugu
data += [
    ("illu ki vellu", "NAVIGATION"), ("intiki teesuko", "NAVIGATION"),
    ("hospital ki vellu", "NAVIGATION"), ("office ki vellu", "NAVIGATION"),
    ("navigate cheyyi", "NAVIGATION"), ("daari chupinchu", "NAVIGATION"),
    ("school ki vellu", "NAVIGATION"), ("airport ki vellu", "NAVIGATION"),
    ("mall ki vellu", "NAVIGATION"), ("akkaḍiki vellu", "NAVIGATION"),
]

# Spanish
data += [
    ("navega a casa", "NAVIGATION"), ("llevame a casa", "NAVIGATION"),
    ("ir al hospital", "NAVIGATION"), ("ir a la oficina", "NAVIGATION"),
    ("navegar a", "NAVIGATION"), ("como llego a", "NAVIGATION"),
    ("llevame al aeropuerto", "NAVIGATION"), ("ir al centro comercial", "NAVIGATION"),
    ("direcciones a", "NAVIGATION"), ("llévame a", "NAVIGATION"),
]


# ─── CALL ──────────────────────────────────────────────────
contacts = ["mom","mum","mother","dad","brother","sister","friend",
            "maa","bhai","behen","papa","dost",
            "amma","nanna","anna","akka","snehithudu",
            "mama","papa","hermano","hermana","amigo","amiga"]

# English
for contact in ["mom","mum","mother","dad","brother","sister","friend"]:
    data += [(f"call {contact}", "CALL"),
             (f"dial {contact}", "CALL"),
             (f"call my {contact}", "CALL"),
             (f"phone {contact}", "CALL")]

# Hindi
data += [
    ("maa ko call karo", "CALL"), ("papa ko call karo", "CALL"),
    ("bhai ko call karo", "CALL"), ("behen ko call karo", "CALL"),
    ("dost ko call karo", "CALL"), ("call karo", "CALL"),
    ("phone karo", "CALL"), ("maa ko phone karo", "CALL"),
    ("call lagao", "CALL"), ("phone milao", "CALL"),
]

# Telugu
data += [
    ("amma ki call cheyyi", "CALL"), ("nanna ki call cheyyi", "CALL"),
    ("anna ki call cheyyi", "CALL"), ("akka ki call cheyyi", "CALL"),
    ("snehithuniki call cheyyi", "CALL"), ("phone cheyyi", "CALL"),
    ("call cheyyi", "CALL"), ("dial cheyyi", "CALL"),
]

# Spanish
data += [
    ("llama a mama", "CALL"), ("llama a papa", "CALL"),
    ("llama a mi hermano", "CALL"), ("llama a mi hermana", "CALL"),
    ("llama a mi amigo", "CALL"), ("hacer una llamada", "CALL"),
    ("llamar a", "CALL"), ("marcar", "CALL"),
    ("telefona a", "CALL"), ("llama a", "CALL"),
]


# ═══════════════════════════════════════════════════════════
#  Build + Train Model
# ═══════════════════════════════════════════════════════════
sentences = [x[0] for x in data]
labels    = [x[1] for x in data]

tokenizer = Tokenizer()
tokenizer.fit_on_texts(sentences)

X = tokenizer.texts_to_sequences(sentences)
X = pad_sequences(X)

label_map   = {label: i for i, label in enumerate(set(labels))}
reverse_map = {i: label for label, i in label_map.items()}
y = np.array([label_map[l] for l in labels])

model = Sequential([
    Embedding(5000, 128),
    LSTM(128),
    Dense(len(label_map), activation='softmax')
])

model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(X, y, epochs=200, verbose=0)

print(f"[SPF] Intent model trained on {len(data)} multilingual samples")


def predict_intent(text):
    seq = tokenizer.texts_to_sequences([text])
    seq = pad_sequences(seq, maxlen=X.shape[1])
    pred = model.predict(seq, verbose=0)
    return reverse_map[np.argmax(pred)]
