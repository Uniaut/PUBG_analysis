import itertools
import matplotlib.pyplot as plt
import numpy as np
from typing import Callable

from chicken_dinner.models.match import Match
from chicken_dinner.models.telemetry import Telemetry
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

    return '#%02x%02x%02x' % value


def plot_kill(kills: list, *, mode: str, **kwargs):
    hset_0 = kwargs['hset_0']
    hset_1 = kwargs['hset_1']
    for killer_loction, victim_lociton in kills:
        kx, ky, _ = killer_loction
        vx, vy, _ = victim_lociton

        if '.' in mode:
            plt.plot(kx, ky, color='#FF0000', marker='x')
            plt.plot(vx, vy, color='#00FF00', marker='o')

        if 'O' in mode:
            Heatmap.add_sticker(*hset_0, pos=(kx, ky), amp=1.0)
            Heatmap.add_sticker(*hset_1, pos=(vx, vy), amp=1.0)

        if '-' in mode:
            plt.arrow(
                kx, ky, vx - kx, vy - ky, color='white',
            )


@Load.pickle_loader('kills.pickle')
def get_kills(match: Match, telemetry_getter: Callable):
    return Kill.get_kills(telemetry_getter(match))


if __name__ == '__main__':
    pubg = Auth.pubg()

    want_map_id = 'Desert_Main'
    xx, yy = Heatmap.ready_heatmap(want_map_id, 400)
    hset_0 = Heatmap.new_grid(xx, yy)
    hset_1 = Heatmap.new_grid(xx, yy)

    # samples = Load.samples()
    samples = itertools.chain.from_iterable(
        pubg.samples(start='2022-05-%02dT%02d:00:00Z' % (19 - day, hour)).match_ids
        for day, hour in itertools.product(range(10), range(0, 24))
    )
    valid_match_cnt = 0
    for s_id in samples:
        match: Match = Load.get_match(s_id, pubg, s_id)

        if match.map_id != want_map_id:
            print('Nah.', match.game_mode, match.map_id)
            continue

        print('Okay', match.id)
        valid_match_cnt += 1

        kill_datas = get_kills(s_id, match, lambda m: m.get_telemetry())
        plot_kill(kill_datas, mode='O', hset_0=hset_0, hset_1=hset_1)

        if valid_match_cnt >= 1800:
            break

    print(valid_match_cnt)

    res_gird = np.log(np.divide(hset_0[2], hset_1[2] + 1.0e-4) + 1)
    Heatmap.plot_heatmap(xx, yy, res_gird)

    map_id: str = want_map_id
    for b, f in [('Heaven', 'Haven'), ('Tiger', 'Taego'), ('Baltic', 'Erangel')]:
        map_id = map_id.replace(b, f)
    Plot.plot_map(map_id, 'High')
    plt.show()
