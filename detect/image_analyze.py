from trafficlight.detect_tl import tl_run
from crosswalk.detect_cw import cw_run
if __name__ == '__main__':

    cw_res = cw_run()
    # cr_res == 1 : Crosswalk exists -> Detect Traffic Light
    # cr_res == -1 : No Crosswalk
    print(cw_res)

    tl_res = tl_run()
    # tl_res == 1 : Go
    # tl_res == -1 : No Traffic Light -> Detect Car
    print(tl_res)
