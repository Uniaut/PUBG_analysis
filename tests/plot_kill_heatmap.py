import itertools
import time
from datetime import datetime, timedelta
from multiprocessing import Pool
from scipy import interpolate
from threading import Thread
from typing import Iterable

import matplotlib.pyplot as plt
import numpy as np
from chicken_dinner.models.match import Match
from chicken_dinner.models.telemetry.telemetry import Telemetry
from chicken_dinner.pubgapi import PUBG

import analysis.samples.load as Load
import analysis.utils.auth as Auth
import analysis.utils.kill as Kill
import analysis.utils.plot as MapPlot
import tests.heatmap as Heatmap


@Load.pickle_loader('kills.pickle')
def get_kill_location(match: Match):
    return Kill.get_kill_location(match.get_telemetry())


def load_kill_list(
    pubg: PUBG, mid_iterator: Iterable, num_matches: int, target_map_id: str, dst_kl: list,
):
    valid_match_cnt = 0
    for s_id in mid_iterator:
        match: Match = Load.get_match(s_id, pubg, s_id)

        if match.map_id != target_map_id:
            # print(f'Nah. {match.map_id}')
            continue
        else:
            print(f'Okay {match.id}')
            valid_match_cnt += 1

        dst_kl.append(get_kill_location(s_id, match))

        if valid_match_cnt == num_matches:
            break


def get_sample_iterators(pubg: PUBG, new: bool, split: int):
    if new:
        today = datetime.utcnow()
        iters = []
        samplers = (
            pubg.samples(
                datetime.strftime(
                    today - timedelta(days=delta_d, hours=delta_h),
                    '%Y-%m-%dT%H:%M:%S.%fZ',
                )
            ).match_ids
            for delta_d, delta_h in itertools.product(range(1, 14), range(24))
        )
        iters = (itertools.chain.from_iterable(sampler) for sampler in itertools.tee(samplers, split))
    else:
        samples = Load.samples()
        iters = itertools.tee(samples, split)

    return iters


def _get_sigma_map_split(linspace_x, linspace_y, kill_locations):
    sigma_hset = Heatmap.new_grid(linspace_x, linspace_y)
    for killer_location, victim_locaiton in kill_locations:
        kx, ky, _ = killer_location
        vx, vy, _ = victim_locaiton
        Heatmap.add_sticker(sigma_hset, pos=(kx, ky), amp=1.0, sigma=70.0)
        Heatmap.add_sticker(sigma_hset, pos=(vx, vy), amp=1.0, sigma=70.0)
    return sigma_hset[2]


def get_sigma_map(target_map_id: str, kill_locations: list, num_split: int):
    linspace_x, linspace_y = Heatmap.ready_heatmap(target_map_id, 100)
    split_args = [(linspace_x, linspace_y, iters) for iters in itertools.tee(kill_locations, num_split)]
    
    if num_split > 1:
        with Pool(processes=num_split) as pool:
            mapped_result = pool.starmap(_get_sigma_map_split, split_args)
    else:
        mapped_result = itertools.starmap(_get_sigma_map_split, split_args)
        print(mapped_result)
    result = sum(mapped_result)
    print(result)
    result = 1 / (np.power(result + 1, 0.5))

    return linspace_x, linspace_y, result


"""
침착하게 생각해보자
read sample from storage as pickle -> multithreading
get telemetry from match url -> multiprocessing
--> from url or from pickle
==> fucking shit.
get kill from telemetry -> multiprocessing

def main:
    kill list = Threads(get kill data) -> end
    sigma_heatmap(kill list, sigma hmap)
    get_sigma_position(grid)
"""

def _get_kill_map_split(linspace_x, linspace_y, kill_locations, sigma_func):
    kill_hset = Heatmap.new_grid(linspace_x, linspace_y)
    death_hset = Heatmap.new_grid(linspace_x, linspace_y)
    for killer_location, victim_locaiton in kill_locations:
        kx, ky, _ = killer_location
        vx, vy, _ = victim_locaiton
        Heatmap.add_sticker(kill_hset, pos=(kx, ky), amp=1.0, sigma=(50 * sigma_func(kx, ky)))
        Heatmap.add_sticker(death_hset, pos=(vx, vy), amp=1.0, sigma=(50 * sigma_func(vx, vy)))
    return kill_hset[2], death_hset[2]


def get_kill_map(target_map_id: str, kill_locations: list, num_split: int, sigma_func: callable):
    linspace_x, linspace_y = Heatmap.ready_heatmap(target_map_id, 400, (0.2, 0.8), (0.2, 0.8))
    split_args = [(linspace_x, linspace_y, iters, sigma_func) for iters in itertools.tee(kill_locations, num_split)]

    if num_split > 1:
        with Pool(processes=num_split) as pool:
            mapped_result = pool.starmap(_get_kill_map_split, split_args)
            kill_result = sum(each[0] for each in mapped_result)
            death_result = sum(each[1] for each in mapped_result)
    else:
        kill_result, death_result = _get_kill_map_split(*split_args[0])
    
    result = np.log((kill_result + 1) / (death_result + 1))
    result = np.tanh(result * 10)

    return linspace_x, linspace_y, result


def plot_kill(kills: list, *, mode: str, **kwargs):
    for killer_loction, victim_lociton in kills:
        kx, ky, _ = killer_loction
        vx, vy, _ = victim_lociton

        if '.' in mode:
            plt.plot(kx, ky, color='#00FF00', marker='o')
            plt.plot(vx, vy, color='#FF0000', marker='x')

        if '-' in mode:
            plt.arrow(
                kx, ky, vx - kx, vy - ky, color='white',
            )


def main():
    pubg = Auth.pubg()

    total_match = 100
    num_split = 1
    target_map_id = 'Baltic_Main'
    is_samples_from_api = True

    iterators = get_sample_iterators(pubg, is_samples_from_api, num_split)

    thread_start = time.time()
    kill_locations = []
    threads = [
        Thread(
            target=load_kill_list,
            args=(
                pubg,
                iterator_unit,
                total_match // num_split,
                target_map_id,
                kill_locations,
            ),
        )
        for iterator_unit in iterators
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    kill_locations = list(itertools.chain.from_iterable(kill_locations))
    print(len(kill_locations))
    thread_end = time.time()
    print(f'thread: {thread_end - thread_start}')


    # GET SIGMA HEATMAP
    NUM_PROCESSES = 1
    process_start = time.time()
    sigma_hset = get_sigma_map(target_map_id, kill_locations, NUM_PROCESSES)
    process_end = time.time()
    print(f'Sigma process: {process_end - process_start}')

    MapPlot.plot_map(target_map_id, 'Low')
    Heatmap.plot_heatmap(sigma_hset)
    plot_kill(kill_locations, mode='.')
    plt.show()

    sigma_func = interpolate.RectBivariateSpline(*sigma_hset)
    print('sigma_func(4000, 4000):', sigma_func(4000, 4000))
    

    process_start = time.time()
    kd_hset = get_kill_map(target_map_id, kill_locations, NUM_PROCESSES, sigma_func)
    process_end = time.time()
    print(f'K/D Process: {process_end - process_start}')

    Heatmap.plot_heatmap(kd_hset)
    MapPlot.plot_map(target_map_id, 'Low')
    plt.show()

    plot_kill(kill_locations, mode='.')
    Heatmap.plot_heatmap(kd_hset)
    MapPlot.plot_map(target_map_id, 'High')
    plt.show()



if __name__ == '__main__':
    main()
