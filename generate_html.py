import requests
from bs4 import BeautifulSoup

# generate_html.py
joueurs = {
    "Joueur1": 100,
    "Joueur2": 95,
    "Joueur3": 87
}

# Génération du HTML
html = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Classement LoL</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; }
        table { border-collapse: collapse; width: 50%; margin: auto; }
        th, td { border: 1px solid #ddd; padding: 10px; text-align: center; }
        th { background-color: #f4f4f4; }
    </style>
</head>
<body>
    <h1 style="text-align:center;">Classement LoL</h1>
    <table>
        <tr><th>Joueur</th><th>Points</th></tr>
"""

for joueur, points in sorted(joueurs.items(), key=lambda x: x[1], reverse=True):
    html += f"<tr><td>{joueur}</td><td>{points}</td></tr>\n"

html += """
    </table>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Fichier HTML généré : index.html")


# Base URL des icônes
icon_base_url = "https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/"

# Rang → ID icône (numérique)
icons = {
    "iron": 0,
    "bronze": 1,
    "silver": 2,
    "gold": 3,
    "platinum": 4,
    "emerald": 6,
    "diamond": 7,
    "master": 8,
    "grandmaster": 9,
    "challenger": 10
}

def get_icon(rank):
    rank_lower = rank.lower().split()[0]  # Ex: "emerald 4" → "emerald"
    icon_id = icons.get(rank_lower)
    if icon_id is not None:
        return f"{icon_base_url}{icon_id}.png?v=9"
    return f"{icon_base_url}0.png?v=9"  # Par défaut: Iron

def get_rank(full_pseudo):
    pseudo_opgg = full_pseudo.replace('#', '-')
    url = f"https://op.gg/de/lol/summoners/euw/{pseudo_opgg}"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        return None

    soup = BeautifulSoup(r.text, 'html.parser')

    meta_desc = soup.find("meta", attrs={"name": "description"})
    if not meta_desc:
        return "Unranked"

    content = meta_desc.get("content", "")
    parts = content.split(" / ")
    if len(parts) > 1:
        rank_info = parts[1].strip()  # Ex: "Emerald 4 38LP"
        words = rank_info.split()
        if len(words) >= 2:
            cleaned_rank = f"{words[0]} {words[1]}"  # "Emerald 4"
            return cleaned_rank
        else:
            return rank_info

    return "Unranked"

def main():
    print("Récupération des rangs...")

    with open("joueurs.txt", "r", encoding="utf-8") as f:
        joueurs = [line.strip() for line in f if line.strip()]

    classement = []
    for j in joueurs:
        print(f" - {j}")
        rank = get_rank(j)
        classement.append((j, rank if rank else "Erreur"))

    # Tri simple (ordre du plus fort au plus faible)
    ordre = ["challenger", "grandmaster", "master", "diamond", "platinum", "emerald", "gold", "silver", "bronze", "iron", "unranked"]
    
    def rang_index(rank):
        for i, o in enumerate(ordre):
            if o in rank.lower():
                return i
        return len(ordre)

    classement.sort(key=lambda x: rang_index(x[1]))

    # Générer le HTML
    html_header = """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
    <meta charset="UTF-8" />
    <title>Classement League of Legends</title>
    <style>
               body {
            background-image: url('background.jpg');
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            color: #c9d1d9;
            font-family: Arial, sans-serif;
            padding: 20px;
        }

        h1 {
            text-align: center;
        }
       .player {
    background-color: rgba(22, 27, 34, 0.85);  /* même couleur, mais avec transparence */
    margin: 10px 0;
    padding: 15px;
    border-radius: 10px;
    display: flex;
    align-items: center;
}

        .icon {
            width: 50px;
            height: 50px;
            margin-right: 15px;
        }
        .pseudo {
            font-weight: bold;
            margin-right: 10px;
        }
        .rank {
            font-style: italic;
            color: #8b949e;
        }
    </style>
    </head>
    <body>
    <h1>Classement League of Legends</h1>
    """

    html_body = ""
    for pseudo, rank in classement:
        icon_url = get_icon(rank)
        html_body += f"""
        <div class="player">
            <img src="{icon_url}" alt="{rank}" class="icon" />
            <span class="pseudo">{pseudo}</span>
            <span class="rank">{rank}</span>
        </div>
        """

    html_footer = """
    </body>
<div id="embedim--snow">
  <style>
    /<div 
<div id="embedim--snow">
  <style>
    #embedim--snow {
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      pointer-events: none;
      overflow: hidden;
      z-index: 9999999;
    }

    .embedim-snow {
      position: absolute;
      width: 10px;
      height: 10px;
      background: white;
      border-radius: 50%;
      top: -10px; /* Positionne chaque flocon en haut */
    }

    .embedim-snow:nth-child(1) {
      opacity: 0.46;
      left: 48.23vw;
      animation: fall-1 10s linear infinite;
      transform: scale(0.57);
    }

    @keyframes fall-1 {
      0% {
        transform: translateY(0vh) scale(0.57);
      }
      100% {
        transform: translateY(110vh) scale(0.57);
      }
    }

    .embedim-snow:nth-child(2) {
      opacity: 0.79;
      left: 29.40vw;
      animation: fall-2 30s linear infinite;
      transform: scale(0.85);
    }

    @keyframes fall-2 {
      0% {
        transform: translateY(0vh) scale(0.85);
      }
      100% {
        transform: translateY(110vh) scale(0.85);
      }
    }
;animation:fall-1 10s -30s linear infinite}@keyframes fall-1{40.00%{transform:translate(55.99vw,40.00vh) scale(0.57)}to{transform:translate(52.11vw, 105vh) scale(0.57)}}.embedim-snow:nth-child(2){opacity:0.79;transform:translate(29.40vw,-10px) scale(0.85);animation:fall-2 30s -28s linear infinite}@keyframes fall-2{50.00%{transform:translate(30.50vw,50.00vh) scale(0.85)}to{transform:translate(29.95vw, 105vh) scale(0.85)}}.embedim-snow:nth-child(3){opacity:0.33;transform:translate(64.75vw,-10px) scale(0.97);animation:fall-3 10s -7s linear infinite}@keyframes fall-3{50.00%{transform:translate(65.01vw,50.00vh) scale(0.97)}to{transform:translate(64.88vw, 105vh) scale(0.97)}}.embedim-snow:nth-child(4){opacity:0.07;transform:translate(60.61vw,-10px) scale(0.60);animation:fall-4 21s -23s linear infinite}@keyframes fall-4{70.00%{transform:translate(58.26vw,70.00vh) scale(0.60)}to{transform:translate(59.44vw, 105vh) scale(0.60)}}.embedim-snow:nth-child(5){opacity:0.94;transform:translate(49.53vw,-10px) scale(0.84);animation:fall-5 11s -9s linear infinite}@keyframes fall-5{60.00%{transform:translate(53.74vw,60.00vh) scale(0.84)}to{transform:translate(51.64vw, 105vh) scale(0.84)}}.embedim-snow:nth-child(6){opacity:0.95;transform:translate(8.69vw,-10px) scale(0.50);animation:fall-6 16s -29s linear infinite}@keyframes fall-6{80.00%{transform:translate(-1.21vw,80.00vh) scale(0.50)}to{transform:translate(3.74vw, 105vh) scale(0.50)}}.embedim-snow:nth-child(7){opacity:0.34;transform:translate(96.73vw,-10px) scale(0.26);animation:fall-7 30s -7s linear infinite}@keyframes fall-7{40.00%{transform:translate(94.47vw,40.00vh) scale(0.26)}to{transform:translate(95.60vw, 105vh) scale(0.26)}}.embedim-snow:nth-child(8){opacity:0.36;transform:translate(45.90vw,-10px) scale(0.26);animation:fall-8 29s -16s linear infinite}@keyframes fall-8{60.00%{transform:translate(43.61vw,60.00vh) scale(0.26)}to{transform:translate(44.76vw, 105vh) scale(0.26)}}.embedim-snow:nth-child(9){opacity:0.71;transform:translate(90.97vw,-10px) scale(0.27);animation:fall-9 15s -27s linear infinite}@keyframes fall-9{70.00%{transform:translate(92.23vw,70.00vh) scale(0.27)}to{transform:translate(91.60vw, 105vh) scale(0.27)}}.embedim-snow:nth-child(10){opacity:0.04;transform:translate(82.71vw,-10px) scale(0.57);animation:fall-10 22s -30s linear infinite}@keyframes fall-10{50.00%{transform:translate(92.21vw,50.00vh) scale(0.57)}to{transform:translate(87.46vw, 105vh) scale(0.57)}}.embedim-snow:nth-child(11){opacity:0.58;transform:translate(40.97vw,-10px) scale(0.82);animation:fall-11 21s -19s linear infinite}@keyframes fall-11{80.00%{transform:translate(36.38vw,80.00vh) scale(0.82)}to{transform:translate(38.68vw, 105vh) scale(0.82)}}.embedim-snow:nth-child(12){opacity:0.16;transform:translate(87.88vw,-10px) scale(0.24);animation:fall-12 30s -21s linear infinite}@keyframes fall-12{80.00%{transform:translate(90.90vw,80.00vh) scale(0.24)}to{transform:translate(89.39vw, 105vh) scale(0.24)}}.embedim-snow:nth-child(13){opacity:0.88;transform:translate(46.21vw,-10px) scale(0.79);animation:fall-13 26s -20s linear infinite}@keyframes fall-13{80.00%{transform:translate(49.89vw,80.00vh) scale(0.79)}to{transform:translate(48.05vw, 105vh) scale(0.79)}}.embedim-snow:nth-child(14){opacity:0.68;transform:translate(98.19vw,-10px) scale(0.52);animation:fall-14 13s -1s linear infinite}@keyframes fall-14{50.00%{transform:translate(90.82vw,50.00vh) scale(0.52)}to{transform:translate(94.50vw, 105vh) scale(0.52)}}.embedim-snow:nth-child(15){opacity:0.48;transform:translate(72.37vw,-10px) scale(0.66);animation:fall-15 19s -4s linear infinite}@keyframes fall-15{70.00%{transform:translate(81.00vw,70.00vh) scale(0.66)}to{transform:translate(76.68vw, 105vh) scale(0.66)}}.embedim-snow:nth-child(16){opacity:0.17;transform:translate(46.12vw,-10px) scale(0.81);animation:fall-16 21s -17s linear infinite}@keyframes fall-16{30.00%{transform:translate(51.70vw,30.00vh) scale(0.81)}to{transform:translate(48.91vw, 105vh) scale(0.81)}}.embedim-snow:nth-child(17){opacity:0.23;transform:translate(5.71vw,-10px) scale(0.77);animation:fall-17 19s -7s linear infinite}@keyframes fall-17{60.00%{transform:translate(12.20vw,60.00vh) scale(0.77)}to{transform:translate(8.96vw, 105vh) scale(0.77)}}.embedim-snow:nth-child(18){opacity:0.37;transform:translate(19.46vw,-10px) scale(0.83);animation:fall-18 22s -25s linear infinite}@keyframes fall-18{60.00%{transform:translate(10.70vw,60.00vh) scale(0.83)}to{transform:translate(15.08vw, 105vh) scale(0.83)}}.embedim-snow:nth-child(19){opacity:0.32;transform:translate(7.30vw,-10px) scale(0.64);animation:fall-19 11s -0s linear infinite}@keyframes fall-19{30.00%{transform:translate(12.58vw,30.00vh) scale(0.64)}to{transform:translate(9.94vw, 105vh) scale(0.64)}}.embedim-snow:nth-child(20){opacity:0.35;transform:translate(21.39vw,-10px) scale(0.42);animation:fall-20 26s -17s linear infinite}@keyframes fall-20{70.00%{transform:translate(23.48vw,70.00vh) scale(0.42)}to{transform:translate(22.43vw, 105vh) scale(0.42)}}.embedim-snow:nth-child(21){opacity:0.00;transform:translate(52.73vw,-10px) scale(0.14);animation:fall-21 14s -21s linear infinite}@keyframes fall-21{60.00%{transform:translate(54.78vw,60.00vh) scale(0.14)}to{transform:translate(53.76vw, 105vh) scale(0.14)}}.embedim-snow:nth-child(22){opacity:0.94;transform:translate(38.89vw,-10px) scale(0.89);animation:fall-22 21s -8s linear infinite}@keyframes fall-22{30.00%{transform:translate(36.04vw,30.00vh) scale(0.89)}to{transform:translate(37.46vw, 105vh) scale(0.89)}}.embedim-snow:nth-child(23){opacity:0.93;transform:translate(97.70vw,-10px) scale(0.53);animation:fall-23 23s -18s linear infinite}@keyframes fall-23{40.00%{transform:translate(91.21vw,40.00vh) scale(0.53)}to{transform:translate(94.45vw, 105vh) scale(0.53)}}.embedim-snow:nth-child(24){opacity:0.23;transform:translate(38.65vw,-10px) scale(0.50);animation:fall-24 12s -7s linear infinite}@keyframes fall-24{40.00%{transform:translate(38.52vw,40.00vh) scale(0.50)}to{transform:translate(38.59vw, 105vh) scale(0.50)}}.embedim-snow:nth-child(25){opacity:0.35;transform:translate(21.19vw,-10px) scale(0.17);animation:fall-25 28s -18s linear infinite}@keyframes fall-25{80.00%{transform:translate(12.03vw,80.00vh) scale(0.17)}to{transform:translate(16.61vw, 105vh) scale(0.17)}}.embedim-snow:nth-child(26){opacity:0.86;transform:translate(83.26vw,-10px) scale(0.56);animation:fall-26 25s -12s linear infinite}@keyframes fall-26{50.00%{transform:translate(75.55vw,50.00vh) scale(0.56)}to{transform:translate(79.40vw, 105vh) scale(0.56)}}.embedim-snow:nth-child(27){opacity:0.08;transform:translate(7.39vw,-10px) scale(0.01);animation:fall-27 22s -11s linear infinite}@keyframes fall-27{40.00%{transform:translate(11.22vw,40.00vh) scale(0.01)}to{transform:translate(9.30vw, 105vh) scale(0.01)}}.embedim-snow:nth-child(28){opacity:0.17;transform:translate(28.07vw,-10px) scale(0.10);animation:fall-28 27s -24s linear infinite}@keyframes fall-28{50.00%{transform:translate(33.88vw,50.00vh) scale(0.10)}to{transform:translate(30.98vw, 105vh) scale(0.10)}}.embedim-snow:nth-child(29){opacity:0.35;transform:translate(8.42vw,-10px) scale(0.68);animation:fall-29 17s -12s linear infinite}@keyframes fall-29{40.00%{transform:translate(8.67vw,40.00vh) scale(0.68)}to{transform:translate(8.54vw, 105vh) scale(0.68)}}.embedim-snow:nth-child(30){opacity:0.57;transform:translate(20.00vw,-10px) scale(0.91);animation:fall-30 20s -22s linear infinite}@keyframes fall-30{60.00%{transform:translate(18.79vw,60.00vh) scale(0.91)}to{transform:translate(19.40vw, 105vh) scale(0.91)}}.embedim-snow:nth-child(31){opacity:0.36;transform:translate(50.67vw,-10px) scale(0.82);animation:fall-31 30s -2s linear infinite}@keyframes fall-31{30.00%{transform:translate(59.61vw,30.00vh) scale(0.82)}to{transform:translate(55.14vw, 105vh) scale(0.82)}}.embedim-snow:nth-child(32){opacity:0.86;transform:translate(69.27vw,-10px) scale(0.21);animation:fall-32 15s -27s linear infinite}@keyframes fall-32{70.00%{transform:translate(72.19vw,70.00vh) scale(0.21)}to{transform:translate(70.73vw, 105vh) scale(0.21)}}.embedim-snow:nth-child(33){opacity:0.33;transform:translate(57.98vw,-10px) scale(0.39);animation:fall-33 30s -6s linear infinite}@keyframes fall-33{50.00%{transform:translate(57.13vw,50.00vh) scale(0.39)}to{transform:translate(57.55vw, 105vh) scale(0.39)}}.embedim-snow:nth-child(34){opacity:0.11;transform:translate(34.89vw,-10px) scale(0.36);animation:fall-34 24s -16s linear infinite}@keyframes fall-34{40.00%{transform:translate(28.40vw,40.00vh) scale(0.36)}to{transform:translate(31.65vw, 105vh) scale(0.36)}}.embedim-snow:nth-child(35){opacity:0.12;transform:translate(39.04vw,-10px) scale(0.41);animation:fall-35 15s -30s linear infinite}@keyframes fall-35{60.00%{transform:translate(35.77vw,60.00vh) scale(0.41)}to{transform:translate(37.40vw, 105vh) scale(0.41)}}.embedim-snow:nth-child(36){opacity:0.08;transform:translate(62.98vw,-10px) scale(0.52);animation:fall-36 12s -25s linear infinite}@keyframes fall-36{50.00%{transform:translate(66.53vw,50.00vh) scale(0.52)}to{transform:translate(64.76vw, 105vh) scale(0.52)}}.embedim-snow:nth-child(37){opacity:0.96;transform:translate(65.16vw,-10px) scale(0.06);animation:fall-37 14s -4s linear infinite}@keyframes fall-37{50.00%{transform:translate(57.25vw,50.00vh) scale(0.06)}to{transform:translate(61.20vw, 105vh) scale(0.06)}}.embedim-snow:nth-child(38){opacity:0.46;transform:translate(96.98vw,-10px) scale(0.64);animation:fall-38 28s -30s linear infinite}@keyframes fall-38{40.00%{transform:translate(97.05vw,40.00vh) scale(0.64)}to{transform:translate(97.02vw, 105vh) scale(0.64)}}.embedim-snow:nth-child(39){opacity:0.44;transform:translate(43.77vw,-10px) scale(0.87);animation:fall-39 11s -9s linear infinite}@keyframes fall-39{50.00%{transform:translate(45.92vw,50.00vh) scale(0.87)}to{transform:translate(44.84vw, 105vh) scale(0.87)}}.embedim-snow:nth-child(40){opacity:0.83;transform:translate(46.37vw,-10px) scale(0.15);animation:fall-40 22s -12s linear infinite}@keyframes fall-40{40.00%{transform:translate(48.51vw,40.00vh) scale(0.15)}to{transform:translate(47.44vw, 105vh) scale(0.15)}}.embedim-snow:nth-child(41){opacity:0.66;transform:translate(68.59vw,-10px) scale(0.23);animation:fall-41 21s -6s linear infinite}@keyframes fall-41{70.00%{transform:translate(71.55vw,70.00vh) scale(0.23)}to{transform:translate(70.07vw, 105vh) scale(0.23)}}.embedim-snow:nth-child(42){opacity:0.94;transform:translate(8.28vw,-10px) scale(0.49);animation:fall-42 22s -7s linear infinite}@keyframes fall-42{80.00%{transform:translate(4.31vw,80.00vh) scale(0.49)}to{transform:translate(6.29vw, 105vh) scale(0.49)}}.embedim-snow:nth-child(43){opacity:0.40;transform:translate(4.22vw,-10px) scale(0.71);animation:fall-43 14s -30s linear infinite}@keyframes fall-43{60.00%{transform:translate(13.12vw,60.00vh) scale(0.71)}to{transform:translate(8.67vw, 105vh) scale(0.71)}}.embedim-snow:nth-child(44){opacity:0.94;transform:translate(73.91vw,-10px) scale(0.38);animation:fall-44 21s -23s linear infinite}@keyframes fall-44{80.00%{transform:translate(75.36vw,80.00vh) scale(0.38)}to{transform:translate(74.64vw, 105vh) scale(0.38)}}.embedim-snow:nth-child(45){opacity:0.12;transform:translate(94.47vw,-10px) scale(0.17);animation:fall-45 13s -16s linear infinite}@keyframes fall-45{80.00%{transform:translate(102.84vw,80.00vh) scale(0.17)}to{transform:translate(98.66vw, 105vh) scale(0.17)}}.embedim-snow:nth-child(46){opacity:0.58;transform:translate(62.20vw,-10px) scale(0.56);animation:fall-46 13s -27s linear infinite}@keyframes fall-46{70.00%{transform:translate(53.20vw,70.00vh) scale(0.56)}to{transform:translate(57.70vw, 105vh) scale(0.56)}}.embedim-snow:nth-child(47){opacity:0.73;transform:translate(82.51vw,-10px) scale(0.14);animation:fall-47 19s -13s linear infinite}@keyframes fall-47{40.00%{transform:translate(83.83vw,40.00vh) scale(0.14)}to{transform:translate(83.17vw, 105vh) scale(0.14)}}.embedim-snow:nth-child(48){opacity:0.39;transform:translate(53.71vw,-10px) scale(0.66);animation:fall-48 29s -20s linear infinite}@keyframes fall-48{80.00%{transform:translate(57.78vw,80.00vh) scale(0.66)}to{transform:translate(55.74vw, 105vh) scale(0.66)}}.embedim-snow:nth-child(49){opacity:0.64;transform:translate(42.58vw,-10px) scale(0.05);animation:fall-49 21s -20s linear infinite}@keyframes fall-49{60.00%{transform:translate(40.96vw,60.00vh) scale(0.05)}to{transform:translate(41.77vw, 105vh) scale(0.05)}}.embedim-snow:nth-child(50){opacity:0.25;transform:translate(21.24vw,-10px) scale(0.66);animation:fall-50 26s -17s linear infinite}@keyframes fall-50{50.00%{transform:translate(16.82vw,50.00vh) scale(0.66)}to{transform:translate(19.03vw, 105vh) scale(0.66)}}.embedim-snow:nth-child(51){opacity:0.15;transform:translate(48.16vw,-10px) scale(0.03);animation:fall-51 27s -11s linear infinite}@keyframes fall-51{40.00%{transform:translate(44.90vw,40.00vh) scale(0.03)}to{transform:translate(46.53vw, 105vh) scale(0.03)}}.embedim-snow:nth-child(52){opacity:0.53;transform:translate(55.78vw,-10px) scale(0.17);animation:fall-52 10s -23s linear infinite}@keyframes fall-52{50.00%{transform:translate(56.56vw,50.00vh) scale(0.17)}to{transform:translate(56.17vw, 105vh) scale(0.17)}}.embedim-snow:nth-child(53){opacity:0.56;transform:translate(38.22vw,-10px) scale(0.52);animation:fall-53 26s -18s linear infinite}@keyframes fall-53{80.00%{transform:translate(33.61vw,80.00vh) scale(0.52)}to{transform:translate(35.92vw, 105vh) scale(0.52)}}.embedim-snow:nth-child(54){opacity:0.77;transform:translate(2.96vw,-10px) scale(0.80);animation:fall-54 28s -18s linear infinite}@keyframes fall-54{60.00%{transform:translate(12.52vw,60.00vh) scale(0.80)}to{transform:translate(7.74vw, 105vh) scale(0.80)}}.embedim-snow:nth-child(55){opacity:0.74;transform:translate(53.04vw,-10px) scale(0.80);animation:fall-55 18s -26s linear infinite}@keyframes fall-55{40.00%{transform:translate(59.18vw,40.00vh) scale(0.80)}to{transform:translate(56.11vw, 105vh) scale(0.80)}}.embedim-snow:nth-child(56){opacity:0.50;transform:translate(74.78vw,-10px) scale(0.04);animation:fall-56 24s -26s linear infinite}@keyframes fall-56{40.00%{transform:translate(77.48vw,40.00vh) scale(0.04)}to{transform:translate(76.13vw, 105vh) scale(0.04)}}.embedim-snow:nth-child(57){opacity:0.20;transform:translate(57.09vw,-10px) scale(0.54);animation:fall-57 24s -4s linear infinite}@keyframes fall-57{30.00%{transform:translate(60.77vw,30.00vh) scale(0.54)}to{transform:translate(58.93vw, 105vh) scale(0.54)}}.embedim-snow:nth-child(58){opacity:0.32;transform:translate(70.57vw,-10px) scale(0.56);animation:fall-58 10s -27s linear infinite}@keyframes fall-58{40.00%{transform:translate(71.00vw,40.00vh) scale(0.56)}to{transform:translate(70.79vw, 105vh) scale(0.56)}}.embedim-snow:nth-child(59){opacity:0.38;transform:translate(38.38vw,-10px) scale(0.12);animation:fall-59 12s -16s linear infinite}@keyframes fall-59{30.00%{transform:translate(40.33vw,30.00vh) scale(0.12)}to{transform:translate(39.35vw, 105vh) scale(0.12)}}.embedim-snow:nth-child(60){opacity:0.24;transform:translate(43.19vw,-10px) scale(0.94);animation:fall-60 17s -12s linear infinite}@keyframes fall-60{70.00%{transform:translate(36.50vw,70.00vh) scale(0.94)}to{transform:translate(39.84vw, 105vh) scale(0.94)}}.embedim-snow:nth-child(61){opacity:0.92;transform:translate(82.22vw,-10px) scale(0.28);animation:fall-61 21s -27s linear infinite}@keyframes fall-61{40.00%{transform:translate(72.68vw,40.00vh) scale(0.28)}to{transform:translate(77.45vw, 105vh) scale(0.28)}}.embedim-snow:nth-child(62){opacity:0.50;transform:translate(24.30vw,-10px) scale(0.94);animation:fall-62 29s -22s linear infinite}@keyframes fall-62{80.00%{transform:translate(16.55vw,80.00vh) scale(0.94)}to{transform:translate(20.43vw, 105vh) scale(0.94)}}.embedim-snow:nth-child(63){opacity:0.23;transform:translate(8.25vw,-10px) scale(0.67);animation:fall-63 20s -6s linear infinite}@keyframes fall-63{80.00%{transform:translate(2.38vw,80.00vh) scale(0.67)}to{transform:translate(5.32vw, 105vh) scale(0.67)}}.embedim-snow:nth-child(64){opacity:0.93;transform:translate(21.46vw,-10px) scale(0.47);animation:fall-64 25s -5s linear infinite}@keyframes fall-64{50.00%{transform:translate(18.83vw,50.00vh) scale(0.47)}to{transform:translate(20.15vw, 105vh) scale(0.47)}}.embedim-snow:nth-child(65){opacity:0.81;transform:translate(92.90vw,-10px) scale(0.80);animation:fall-65 17s -23s linear infinite}@keyframes fall-65{80.00%{transform:translate(92.23vw,80.00vh) scale(0.80)}to{transform:translate(92.57vw, 105vh) scale(0.80)}}.embedim-snow:nth-child(66){opacity:0.19;transform:translate(5.79vw,-10px) scale(0.69);animation:fall-66 27s -8s linear infinite}@keyframes fall-66{60.00%{transform:translate(10.54vw,60.00vh) scale(0.69)}to{transform:translate(8.16vw, 105vh) scale(0.69)}}.embedim-snow:nth-child(67){opacity:0.27;transform:translate(95.01vw,-10px) scale(0.28);animation:fall-67 15s -0s linear infinite}@keyframes fall-67{30.00%{transform:translate(87.61vw,30.00vh) scale(0.28)}to{transform:translate(91.31vw, 105vh) scale(0.28)}}.embedim-snow:nth-child(68){opacity:0.50;transform:translate(79.81vw,-10px) scale(0.89);animation:fall-68 14s -9s linear infinite}@keyframes fall-68{30.00%{transform:translate(88.92vw,30.00vh) scale(0.89)}to{transform:translate(84.36vw, 105vh) scale(0.89)}}.embedim-snow:nth-child(69){opacity:0.34;transform:translate(61.79vw,-10px) scale(0.47);animation:fall-69 17s -26s linear infinite}@keyframes fall-69{80.00%{transform:translate(69.82vw,80.00vh) scale(0.47)}to{transform:translate(65.80vw, 105vh) scale(0.47)}}.embedim-snow:nth-child(70){opacity:0.64;transform:translate(45.47vw,-10px) scale(0.91);animation:fall-70 13s -17s linear infinite}@keyframes fall-70{60.00%{transform:translate(50.73vw,60.00vh) scale(0.91)}to{transform:translate(48.10vw, 105vh) scale(0.91)}}.embedim-snow:nth-child(71){opacity:0.33;transform:translate(13.36vw,-10px) scale(0.49);animation:fall-71 18s -8s linear infinite}@keyframes fall-71{60.00%{transform:translate(10.35vw,60.00vh) scale(0.49)}to{transform:translate(11.85vw, 105vh) scale(0.49)}}.embedim-snow:nth-child(72){opacity:0.07;transform:translate(95.69vw,-10px) scale(0.67);animation:fall-72 10s -3s linear infinite}@keyframes fall-72{80.00%{transform:translate(105.05vw,80.00vh) scale(0.67)}to{transform:translate(100.37vw, 105vh) scale(0.67)}}.embedim-snow:nth-child(73){opacity:0.99;transform:translate(30.91vw,-10px) scale(0.25);animation:fall-73 23s -17s linear infinite}@keyframes fall-73{80.00%{transform:translate(30.04vw,80.00vh) scale(0.25)}to{transform:translate(30.48vw, 105vh) scale(0.25)}}.embedim-snow:nth-child(74){opacity:0.77;transform:translate(49.12vw,-10px) scale(0.33);animation:fall-74 24s -14s linear infinite}@keyframes fall-74{40.00%{transform:translate(39.51vw,40.00vh) scale(0.33)}to{transform:translate(44.31vw, 105vh) scale(0.33)}}.embedim-snow:nth-child(75){opacity:0.47;transform:translate(45.34vw,-10px) scale(0.55);animation:fall-75 30s -7s linear infinite}@keyframes fall-75{60.00%{transform:translate(38.73vw,60.00vh) scale(0.55)}to{transform:translate(42.04vw, 105vh) scale(0.55)}}.embedim-snow:nth-child(76){opacity:0.40;transform:translate(18.80vw,-10px) scale(0.94);animation:fall-76 28s -6s linear infinite}@keyframes fall-76{40.00%{transform:translate(13.53vw,40.00vh) scale(0.94)}to{transform:translate(16.17vw, 105vh) scale(0.94)}}.embedim-snow:nth-child(77){opacity:0.12;transform:translate(8.25vw,-10px) scale(0.28);animation:fall-77 15s -27s linear infinite}@keyframes fall-77{80.00%{transform:translate(16.87vw,80.00vh) scale(0.28)}to{transform:translate(12.56vw, 105vh) scale(0.28)}}.embedim-snow:nth-child(78){opacity:0.81;transform:translate(53.96vw,-10px) scale(0.23);animation:fall-78 16s -23s linear infinite}@keyframes fall-78{70.00%{transform:translate(55.74vw,70.00vh) scale(0.23)}to{transform:translate(54.85vw, 105vh) scale(0.23)}}.embedim-snow:nth-child(79){opacity:0.76;transform:translate(93.90vw,-10px) scale(0.79);animation:fall-79 17s -29s linear infinite}@keyframes fall-79{30.00%{transform:translate(88.91vw,30.00vh) scale(0.79)}to{transform:translate(91.41vw, 105vh) scale(0.79)}}</style><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i><i class="embedim-snow"></i></div>
</div>

    </html>
    """

    with open("classement.html", "w", encoding="utf-8") as f:
        f.write(html_header + html_body + html_footer)

    print("✅ Fichier classement.html généré avec succès ! Ouvre-le dans ton navigateur.")

if __name__ == "__main__":
    main()

