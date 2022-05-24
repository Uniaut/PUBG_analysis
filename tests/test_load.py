from chicken_dinner.models.telemetry import Telemetry

import analysis.samples.load as Load
import analysis.utils.auth as Auth


@Load.pickle_loader('test')
def test(telemetry: Telemetry):
    return telemetry.map_name()


if __name__ == '__main__':
    pubg = Auth.pubg()
    match_id_list = pubg.samples(start=None, shard='steam').match_ids

    for match_id in match_id_list[:10]:
        print(f'[LOG]\tLoading {match_id}')
        match = Load.get_match(match_id, pubg, match_id)
        telemetry = Load.get_telemetry(match_id, match)
        print(f'MAP: {telemetry.map_id()}')
