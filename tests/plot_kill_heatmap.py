import datetime
import json
import matplotlib.pyplot as plt
import os

import chicken_dinner.models.match as Match
import chicken_dinner.models.telemetry as Telemetry
from chicken_dinner.pubgapi import PUBG

import analysis.utils.kill as Kill
import analysis.utils.plot as Plot
import analysis.utils.auth as Auth
import analysis.samples.load as Load
import tests.heatmap as Heatmap

def spectrum(progress) -> str:
    if progress < 1 / 3:
        subprog = round(progress * 3 * 255)
        value = (255 - subprog, subprog, 0)
    elif progress < 2 / 3:
        subprog = round((progress * 3 - 1) * 255)
        value = (0, 255 - subprog, subprog)
    else:
        subprog = round((progress * 3 - 2) * 255)
        value = (subprog, 0, 255 - subprog)

    return "#%02x%02x%02x" % value


def plot_kill(kills: list, *, mode: str, hset: tuple):
    for killer_loction, victim_lociton in kills:
        kx, ky, _ = killer_loction
        vx, vy, _ = victim_lociton

        if '.' in mode:
            plt.plot(kx, ky, color='#FF0000', marker="x")
            plt.plot(vx, vy, color='#00FF00', marker="o")
        
        if 'O' in mode:
            Heatmap.add_sticker(*hset, pos=(kx, ky), amp=1.0)
            Heatmap.add_sticker(*hset, pos=(vx, vy), amp=-1.0)

        if '-' in mode:
            plt.arrow(
                kx,
                ky,
                vx - kx,
                vy - ky,
                color="white",
            )


if __name__ == "__main__":
    pubg = Auth.pubg()
    
    hset = Heatmap.ready_heatmap()

    # samples = pubg.samples().match_ids[:100]
    samples = Load.samples()
    valid_match_cnt = 0
    for s_id in samples:
        match = Load.load_match(pubg, s_id)

        if match.map_id != 'Desert_Main':
            print('Nah.', match.game_mode, match.map_id)
            continue
        
        print(match.id, 'is working!')
        valid_match_cnt += 1

        telemetry = Load.load_telemetry(match)
        kill_datas = Kill.get_kills(telemetry)
        plot_kill(kill_datas, mode='O', hset=hset)

        
        if valid_match_cnt >= 50:
            break
    
    Heatmap.plot_heatmap(*hset)

    map_id: str = match.map_id.replace(" ", "_")
    for b, f in [('Heaven', 'Haven'), ('Tiger', 'Taego'), ('Baltic', 'Erangel')]:
        map_id = map_id.replace(b, f)
    Plot.plot_map(map_id, "High")
    plt.show()
