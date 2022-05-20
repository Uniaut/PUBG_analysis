import analysis.samples.load as Load
import analysis.utils.auth as Auth

if __name__ == '__main__':
    print(Load.samples())

    pubg = Auth.pubg()
    match_id_list = pubg.samples(start=None, shard='steam').match_ids

    for match_id in match_id_list[150:151]:
        print(f'[LOG]\tLoading {match_id}')
        match = Load.load_match(pubg, match_id)
        telemetry = Load.load_telemetry(match)
        print(f'[LOAD]\t{telemetry.map_id()}')
        print(Load.modify(telemetry, match_id=match_id))
